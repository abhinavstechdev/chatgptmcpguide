# Checkout API reference

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Overview

Plugin developers are responsible for choosing how to monetize their experience. Today, the **recommended** and **generally available** approach is to use **external checkout**, where users complete purchases on the developer’s own domain. While current approval is limited to plugins for physical goods purchases, we are actively working to support a wider range of commerce use cases.

We’re also enabling **embedded checkout with the ChatGPT payment sheet** for
select marketplace partners (beta), with plans to extend access to more
marketplaces and physical-goods retailers over time. Until then, we recommend
routing purchase flows to your standard external checkout.

## Recommended Monetization Approach

### ✅ External Checkout (recommended)

**External checkout** means directing users from ChatGPT to a **merchant-hosted checkout flow** on your own website or application, where you handle pricing, payments, shipping, and fulfillment for eligible physical goods.

This is the recommended approach for most plugin developers.

#### How it works

1. A user interacts with your plugin UI in ChatGPT.
2. Your plugin UI presents eligible physical goods (for example, with a “Buy now” action).
3. When the user decides to purchase, your plugin UI links or redirects them out of ChatGPT and to your external checkout flow.
4. Payment, billing, taxes, refunds, and compliance are handled entirely on your domain.
5. After purchase, the user can return to ChatGPT with order confirmation or tracking details.

### Checkout with saved payment methods

Plugin developers can build a checkout flow in optional UI that allows customers to use payment methods already saved with the merchant. This flow can only display saved payment methods and cannot collect new payment method credentials from customers.

In this approach, the customer does not need to be redirected to another surface outside ChatGPT to complete the purchase.

#### How it works

1. A user interacts with your plugin UI in ChatGPT.
2. Your plugin UI presents eligible physical goods with the relevant totals.
3. Your plugin UI displays eligible payment methods that the customer has already saved with you.
4. The customer selects a saved payment method and confirms the purchase in ChatGPT.
5. Your server processes the purchase with the saved payment method and returns confirmation to the plugin.

### Checkout with the ChatGPT payment sheet (private beta)



Checkout with the ChatGPT payment sheet is limited to select marketplaces
  today and is not available to all users.



To collect new payment methods within the checkout flow, plugin developers must
use the ChatGPT payment sheet. Call `requestCheckout` with checkout session data
(line items, totals, saved payment methods) to open the sheet. When the user
selects buy, ChatGPT sends a token representing the selected payment method to
your MCP server through the `complete_checkout` tool call. Use your PSP
integration to collect payment with this token, then return finalized order
details from `complete_checkout`.

### Flow at a glance

1. **Server prepares session**: An MCP tool returns checkout session data (session id, line items, totals, payment provider) in `structuredContent`.
2. **Widget previews cart**: The widget renders line items and totals so the user can confirm.
3. **Widget calls `requestCheckout`**: The widget invokes `requestCheckout(session_data)`. ChatGPT opens the payment sheet, displays the amount to charge, and displays various payment methods.
4. **Server finalizes**: Once the user clicks the pay button, the widget calls back to your MCP via the `complete_checkout` tool call. The MCP tool returns the completed order, which will be returned back to widget as a response to `requestCheckout`.

## Checkout session

You are responsible for constructing the checkout session payload that the host will render. The exact values for certain fields such as `id` and `payment_provider` depend on your payment service provider and commerce system. In practice, your MCP tool should return:

- Line items and quantities the user is purchasing.
- Totals (subtotal, tax, discounts, fees, total) that match your server calculations.
- Provider metadata required by your PSP integration.
- Legal and policy links (terms, refund policy, etc.).

## Widget: Call `requestCheckout`

The host provides `window.openai.requestCheckout`. Use it to open the ChatGPT payment sheet when the user initiates a purchase:

Example:
```tsx
async function handleCheckout(sessionJson: string) {
  const session = JSON.parse(sessionJson);

  if (!window.openai?.requestCheckout) {
    throw new Error("requestCheckout is not available in this host");
  }

  // Host opens the ChatGPT payment sheet.
  const order = await window.openai.requestCheckout({
    ...session,
    id: String(checkout_session_id), // Use a unique ID for every checkout session.
  });

  return order; // Host returns the order payload.
}
```

In your component, you might initiate this in a button click:

```tsx


{
    setIsLoading(true);
    try {
      const orderResponse = await handleCheckout(checkoutSessionJson);
      setOrder(orderResponse);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }}
>
  {isLoading ? "Loading..." : "Checkout"}


```

Here is a complete checkout session example that your widget can pass to the
host. Your plugin supplies the checkout session fields below. ChatGPT adds
host-owned fields such as `merchant`, `logo_url`, `conversation_id`,
`connector_id`, and `ecosystem_app_uri`. Populate the `merchant_id` field with
the value specified by your PSP:

