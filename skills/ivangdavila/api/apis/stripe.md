# Stripe

## Base URL
```
https://api.stripe.com/v1
```

## Authentication
```bash
curl https://api.stripe.com/v1/customers \
  -u sk_test_xxx:
# Note: colon after key, no password
```

Or with header:
```bash
-H "Authorization: Bearer sk_test_xxx"
```

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /customers | GET | List customers |
| /customers | POST | Create customer |
| /customers/:id | GET | Get customer |
| /payment_intents | POST | Create payment |
| /subscriptions | POST | Create subscription |
| /invoices | GET | List invoices |
| /refunds | POST | Create refund |

## Quick Examples

### Create Customer
```bash
curl https://api.stripe.com/v1/customers \
  -u sk_test_xxx: \
  -d email="customer@example.com" \
  -d name="John Doe"
```

### Create Payment Intent
```bash
curl https://api.stripe.com/v1/payment_intents \
  -u sk_test_xxx: \
  -d amount=2000 \
  -d currency=usd \
  -d "payment_method_types[]"=card
```

### Create Subscription
```bash
curl https://api.stripe.com/v1/subscriptions \
  -u sk_test_xxx: \
  -d customer=cus_xxx \
  -d "items[0][price]"=price_xxx
```

### List Payments
```bash
curl https://api.stripe.com/v1/payment_intents?limit=10 \
  -u sk_test_xxx:
```

## Webhooks

```bash
# Verify webhook signature
stripe_signature = request.headers['Stripe-Signature']
# Use stripe library to verify
```

Common events:
- `payment_intent.succeeded`
- `customer.subscription.created`
- `invoice.paid`
- `charge.refunded`

## Common Traps

- Amount in cents (2000 = $20.00)
- Test keys start with `sk_test_`, live with `sk_live_`
- Always use idempotency key for payments
- Webhook signatures required in production

## Rate Limits

- 100 read requests/sec (test mode)
- 100 write requests/sec (test mode)
- Higher limits in live mode

## Official Docs
https://stripe.com/docs/api
