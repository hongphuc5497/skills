---
name: context-hub
description: "Fetch current API/SDK docs before writing integration code. Use whenever writing code that integrates with an external service, SDK, or API. Not for general documentation browsing or research."
license: MIT
metadata:
  version: 1.0.0
  category: general
  author: hongphuc5497
---

# Context Hub

Fetch current API/SDK documentation before writing integration code.

## When to Use

Use when writing integration code with an external API, SDK, or service. Trigger on phrases like "integrate with X", "use the Y API", "call the Z service", "what's the latest SDK for". Skip for general documentation browsing or reading internal project docs.

## Instructions

1. Identify the API/SDK the user needs documentation for
2. Fetch the latest documentation (prefer official docs, not third-party blogs)
3. Extract key patterns: authentication, base endpoints, request/response shapes, rate limits, error handling
4. Save the distilled reference to `references/<service>.md` for future reuse
5. Write integration code using the verified documentation

## Pattern

```bash
# Fetch docs
curl -sL https://api.example.com/docs
# Or
curl -sL https://docs.example.com/openapi.json

# Save distilled reference
```

## Cached References

When you fetch docs for a service, save a distilled version in `references/` so future skills can skip the re-fetch.

## Verification

- Confirm the API works with a minimal test call before writing full integration
- Always check for API versioning (v1/v2)
- Note rate limits and authentication requirements
