# PAM and Zero Trust

## What is PAM (Privileged Access Management)?
PAM secures powerful accounts such as admins and service accounts. Core ideas: vault credentials, rotate passwords, just-in-time access, session recording and approval for privileged sessions. CyberArk, Delinea and BeyondTrust are common tools.

## What is CyberArk?
CyberArk is a leading PAM product. The Digital Vault stores privileged credentials, CPM rotates them, PSM records and proxies sessions, and Conjur or Secrets Manager handles application secrets.

## What is Saviynt?
Saviynt is a cloud IGA platform that also covers application access governance, SoD analytics and PAM features. It is a SailPoint alternative with strong risk and compliance analytics.

## What is Zero Trust?
Zero Trust means never trust, always verify: authenticate and authorize every request using identity, device health and context, assume breach and apply least privilege and microsegmentation.

## What is Conditional Access?
Conditional access applies policies at sign-in, for example requiring MFA from new locations or blocking non-compliant devices. It is risk-based authentication in practice.

## What is a brute force vs password spraying attack?
Brute force tries many passwords against one account. Password spraying tries a few common passwords against many accounts to avoid lockouts. Defenses: MFA, lockout and rate limits, breached-password checks and monitoring of failed logins.

## What is Identity Threat Detection and Response (ITDR)?
ITDR monitors identity systems for attacks such as credential theft, Kerberoasting, privilege escalation and anomalous logins, and automates responses like forcing resets or revoking sessions.