```tsx
const checkoutRequest = {
  id: "checkout_session_123",
  payment_provider: {
    provider: "stripe",
    merchant_id: "merchant_123",
    supported_payment_methods: [
      {
        type: "card",
        allowed_card_brands: ["visa", "mastercard"],
      },
      { type: "apple_pay" },
      { type: "google_pay" },
    ],
    managed_payment_methods: [
      {
        type: "card",
        id: "pm_123",
        display_name: "Visa ending in 4242",
        display_last4: "4242",
        display_brand: "visa",
      },
    ],
  },
  payment_mode: "live",
  status: "ready_for_payment",
  currency: "USD",
  metadata: {
    cart_id: "cart_123",
    merchant_order_reference: "order_ref_123",
  },
  line_items: [
    {
      id: "line_item_123",
      item: {
        id: "item_123",
        quantity: 1,
      },
      name: "Canvas backpack",
      description: "A weather-resistant everyday backpack.",
      images: ["https://merchant.example.com/images/canvas-backpack.png"],
      base_amount: 3000,
      discount: 0,
      subtotal: 3000,
      tax: 300,
      total: 3300,
    },
  ],
  totals: [
    {
      type: "items_base_amount",
      display_text: "Items subtotal",
      amount: 3000,
    },
    {
      type: "subtotal",
      display_text: "Subtotal",
      amount: 3000,
    },
    {
      type: "fulfillment",
      display_text: "Shipping",
      amount: 550,
    },
    {
      type: "tax",
      display_text: "Tax",
      amount: 300,
    },
    {
      type: "total",
      display_text: "Total",
      amount: 3850,
    },
  ],
  fulfillment_options: [
    {
      id: "standard_shipping",
      type: "shipping",
      title: "Standard shipping",
      subtitle: "Arrives in 3-5 business days",
      carrier: "USPS",
      earliest_delivery_time: "2027-01-15T15:00:00Z",
      latest_delivery_time: "2027-01-19T18:00:00Z",
      subtotal: 500,
      tax: 50,
      total: 550,
    },
  ],
  fulfillment_option_id: "standard_shipping",
  fulfillment_address: {
    name: "Jane Customer",
    line_one: "123 Main St",
    line_two: "Apt 4B",
    city: "San Francisco",
    state: "CA",
    country: "US",
    postal_code: "94107",
    phone_number: "+14155550123",
  },
  messages: [
    {
      type: "info",
      param: "fulfillment_address",
      content_type: "plain",
      content: "Free returns within 30 days.",
    },
  ],
  links: [
    { type: "terms_of_use", url: "https://merchant.example.com/terms" },
    { type: "privacy_policy", url: "https://merchant.example.com/privacy" },
    { type: "support_url", url: "https://merchant.example.com/support" },
  ],
};

const response = await window.openai.requestCheckout(checkoutRequest);
```

Key points:

- `window.openai.requestCheckout(session)` opens the host checkout UI.
- The promise resolves with the order result or rejects on error/cancel.
- Render the session JSON so users can review what they’re paying for.
- Use integer minor currency units for all amount fields.
- Use `payment_provider.managed_payment_methods` for payment methods the customer has already saved with your merchant.
- Keep `metadata` values as strings.
- Use the PSP slug required by your integration for `provider`, and consult your PSP to get its `merchant_id` value.

## MCP server: Expose the `complete_checkout` tool

You can mirror this pattern and swap in your logic:

For direct `CallToolResult` returns, the Python MCP SDK uses the `Annotated`
return type below to declare the tool `outputSchema` for `structuredContent`.

```py
from typing import Annotated, Any

from pydantic import BaseModel


class CompleteCheckoutOutput(BaseModel):
    id: str
    status: str
    currency: str
    line_items: list[dict[str, Any]]
    fulfillment_address: dict[str, Any]
    fulfillment_options: list[dict[str, Any]]
    fulfillment_option_id: str
    totals: list[dict[str, Any]]
    order: dict[str, Any]


@tool(description="")
async def complete_checkout(
    self,
    checkout_session_id: str,
    buyer: Buyer,
    payment_data: PaymentData,
) -> Annotated[types.CallToolResult, CompleteCheckoutOutput]:
    return types.CallToolResult(
        content=[],
        structuredContent={
            "id": checkout_session_id,
            "status": "completed",
            "currency": "USD",
            "line_items": [
                {
                    "id": "line_item_1",
                    "item": {
                        "id": "item_1",
                        "quantity": 1,
                    },
                    "base_amount": 3000,
                    "discount": 0,
                    "subtotal": 3000,
                    "tax": 300,
                    "total": 3300,
                },
            ],
            "fulfillment_address": {
                "name": "Jane Customer",
                "line_one": "123 Main St",
                "line_two": "Apt 4B",
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
                "postal_code": "94107",
                "phone_number": "+1 (555) 555-5555",
            },
            "fulfillment_options": [
                {
                    "id": "fulfillment_option_1",
                    "type": "shipping",
                    "title": "Standard shipping",
                    "subtitle": "3-5 business days",
                    "carrier": "USPS",
                    "earliest_delivery_time": "2026-02-24T15:00:00Z",
                    "latest_delivery_time": "2026-02-28T18:00:00Z",
                    "subtotal": 0,
                    "tax": 0,
                    "total": 0,
                },
            ],
            "fulfillment_option_id": "fulfillment_option_1",
            "totals": [
                {
                    "type": "items_base_amount",
                    "display_text": "Items subtotal",
                    "amount": 3000,
                },
                {
                    "type": "subtotal",
                    "display_text": "Subtotal",
                    "amount": 3000,
                },
                {
                    "type": "tax",
                    "display_text": "Tax",
                    "amount": 300,
                },
                {
                    "type": "total",
                    "display_text": "Total",
                    "amount": 3300,
                },
            ],
            "order": {
                "id": "order_id_123",
                "checkout_session_id": checkout_session_id,
                "permalink_url": "",
            },
        },
        _meta={META_SESSION_ID: "checkout-flow"},
        isError=False,
    )
```

