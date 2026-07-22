# Troubleshooting

## gRPC "Failed to frame message"

```text
Status{code=CANCELLED, description=Failed to stream message,
cause=io.grpc.StatusRuntimeException: INTERNAL: Failed to frame message}
```

**Cause / fix.** A conflicting gRPC version pulled in by another Maven dependency. Make sure no other
dependency conflicts with the gRPC version bundled in the SDK. The SDK uses **`io.grpc` version
1.56.0**.

## Demo app won't start

```bash
# Check Docker is running
docker --version

# Check the container logs
docker logs datau-demo-app
```

## Cannot connect to ProxyU

```text
Error: io.grpc.StatusRuntimeException: UNAVAILABLE: io exception
```

**Fix.** Ensure the ProxyU server is running and accessible at the configured host (default
`proxyu0:9365`). This error is expected until you have a running ProxyU server.

## Certificate errors

```text
Error: Certificate validation failed
```

**Fix.** Verify that your certificates are in `src/main/resources/tls/`, are named correctly
(`proxyu0.key`, `proxyu0.crt`, `root.crt`), and were issued by the DataU CA.

## Port already in use

```text
Error: Bind for 0.0.0.0:8080 failed: port is already allocated
```

**Fix.** Change the port in `docker-compose.yml`, or stop the conflicting service.

## Getting help

Contact **[datau.support@jibecompany.com](mailto:datau.support@jibecompany.com)** for:

- ProxyU server endpoint details
- TLS certificates issued by the DataU CA

## Additional resources

- **ProxyU integration documentation** — bundled in the SDK jar (`README.MD`).
- **gRPC protocol** — the `proxyu.proto` file in the SDK's resources folder.
