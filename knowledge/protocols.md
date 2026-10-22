# Protocols

## What is OAuth 2.0?
OAuth 2.0 is an authorization framework that lets an app access resources on behalf of a user using access tokens, without sharing the password. Common flows: authorization code with PKCE for web and mobile, client credentials for machine-to-machine.

## What is OpenID Connect (OIDC)?
OIDC is an identity layer on top of OAuth 2.0. It adds an ID token (a JWT) that tells the app who the user is, plus the userinfo endpoint. Used for modern SSO.

## What is SAML?
SAML 2.0 is an XML-based standard for SSO between an identity provider (IdP) and service provider (SP) using signed assertions. Common in enterprise and legacy applications.

## What is a JWT (JSON Web Token)?
A JWT has three Base64URL parts: header, payload (claims such as iss, sub, aud, exp) and signature. Always validate the signature, issuer, audience and expiry, and reject alg=none. Do not put secrets in the payload because it is only encoded, not encrypted.

## What is SCIM?
SCIM (System for Cross-domain Identity Management) is a REST and JSON standard to provision and deprovision users and groups across systems automatically. It is widely used with IAM tools for JML.

## What are LDAP, Active Directory and Kerberos?
LDAP is a directory protocol to query identities. Active Directory is Microsoft's directory service built on LDAP and Kerberos. Kerberos uses tickets for passwordless network authentication; attacks include Kerberoasting and golden tickets.

## PKCE and common OAuth mistakes
PKCE protects the authorization code flow from interception. Common mistakes: using the implicit flow, loose redirect URI matching, long-lived tokens, storing tokens in local storage, and missing state parameter checks.
