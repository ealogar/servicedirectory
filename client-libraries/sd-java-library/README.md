# Service Directory Java Library

## Overview

Java 7 library that allows requesting endpoints to the Service Directory.

## Usage

### Maven

Include this dependency in your maven descriptor file.

```xml
<dependency>
	<groupId>com.tdigital</groupId>
    <artifactId>sd-java-library</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Property File

```
sd_host=demo-tdaf-sd-01
sd_port=8000

# TTL Hours value.
ttl=168

# TTR Seconds value.
ttr=3600

sd_version=v1

# timeout in seconds.
timeout=20
```

### Development


```java
SDDiscovery sd = new SDDiscoveryImpl()
//Search the premium endpoints of sample capability in development environment.
Map<String, String> map = new HashMap<String, String>();
map.put("premium", "true");
List<Endpoint> endpoints =sdDiscovery.getEndpoints("sample", "development", map);
```