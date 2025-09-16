"""
Test Suite for Offer and Product Dataclasses and APIResponse dataclass from services module.

This module contains unit tests for the Offer, Product and APIResponse dataclasses
defined in the Offers SDK. The tests verify the correct initialization,
string representation, and functionality of methods within these classes.
"""

import pytest
from uuid import uuid4
from offers_sdk.models import Offer, Product
from offers_sdk.services import APIResponse


# Test for the Offer dataclass
def test_offer_initialization():
    """
    Test the initialization of the Offer dataclass.

    Verifies that an Offer instance is created with the correct attributes.
    """
    offer_id = uuid4()
    price = 1999  # Price in cents
    items_in_stock = 50

    offer = Offer(id=offer_id, price=price, items_in_stock=items_in_stock)

    assert offer.id == offer_id
    assert offer.price == price
    assert offer.items_in_stock == items_in_stock


def test_offer_repr():
    """
    Test the string representation of the Offer dataclass.

    Verifies that the __repr__ method returns the expected string format.
    """
    offer_id = uuid4()
    offer = Offer(id=offer_id, price=1999, items_in_stock=50)

    expected_repr = f"Offer(id={offer_id!r}, price={1999!r}, items_in_stock={50!r})"
    assert repr(offer) == expected_repr


# Test for the Product dataclass
def test_product_initialization():
    """
    Test the initialization of the Product dataclass.

    Verifies that a Product instance is created with the correct attributes.
    """
    product_id = uuid4()
    name = "Sample Product"
    description = "This is a sample product."

    product = Product(id=product_id, name=name, description=description)

    assert product.id == product_id
    assert product.name == name
    assert product.description == description


def test_product_to_dict():
    """
    Test the to_dict method of the Product dataclass.

    Verifies that the to_dict method returns the expected dictionary representation
    of the Product instance.
    """
    product_id = uuid4()
    product = Product(
        id=product_id, name="Sample Product", description="This is a sample product."
    )

    expected_dict = {
        "id": str(product_id),
        "name": "Sample Product",
        "description": "This is a sample product.",
    }
    assert product.to_dict() == expected_dict


def test_product_repr():
    """
    Test the string representation of the Product dataclass.

    Verifies that the __repr__ method returns the expected string format.
    """
    product_id = uuid4()
    product = Product(
        id=product_id, name="Sample Product", description="This is a sample product."
    )

    expected_repr = f"Product(id={product_id!r}, name={product.name!r}, description={product.description!r})"
    assert repr(product) == expected_repr


# Test for the APIResponse dataclass
def test_api_response_initialization():
    """
    Test the initialization of the APIResponse dataclass.

    Verifies that an APIResponse instance is created with the correct attributes.
    """
    response_data = {"key": "value", "another_key": 123}
    status_code = 200

    api_response = APIResponse(data=response_data, status_code=status_code)

    assert api_response.data == response_data
    assert api_response.status_code == status_code


def test_api_response_repr():
    """
    Test the string representation of the APIResponse dataclass.

    Verifies that the __repr__ method returns the expected string format.
    """
    response_data = {"key": "value", "another_key": 123}
    status_code = 200

    api_response = APIResponse(data=response_data, status_code=status_code)

    expected_repr = f"APIResponse(status_code={status_code!r}, data={response_data!r})"
    assert repr(api_response) == expected_repr
