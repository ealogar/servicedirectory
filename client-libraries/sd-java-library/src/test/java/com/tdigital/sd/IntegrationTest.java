package com.tdigital.sd;

import com.github.tomakehurst.wiremock.junit.WireMockClassRule;
import com.tdigital.sd.SDDiscovery;
import com.tdigital.sd.SDDiscoveryImpl;
import com.tdigital.sd.exceptions.RemoteException;
import com.tdigital.sd.exceptions.SDLibraryException;
import com.tdigital.sd.model.Endpoint;
import junit.framework.Assert;
import org.junit.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static com.github.tomakehurst.wiremock.client.WireMock.*;

public class IntegrationTest {

    private SDDiscovery sdDiscovery;

    @ClassRule
    @Rule
    public static WireMockClassRule wireMockRule = new WireMockClassRule(8089);


    @Before
    public void init() throws SDLibraryException {
        stubFor(get(urlEqualTo("/sd/info"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withHeader("Content-Type", "application/json")
                        .withBodyFile("responses/sd-info.json")));
        sdDiscovery = new SDDiscoveryImpl();
        verify(1, getRequestedFor(urlEqualTo("/sd/info")).withHeader("Content-Type", equalTo("application/json")));
    }

    @Test
    public void callWithoutMapParamsTest() throws Exception {
        stubFor(get(urlEqualTo("/sd/v1/apis/sample/endpoints?environment=development&behaviour=PARAM_NO_CHECK"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withHeader("Content-Type", "application/json")
                        .withBodyFile("responses/case1.json")));

        Map<String, String> map = new HashMap<String, String>();

        List<Endpoint> endpoints =sdDiscovery.getEndpoints("sample", "development", map);
        verify(1, getRequestedFor(urlEqualTo("/sd/v1/apis/sample/endpoints?environment=development&behaviour=PARAM_NO_CHECK")).withHeader("Content-Type", equalTo("application/json")));
        Assert.assertEquals(1, endpoints.size());
        Assert.assertEquals("sample", endpoints.get(0).getApiName());
        Assert.assertEquals("development", endpoints.get(0).getEnvironment());
    }


    @Test
    public void callWithMapParamsTest() throws Exception {
        stubFor(get(urlEqualTo("/sd/v1/apis/sample/endpoints?environment=development&behaviour=PARAM_NO_CHECK&premium=true"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withHeader("Content-Type", "application/json")
                        .withBodyFile("responses/case2.json")));

        Map<String, String> map = new HashMap<String, String>();
        map.put("premium", "true");

        List<Endpoint> endpoints =sdDiscovery.getEndpoints("sample", "development", map);
        Assert.assertEquals(2, endpoints.size());
        Assert.assertEquals("sample", endpoints.get(0).getApiName());
        Assert.assertEquals("development", endpoints.get(0).getEnvironment());
        Assert.assertEquals("http://sample2.dev", endpoints.get(1).getUrl());
        verify(1, getRequestedFor(urlEqualTo("/sd/v1/apis/sample/endpoints?environment=development&behaviour=PARAM_NO_CHECK&premium=true")).withHeader("Content-Type", equalTo("application/json")));
    }

    @Test
    public void callCacheTTRRecoveryTest() throws Exception {
        stubFor(get(urlEqualTo("/sd/v1/apis/sample2/endpoints?environment=development&behaviour=PARAM_NO_CHECK&premium=false"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withHeader("Content-Type", "application/json")
                        .withBodyFile("responses/case4.json")));

        Map<String, String> map = new HashMap<String, String>();
        map.put("premium", "false");

        List<Endpoint> endpoints =sdDiscovery.getEndpoints("sample2", "development", map);
        Assert.assertEquals(2, endpoints.size());
        Assert.assertEquals("sample2", endpoints.get(0).getApiName());
        Assert.assertEquals("development", endpoints.get(0).getEnvironment());
        Assert.assertEquals("http://sample2.dev", endpoints.get(1).getUrl());

        List<Endpoint> endpoints2 =sdDiscovery.getEndpoints("sample2", "development", map);
        Assert.assertEquals(2, endpoints2.size());
        Assert.assertEquals("sample2", endpoints2.get(0).getApiName());
        Assert.assertEquals("development", endpoints2.get(0).getEnvironment());
        Assert.assertEquals("http://sample2.dev", endpoints2.get(1).getUrl());
        verify(1, getRequestedFor(urlEqualTo("/sd/v1/apis/sample2/endpoints?environment=development&behaviour=PARAM_NO_CHECK&premium=false")).withHeader("Content-Type", equalTo("application/json")));
    }

    @Test
    public void callCacheTTRExpirationTest() throws Exception {
        stubFor(get(urlEqualTo("/sd/v1/apis/sample3/endpoints?environment=development&behaviour=PARAM_NO_CHECK&premium=false"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withHeader("Content-Type", "application/json")
                        .withBodyFile("responses/case5.json")));

        Map<String, String> map = new HashMap<String, String>();
        map.put("premium", "false");

        List<Endpoint> endpoints =sdDiscovery.getEndpoints("sample3", "development", map);
        Assert.assertEquals(2, endpoints.size());
        Assert.assertEquals("sample3", endpoints.get(0).getApiName());
        Assert.assertEquals("development", endpoints.get(0).getEnvironment());
        Assert.assertEquals("http://sample2.dev", endpoints.get(1).getUrl());

        Thread.sleep(1500);

        List<Endpoint> endpoints2 =sdDiscovery.getEndpoints("sample3", "development", map);
        Assert.assertEquals(2, endpoints2.size());
        Assert.assertEquals("sample3", endpoints2.get(0).getApiName());
        Assert.assertEquals("development", endpoints2.get(0).getEnvironment());
        Assert.assertEquals("http://sample2.dev", endpoints2.get(1).getUrl());
        verify(2, getRequestedFor(urlEqualTo("/sd/v1/apis/sample3/endpoints?environment=development&behaviour=PARAM_NO_CHECK&premium=false")).withHeader("Content-Type", equalTo("application/json")));
    }


    @Test(expected = RemoteException.class)
    public void apiNotFoundInSDTest() throws Exception {
        stubFor(get(urlEqualTo("/sd/v1/apis/unknownApi/endpoints?environment=development&behaviour=PARAM_NO_CHECK&premium=false"))
                .willReturn(aResponse()
                        .withStatus(404)
                        .withHeader("Content-Type", "application/json")
                        .withBodyFile("responses/error-not-found.json")));

        Map<String, String> map = new HashMap<String, String>();
        map.put("premium", "false");
        try {
            sdDiscovery.getEndpoints("unknownApi", "development", map);
        } catch(Exception e) {
            verify(1, getRequestedFor(urlEqualTo("/sd/v1/apis/unknownApi/endpoints?environment=development&behaviour=PARAM_NO_CHECK&premium=false")).withHeader("Content-Type", equalTo("application/json")));
            throw e;
        }

    }



}
