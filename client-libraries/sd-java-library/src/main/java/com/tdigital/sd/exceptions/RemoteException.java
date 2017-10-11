package com.tdigital.sd.exceptions;


public class RemoteException extends SDLibraryException {

    public RemoteException() {
        super("Remote Exception.");
    }

    public RemoteException(String message) {
        super(message);
    }

    public RemoteException(Throwable e) {
        super(e);
    }

    public RemoteException(String message, Throwable e) {
        super(message, e);
    }
}
