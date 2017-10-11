package com.tdigital.sd.model;


import org.codehaus.jackson.annotate.JsonProperty;

public class SDError {
    private String description;
    @JsonProperty("error_code")
    private String errorCode;

    public SDError() {

    }

    public SDError(String description, String errorCode) {
        this.description = description;
        this.errorCode = errorCode;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    @JsonProperty("error_code")
    public String getErrorCode() {
        return errorCode;
    }

    @JsonProperty("error_code")
    public void setErrorCode(String errorCode) {
        this.errorCode = errorCode;
    }
}
