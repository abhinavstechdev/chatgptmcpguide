# Product checkout conversion spec

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Product checkout conversion plugins in ChatGPT are currently in beta and being
  tested with approved partners. To apply for access, fill out this form 
  [here](https://chatgpt.com/merchants)

## Purpose

Our goal is to let ChatGPT directly invoke partner plugins for high-intent use
cases such as product checkout.

Once partners provide us with a product feed for search, we can connect their
MCP servers for bottom-of-funnel conversion actions. To do this, partner
plugins must follow a standardized contract for widget name, tool name, and
tool input.

If you want to build a plugin that follows this spec, apply for access through the
[ChatGPT merchants form](https://chatgpt.com/merchants/).

## User experience

When users search for products, the product entity sidebar can show **Open**
buttons for sellers. If a seller has a plugin, ChatGPT can open that plugin
inline for checkout instead of punching out to an external website.

## Required contract (today)

- Widget name: `ui://widget/checkout-session.html`
- Tool name: `checkout_session`

`checkout_session` must set:

```ts
_meta.ui.resourceUri = "ui://widget/checkout-session.html";
```

Any tool called directly from a widget must set:

```ts
_meta["openai/widgetAccessible"] = true;
```

## `checkout_session` input

Each checkout item requires only `id` and `quantity`. `offerId` and metadata for
the selected merchant offer are optional:

```json
{
  "checkout_session": {
    "items": [
      {
        "id": "string",
        "quantity": 1,
        "offerId": "string",
        "name": "Wireless headphones",
        "description": "Wireless headphones with noise cancellation.",
        "images": [
          "https://merchant.example.com/images/headphones.jpg",
          "https://merchant.example.com/images/headphones-side.jpg"
        ],
        "url": "https://merchant.example.com/products/headphones",
        "merchant_name": "Example Merchant",
        "price": "$24.99"
      }
    ]
  }
}
```

The following item fields are optional:

| Field           | Description                                         |
| --------------- | --------------------------------------------------- |
| `offerId`       | The identifier of the selected merchant offer.      |
| `name`          | The selected offer's product name.                  |
| `description`   | A description from the merchant's own feed.         |
| `images`        | Ordered merchant-feed image URLs; first is primary. |
| `url`           | The selected merchant offer's URL.                  |
| `merchant_name` | The name of the selected merchant.                  |
| `price`         | The displayed offer price as a string.              |

`images` contains zero or more URLs from the selected merchant's feed. When
present, the first URL is the primary displayed image. ChatGPT omits unavailable
optional fields. It doesn't generate a description or use another merchant's
description or images. Declare these item fields as optional in your tool's input
schema, and use the checkout item and offer IDs to retrieve authoritative
product, inventory, and pricing data from your own catalog.

The nested checkout session aligns with the Commerce checkout session shape documented
[here](https://developers.openai.com/commerce/specs/checkout/#post-checkout_sessions).