# QA and automation for IAM

## How do I test an IAM application in UAT?
Cover joiner, mover and leaver flows, access request and approval, SoD policy blocks, certification campaigns, password reset, MFA and error paths. Use test identities, record expected results, raise defects with steps, evidence and severity, and retest after fixes.

## How do I write a good defect report?
Include a clear title, environment, steps to reproduce, expected vs actual result, screenshots or logs, severity and priority, and the build version. Link it to the test case in your test management tool such as Micro Focus ALM.

## What is Selenium and how do I make tests stable?
Selenium automates browsers. Use the Page Object Model, explicit waits instead of sleeps, stable locators such as ids and data attributes, independent test data, and run tests in CI with reports.

## What is Playwright and why use it?
Playwright is a modern automation framework with auto-waiting, multiple browsers, tracing and API testing. It is fast and has good debugging tools, and works with AI agents through MCP for prompt-driven tests.

## How can AI help QA?
AI can generate test cases from requirements, suggest locators, summarize failures and draft scripts. Always review generated tests, keep humans in the loop, and avoid sending sensitive data to external services.

## What is API testing for IAM?
Test REST and SCIM endpoints for status codes, schema, authentication, authorization (a user must not read others' data) and rate limiting. Tools: Postman, REST Assured, Playwright API tests.
