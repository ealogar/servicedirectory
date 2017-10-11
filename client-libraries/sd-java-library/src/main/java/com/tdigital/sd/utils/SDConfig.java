package com.tdigital.sd.utils;


public class SDConfig {

    private String host;
    private Integer port;
    private Double ttl;
    private Integer ttr;
    private String sdVersion;
    private Integer timeout;



    public SDConfig() {
    }

    public SDConfig(String host, int port, double ttl, int ttr, String sdVersion) {
        this.host = host;
        this.port = port;
        this.ttl = ttl;
        this.ttr = ttr;
        this.sdVersion = sdVersion;
    }

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public Integer getPort() {
        return port;
    }

    public void setPort(Integer port) {
        this.port = port;
    }

    public Double getTtl() {
        return ttl;
    }

    public void setTtl(Double ttl) {
        this.ttl = ttl;
    }

    public Integer getTtr() {
        return ttr;
    }

    public void setTtr(Integer ttr) {
        this.ttr = ttr;
    }

    public String getSdVersion() {
        return sdVersion;
    }

    public void setSdVersion(String sdVersion) {
        this.sdVersion = sdVersion;
    }

    public Integer getTimeout() {
        return timeout;
    }

    public void setTimeout(Integer timeout) {
        this.timeout = timeout;
    }

    @Override
    public String toString() {
        return "SdConfig{" +
                "host='" + host + '\'' +
                ", port='" + port + '\'' +
                ", ttl=" + ttl +
                ", ttr=" + ttr +
                ", sdVersion='" + sdVersion + '\'' +
                ", timeout=" + timeout +
                '}';
    }
}
