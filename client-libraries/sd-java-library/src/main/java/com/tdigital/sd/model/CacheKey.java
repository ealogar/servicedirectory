package com.tdigital.sd.model;

import java.io.Serializable;
import java.util.TreeMap;

public class CacheKey implements Serializable {

    private String apiName;
    private String environment;
    private String version;
    private TreeMap<String, String> endpointsAttributes;
    private General.behaviour behaviour;

    public CacheKey(String apiName, String environment, String version, TreeMap<String, String> endpointsAttributes, General.behaviour behaviour) {
        this.apiName = apiName;
        this.environment = environment;
        this.version = version;
        this.endpointsAttributes = endpointsAttributes;
        this.behaviour = behaviour;
    }

    public CacheKey() {
    }

    public String getApiName() {
        return apiName;
    }

    public void setApiName(String apiName) {
        this.apiName = apiName;
    }

    public String getEnvironment() {
        return environment;
    }

    public void setEnvironment(String environment) {
        this.environment = environment;
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    public TreeMap<String, String> getEndpointsAttributes() {
        return endpointsAttributes;
    }

    public void setEndpointsAttributes(TreeMap<String, String> endpointsAttributes) {
        this.endpointsAttributes = endpointsAttributes;
    }

    public General.behaviour getBehaviour() {
        return behaviour;
    }

    public void setBehaviour(General.behaviour behaviour) {
        this.behaviour = behaviour;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof CacheKey)) return false;

        CacheKey cacheKey = (CacheKey) o;

        if (!apiName.equals(cacheKey.apiName)) return false;
        if (behaviour != cacheKey.behaviour) return false;
        if (endpointsAttributes != null ? !endpointsAttributes.equals(cacheKey.endpointsAttributes) : cacheKey.endpointsAttributes != null)
            return false;
        if (!environment.equals(cacheKey.environment)) return false;
        if (version != null ? !version.equals(cacheKey.version) : cacheKey.version != null) return false;

        return true;
    }

    @Override
    public int hashCode() {
        int result = apiName.hashCode();
        result = 31 * result + environment.hashCode();
        result = 31 * result + (version != null ? version.hashCode() : 0);
        result = 31 * result + (endpointsAttributes != null ? endpointsAttributes.hashCode() : 0);
        result = 31 * result + behaviour.hashCode();
        return result;
    }
}