Adapt this to:

- Integrate with your payment service provider to charge the payment method
  within `payment_data`.
- Persist the order in your system.
- Return authoritative order/receipt data.
- Include `_meta.ui.resourceUri` if you want to render a confirmation widget (ChatGPT honors `_meta["openai/outputTemplate"]` as an optional compatibility alias).

The following payment service providers support processing for the ChatGPT
payment sheet:

- [Adyen](https://docs.adyen.com/online-payments/agentic-commerce)
- [Checkout.com](https://api-reference.checkout.com/tag/Agentic-Commerce-Protocol/)
- Fiserv
- [PayPal](https://docs.paypal.ai/growth/agentic-commerce/agent-ready)
- [Stripe](https://docs.stripe.com/agentic-commerce/apps)
- [Worldpay](https://docs.worldpay.com/access/products/ai/acp)

## Optional: Receive Raw Payment Methods

If you are a merchant with a PCI DSS Level 1 certificate, you can receive raw payment methods directly by implementing the Agentic Commerce Protocol Delegate Payment endpoint. The delegated payment request will include the full payment method details your payment flow requires, including the raw card number, expiration date, CVC, billing address, allowance constraints, risk signals, and metadata.

For example, a raw card payment method request is as follows:

```json
{
  "payment_method": {
    "type": "card",
    "card_number_type": "fpan",
    "number": "4242424242424242",
    "exp_month": "11",
    "exp_year": "2026",
    "name": "Jane Doe",
    "cvc": "223",
    "checks_performed": ["avs", "cvv"],
    "iin": "424242",
    "display_card_funding_type": "credit",
    "display_brand": "visa",
    "display_last4": "4242",
    "metadata": {}
  },
  "allowance": {
    "reason": "one_time",
    "max_amount": 5000,
    "currency": "usd",
    "checkout_session_id": "cs_01HV3P3ABC123",
    "merchant_id": "acme_corp",
    "expires_at": "2026-02-13T12:00:00Z"
  },
  "billing_address": {
    "name": "Jane Doe",
    "line_one": "185 Berry Street",
    "line_two": "Suite 550",
    "city": "San Francisco",
    "state": "CA",
    "country": "US",
    "postal_code": "94107"
  },
  "risk_signals": [
    {
      "type": "card_testing",
      "score": 5,
      "action": "authorized"
    }
  ],
  "metadata": {
    "session_id": "sess_abc123",
    "user_agent": "ChatGPT/2.0"
  }
}
```

The corresponding response should return an id representing the payment method. This id will be passed to `complete_checkout` as part of `payment_data`.

```json
{
  "id": "vt_01J8Z3WXYZ9ABC123",
  "created": "2026-02-12T14:30:00Z",
  "metadata": {
    "source": "agent_checkout",
    "merchant_id": "acme_corp",
    "idempotency_key": "idem_xyz789"
  }
}
```

## Error Handling

The `complete_checkout` tool call can send back messages of type `error`. Error messages with `code` set to `payment_declined` or `requires_3ds` will be displayed on the ChatGPT payment sheet. All other error messages will be sent back to the widget as a response to `requestCheckout`. The widget can display the error as desired.

## Test payment mode

You can set the value of the `payment_mode` field to `test` in the call to `requestCheckout`. This will present a ChatGPT payment sheet that accepts test cards (such as the 4242 test card). The resulting `token` within `payment_data` that is passed to the `complete_checkout` tool can be processed in the staging environment of your PSP. This allows you to test end-to-end flows without moving real funds.

Note that in test payment mode, you might have to set a different value for
`merchant_id`. Refer to your payment provider's monetization guide for more
details.

## Implementation checklist

1. **Define your checkout session model**: Include IDs, the payment provider
   object, line items, totals, and legal links.
2. **Return the session from your MCP tool** in `structuredContent` alongside your widget template.
3. **Render the session in the widget** so users can review items, totals, and terms.
4. **Call `requestCheckout(session_data)`** on user action; handle the resolved order or error.
5. **Charge the user** by implementing the `complete_checkout` MCP tool which
   returns a response that follows the checkout spec.
6. **Test end-to-end** with realistic amounts, taxes, and discounts to ensure the host renders the totals you expect.