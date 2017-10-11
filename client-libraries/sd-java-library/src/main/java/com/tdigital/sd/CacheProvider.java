/*
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
*/
package com.tdigital.sd;


import com.tdigital.sd.model.CacheKey;
import com.tdigital.sd.model.Endpoint;
import net.sf.ehcache.Cache;
import net.sf.ehcache.CacheManager;
import net.sf.ehcache.Element;
import net.sf.ehcache.config.CacheConfiguration;
import net.sf.ehcache.config.Configuration;

import java.util.ArrayList;

public class CacheProvider {

    private static Cache cacheTtl;
    private static Cache cacheTtr;
    private static CacheManager manager;

    private static CacheProvider instance;

    private static int SECONDS_HOUR = 3600;

    private CacheProvider() {};

    private CacheProvider( double ttl, int ttr) {
        Configuration config = new Configuration();
        CacheConfiguration defaultCacheConfiguration = new CacheConfiguration();
        defaultCacheConfiguration.setTimeToIdleSeconds(60);
        defaultCacheConfiguration.setTimeToLiveSeconds(120);
        defaultCacheConfiguration.setMaxEntriesLocalHeap(10000L);
        defaultCacheConfiguration.setMaxEntriesLocalDisk(1000000L);
        config.setDefaultCacheConfiguration(defaultCacheConfiguration);
        config.setUpdateCheck(false);
        manager = CacheManager.create(config);
        cacheTtl = new Cache("cacheTtl", 10000, false, false, (int) (ttl * SECONDS_HOUR), (int) (ttl * SECONDS_HOUR), false, 30);
        cacheTtr = new Cache("cacheTtr", 10000, false, false, ttr, ttr, false, 30);
        manager.addCache(cacheTtl);
        manager.addCache(cacheTtr);
    }

    public static CacheProvider getInstance(double ttl, int ttr) {
          if (instance == null) {
              instance = new CacheProvider(ttl, ttr);
          }
          return instance;
    }

    public void saveKeyInTtl(CacheKey cacheKey, ArrayList<Endpoint> cacheValue) {
        cacheTtl.put(new Element(cacheKey, cacheValue));
    }

    public ArrayList<Endpoint> getValueFromTtl(CacheKey cacheKey) {
        Element e = cacheTtl.get(cacheKey);
        if(e == null) {
            return null;
        } else {
            return (ArrayList<Endpoint>) e.getObjectValue();
        }
    }

    public void saveKeyInTtr(CacheKey cacheKey, ArrayList<Endpoint> cacheValue) {
        cacheTtr.put(new Element(cacheKey, cacheValue));
    }

    public ArrayList<Endpoint> getValueFromTtr(CacheKey cacheKey) {
        Element e = cacheTtr.get(cacheKey);
        if(e == null) {
            return null;
        } else {
            return (ArrayList<Endpoint>) e.getObjectValue();
        }
    }
}
