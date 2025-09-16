"""
CLI for Offers SDK

This script provides a command-line interface to interact with the Offers SDK,
allowing users to register products/offers and fetch offer information directly
from the command line. It supports both single and batch operations.

---

Structure:

1. Helpers
   - `_parse_products(file_path: str) -> List[Product]`
     Parses a JSON file into a list of Product objects.

   - `_parse_ids(file_path: str) -> List[UUID]`
     Parses a JSON file into a list of UUIDs.

2. Commands
   - `register(client: Client, id: str, name: str, description: str)`
     Register a single product/offer.

   - `register_batch(client: Client, file_path: str)`
     Register multiple products/offers from a JSON file concurrently.

   - `get_offers(client: Client, id: str)`
     Fetch offers for a single product/offer ID.

   - `get_offers_batch(client: Client, file_path: str)`
     Fetch offers for multiple product/offer IDs from a JSON file concurrently.

3. CLI Entrypoint (`main()`)
   Uses argparse to parse command-line arguments:
     --client-location : required path to dumped client configuration.
     Subcommands:
       - register
       - register_batch
       - get_offers
       - get_offers_batch

Example usage:

    # Register a single product
    python -m offers_sdk.cli --client-location client.json register \
        --id ad4c8529-0804-4053-a8d7-5e8b972422c7 \
        --name "Product A" --description "Example product"

    # Register multiple products from a JSON file
    python -m offers_sdk.cli --client-location client.json register_batch --file products.json

    # Get offers for a single product
    python -m offers_sdk.cli --client-location client.json get_offers --id ad4c8529-0804-4053-a8d7-5e8b972422c7

    # Get offers for multiple products from a JSON file
    python -m offers_sdk.cli --client-location client.json get_offers_batch --file ids.json
"""

import argparse
import asyncio
import json
from typing import List
from uuid import UUID

from .client import Client
from .models import Offer, Product


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _parse_products(file_path: str) -> List[Product]:
    """Parse a JSON file into a list of Product objects."""
    with open(file_path, "r", encoding="utf-8") as f:
        products_json = json.load(f)

    if not isinstance(products_json, list):
        raise ValueError("JSON file must contain a list of offers")

    return [
        Product(
            id=UUID(data["id"]),
            name=data["name"],
            description=data["description"],
        )
        for data in products_json
    ]


def _parse_ids(file_path: str) -> List[UUID]:
    """Parse a JSON file into a list of UUIDs."""
    with open(file_path, "r", encoding="utf-8") as f:
        ids_json = json.load(f)

    if not isinstance(ids_json, list):
        raise ValueError("JSON file must contain a list of ids")

    return [UUID(id) for id in ids_json]


# ----------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------
def register(client: Client, id: str, name: str, description: str):
    """Register a single product/offer."""
    product = Product(id=UUID(id), name=name, description=description)
    asyncio.run(client.register_product(product))


def register_batch(client: Client, file_path: str):
    """Register multiple products from JSON file."""
    products: List[Product] = _parse_products(file_path)

    async def _register_all():
        tasks = [client.register_product(p) for p in products]
        return await asyncio.gather(*tasks)

    return asyncio.run(_register_all())


def get_offers(client: Client, id: str):
    """Fetch offers for a given ID."""
    offers: List[Offer] = asyncio.run(client.get_offers(UUID(id)))

    for offer in offers:
        print(offer)


def get_offers_batch(client: Client, file_path: str):
    """Fetch offers for multiple IDs from JSON file."""
    product_ids: List[UUID] = _parse_ids(file_path)

    async def _fetch_all():
        tasks = [client.get_offers(pid) for pid in product_ids]
        return await asyncio.gather(*tasks)

    # return asyncio.run(_fetch_all())
    offers_for_products: List[List[Offer]] = asyncio.run(_fetch_all())
    for product_id, offers in zip(product_ids, offers_for_products):
        print(f"For product {product_id}, following offers were obtained:")
        for offer in offers:
            print(offer)


# ----------------------------------------------------------------------
# CLI Entrypoint
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        prog="offers-cli",
        description="Command line interface for Offers SDK",
    )

    parser.add_argument(
        "--client-location",
        required=True,
        help="Path to dumped client configuration or credentials",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # register
    register_parser = subparsers.add_parser(
        "register",
        help="Register a single product/offer",
    )
    register_parser.add_argument(
        "--id", required=True, help="UUID of the product/offer"
    )
    register_parser.add_argument(
        "--name", required=True, help="Name of the product/offer"
    )
    register_parser.add_argument(
        "--description",
        required=True,
        help="Description of the product/offer",
    )

    # register_batch
    register_batch_parser = subparsers.add_parser(
        "register_batch",
        help="Register multiple products/offers",
    )
    register_batch_parser.add_argument(
        "--file",
        required=True,
        help="Path to JSON file containing products",
    )

    # get_offers
    get_offers_parser = subparsers.add_parser(
        "get_offers",
        help="Get offers for a given ID",
    )
    get_offers_parser.add_argument(
        "--id", required=True, help="UUID of the offer/product"
    )

    # get_offers_batch
    get_offers_batch_parser = subparsers.add_parser(
        "get_offers_batch",
        help="Get offers for multiple IDs",
    )
    get_offers_batch_parser.add_argument(
        "--file",
        required=True,
        help="Path to JSON file containing IDs",
    )

    args = parser.parse_args()
    client = Client.load_from_file(args.client_location)

    if args.command == "register":
        register(client, args.id, args.name, args.description)

    elif args.command == "register_batch":
        register_batch(client, args.file)

    elif args.command == "get_offers":
        get_offers(client, args.id)

    elif args.command == "get_offers_batch":
        get_offers_batch(client, args.file)

    client.save_to_file(args.client_location)


if __name__ == "__main__":
    main()
