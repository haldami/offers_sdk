"""
Offers SDK Client module.

Provides a Client class to interact with the Offers API, including:
- Authentication and access token management
- Product registration
- Offer retrieval
- HTTP client abstraction (requests, httpx, aiohttp)

Raises custom exceptions for API errors and authentication issues.
"""

import os
import json
from json import JSONDecodeError
from pathlib import Path
from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from .exceptions import (
    InvalidAPIRequestException,
    InvalidClientTypeException,
    APIException,
    AuthException,
)
from .models import Offer, Product
from .services import APIResponse
from .services import IHttpClient, AioHttpClient, HttpxClient, RequestsClient


class Client:
    """
    SDK for interacting with the Offers API.

    Handles:
        - Authentication and token refreshing
        - HTTP request execution via pluggable clients
        - Product registration
        - Offer retrieval

    Attributes:
        AUTH: Endpoint for authentication
        PRODUCT_REGISTER: Endpoint to register a product
        OFFERS: Endpoint to retrieve offers for a product
        ACCESS_TOKEN_TIMEOUT: Token validity period in minutes
        HTTP_CLIENT_CLASSES: Supported HTTP client implementations
    """

    AUTH = "/api/v1/auth"
    PRODUCT_REGISTER = "/api/v1/products/register"
    OFFERS = "/api/v1/products/{product_id}/offers"
    ACCESS_TOKEN_TIMEOUT: float = 5.0  # minutes

    HTTP_CLIENT_CLASSES = {
        "requests": RequestsClient,
        "aiohttp": AioHttpClient,
        "httpx": HttpxClient,
    }

    def __init__(
        self,
        refresh_token: str,
        base_url: str = "https://python.exercise.applifting.cz",
        http_client_type: str = "requests",
        logging: bool = False,
        log_dir: str = "logs",
    ) -> None:
        self.base_url = base_url
        self.refresh_token = refresh_token
        self.access_token: str = ""
        self.token_expiry: datetime = datetime.min
        self.logging = logging
        self.log_dir = log_dir
        self.http_client_type: str = http_client_type
        self.http_client: IHttpClient

        self._init_http_client(http_client_type)

    def _init_http_client(self, http_client_type: str) -> None:
        """Initialize the HTTP client based on the provided type."""
        http_client_class = self.HTTP_CLIENT_CLASSES.get(http_client_type)
        if not http_client_class:
            raise InvalidClientTypeException(
                f"Unsupported HTTP client type: {http_client_type}\n"
                f"Supported types: {list(self.HTTP_CLIENT_CLASSES.keys())}"
            )
        self.http_client = http_client_class()

    def _log_request(
        self,
        req_type: str,
        url: str,
        headers: dict,
        data: dict,
        api_response: APIResponse,
    ) -> None:
        """Log API requests and responses to files in the specified log directory."""
        os.makedirs(self.log_dir, exist_ok=True)
        datetime_string = (
            datetime.now()
            .isoformat(timespec="milliseconds")
            .replace("T", "-")
            .replace(":", "")
            .replace(".", "-")
        )
        log_path = os.path.join(self.log_dir, f"{datetime_string}-{req_type}.log")
        with open(log_path, "w") as log_file:
            log_file.write(f"URL: {url}\n")
            log_file.write("Headers:\n")
            log_file.write(f"{headers}\n")
            log_file.write("Data:\n")
            log_file.write(f"{data}\n")
            log_file.write("API Response:\n")
            log_file.write(f"{api_response}\n")

    # -------------------------------------------------------------------------
    # Authentication
    # -------------------------------------------------------------------------

    def retrieve_access_token(self) -> None:
        """
        Retrieve a new access token using the refresh token.

        Raises:
            AuthException, InvalidAPIRequestException, APIException
        """
        url = f"{self.base_url}{self.AUTH}"
        headers = {"accept": "application/json", "Bearer": self.refresh_token}
        data = {}

        api_response = self.http_client.sync_post(url=url, data=data, headers=headers)

        if self.logging:
            self._log_request("auth", url, headers, data, api_response)

        match api_response.status_code:
            case 201:
                access_token = api_response.data.get("access_token")
                if not access_token:
                    raise APIException(
                        "Auth response missing 'access_token'."
                        f"Response: {api_response.data}"
                    )
                self.access_token = access_token
                self.token_expiry = datetime.now() + timedelta(
                    minutes=self.ACCESS_TOKEN_TIMEOUT
                )
            case 400:
                raise InvalidAPIRequestException(
                    f"HTTP 400 Bad request: {api_response.data}"
                )
            case 401:
                self._http_code_401(api_response)
            case 422:
                self._http_code_422(api_response)
            case _:
                self._http_code_unknown(api_response)

    def _ensure_token_valid(self) -> None:
        """Refresh access token if missing or expired."""
        if not self.access_token or datetime.now() >= self.token_expiry:
            self.retrieve_access_token()

    # -------------------------------------------------------------------------
    # Product Registration
    # -------------------------------------------------------------------------

    async def register_product(self, product: Product) -> None:
        """
        Register a new product with the API.

        Args:
            product: Product instance to register

        Raises:
            APIException, AuthException
        """
        self._ensure_token_valid()

        url = f"{self.base_url}{self.PRODUCT_REGISTER}"
        headers = {"accept": "application/json", "Bearer": self.access_token}
        data = {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
        }

        api_response = await self.http_client.async_post(
            url=url, data=data, headers=headers
        )

        if self.logging:
            self._log_request("register", url, headers, data, api_response)

        match api_response.status_code:
            case 201:
                product_id = api_response.data.get("id")
                if product_id != str(product.id):
                    raise APIException(
                        f"Product registration mismatch. Sent: {product.id}, Received: {product_id}"
                    )
                print(f"Product {product} registered successfully.")
            case 401:
                self._http_code_401(api_response)
            case 409:
                print(f"Product {product} already registered.")
            case 422:
                self._http_code_422(api_response)
            case _:
                self._http_code_unknown(api_response)

    # -------------------------------------------------------------------------
    # Offer Retrieval
    # -------------------------------------------------------------------------

    def _parse_offers(self, data: List) -> List[Offer]:
        offers = []
        for item in data:
            offers.append(
                Offer(
                    id=UUID(item["id"]),
                    price=int(item["price"]),
                    items_in_stock=int(item["items_in_stock"]),
                )
            )
        return offers

    async def get_offers(self, product_id: UUID) -> List[Offer]:
        """
        Retrieve offers for a specific product.

        Args:
            product_id: UUID of the product

        Returns:
            Dictionary of offers or None if not found
        """
        self._ensure_token_valid()

        url = f"{self.base_url}{self.OFFERS.format(product_id=product_id)}"
        headers = {"accept": "application/json", "Bearer": self.access_token}

        api_response = await self.http_client.async_get(url=url, headers=headers)

        if self.logging:
            self._log_request("get_offers", url, headers, {}, api_response)

        match api_response.status_code:
            case 200:
                try:
                    return self._parse_offers(list(api_response.data))
                except (KeyError, JSONDecodeError) as e:
                    raise APIException(
                        "Non standard json response from API. Did the docs change?\n"
                        f"{api_response}\n"
                        f"{e}"
                    )
            case 401:
                self._http_code_401(api_response)
            case 404:
                print(
                    f"Product ID {product_id} not registered. Response: {api_response.data}"
                )
                return []
            case 422:
                self._http_code_422(api_response)
            case _:
                self._http_code_unknown(api_response)

    # -------------------------------------------------------------------------
    # Internal HTTP error handlers
    # -------------------------------------------------------------------------

    def _http_code_401(self, api_response: APIResponse):
        raise AuthException(f"HTTP 401: Bad authentication.\n{api_response.data}")

    def _http_code_422(self, api_response: APIResponse):
        # Should not be raised! - The client does not allow invalid requests!
        raise Exception(f"HTTP 422: Validation Error.\n{api_response.data}")

    def _http_code_unknown(self, api_response: APIResponse):
        raise APIException(
            f"Unhandled status code {api_response.status_code}.\n{api_response.data}"
        )

    # -------------------------------------------------------------------------
    # Serialization / JSON handling
    # -------------------------------------------------------------------------

    def to_json(self) -> str:
        """Serialize Client state to JSON string."""
        return json.dumps(
            {
                "base_url": self.base_url,
                "refresh_token": self.refresh_token,
                "access_token": self.access_token,
                "token_expiry": self.token_expiry.isoformat(),
                "http_client_type": self.http_client_type,
                "logging": self.logging,
                "log_dir": self.log_dir,
            },
            indent=4,
        )

    @classmethod
    def from_json(cls, json_str: str) -> "Client":
        """Deserialize Client state from a JSON string."""
        data = json.loads(json_str)
        obj = cls(
            refresh_token=data["refresh_token"],
            base_url=data.get("base_url", "https://python.exercise.applifting.cz"),
            http_client_type=data.get("http_client_type", "requests"),
            logging=data.get("logging", False),
            log_dir=data.get("log_dir", "logs"),
        )
        obj.access_token = data.get("access_token", "")
        obj.token_expiry = datetime.fromisoformat(
            data.get("token_expiry", datetime.min.isoformat())
        )
        return obj

    def save_to_file(self, filepath: str | Path) -> None:
        """Save client state to a JSON file."""
        path = Path(filepath)
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load_from_file(cls, filepath: str | Path) -> "Client":
        """Load client state from a JSON file."""
        path = Path(filepath)
        return cls.from_json(path.read_text(encoding="utf-8"))

    def __repr__(self) -> str:
        return (
            f"Client(base_url={self.base_url!r}, refresh_token={self.refresh_token!r}, "
            f"access_token={self.access_token!r}, token_expiry={self.token_expiry!r}, "
            f"http_client_type={self.http_client_type!r}, logging={self.logging!r}, "
            f"log_dir={self.log_dir!r})"
        )
