# Didn't find your language?

There is no ProxyU client for your stack yet — only [Java](../java-client/index.md) is available today, with
[Go](../go-client.md) under construction. You can still integrate, in one of two ways.

## Run the Java application as a microservice

Deploy the provided demo application as a microservice. It is a Spring Boot app that already
integrates and exposes the SDK's capabilities. You can run it on Docker or directly on your server
using the runnable jar produced by building the app.

!!! note
    The app is just an example — adapt the code to your needs, especially the exposed endpoints you
    will consume.

1. Download the [demo application and the SDK](../java-client/index.md#downloads)
   (`proxyu-java-client-dp-demo-app-1.1.0.zip` and `proxyu-java-client-SDK-1.1.0.zip`).
2. Copy the contents of the SDK zip to
   `~/.m2/repository/com/jibecompany/proxyu-java-client/1.1.0/`.
3. Set these properties in your `application.properties`:

    ```properties
    proxyU.host=proxyu:9365            # FQDN and port of your proxyU instance
    proxyU.privateKey=path/to/proxyu.key
    proxyU.certificate=path/to/proxyu.pem
    proxyU.rootCertificate=path/to/root.crt
    ```

4. Build and deploy the app. If you're new to deploying Spring Boot apps, these guides help:
    - <https://javatechonline.com/deploy-spring-boot-docker-spring-boot/>
    - <https://dev.to/nikhilxd/deploying-a-spring-boot-application-a-comprehensive-guide-3iai>

See the full [Demo Application guide](../demo-app.md) for the Docker setup.

## Build your own client

Implement your own client library (in your backend's
preferred language) that interacts with the ProxyU server.

!!! abstract "Reference material"
    - [:octicons-file-code-24: `proxyu.proto`](../proxyu.proto) — the gRPC service and message
      definitions. Generate your client from this file.
    - [:octicons-book-24: Integration Protocol Specification](../proxyu-integration.md) — what each RPC
      and message field means, and the error numbers you must return.

1. Use [`proxyu.proto`](../proxyu.proto) to generate a gRPC client for your language:
    - **Node** → <https://grpc.io/docs/languages/node/basics/#loading-service-descriptors-from-proto-files>
    - **PHP** → <https://grpc.io/docs/languages/php/basics/#protoc>
    - **.NET** → <https://learn.microsoft.com/en-us/aspnet/core/grpc/basics#add-a-proto-file-to-a-c-app>
    - **Other languages** → <https://grpc.io/docs/languages/>
2. Implement the five RPCs of the `ProxyUIntegration` service — `Correlation`, `SubmitDocument`,
   `Permission`, `Data`, and `GetDataIdentificationGraph`. The
   [Integration Protocol Specification](../proxyu-integration.md#integration-api) documents the message
   flow for each one; note that `Correlation`, `Permission`, and `Data` are **streams**.
3. Return the [documented error numbers](../proxyu-integration.md#error-numbers) on every `error` field
   — they are negative integers.
4. Use the provided SDK as a reference for building your client from the generated code — see the
   `ProxyUClientConfiguration` and `ProxyUClient` classes.
5. Use the connection details and certificates for your ProxyU instance to test it and confirm you
   can generate a correlation message.

!!! question "Need access?"
    Either route needs a ProxyU server endpoint and TLS certificates issued by the DataU CA. Contact
    **[datau.support@jibecompany.com](mailto:datau.support@jibecompany.com)** to get set up.
