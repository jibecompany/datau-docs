# DataU Documentation

Welcome to the documentation for the **DataU platform** and the **SPOON toolset** — a suite of
EU-funded digital tools developed by **Jibe Company BV** under Work Package 2 of the
[SPOON](https://www.spoon-he.eu/) Horizon Europe project (Grant Agreement 101182299).

DataU is the **data-sovereignty infrastructure** behind SPOON. Its founding principle is simple:
**citizens own their data**. Personal data stays under the citizen's control at all times — stored
in their Personal Data Wallet, shared only with explicit consent, and anonymised before it reaches
any research team.

## Choose your path

<div class="grid cards" markdown>

-   :material-account-heart: **End Users / Data Subjects**

    ---

    You participate in SPOON studies and want to control your data. Learn how to use **DashboardU**
    and the connected SPOON apps — the SPOON Dashboard, Questionnaire Tool, Data Lake, and Personal
    Data Wallet.

    [:octicons-arrow-right-24: Go to the user guides](data-subjects/index.md)

-   :material-code-braces: **Developers / Data Processors**

    ---

    You are building an application on top of DataU and need to request and receive data from data
    subjects. Learn how to integrate the **ProxyU Java client (SDK)**, generate correlation and
    permission messages, and run the demo app.

    [:octicons-arrow-right-24: Go to the developer guides](developers/index.md)

</div>

## The DataU platform at a glance

| Tool | URL | Role |
| --- | --- | --- |
| **SPOON Dashboard** | home.datau.jibe.cloud | Single entry point for all users |
| **Questionnaire Tool** | forms.datau.jibe.cloud | Study design & survey authoring (researchers) |
| **Data Lake** | lake.datau.jibe.cloud | Anonymised dataset storage & exploration |
| **Personal Data Wallet** | wallet.datau.jibe.cloud | Citizen-controlled personal data store |
| **DataU Dashboard (DashboardU)** | dashboardu.datau.jibe.cloud | Citizen view of shared data & consent |
| **Authentication** | auth.datau.jibe.cloud | Keycloak / OpenID Connect single sign-on |

!!! info "Data governance principles"
    - **Citizen ownership** — data subjects keep full GDPR rights over their personal data.
      Consent is a lawful basis for processing only, never a transfer of ownership.
    - **Partner content ownership** — partners own the questionnaires and datasets they author;
      Jibe hosts that content under an operational licence.
    - **Platform ownership** — all DataU software and infrastructure is Jibe-owned, and remains so
      after the SPOON project ends.
