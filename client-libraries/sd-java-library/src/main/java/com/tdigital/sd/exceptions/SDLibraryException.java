package com.tdigital.sd.exceptions;


public class SDLibraryException extends Exception {

    public SDLibraryException() {
        super("Service Directory Library Exception.");
    }

    public SDLibraryException(String message) {
        super(message);
    }

    public SDLibraryException(Throwable e) {
        super(e);
    }

    public SDLibraryException(String message, Throwable e) {
        super(message, e);
    }
}
