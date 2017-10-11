package com.tdigital.sd.utils;


import com.tdigital.sd.exceptions.SDLibraryException;
import com.tdigital.sd.model.General;
import com.tdigital.sd.model.InfoView;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.jboss.resteasy.client.ClientExecutor;
import org.jboss.resteasy.client.ClientRequest;
import org.jboss.resteasy.client.ClientResponse;
import org.jboss.resteasy.client.core.executors.ApacheHttpClient4Executor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

public class ConfigurationReader {
    private static final Logger logger = LoggerFactory.getLogger(ConfigurationReader.class);

    private static final String RESOURCE_FILE = "service-directory";

    private static final String SD_HOST = "sd_host";
    private static final String SD_PORT = "sd_port";
    private static final String TTL = "ttl";
    private static final String TTR = "ttr";
    private static final String SD_VERSION = "sd_version";
    private static final String TIMEOUT = "timeout";

    private static final Double DEFAULT_TTL = (double) 168;
    private static final Integer DEFAULT_TTR = 3600;
    private static final Integer DEFAULT_TIMEOUT = 15;

    private static final String SD_URL_PROTOCOL = "http://";

    private static final String SUFFIX_URL = "/sd/info";

    private ResourceBundle rb;

    private SDConfig sdConfig;

    public ConfigurationReader() throws SDLibraryException {
        this.sdConfig = loadConfigFromFile();
        checkSdConfig();

    }

    public ConfigurationReader(String sdHost, int sdPort, int ttl, int ttr, String sdVersion) throws SDLibraryException {
        SDConfig partialSDConfig = new SDConfig(sdHost, sdPort, ttl, ttr, sdVersion);
        SDConfig fileConfig = loadConfigFromFile();
        this.sdConfig = generateFinalSdConfig(partialSDConfig, fileConfig);
        checkSdConfig();
    }

    private void checkSdConfig() throws SDLibraryException {
        if (this.sdConfig.getSdVersion() == null) {
            this.sdConfig.setSdVersion(getVersionFromServiceDirectory());
        }
        if (this.sdConfig.getHost() == null) {
           throw new NullPointerException("Service Directory Host not found.");
        }
        if (this.sdConfig.getPort() == null) {
            throw new NullPointerException("Service Directory Port not found.");
        }
        if (this.sdConfig.getTimeout() == null) {
            this.sdConfig.setTimeout(DEFAULT_TIMEOUT);
        }
        if (this.sdConfig.getTtl() == null) {
            logger.debug("Using Default Ttl.");
            this.sdConfig.setTtl(DEFAULT_TTL);
        }
        if (this.sdConfig.getTtr() == null) {
            logger.debug("Using Default Ttr.");
            this.sdConfig.setTtr(DEFAULT_TTR);
        }
    }

    private String getVersionFromServiceDirectory() throws SDLibraryException {
        // perform request to get the current api version.
        //hardcoded.
        logger.info("Getting version from server.");
        String baseUrl = createBaseUrl(sdConfig.getHost(), sdConfig.getPort());
        DefaultHttpClient httpClient = new DefaultHttpClient();
        HttpParams params = httpClient.getParams();
        HttpConnectionParams.setConnectionTimeout(params, sdConfig.getTimeout() * General.SECONDS_TO_MILLIS_FACTOR);
        HttpConnectionParams.setSoTimeout(params, sdConfig.getTimeout() * General.SECONDS_TO_MILLIS_FACTOR);
        ClientExecutor executor = new ApacheHttpClient4Executor(httpClient);
        ClientRequest clientRequest = new ClientRequest(baseUrl, executor);
        try {
                ClientResponse<InfoView> result = clientRequest.get(InfoView.class);
            return result.getEntity().getDefaultVersion();
        } catch (Exception e) {
            throw new SDLibraryException(e.getMessage());
        }
    }

    private String createBaseUrl(String sdHost, int sdPort) {
        StringBuilder sb = new StringBuilder(SD_URL_PROTOCOL).append(sdHost).append(":")
                .append(sdPort).append(SUFFIX_URL);
        return sb.toString();
    }

    private SDConfig loadConfigFromFile() {
        try {
            rb = ResourceBundle.getBundle(RESOURCE_FILE);
            SDConfig result = new SDConfig();
            result.setHost(rb.containsKey(SD_HOST) ? rb.getString(SD_HOST) : null);
            result.setPort(rb.containsKey(SD_PORT) ? Integer.parseInt(rb.getString(SD_PORT)) : null);
            result.setTtr(rb.containsKey(TTR) ? Integer.parseInt(rb.getString(TTR)) : null);
            result.setTtl(rb.containsKey(TTL) ? Double.parseDouble(rb.getString(TTL)) : null);
            result.setTimeout(rb.containsKey(TIMEOUT) ? Integer.parseInt(rb.getString(TIMEOUT)) : null);
            result.setSdVersion(rb.containsKey(SD_VERSION) ? rb.getString(SD_VERSION) : null);

            return result;
        } catch (MissingResourceException e) {
            //logger.warn("Missing Resource. Applying default values.");
            //throw exception?
            return null;
        }
    }

    private SDConfig generateFinalSdConfig(SDConfig partialSDConfig, SDConfig fileConfig) {
        if (partialSDConfig == null) {
            return fileConfig;
        }
        return UpdateTool.updateObject(partialSDConfig, fileConfig);
    }

    public SDConfig getSdConfig() {
        return sdConfig;
    }
}
