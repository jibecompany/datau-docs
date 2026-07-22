# DataU

**DataU** is a **data-sovereignty platform**. Its founding principle is simple: **people own their
data**. Personal data stays under the individual's control at all times — stored on their behalf,
shared only with explicit consent, and anonymised before it reaches any organisation that processes
it.

DataU provides the identity, authentication, consent, and data-governance layer that applications
build on. A unified identity layer (Keycloak / OpenID Connect) gives users a single sign-on across
every connected tool, so they authenticate once and move freely between applications.

!!! info "More coming soon"
    This is the general overview of DataU. More platform documentation will be added here over time.

## Documentation

<div class="grid cards" markdown>

-   :material-account-heart: **User Guide (Data Subject)**

    ---

    For people who want to control their own data. Learn how to use **DashboardU** — your control
    centre for signing in, seeing who you've shared data with, and managing consent.

    [:octicons-arrow-right-24: DashboardU User Guide](data-subjects/dashboardu.md)

-   :material-code-braces: **Developer Guide (Data Processor)**

    ---

    For developers building applications on top of DataU. Learn how to integrate the **ProxyU
    client**, correlate with data subjects, and request data with consent.

    [:octicons-arrow-right-24: ProxyU Client Guide](developers/index.md)

</div>

## Data governance principles

DataU is built on a small set of inalienable principles:

- **Individual ownership** — data subjects keep full GDPR rights over their personal data. Consent
  is a lawful basis for processing only, never a transfer of ownership.
- **Consent-based sharing** — data is shared only with explicit consent, given at the moment each
  data item is saved.
- **Anonymisation** — personal identifiers (such as names and addresses) are replaced with
  anonymised tokens before storage. Processors never see the real values.
- **GDPR compliance** — the platform implements GDPR-rooted controls: access, rectification,
  erasure, and portability.
