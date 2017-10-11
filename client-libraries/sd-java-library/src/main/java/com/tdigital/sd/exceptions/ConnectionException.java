package com.tdigital.sd.exceptions;


public class ConnectionException extends SDLibraryException {

    public ConnectionException() {
        super("Connection Exception.");
    }

    public ConnectionException(String message) {
        super(message);
    }

    public ConnectionException(Throwable e) {
        super(e);
    }

    public ConnectionException(String message, Throwable e) {
        super(message, e);
    }

}
