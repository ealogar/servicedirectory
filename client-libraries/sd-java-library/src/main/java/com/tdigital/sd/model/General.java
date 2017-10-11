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

public class General {

    public static final String SD_URL = "http://localhost:8000/sd/v1/apis/{apiName}/endpoints";
    public static enum behaviour {PARAM_CHECK_STRICT, PARAM_NO_CHECK};
    public static final int SECONDS_TO_MILLIS_FACTOR = 1000;

}
