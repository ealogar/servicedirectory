/*
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
*/

package com.tdigital.sd.model;


import java.io.Serializable;
import java.util.LinkedHashMap;
import java.util.Map;

public class Endpoint implements Serializable {

    private String id;
    private String apiName;
    private String version;
    private String url;
    private String environment;

    private Map<String, Object> optionalParameters;


    public Endpoint() {
        optionalParameters = new LinkedHashMap<String, Object>();
    }


    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getApiName() {
        return apiName;
    }

    public void setApiName(String apiName) {
        this.apiName = apiName;
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getEnvironment() {
        return environment;
    }

    public void setEnvironment(String environment) {
        this.environment = environment;
    }

    public Map<String, Object> getOptionalParameters() {
        return optionalParameters;
    }

    public void setOptionalParameters(Map<String, Object> optionalParameters) {
        this.optionalParameters = optionalParameters;
    }
}
