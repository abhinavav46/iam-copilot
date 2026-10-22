# IAM basics

## What is IAM (Identity and Access Management)?
IAM is the set of processes and tools that make sure the right people and systems have the right access to the right resources at the right time. It covers identity lifecycle, authentication, authorization, governance and auditing.

## What is the difference between authentication and authorization?
Authentication (AuthN) proves who you are, for example password plus MFA. Authorization (AuthZ) decides what you may do after that, for example roles and policies.

## What is least privilege?
Least privilege means users and services get only the minimum access needed for their job, for the shortest time needed. It limits the damage of compromised accounts and insider mistakes.

## What is the Joiner Mover Leaver (JML) lifecycle?
Joiner: create accounts and give birthright access when someone starts. Mover: adjust access when the role or department changes and remove old access. Leaver: disable and delete accounts promptly on exit. Automating JML removes orphan and stale accounts.

## What is RBAC vs ABAC?
RBAC (role-based access control) grants access through roles such as Finance Analyst. ABAC (attribute-based) decides using attributes like department, location, device and time. RBAC is simple to audit; ABAC is more flexible. Many companies combine both.

## What is Segregation of Duties (SoD)?
SoD prevents one person from holding conflicting permissions, such as creating a vendor and approving its payment. IAM tools detect SoD violations and block or flag them during requests and certifications.

## What is an orphan account or dormant account?
An orphan account has no valid owner, for example after the owner left. A dormant account is unused for a long period, often 90 days. Both are security risks and should be reviewed and disabled.

## What is MFA (multi-factor authentication)?
MFA requires two or more factors: something you know, have, or are. Phishing-resistant options such as FIDO2 passkeys are stronger than SMS codes. MFA blocks most credential-stuffing attacks.

## What is SSO (single sign-on)?
SSO lets a user authenticate once and access many applications through a trusted identity provider using SAML or OpenID Connect. It improves user experience and centralizes control and logging.
