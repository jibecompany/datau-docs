# Developers / Data Processors

This section is for **data processors** — developers building applications on top of DataU that need
to request and receive personal data from data subjects, with consent and full traceability.

Your application never talks to citizens' data directly. Instead it integrates with **ProxyU**, the
DataU integration bridge, and drives two core flows:

1. **Correlation** — link your application to a data subject's DataU identity.
2. **Permission** — request the subject's consent to access specific data, then receive that data
   through callbacks.

## Core concepts

- **Data subject** — the citizen who owns the data and grants (or revokes) consent, using
  [DashboardU](../data-subjects/dashboardu.md).
- **Data processor** — you: the application requesting and processing data.
- **ProxyU** — the per-tenant bridge your app connects to (over gRPC + mTLS) to run correlation and
  permission flows.
- **Correlation message** — a token your app generates and the subject consumes (via QR code or a
  DashboardU link) to establish the link between you and them.
- **Permission message** — a token that encodes a request for specific data, a process type
  (`BULK` or `INDIVIDUAL`), and the Terms & Conditions document the subject consents to.

## The correlation → permission flow

![Correlation & permission flows](../assets/correlation-permission.png)

At a high level:

1. Your app creates a **correlation message** and shows it to the subject (QR code or DashboardU
   link).
2. The subject consumes it in DashboardU; your app receives their **public key** via a callback.
3. Your app creates a **permission message** for a specific data field and shows it to the subject.
4. The subject approves in DashboardU; your app receives the **granted status** and the data via
   callbacks.

## Get started

<div class="grid cards" markdown>

-   :material-language-java: **[ProxyU Java SDK](proxyu-java-sdk/index.md)**

    ---

    The recommended path for JVM applications. Integrate the SDK as a library, or deploy the
    ready-made demo microservice.

    [:octicons-arrow-right-24: Read the SDK guide](proxyu-java-sdk/index.md)

</div>

!!! question "Need access?"
    To integrate you'll need a ProxyU server endpoint and TLS certificates issued by the DataU CA.
    Contact **[datau.support@jibecompany.com](mailto:datau.support@jibecompany.com)** to get set up.
