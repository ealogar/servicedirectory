package com.tdigital.sd;

import com.tdigital.sd.utils.SDConfig;
import com.tdigital.sd.utils.UpdateTool;
import junit.framework.Assert;
import org.junit.Before;
import org.junit.Test;


public class UpdateToolTest {

    private String host1;
    private String host2;
    private Integer port1;

    @Before
    public void init() {
        host1 = "localhost1";
        host2 = "localhost2";
        port1 = 1234;
    }


    @Test
    public void mixPartialConfigurations() {
        SDConfig sdConfig1 = new SDConfig();
        sdConfig1.setHost(host1);
        SDConfig sdConfig2 = new SDConfig();
        sdConfig2.setPort(port1);

        SDConfig result = UpdateTool.updateObject(sdConfig1, sdConfig2);
        Assert.assertEquals(result.getHost(), host1);
        Assert.assertEquals(result.getPort(), port1);
    }

    @Test
    public void mixPartialConfigurationsWithTwoHost() {
        SDConfig sdConfig1 = new SDConfig();
        sdConfig1.setHost(host1);
        SDConfig sdConfig2 = new SDConfig();
        sdConfig2.setPort(port1);
        sdConfig2.setHost(host2);

        SDConfig result = UpdateTool.updateObject(sdConfig1, sdConfig2);
        Assert.assertEquals(result.getHost(), host1);
        Assert.assertEquals(result.getPort(), port1);
    }
}
