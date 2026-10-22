# SailPoint and governance

## What is SailPoint IdentityIQ or Identity Security Cloud?
SailPoint is an identity governance and administration (IGA) platform. It aggregates accounts from applications, correlates them to identities, manages access requests, certifications, provisioning, and policy such as SoD.

## What are aggregation and correlation in SailPoint?
Aggregation pulls accounts and entitlements from a source application into the IAM tool. Correlation matches those accounts to the right identity using rules or attributes like employee ID or email. Uncorrelated accounts become orphan accounts.

## What are roles in SailPoint?
Roles bundle entitlements. Business roles describe job functions and IT roles bundle technical access. Role mining finds patterns to build roles. Birthright roles are granted automatically.

## What is an access certification or access review?
Managers or owners periodically confirm whether users still need their access and revoke what is not needed. It supports compliance such as SOX, ISO 27001 and HIPAA. Typical cadence is quarterly or yearly for sensitive access.

## What are SailPoint workflows, rules and connectors?
Connectors integrate target systems such as AD, databases and SaaS. Rules (BeanShell or Java in IdentityIQ) customize aggregation, correlation and provisioning. Workflows orchestrate approvals and provisioning steps.

## What is provisioning?
Provisioning creates, updates or removes accounts and entitlements on target systems based on approved requests or lifecycle events. Deprovisioning on leaver events is a key control.

## What compliance frameworks relate to IAM?
SOX (financial controls, SoD), ISO 27001 (access control), HIPAA, PCI DSS (restrict access, MFA), GDPR (data minimization). Auditors ask for evidence of reviews, approvals and timely removal of access.
