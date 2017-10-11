package com.tdigital.sd.model;


import org.codehaus.jackson.annotate.JsonProperty;

public class InfoView {

    @JsonProperty("app_name")
    public String appName;
    @JsonProperty("default_version")
    public String defaultVersion;

    public InfoView() {
    }

    public InfoView(String appName, String defaultVersion) {
        this.appName = appName;
        this.defaultVersion = defaultVersion;
    }

    public String getAppName() {
        return appName;
    }

    public void setAppName(String appName) {
        this.appName = appName;
    }

    public String getDefaultVersion() {
        return defaultVersion;
    }

    public void setDefaultVersion(String defaultVersion) {
        this.defaultVersion = defaultVersion;
    }
}
