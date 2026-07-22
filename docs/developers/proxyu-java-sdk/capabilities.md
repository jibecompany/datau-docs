# SDK Capabilities

This is a summary of the SDK's capabilities. For full details, consult the SDK's Java documentation
(Javadoc).

!!! warning "Respect parameter sizes"
    Make sure you respect the size limits of each parameter when calling the methods below. You can
    find the size of each parameter in the method's description in the Java documentation.

![Correlation & permission flows](../../assets/correlation-permission.png)

## Correlation

Correlation links your application to a data subject's DataU identity.

### Generating a correlation message

Use `proxyUClient#createCorrelationMessage` to create a correlation message.

To use the correlation message you have two options:

- **Option A** — Embed it in a **QR code** that your data subjects scan.
- **Option B** — Embed it in a **button** that links to DashboardU:

    ```text
    $DASHBOARDU_ENV_NAME/#/decode?message=URL_ENCODED_CORRELATION_MESSAGE
    ```

!!! example "Example"
    For this correlation message:

    ```text
    1kC0HYOItVV8gUNrdwCjYh1zw47IvQRdAIqZ3ukao0cDESPhhi/r8X5ZthJtFMZFXhYr6BC4qFht0x5evjAnBYT4g/NU1kcLqeOe4tHZXbBy6Yu21qO5EDojVlUQPUnWizw8d9nm3SXrcxb9N9ytdg==
    ```

    - On **STAGE**, the link would be:
      `https://dashboardu.datau-stage.jibe.cloud/#/decode?message=1kC0HYOItVV8gUNrdwCjYh1zw47IvQRdAIqZ3ukao0cDESPhhi%2Fr8X5ZthJtFMZFXhYr6BC4qFht0x5evjAnBYT4g%2FNU1kcLqeOe4tHZXbBy6Yu21qO5EDojVlUQPUnWizw8d9nm3SXrcxb9N9ytdg%3D%3D`
    - On **PROD**, the link would be:
      `https://dashboardu.datau.jibe.cloud/#/decode?message=1kC0HYOItVV8gUNrdwCjYh1zw47IvQRdAIqZ3ukao0cDESPhhi%2Fr8X5ZthJtFMZFXhYr6BC4qFht0x5evjAnBYT4g%2FNU1kcLqeOe4tHZXbBy6Yu21qO5EDojVlUQPUnWizw8d9nm3SXrcxb9N9ytdg%3D%3D`

!!! note "The correlation message MUST be URL-encoded."

Upon consuming the link, the correlation message is decoded and the correlation between the data
processor (you) and the data subject happens.

### Redirecting the user back to your app

Add the `redirect_uri` query parameter to send the user back to your application:

```text
&redirect_uri=https%3A%2F%2Fgoogle.com
```

!!! note
    The `redirect_uri` value **MUST be URL-encoded**. By default the user is redirected in the same
    tab; add `&target=_blank` to open the URI in a new tab.

### Handling the result

- Implement the **`onPublicKeyReceived`** callback. Use it to save the `publicKey:correlationMessage`
  mapping for later use when generating permission-request messages, and to link the `publicKey` with
  a user via the `correlationMessage` received both here and in `proxyUClient#createCorrelationMessage`.
- A correlation message is valid **72 hours** from the moment it was generated.

## Document submission

Submit a **Terms & Conditions** document for the data subject to see when giving consent.

Use `proxyUClient#submitDocument` with a `LegalPolicyDocument` object containing:

- The **URL** where the document is stored. This must be a public URL (a CDN is fine).
- The **SHA3-256 hash** of the document in Hex format.

!!! example
    For the document at
    `https://repo.maven.apache.org/maven2/springframework/spring-web/1.2.6/maven-metadata.xml`, the
    SHA3-256 hash in Hex would be
    `4025edc8feca5c9e7a387b78a4ff4b9860d7723039e4e269d177c384cfdc745d`.

## Permission

Permission requests the subject's consent to access specific data.

### Generating a permission message

Use `proxyUClient#createPermissionRequestMessage` to create a permission message. Its parameters:

| Parameter | How to build it |
| --- | --- |
| **subject** | The public key received in `ClientCallbacks#onPublicKeyReceived` after `/correlation`. |
| **data** | Use `DataIdentificationGraphHelper#getNodeUUID` to get the UUID of a data field or a group of DATA fields. Look through the SDK's `didgraph.yaml` and use the description of the node that suits you. |
| **process** | Use `DataIdentificationGraphHelper#getProcessUUID` with `BULK` or `INDIVIDUAL` (see below). |
| **policy** | The SHA3-256 file hash (Hex) of the Terms & Conditions document. |
| **reason** | Optional — you can send a random UUID. |
| **rewardPoints** | Points awarded to the subject on granting access. Set to `0` to skip rewards. |

!!! warning "Validate the node UUID"
    Check whether the result of `getNodeUUID` is `null` — that means the data field/group name is
    invalid or does not exist in DataU.

**Process types:**

- **`BULK`** — request CSV files with multiple data values from a data subject.
- **`INDIVIDUAL`** — request single data values.

!!! note "BULK metadata fields"
    On the `BULK` flow, the shared file must contain the metadata fields `user_id` and `date_time`.

### Using the permission message

As with correlation, use it via a QR code (**Option A**) or a DashboardU link (**Option B**):

```text
$DASHBOARDU_ENV_NAME/#/decode?message=URL_ENCODED_PERMISSION_MESSAGE
```

!!! note
    The permission message **MUST be URL-encoded**. Add `&redirect_uri=<url-encoded-uri>` to return
    the user to your app, and `&target=_blank` to open it in a new tab.

Upon consuming the link, the permission message is decoded into a permission request for the data you
created it for.

### Handling the result

- Implement the **`onGrantedStatusReceived`** callback. Use it to save the `granted:permissionMessage`
  mapping, so you can later link the granted status with a user via the `permissionMessage` received
  both here and in `proxyUClient#createPermissionRequestMessage`.
- A permission message is valid **72 hours** from the moment it was generated.
