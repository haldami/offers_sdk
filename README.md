# Offers SDK

Async first Python SDK for interacting with the Offers API. Handles authentication, token management, product registration, and fetching offers. Supports multiple HTTP clients (`requests`, `httpx`, `aiohttp`).

---

## Features

* Simple authentication with refresh tokens.
* Automatic token expiration handling.
* Register products to the Offers API.
* Retrieve offers for products.
* Support for multiple HTTP clients:
  * `RequestsClient`
  * `HttpxClient`
  * `AioHttpClient`
* Optional logging of all API requests.
* Dumping and loading implemented for the client.

---

## Installation

Install via `pip` from PyPI (once published):

```bash
pip install offers-sdk
```

Or install locally from your repository:

```bash
git clone https://github.com/haldami/offers_sdk.git
cd offers_sdk
pip install .
```

---

## Usage

### Basic Client Initialization

```python
from offers_sdk import Client

# Load client from saved JSON file
client = Client.load_from_file("dumped_clients/requests.json")

# Retrieve access token
client.retrieve_access_token()
print(client.access_token)
```

---

### Using Different HTTP Clients

```python
from offers_sdk import Client
from offers_sdk.services import RequestsClient, HttpxClient, AioHttpClient

# Requests client
client_requests = Client.load_from_file("dumped_clients/requests.json")
assert isinstance(client_requests.http_client, RequestsClient)

# Httpx client
client_httpx = Client.load_from_file("dumped_clients/httpx.json")
assert isinstance(client_httpx.http_client, HttpxClient)

# AioHttp client
client_aiohttp = Client.load_from_file("dumped_clients/aiohttp.json")
assert isinstance(client_aiohttp.http_client, AioHttpClient)
```

---

### Registering Products

```python
import uuid
import asyncio
from offers_sdk import Client
from offers_sdk.models import Product

client = Client.load_from_file("dumped_clients/requests.json")

product = Product(
    id=uuid.uuid4(),
    name="Test Product",
    description="Created via Offers SDK"
)

# Async registration
asyncio.run(client.register_product(product))
```

---

### Fetching Offers

```python
from uuid import UUID
import asyncio

client = Client.load_from_file("dumped_clients/aiohttp.json")

# Get offers for a specific product
asyncio.run(client.get_offers(product.id))
```

---

### Handling Exceptions

```python
from offers_sdk import Client
from offers_sdk.exceptions import AuthException, InvalidAPIRequestException

try:
    client.retrieve_access_token()
except AuthException:
    print("Invalid refresh token or authentication failed")
except InvalidAPIRequestException as e:
    print("Request rejected by API:", e)
```

---

## Saving and Loading Client State

```python
from offers_sdk import Client

# Only refresh token is required. For full options see `Client.__init__` documentation.
client = Client(refresh_token="your_refresh_token")

# Save the client state including access token
client.save_to_file("dumped_clients/requests_w_access_token.json")

# Load it later
client = Client.load_from_file("dumped_clients/requests_w_access_token.json")
```

---

## Project Structure

```
offers_sdk
├── client.py             # Main SDK client
├── exceptions.py         # Custom exception classes
├── __init__.py
├── models
│   ├── offer.py
│   ├── product.py
│   └── __init__.py
└── services
    ├── aio_http_client.py
    ├── api_response.py
    ├── http_client_interface.py
    ├── httpx_client.py
    ├── requests_client.py
    └── __init__.py
```

---

## Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest --client=requests
# --client can have also values httpx and aiohttp
# use -s option to see printed output
# run the tests with 5 minutes break between them
# - real API is used for testing, which does not allow repeated authentication
```

> Make sure to have valid credentials saved in `tests/dumped_clients/` before running tests.

---

## License

MIT License © 2025 Milos Halda

---

### Notes

* While sync/async calls were included for all HTTP client implementations, the best experience for async calls is achieved using httpx/aiohttp libraries.
* Logging is optional and can be enabled with `logging=True` when initializing the client.
* API responses are wrapped in `APIResponse` objects.
* Refresh token of the author was left in the `dumped_clients/*.json` files for testing.
* If you want to initialize client 5 minutes from the last client authentication, you need to load the auth_token explicitly.
  * The access token is saved automatically to the dumped json file or can be found from the Auth call log file.
