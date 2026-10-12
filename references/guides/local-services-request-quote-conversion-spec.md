# Local services Get Quote conversion spec

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Local services Get Quote conversion plugins in ChatGPT are currently in beta
  and being tested with approved partners. To apply for access, complete the
  [ChatGPT merchants form](https://chatgpt.com/merchants/).

## Purpose

ChatGPT can directly invoke partner plugins for high-intent local services use
cases, such as requesting a quote.

To enable this flow, provide local business data that identifies your service,
and expose an MCP tool that opens your quote-request widget.

If you want to build a plugin that follows this spec, apply for access through
the [ChatGPT merchants form](https://chatgpt.com/merchants/).

## User experience

When a user searches for an eligible local business, the business card or
sidebar can display a **Get Quote** button. Selecting the button opens the
provider's quote-request widget in a modal in ChatGPT.

ChatGPT displays the button only when the business has an eligible service
provider and that provider has a configured partner plugin.

## Required contract

Register an MCP tool named `request_service` with
`ui://widget/request-service.html` as its widget resource. ChatGPT launches the
widget in `modal` display mode and sends the provider's business ID when a user
selects **Get Quote**:

```ts
const launcherTool = {
  name: "request_service",
  _meta: {
    ui: {
      resourceUri: "ui://widget/request-service.html",
    },
  },
};

const launcherInput = {
  business_id: "biz_123",
};
```

Set `_meta["openai/widgetAccessible"] = true` on any helper tool that the
widget calls directly. This metadata applies to widget-accessible helper tools,
not to the launcher solely because it opens the widget.

The launcher input `business_id` must be the `provider_business_id` from the
matching service provider record. It can differ from the ID of the containing
local business record.

## Business feed requirements

A business feed is a paginated collection of local business records that you
provide to ChatGPT. ChatGPT indexes these records for search and uses their
service provider data to determine whether a business supports **Get Quote**.

### Required business fields

Each business record must include:

- `id`: A stable business ID unique within your feed.
- `name`: The business name.
- `address`: A structured address or a human-readable formatted address.
- `location`: An object containing `latitude` and `longitude`.
- `phone_number`: A business phone number, preferably in E.164 format.
- `website_url`: The business website.
- `platform_url`: Your canonical listing URL for the business.

### Quote-request action

For every business that accepts quote requests, add a `service_providers` array
containing a record with these fields:

- `provider`: Your provider name. It must match the configured partner plugin.
- `provider_business_id`: Your nonempty identifier for the business. ChatGPT
  passes this value as `business_id` to `request_service`.
- `action_type`: Set this to `request_a_quote` for a quote request.
- `provider_action_url`: A valid absolute HTTP or HTTPS URL for your
  quote-request action.
- `display_name`: An optional provider-supplied display name.

### Paginated listing endpoint

Expose a listing endpoint such as `GET /v1/businesses` and support one
pagination style:

- `page` and `page_size`.
- `offset` and `limit`.
- An opaque `next_page_token`.

Accept an optional `changes_token` to identify the previous synchronization
checkpoint. Return `checksum` to show whether the feed has changed,
`businesses` for the current page, and the metadata for your pagination style.

For example, the following request fetches one business from a page-based feed:

```http
GET /v1/businesses?page=1&page_size=1&changes_token=sync_001
```

Return the complete business record and its quote-request action:

```json
{
  "checksum": true,
  "page": 1,
  "page_size": 1,
  "total_pages": 1,
  "businesses": [
    {
      "id": "local_biz_456",
      "name": "Acme Plumbing",
      "address": {
        "line1": "123 Market St",
        "locality": "San Francisco",
        "region": "CA",
        "postal_code": "94105",
        "country": "US",
        "formatted": "123 Market St, San Francisco, CA 94105, US"
      },
      "location": {
        "latitude": 37.793,
        "longitude": -122.396
      },
      "phone_number": "+14155551234",
      "website_url": "https://acmeplumbing.example",
      "platform_url": "https://provider.example/businesses/local_biz_456",
      "service_providers": [
        {
          "provider": "example_provider",
          "provider_business_id": "biz_123",
          "action_type": "request_a_quote",
          "provider_action_url": "https://provider.example/request-quote/biz_123",
          "display_name": "Get Quote"
        }
      ]
    }
  ]
}
```

### Quote-launch eligibility

ChatGPT builds an in-chat launcher only when the containing business has a
nonempty ID, the service provider has a nonempty `provider_business_id` and a
valid `provider_action_url`, and the provider has a configured partner plugin.
The quote button uses the ChatGPT UI label **Get Quote**; the provider's
`display_name` does not override that label for `request_a_quote` actions.

## Future expansion

This contract covers quote requests. Other service actions, such as appointment
booking, are not required for the quote-request flow.