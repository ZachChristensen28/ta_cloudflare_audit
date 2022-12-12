# Cloudflare Audit Add-on (ta_cloudflare_audit) for Splunk

![GitHub](https://img.shields.io/github/license/zachchristensen28/ta_cloudflare_audit)
![Appinspect](https://github.com/ZachChristensen28/ta_cloudflare_audit/actions/workflows/appinspect-caller.yml/badge.svg)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/ZachChristensen28/ta_cloudflare_audit)
[![Cloudflare API Compatibility](https://img.shields.io/badge/Cloudflare%20API%20Compatibility-v4-success)](https://developers.cloudflare.com/api)
![Splunk Cloud Compatibility](https://img.shields.io/badge/Splunk%20Cloud%20Ready-Victoria%20|%20Classic-informational?logo=splunk)

This Splunk Technical Add-on allows collection of Audit events on a scheduled interval from Cloudfare's API.

## Documentation

Full documentation coming Soon.

### API Token Requirements (not global token)

Create a custom token with the following permissions.

Setting | Item | Permission
------- | ---- | ----------
Account | Access: Audit Logs | Read
Account | Account Settings | Read

\***Include `All accounts` for Account Resources.**

- Set Client IP address Filtering and TTL as needed.

## Disclaimer

> *This Technical Add-on (TA) is __not__ affiliated with [__Cloudflare, Inc.__](https://www.cloudflare.com/) and is not sponsored or sanctioned by the Cloudflare team. Cloudflare is and the Cloudflare web badges are [registered trademarks](https://www.cloudflare.com/trademark/) of Cloudflare, Inc. Please visit [https://www.cloudflare.com/](https://www.cloudflare.com/) for more information about Cloudflare.*

## About

Info | Description
------|----------
ta_cloudflare_audit | 0.0.1 - Splunkbase - TBD \| [GitHub](https://github.com/ZachChristensen28/ta_cloudflare_audit)

## Issues or Feature Requests

Please open an issue or feature request on [Github](https://github.com/ZachChristensen28/ta_cloudflare_audit/issues).
