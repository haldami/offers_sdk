"""
Tests for product registration and offer retrieval in the Offers SDK.

These tests use the live API and require a valid access token.
- `register_product` tests new product registration and handling of conflicts.
- `get_offers` tests retrieving offers for registered and unregistered products.
"""

import pytest
import uuid
import asyncio
from offers_sdk.client import Client
from offers_sdk.models import Product, Offer


def test_register_product(client_type: str) -> None:
    """
    Register a new product with the API.

    Args:
        client_type: Type of HTTP client ('requests', 'httpx', or 'aiohttp').

    Notes:
        - The registration should either succeed (201) or return conflict (409)
          if the product was already registered.
    """
    client = Client.load_from_file(f"dumped_clients/{client_type}_w_access_token.json")

    product = Product(
        id=uuid.uuid4(),
        name="Test Product",
        description="Registered from pytest"
    )

    asyncio.run(client.register_product(product))


def test_register_product_conflict(client_type: str) -> None:
    """
    Register the same product twice. The first call should succeed, the second
    call should report a conflict (409) but not raise an exception.

    Args:
        client_type: Type of HTTP client.
    """
    client = Client.load_from_file(f"dumped_clients/{client_type}_w_access_token.json")

    product_id = uuid.uuid4()
    product = Product(id=product_id, name="Double Product", description="Conflict test")

    # First registration
    asyncio.run(client.register_product(product))

    # Second registration should trigger conflict handling
    asyncio.run(client.register_product(product))


def test_get_offers_existing_product(client_type: str) -> None:
    """
    Retrieve offers for an existing product. The product is first registered.

    Args:
        client_type: Type of HTTP client.

    Notes:
        - The call should succeed and return offers or an empty list.
    """
    client = Client.load_from_file(f"dumped_clients/{client_type}_w_access_token.json")

    product = Product(
        id=uuid.uuid4(),
        name="Product With Offers",
        description="Testing get_offers"
    )

    # Register product first
    asyncio.run(client.register_product(product))

    # Retrieve offers for the registered product
    list_offers = asyncio.run(client.get_offers(product.id))

    for offer in list_offers: # If there are offers, they are of offer type
        assert type(offer) == Offer
        # Print offers to check them exactly
        #(can be viewed when running pytest with -s option)
        print(offer)


def test_get_offers_nonexistent_product(capfd, client_type: str) -> None:
    """
    Attempt to retrieve offers for a non-registered product. Should trigger
    a 404 response from the API.

    Args:
        client_type: Type of HTTP client.
    """
    client = Client.load_from_file(f"dumped_clients/{client_type}_w_access_token.json")

    random_id = uuid.uuid4()

    # Should print 404 message, but not raise an exception
    asyncio.run(client.get_offers(random_id))

    text_output = capfd.readouterr().out
    assert f"Product ID {random_id} not registered. Response: {{'detail': 'Product does not exist'}}\n"

