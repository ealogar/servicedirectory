/*
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
*/

package com.tdigital.sd;

import com.tdigital.sd.model.Endpoint;
import com.tdigital.sd.model.General;

import java.util.List;
import java.util.Map;
import java.util.Set;

public interface SDDiscovery {

    List<Endpoint> getEndpoints(String apiName, String environment, String version, Map<String, String> params, General.behaviour behaviour) throws Exception;

    List<Endpoint> getEndpoints(String apiName, String environment, String version, Map<String, String> params) throws Exception;

    List<Endpoint> getEndpoints(String apiName, String environment, Map<String, String> params, General.behaviour behaviour) throws Exception;

    List<Endpoint> getEndpoints(String apiName, String environment, Map<String, String> params) throws Exception;
}
