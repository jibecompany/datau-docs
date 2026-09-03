# Demo Application

The **DataU Data Processor Demo Application** is a Spring Boot app that integrates the ProxyU Java
SDK and exposes its capabilities through REST endpoints. Use it as a ready-to-run reference for your
own integration.

## Prerequisites

1. **The demo application** — download the demo application zip from
   [Downloads](java-client/index.md#downloads) and unzip it. It tracks the SDK version, so use the
   zip matching your SDK; earlier releases are listed under
   [previous versions](java-client/index.md#previous-versions).
2. **Docker Desktop** installed and running — <https://www.docker.com/products/docker-desktop>.
3. **Certificates**, placed in `src/main/resources/tls/`:
    - `proxyu0.key` — your private key
    - `proxyu0.crt` — your certificate
    - `root.crt` — the DataU root certificate

## Project structure

```text
demo/
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Multi-container orchestration
├── src/main/java/com/example/demo/
│   ├── DemoApplication.java      # Main Spring Boot app
│   ├── DemoController.java       # REST API endpoints
│   ├── DemoService.java          # Business logic (ProxyU client wrapper)
│   ├── ClientCallbacks.java      # Handles async responses from ProxyU
│   ├── StorageService.java       # Data persistence (BoltDB)
│   └── BeanConfiguration.java    # Spring dependency injection
├── src/main/resources/
│   ├── application.properties    # Configuration
│   └── tls/                      # proxyu0.key, proxyu0.crt, root.crt
└── pom.xml                       # Maven dependencies
```

## Quick start

```bash
# Start all services
docker-compose up --build

# Or run in the background
docker-compose up -d --build
```

## API endpoints

### `GET /correlation`

Generate a link that correlates your app with a user's DataU identity.

```bash
curl http://localhost:8080/correlation
```

**Response:** a URL that redirects to the DataU dashboard. The user opens the link in DashboardU;
your app then receives the user's public key via `ClientCallbacks.onPublicKeyReceived()`.

### `GET /permission?subjectPublicKey={base64_encoded_key}`

Request permission to access specific data from a user.

```bash
# Replace with the actual public key from the correlation step
curl "http://localhost:8080/permission?subjectPublicKey=O5Dus4NUS4Ln%2BKmDUbadoA%2BjbKsEXM%2FWkNJnE6QtoqM%3D"
```

**Response:** a URL that redirects to the DataU dashboard with the permission request. The user
approves or denies in DashboardU; your app receives the status via
`ClientCallbacks.onGrantedStatusReceived()`.

### `POST /documents`

Submit legal documents (Terms & Conditions) to the DataU platform (recorded on the blockchain system
for transparency over T&Cs referenced in a permission request).

```bash
curl -X POST http://localhost:8080/documents \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/terms.pdf",
    "hash": "128d4f4c170f0e96f18f0188c9036d76f6180cdd17cd7de4a30a6cfb95319b01"
  }'
```

**Response:** `SUCCESS` or `FAILED`.

## Application flow — the complete user journey

1. App calls `/correlation` → save the `correlationId` for the user
   (e.g. `user.setDataUCorrelationId(correlationMessage.getCorrelationId())`).
2. User clicks the correlation link and goes to DashboardU.
3. `ProxyUClientCallbacks.onPublicKeyReceived()` fires → save the user's `publicKey` for
   `CorrelationMessage.getCorrelationId()`.
4. App calls `/permission` with the user's `publicKey`.
5. User clicks the permission-request link and approves in DashboardU.
6. `ProxyUClientCallbacks.onGrantedStatusReceived()` fires → save the consent status for the user.
7. `ProxyUClientStorage.saveOrUpdateUserData()` fires → implement it to save the received data.
8. Later, the user goes to DashboardU to see their shared data.
9. `ProxyUClientStorage.extractUserData()` fires → implement it so the user can retrieve and view
   their data in DashboardU.
10. At some point, the user decides to revoke consent.
11. `ProxyUClientStorage.deleteData()` fires → implement it to remove stored data for the user.

## Understanding the code

### `DemoService.java` — core business logic

```java
@Service
public class DemoService {
    private final ProxyUClient proxyUClient;  // SDK client

    // Generates a correlation message
    public String createCorrelationMessage() {
        return proxyUClient.createCorrelationMessage();
    }

    // Generates a permission-request message
    public String createPermissionRequestMessage(...) {
        return proxyUClient.createPermissionRequestMessage(...);
    }
}
```

### `ClientCallbacks.java` — async response handlers

```java
public class ClientCallbacks implements ProxyUClientCallbacks {

    // Called when the user clicks the correlation link
    @Override
    public void onPublicKeyReceived(String publicKey, String correlationMessage) {
        // TODO: save publicKey to link with your user ID
    }

    // Called when the user approves/denies the permission request
    @Override
    public void onGrantedStatusReceived(boolean granted, String permissionMessage) {
        // TODO: save consent status
    }
}
```

### `StorageService.java` — data persistence

Uses **BoltDB** (an embedded key-value database) as an example to store received user data,
organised by *subject → process → data UUID*.

## Configuration

Override these in `docker-compose.yml` or via the `-e` flag:

| Variable | Default | Description |
| --- | --- | --- |
| `PROXYU_HOST` | `proxyu0:9365` | ProxyU server address |
| `PROXYU_PRIVATE_KEY` | `/app/resources/tls/proxyu0.key` | Private key path |
| `PROXYU_CERTIFICATE` | `/app/resources/tls/proxyu0.crt` | Certificate path |
| `PROXYU_ROOT_CERT` | `/app/resources/tls/root.crt` | Root CA cert path |
| `DB_BOLT_FILENAME` | `/app/resources/data.db` | Database file path |
| `SERVER_PORT` | `8080` | Spring Boot port |

## Docker commands

```bash
docker-compose up               # start services
docker-compose up -d            # start in the background
docker-compose logs -f dp-demo-app   # view logs
docker-compose down             # stop services
docker-compose up --build       # rebuild and restart
```

## Important notes

!!! warning "ProxyU server required"
    This application **cannot run standalone**. It requires:

    1. A **ProxyU server** running and accessible — update `PROXYU_HOST` to point at an existing
       ProxyU server.
    2. **Valid certificates** issued by the DataU CA, placed in `src/main/resources/tls/`.

    The app will start but fail to connect to ProxyU if the server isn't running (you'll see
    `io.grpc.StatusRuntimeException: UNAVAILABLE`). This is expected until you have a running ProxyU
    server.

## Next steps

1. Contact **[datau.support@jibecompany.com](mailto:datau.support@jibecompany.com)** to obtain your
   ProxyU server endpoint details and TLS certificates.
2. Test the flow: start the services, call `/correlation`, click the correlation link, then request
   a permission.

See [Troubleshooting](troubleshooting.md) if you hit errors.
