'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from collections import namedtuple
from functools import update_wrapper
from threading import RLock
import time
import logging


logger = logging.getLogger(__name__)

_CacheInfo = namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"])
_CacheValue = namedtuple("CacheValue", ["ttl_expiry", "ttr_expiry", "value"])


class _HashableDict(dict):
    def __key(self):
        return tuple((k, self[k]) for k in sorted(self))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()


class _HashedSeq(list):
    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):   # @ReservedAssignment
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


def _make_key(args, kwds, typed,
             kwd_mark=(object(),),
             fasttypes=(int, str, frozenset, type(None)),
             sorted=sorted, tuple=tuple, type=type, len=len):  # @ReservedAssignment
    'Make a cache key from optionally typed positional and keyword arguments'
    key = tuple(map(lambda x: _HashableDict(x) if isinstance(x, dict) else x, args))
    if kwds:
        sorted_items = sorted(kwds.items())
        key += kwd_mark
        for item in sorted_items:
            if isinstance(item[1], dict):
                key += (item[0], _HashableDict(item[1]))
            else:
                key += item
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for k, v in sorted_items)  # @UnusedVariable
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)


def _check_refresh_ttr(link, ttr, ttl, now,  cache, exceptions, user_function, args, kwds):
    """
    Internal method for the logic of ttr, ttl expiration:
    When ttr has expired, the cache should be updated by calling the user_function
    The cache key is then updated with the recovered value
    If the user_function raises exception, the value from cache is returned if ttl has not expired,
    otherwise, the exception is raised
    """
    # unpack the cache value if needed
    if isinstance(link, list):
        link_prev, link_next, key, cache_value = link
    else:
        cache_value = link  # max

    if cache_value.ttr_expiry < now:
        logger.info("TTR expired, we try to refresh the element in cache calling SD")
        try:
            result = user_function(*args, **kwds)

            # pack the result_function in CacheValue
            cache_value = _CacheValue((now + ttl * 3600), now + ttr, result)

            # update the cache key with the refreshed result
            if isinstance(link, list):
                cache[key] = [link_prev, link_next, key, cache_value]
            else:
                cache[key] = cache_value
        except exceptions as e:
            logger.warning("Problem when calling SD: {0}".format(str(e)))
            logger.info("Trying to return cached value if ttl not expired")
            # If ttl expired raise exception and clean cache key
            if cache_value.ttl_expiry < now:
                logger.error("TTL expired, removing element from cache and raising exception")
                del cache[key]
                raise e

    return cache_value.value


def lru_cache(maxsize=100, typed=False, ttr=60 * 60, ttl=7 * 24, exceptions=(Exception,)):
    """Least-recently-used cache decorator.

    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.

    The expiration time of the element in cache is controlled by two times, ttr and ttl:

    ttr is the first expiration time, expressed in seconds. It defines the time
    within the element of the cache would be returned without calling the function.

    ttl is the second expiration time, expressed in seconds. When ttr has expired
    the function is called, if exception happens, the cached value would be returned.
    If the value of ttl is zero, no caching will be applied.
    When ttl has expired and no value is got from the function or exception is raised, this
    would be directly returned.

    If no element is cached or ttr has expired, the decorated function will be called and the returned
    value will be cached; ttr and ttl will be updated.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize) with
    f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used

    """

    # Users should only access the lru_cache through its public API:
    #       cache_info, cache_clear, and f.__wrapped__
    # The internals of the lru_cache are encapsulated for thread safety and
    # to allow the implementation to change (including a possible C version).

    def decorating_function(user_function):

        cache = dict()
        stats = [0, 0]                  # make statistics updateable non-locally
        HITS, MISSES = 0, 1             # names for the stats fields
        make_key = _make_key
        cache_get = cache.get           # bound method to lookup key or return None
        _len = len                      # localize the global len() function
        lock = RLock()                  # because linkedlist updates aren't threadsafe
        root = []                       # root of the circular doubly linked list
        root[:] = [root, root, None, None]      # initialize by pointing to self
        nonlocal_root = [root]                  # make updateable non-locally
        PREV, NEXT, KEY, RESULT = 0, 1, 2, 3    # names for the link fields

        def wrapper(*args, **kwds):
            now = time.time()
            # size limited caching that tracks accesses by recency
            key = make_key(args, kwds, typed) if kwds or typed else args
            with lock:
                link = cache_get(key)
                if link is not None:
                    # record recent use of the key by moving it to the front of the list
                    root, = nonlocal_root
                    link_prev, link_next, key, result = link
                    link_prev[NEXT] = link_next
                    link_next[PREV] = link_prev
                    last = root[PREV]
                    last[NEXT] = root[PREV] = link
                    link[PREV] = last
                    link[NEXT] = root
                    stats[HITS] += 1
                    result = _check_refresh_ttr(link, ttr, ttl, now,  cache,
                                          exceptions, user_function, args, kwds)
                    return result
            result = user_function(*args, **kwds)
            with lock:
                root, = nonlocal_root
                if key in cache:
                    # getting here means that this same key was added to the
                    # cache while the lock was released.  since the link
                    # update is already done, we need only return the
                    # computed result and update the count of misses.
                    pass
                elif _len(cache) >= maxsize:
                    # use the old root to store the new key and result
                    oldroot = root
                    oldroot[KEY] = key
                    oldroot[RESULT] = _CacheValue(now + ttl * 3600, now + ttr, result)
                    # empty the oldest link and make it the new root
                    root = nonlocal_root[0] = oldroot[NEXT]
                    oldkey = root[KEY]
                    oldvalue = root[RESULT]  # @UnusedVariable
                    root[KEY] = root[RESULT] = None
                    # now update the cache dictionary for the new links
                    del cache[oldkey]
                    cache[key] = oldroot
                else:
                    # put result in a new link at the front of the list
                    last = root[PREV]
                    link = [last, root, key, _CacheValue(now + ttl * 3600, now + ttr, result)]
                    last[NEXT] = root[PREV] = cache[key] = link
                stats[MISSES] += 1
            return result

        def cache_info():
            """Report cache statistics"""
            with lock:
                return _CacheInfo(stats[HITS], stats[MISSES], maxsize, len(cache))

        def cache_clear():
            """Clear the cache and cache statistics"""
            with lock:
                cache.clear()
                root = nonlocal_root[0]
                root[:] = [root, root, None, None]
                stats[:] = [0, 0]

        wrapper.__wrapped__ = user_function
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return update_wrapper(wrapper, user_function)

    return decorating_function
