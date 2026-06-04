---
name: stripe-payments-api
description: Integrating Stripe payments, managing subscription billing checkout sessions, and validation signatures on webhooks.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Stripe Payments Api

## Overview
Stripe is a suite of APIs powering online payment processing and commerce solutions.

## When to Use This Skill
Use to implement e-commerce checkouts or software-as-a-service subscription pricing models.

## Quick Start (with runnable code examples)

```python
import stripe

stripe.api_key = "sk_test_..."

def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Agent subscription'},
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )
    return session.url
```

## Advanced Usage
Handle Stripe webhook event signature verification (`stripe.Webhook.construct_event`) and customer portals.

## Key References
- [Stripe API Docs](https://stripe.com/docs/api)

## Dependencies
- stripe>=8.0.0
