# Getting Started

There are three integration approaches. Pick the one that matches your stack.

## Approach 1 — Deploy the Java application

Deploy the provided demo application as a microservice. It is a Spring Boot app that already
integrates and exposes the SDK's capabilities. You can run it on Docker or directly on your server
using the runnable jar produced by building the app.

!!! note
    The app is just an example — adapt the code to your needs, especially the exposed endpoints you
    will consume.

1. Copy the contents of `ProxyU-Client-JavaSDK-{version}.zip` to
   `~/.m2/repository/com/jibecompany/proxyu-java-client/{version}/`.
2. Set these properties in your `application.properties`:

    ```properties
    proxyU.host=proxyu:9365            # FQDN and port of your proxyU instance
    proxyU.privateKey=path/to/proxyu.key
    proxyU.certificate=path/to/proxyu.pem
    proxyU.rootCertificate=path/to/root.crt
    ```

3. Build and deploy the app. If you're new to deploying Spring Boot apps, these guides help:
    - <https://javatechonline.com/deploy-spring-boot-docker-spring-boot/>
    - <https://dev.to/nikhilxd/deploying-a-spring-boot-application-a-comprehensive-guide-3iai>

See the full [Demo Application guide](demo-app.md) for the Docker setup.

## Approach 2 — Integrate the Java SDK as a library

Integrate the SDK directly into your own application.

!!! note "Prerequisite"
    Java 17 is required.

1. Copy the contents of `ProxyU-Client-JavaSDK-{version}.zip` to
   `~/.m2/repository/com/jibecompany/proxyu-java-client/{version}/`.

2. Add the Maven dependency:

    ```xml
    <!-- ProxyU Java SDK -->
    <dependency>
        <groupId>com.jibecompany</groupId>
        <artifactId>proxyu-java-client</artifactId>
        <version>${version}</version>
    </dependency>
    ```

3. Set these properties in your `application.properties`:

    ```properties
    proxyU.host=proxyu:9365            # FQDN and port of your proxyU instance
    proxyU.privateKey=path/to/proxyu.key
    proxyU.certificate=path/to/proxyu.pem
    proxyU.rootCertificate=path/to/root.crt
    ```

4. Implement the **`ProxyUClientStorage`** interface — provide your own custom DB implementation.
5. Implement the **`ProxyUClientCallbacks`** interface — provide behaviour for handling received data.
6. Import **`ProxyUClientConfiguration`** in your configuration file and define the
   `proxyUClientStorage`, `proxyUClientCallbacks`, and `proxyUClient` beans:

    ```java
    @Bean
    ProxyUClientStorage proxyUClientStorage() {
        return new StorageService();
    }

    @Bean
    ProxyUClientCallbacks proxyUClientCallbacks() {
        return new ClientCallbacks();
    }

    @Bean
    ProxyUClient proxyUClient(
            ManagedChannel channel,
            ProxyUClientStorage proxyUClientStorage,
            ProxyUClientCallbacks proxyUClientCallbacks
    ) {
        return new ProxyUClient(channel, proxyUClientStorage, proxyUClientCallbacks);
    }
    ```

7. Inject `proxyUClient` in your service:

    ```java
    private final ProxyUClient proxyUClient;

    public DemoService(ProxyUClient proxyUClient) {
        this.proxyUClient = proxyUClient;
    }
    ```

Then use the client to drive the flows — see [SDK Capabilities](capabilities.md). The
[Demo Application](demo-app.md) shows all of these integration steps in a working example.

## Approach 3 — Build your own SDK

If the first two approaches don't suit you, implement your own client library (in your backend's
preferred language) that interacts with the ProxyU server.

1. Use the `proxyu.proto` protocol file in the SDK's resources folder to generate a gRPC client for
   your language:
    - **Node** → <https://grpc.io/docs/languages/node/basics/#loading-service-descriptors-from-proto-files>
    - **PHP** → <https://grpc.io/docs/languages/php/basics/#protoc>
    - **.NET** → <https://learn.microsoft.com/en-us/aspnet/core/grpc/basics#add-a-proto-file-to-a-c-app>
    - **Other languages** → <https://grpc.io/docs/languages/>
2. Use the provided SDK as a reference for building your client from the generated code — see the
   `ProxyUClientConfiguration` and `ProxyUClient` classes.
3. Use the connection details and certificates for your ProxyU instance to test it and confirm you
   can generate a correlation message.
