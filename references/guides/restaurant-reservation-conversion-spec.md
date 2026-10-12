# Restaurant reservation conversion spec

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Restaurant reservation conversion plugins in ChatGPT are currently in beta and
  being tested with approved partners. To apply for access, fill out this form 
  [here](https://chatgpt.com/merchants)

## Purpose

Our goal is to let ChatGPT directly invoke partner plugins for high-intent use
cases such as restaurant reservations.

Once partners provide us with a feed for search, we can connect their MCP
servers for bottom-of-funnel conversion actions. To do this, partner plugins
must follow a standardized contract for widget name, tool name, and tool input.

If you want to build a plugin that follows this spec, apply for access through the
[ChatGPT merchants form](https://chatgpt.com/merchants/).

## User experience

When users search for restaurants around them, the restaurant entity card and
sidebar include a **Reserve** button that can open the restaurant's reservation
provider UI.

Reserve button in restaurant UI:

![Reserve button in restaurant UI](https://developers.openai.com/images/apps-sdk/conversion-specs/reserve-button.png)

Reservation modal opened from that button:

![Reservation modal opened from Reserve button](https://developers.openai.com/images/apps-sdk/conversion-specs/reservation-modal.png)

## Required contract (today)

For the current reservation integration, only the following are required:

- Widget name: `ui://widget/restaurant-reservation.html`
- Tool name: `restaurant_reservation`

`restaurant_reservation` must set:

```ts
_meta.ui.resourceUri = "ui://widget/restaurant-reservation.html";
```

Any tool called directly from a widget must set:

```ts
_meta["openai/widgetAccessible"] = true;
```

## `restaurant_reservation` input

Minimum payload (always sent):

```json
{
  "restaurant_id": "string"
}
```

We might also send the payload below. You can use it for optimistic rendering
in the modal (for example, to avoid skeleton/loading states while data
hydrates):

```json
{
  "restaurant_name": "string",
  "restaurant_image": "string",
  "restaurant_address": {
    "address": "string",
    "city": "string",
    "state": "string",
    "zipcode": "string",
    "country": "string"
  }
}
```

## Feed requirement (search integration)

To enable Reserve-button routing, we ingest a business feed from partners.

### Purpose and scope

This feed contract defines:

- Minimum business data required for matching and ranking.
- A paginated listing API.
- Change detection so we can avoid unnecessary full fetches.

### Business record (minimum required fields)

A `Business` object must include:

- `id` (`string`): stable and unique within the provider.
- `name` (`string`)
- `address` (`object` or formatted `string`)
- `location` (`object` with latitude/longitude)
- `phone_number` (`string`, E.164 preferred)
- `website_url` (`string`, URL)
- `platform_url` (`string`, URL to your canonical listing)

Recommended minimal shape:

```json
{
  "id": "biz_123",
  "name": "Acme Coffee",
  "address": {
    "line1": "123 Market St",
    "line2": "Suite 5",
    "locality": "San Francisco",
    "region": "CA",
    "postal_code": "94105",
    "country": "US",
    "formatted": "123 Market St, Suite 5, San Francisco, CA 94105, US"
  },
  "location": {
    "latitude": 37.793,
    "longitude": -122.396
  },
  "phone_number": "+14155551234",
  "website_url": "https://acmecoffee.example",
  "platform_url": "https://provider.example/biz/biz_123"
}
```

If structured address components are unavailable, `address` may be a single
formatted string, but it must be consistent and human-readable.

### Paginated listing endpoint

Endpoint example:

- `GET /v1/businesses`

Query parameters:

- Pagination: use one style
- `page` + `page_size`
- `offset` + `limit`
- or `next_page_token` (opaque token; preferred when supported)
- `changes_token` (`string`, optional): indicates whether data changed since
  the last sync checkpoint.

Response must include:

- `checksum` (`boolean`): whether anything changed since the provided
  `changes_token` (or `true` if none was provided).
- `businesses` (`Business[]`): current page payload.
- Pagination metadata for your selected style:
- `page`, `page_size`, `total_pages` (optional), or
- `offset`, `limit`, `total` (optional), or
- `next_page_token` (`string | null`)

### Example request and response

Request:

```http
GET /v1/businesses?page=1&page_size=2&changes_token=sync_2026_03_10
```

Response:

```json
{
  "checksum": true,
  "page": 1,
  "page_size": 2,
  "total_pages": 120,
  "businesses": [
    {
      "id": "biz_123",
      "name": "Acme Coffee",
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
      "website_url": "https://acmecoffee.example",
      "platform_url": "https://provider.example/biz/biz_123"
    },
    {
      "id": "biz_124",
      "name": "Golden Diner",
      "address": "200 Howard St, San Francisco, CA 94105, US",
      "location": {
        "latitude": 37.789,
        "longitude": -122.391
      },
      "phone_number": "+14155559876",
      "website_url": "https://goldendiner.example",
      "platform_url": "https://provider.example/biz/biz_124"
    }
  ]
}
```

### How we use this feed for search

We treat the business feed as a search index. At query time, we retrieve
candidates with fuzzy matching (name + location/address), then rank and remove
duplicates using name/address similarity, with location/phone/URL as additional
signals.

## Good-to-have expansion (not required today)

For full end-to-end in-chat completion, we recommend adding:

- `refresh_availability`
- `make_reservation`
- `reservation_confirmation`