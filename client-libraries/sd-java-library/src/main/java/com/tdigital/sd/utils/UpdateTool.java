package com.tdigital.sd.utils;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class UpdateTool {

    private static final Logger LOGGER = LoggerFactory.getLogger(UpdateTool.class);

    public static SDConfig updateObject(SDConfig to, SDConfig from) {
        if (to.getHost() == null && from.getHost() != null) {
            to.setHost(from.getHost());
        } else {
            LOGGER.debug("Property Host not present.");
        }
        if  (to.getPort() == null && from.getPort() != null) {
            to.setPort(from.getPort());
        } else {
            LOGGER.debug("Port Host not present.");
        }
        if  (to.getSdVersion() == null && from.getSdVersion() != null) {
            to.setSdVersion(from.getSdVersion());
        }
        if  (to.getTtl() == null && from.getTtl() != null) {
            to.setTtl(from.getTtl());
        }
        if  (to.getTtr() == null && from.getTtr() != null) {
            to.setTtr(from.getTtr());
        }
        if  (to.getTimeout() == null && from.getTimeout() != null) {
            to.setTimeout(from.getTimeout());
        }
        return to;
    }

}
