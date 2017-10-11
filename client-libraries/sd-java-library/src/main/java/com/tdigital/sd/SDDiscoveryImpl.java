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

import com.tdigital.sd.exceptions.ConnectionException;
import com.tdigital.sd.exceptions.RemoteException;
import com.tdigital.sd.exceptions.SDLibraryException;
import com.tdigital.sd.model.CacheKey;
import com.tdigital.sd.model.Endpoint;
import com.tdigital.sd.model.General;
import com.tdigital.sd.model.SDError;
import com.tdigital.sd.utils.ConfigurationReader;
import com.tdigital.sd.utils.SDConfig;
import org.apache.http.conn.HttpHostConnectException;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.jboss.resteasy.client.ClientExecutor;
import org.jboss.resteasy.client.ClientRequest;
import org.jboss.resteasy.client.ClientResponse;
import org.jboss.resteasy.client.core.executors.ApacheHttpClient4Executor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.ws.rs.core.Response;
import java.util.*;

public class SDDiscoveryImpl implements SDDiscovery {

    private static final Logger logger = LoggerFactory.getLogger(SDDiscoveryImpl.class);

    private static final String[] MANDATORY_FIELDS = {"url", "id", "environment", "api_name", "version"};

    private static final String SD_URL_PROTOCOL = "http://";

    private static final String SUFFIX_URL = "/apis/{apiName}/endpoints";

    private ClientRequest clientRequest;

    private SDConfig sdConfig;

    private CacheProvider cacheProvider;

    private ClientExecutor clientExecutor;
    private String baseUrl;

    public SDDiscoveryImpl() throws SDLibraryException {
        ConfigurationReader configurationReader = new ConfigurationReader();
        sdConfig =  configurationReader.getSdConfig();
        logger.debug("Config: " + sdConfig);
        commonOperations(sdConfig);
    }

    public SDDiscoveryImpl(String sdHost, int sdPort, int ttl, int ttr, String sdVersion) throws SDLibraryException {
        ConfigurationReader configurationReader = new ConfigurationReader(sdHost, sdPort, ttl, ttr, sdVersion);
        sdConfig =  configurationReader.getSdConfig();
        logger.debug("Config: " + sdConfig);
        commonOperations(sdConfig);
    }

    private void commonOperations(SDConfig sdConfig) {
        baseUrl = createBaseUrl(sdConfig.getHost(), sdConfig.getPort(), sdConfig.getSdVersion());
        DefaultHttpClient httpClient = new DefaultHttpClient();
        HttpParams params = httpClient.getParams();
        HttpConnectionParams.setConnectionTimeout(params, sdConfig.getTimeout() * General.SECONDS_TO_MILLIS_FACTOR);
        HttpConnectionParams.setSoTimeout(params, sdConfig.getTimeout() * General.SECONDS_TO_MILLIS_FACTOR);
        clientExecutor = new ApacheHttpClient4Executor(httpClient);

        if (!sdConfig.getTtl().equals(0)) {
            cacheProvider = CacheProvider.getInstance(sdConfig.getTtl(), sdConfig.getTtr());
            logger.debug("Enabled cache System.");
        } else {
            logger.debug("Disabled cache System.");
        }

    }

    private String createBaseUrl(String sdHost, int sdPort, String sdVersion) {
        StringBuilder sb = new StringBuilder(SD_URL_PROTOCOL).append(sdHost).append(":")
                .append(sdPort).append("/sd/").append(sdVersion)
                .append(SUFFIX_URL);
        return sb.toString();
    }

    @Override
    public List<Endpoint> getEndpoints(String apiName, String environment, String version, Map<String, String> endpointsAttributes, General.behaviour behaviour) throws Exception {

        if (behaviour == null) {
            behaviour = General.behaviour.PARAM_NO_CHECK;
        }
        checkMandatoryArguments(apiName, environment, endpointsAttributes);
        if (!sdConfig.getTtl().equals(0)) {
            //Cache activated
            CacheKey cacheKey = createCacheKey(apiName, environment, version, endpointsAttributes, behaviour);

            List<Endpoint> endpointsTtr = cacheProvider.getValueFromTtr(cacheKey);

            if (endpointsTtr != null) {
                logger.info("Returning endpoints from TTR Cache.");
                return endpointsTtr;
            } else {
                logger.debug("TTR cache empty");
                try {
                    List<Endpoint> remoteEndpoints = getEndpointFromRemote(apiName, environment, version, endpointsAttributes, behaviour);
                    logger.debug("Saving new values in caches.");
                    cacheProvider.saveKeyInTtr(cacheKey, (ArrayList<Endpoint>) remoteEndpoints);
                    cacheProvider.saveKeyInTtl(cacheKey, (ArrayList<Endpoint>) remoteEndpoints);
                    return remoteEndpoints;
                    // Change exceptions.
                } catch (HttpHostConnectException e) {
                    List<Endpoint> endpointsTtl = cacheProvider.getValueFromTtl(cacheKey);
                    if (endpointsTtl != null) {
                        logger.warn("Service directory request error.");
                        return endpointsTtl;
                    } else {
                        throw new ConnectionException();
                    }
                }
            }
        } else {
            return getEndpointFromRemote(apiName, environment, version, endpointsAttributes, behaviour);
        }
    }

