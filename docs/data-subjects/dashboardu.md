# DashboardU User Guide

**DashboardU** (the DataU Dashboard) at [dashboardu.datau.jibe.cloud](https://dashboardu.datau.jibe.cloud)
is your control centre for monitoring how your data is shared. It is powered by **DataU**, the
data-sovereignty layer that handles identity, authentication, consent, and data governance for every
connected tool.

## Authentication & single sign-on

DataU uses **Keycloak** at `auth.datau.jibe.cloud` with **OpenID Connect (OIDC)** to provide secure
single sign-on across all tools. You log in once and move freely between tools without re-entering
your credentials.

### Logging in

1. Click **Continue with DataU** or **Log in** on any connected tool.
2. You are redirected to `auth.datau.jibe.cloud`.
3. Enter your credentials and sign in.
4. You are redirected back — now authenticated across all tools simultaneously.

### Registering a new account

1. On any DataU app's landing page, click **Register**.
2. Complete the DataU registration form.
3. Verify your email address.
4. Log in with your new credentials.

## My Shared Data

DashboardU has two sections in the bottom navigation bar.

### My Data

Shows all organisations you have shared data with. Use the **Search organisation** field to filter.
Each entry shows *what* data was shared and *when*. It displays **"No data"** when no sharing has
occurred yet.

!!! note "Figure — My Data view showing no shared data yet"
    *Screenshot to be added.*

### My Settings

- **Language** — change the display language.
- **Terms and conditions** — view the platform T&Cs.
- **Help** — access support documentation.
- **Log out** — sign out of DataU.

!!! note "Figure — My Settings with language, terms, help and logout options"
    *Screenshot to be added.*

## Roles & permissions

Your DataU account determines which tools you can access.

=== "Citizen / User"

    - Create and manage personal data items across all categories.
    - Control consent for each data item before sharing.
    - Monitor what data has been shared with which organisations via DashboardU.

=== "Researcher / Admin"

    - Create, publish, and analyse data-collection instruments.
    - Upload and browse anonymised datasets.
    - Sees only anonymised, token-based data — never real personal information.

!!! tip "The decode link"
    When a connected app asks to correlate with you or requests permission for a data item, you'll
    open a link that lands in DashboardU (at `/#/decode?message=...`). DashboardU decodes the
    request and lets you approve or deny it. This is the citizen side of the developer
    [correlation & permission flow](../developers/proxyu-java-sdk/capabilities.md).

## Privacy & data sovereignty

DataU is built on a data-sovereignty model — you are an active participant who decides how your data
is used:

- **Consent-based collection** — data is shared only with your explicit consent, given when you save
  each item.
- **Anonymisation** — identifiers such as names and addresses are replaced with anonymised tokens
  before storage.
- **GDPR compliance** — the platform is designed to meet EU data-protection regulations and
  European data-governance standards.
