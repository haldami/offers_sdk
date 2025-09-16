# Offers SDK

Async first Python SDK for interacting with the Offers API as described in [Swagger](https://python.exercise.applifting.cz/docs) or [Redoc](https://python.exercise.applifting.cz/redoc) documentation. Handles authentication, token management, product registration, and fetching offers. Supports multiple HTTP clients (`requests`, `httpx`, `aiohttp`).

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

<!-- Install via `pip` from PyPI (once published):

```bash
pip install offers-sdk
``` -->

Install locally from your repository:

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

# Simple client initiation
# Only refresh token is required. For full options see `Client.__init__` documentation.
client = Client(refresh_token="your_refresh_token")

# Save the client state including access token
client.save_to_file("dumped_clients/your_client.json")

# Load it later
client = Client.load_from_file("dumped_clients/your_client.json")
```

---

## Command Line Interface (CLI)

The Offers SDK provides a **fully-featured CLI** to interact with the API directly from the terminal.
It supports both **single** and **batch operations** for registering products/offers and fetching offers.

---

Example JSON **input files for batch operations** are available in the [`example_input_files`](example_input_files) folder:

* **products.json** – list of products to register
* **ids.json** – list of product/offer UUIDs to fetch offers

Each file should be a valid JSON array. For example:

**products.json**

```json
[
  {
    "id": "11111111-1111-1111-1111-111111111111",
    "name": "Product A",
    "description": "Description for Product A"
  },
  {
    "id": "22222222-2222-2222-2222-222222222222",
    "name": "Product B",
    "description": "Description for Product B"
  }
]
```

**ids.json**

```json
[
  "11111111-1111-1111-1111-111111111111",
  "22222222-2222-2222-2222-222222222222"
]
```

### Usage Examples

**1. Register a single product**

```bash
python -m offers_sdk.cli \
    --client-location dumped_clients/requests.json \
    register \
    --id ad4c8529-0804-4053-a8d7-5e8b972422c7 \
    --name "Product A" \
    --description "Example product"
```

**2. Register multiple products from a JSON file**

```bash
python -m offers_sdk.cli \
    --client-location dumped_clients/requests.json \
    register_batch \
    --file example_input_files/products.json
```

**3. Fetch offers for a single product**

```bash
python -m offers_sdk.cli \
    --client-location dumped_clients/requests.json \
    get_offers \
    --id ad4c8529-0804-4053-a8d7-5e8b972422c7
```

**4. Fetch offers for multiple products from a JSON file**

```bash
python -m offers_sdk.cli \
    --client-location dumped_clients/requests.json
    get_offers_batch \
    --file example_input_files/ids.json
```

### Notes

* `--client-location` is **required** and should point to a valid dumped client configuration (`.json`).
  * the file is used for storage of auth token across the sessions.
* Batch commands (`register_batch` and `get_offers_batch`) expect **valid JSON arrays** as input.
* The CLI automatically handles **async execution** for batch operations, so all requests run concurrently.

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
# pytest of specified version was used for testing
# black was used for formatting
pip install pytest==8.4.1 black==25.1.0
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

### Formatting using black

```bash
black offers_sdk/ # run in repo root folder, formats every .py file 
```
---

### Notes

* While sync/async calls were included for all HTTP client implementations, the best experience for async calls is achieved using httpx/aiohttp libraries.
* Logging is optional and can be enabled with `logging=True` when initializing the client.
* API responses are wrapped in `APIResponse` objects.
* Refresh token of the author was left in the `dumped_clients/*.json` files for testing.
* If you want to initialize client 5 minutes from the last client authentication, you need to load the auth_token explicitly.
  * The access token is saved automatically to the dumped json file or can be found from the Auth call log file.

---

## License

MIT License © 2025 Milos Halda