    private List<Endpoint> getEndpointFromRemote(String apiName, String environment, String version, Map<String, String> endpointsAttributes, General.behaviour behaviour) throws Exception {
        clientRequest = new ClientRequest(baseUrl, clientExecutor);
        logger.debug( "clientRequest created. " + clientRequest.toString());
        List<Endpoint> result = new ArrayList<Endpoint>();
        clientRequest.pathParameter("apiName", apiName);
        addQueryParams(environment, version, endpointsAttributes, behaviour);

        ClientResponse<List> res = clientRequest.get(List.class);
        logger.debug("Doing get.");
        if (res.getStatus() == Response.Status.OK.getStatusCode()) {
            List<Map<String, Object>> serverResult = res.getEntity();
            logger.debug("Recovering body.....");
            for (Map<String, Object> servEndpoint: serverResult) {
                Endpoint endpoint = new Endpoint();
                endpoint.setUrl((String) servEndpoint.get("url"));
                endpoint.setId((String) servEndpoint.get("id"));
                endpoint.setEnvironment((String) servEndpoint.get("environment"));
                endpoint.setApiName((String) servEndpoint.get("api_name"));
                endpoint.setVersion((String) servEndpoint.get("version"));

                Set<String> endpointKeys = servEndpoint.keySet();
                List<String> mandatoryFields = Arrays.asList(MANDATORY_FIELDS);
                for (String key: endpointKeys) {
                    if (!mandatoryFields.contains(key)) {
                        endpoint.getOptionalParameters().put(key, servEndpoint.get(key));
                    }
                }
                result.add(endpoint);
            }
            logger.debug("Releasing connection.");
            res.releaseConnection();
            logger.debug("Returning List of endpoints.");
            return result;
        } else if (res.getStatus() == Response.Status.INTERNAL_SERVER_ERROR.getStatusCode()) {
            throw new ConnectionException("Internal Server Error.");
        } else {
            SDError serverError = res.getEntity(SDError.class);
            logger.debug("Releasing connection.");
            res.releaseConnection();
            throw new RemoteException(serverError.getDescription());
        }
    }

    private void checkMandatoryArguments(String apiName, String environment, Map<String, String> endpointsAttributes) {
        if (apiName == null) {
            throw new NullPointerException("ApiName parameter must not be null.");
        }
        if (environment == null) {
            throw new NullPointerException("Environment parameter must not be null.");
        }
        if(endpointsAttributes == null) {
            throw new NullPointerException("EndpointsAttributes parameter must not be null.");
        }
    }

    private void addQueryParams(String environment, String version, Map<String,String> endpointsAttributes, General.behaviour behaviour) {
        clientRequest.queryParameter("environment", environment);
        if (version != null) {
            clientRequest.queryParameter("version", version);
        }
        Set<String> endpointsAttributesKeys = endpointsAttributes.keySet();
        for (String key: endpointsAttributesKeys) {
            clientRequest.queryParameter(key, endpointsAttributes.get(key));
        }
        clientRequest.queryParameter("behaviour", behaviour.toString());
    }

    private CacheKey createCacheKey(String apiName, String environment, String version, Map<String,String> endpointsAttributes, General.behaviour behaviour) {
        TreeMap<String, String> sortedMap =  new TreeMap<String, String>();
        sortedMap.putAll(endpointsAttributes);
        return new CacheKey(apiName, environment, version, sortedMap, behaviour);
    }

    @Override
    public List<Endpoint> getEndpoints(String apiName, String environment, String version, Map<String, String> endpointsAttributes) throws Exception {
        return getEndpoints(apiName, environment, version, endpointsAttributes, General.behaviour.PARAM_NO_CHECK);
    }

    @Override
    public List<Endpoint> getEndpoints(String apiName, String environment, Map<String, String> params, General.behaviour behaviour) throws Exception {
        return getEndpoints(apiName, environment, null, params, behaviour);
    }

    @Override
    public List<Endpoint> getEndpoints(String apiName, String environment, Map<String, String> params) throws Exception {
        return getEndpoints(apiName, environment, null, params, General.behaviour.PARAM_NO_CHECK);
    }

}
