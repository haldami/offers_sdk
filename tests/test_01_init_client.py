"""
Tests for Client initialization with different HTTP client types.

These tests ensure that:
1. The Client correctly instantiates the desired HTTP client.
2. Invalid client types raise the appropriate exception.
"""

import pytest
from offers_sdk.client import Client
from offers_sdk.services import AioHttpClient, HttpxClient, RequestsClient
from offers_sdk.exceptions import InvalidClientTypeException


def test_init_requests() -> None:
    """
    Test that a Client initialized from a 'requests' JSON uses RequestsClient.
    """
    client = Client.load_from_file("dumped_clients/requests.json")
    assert isinstance(
        client.http_client, RequestsClient
    ), "Client.http_client should be of type RequestsClient."


def test_init_httpx() -> None:
    """
    Test that a Client initialized from a 'httpx' JSON uses HttpxClient.
    """
    client = Client.load_from_file("dumped_clients/httpx.json")
    assert isinstance(
        client.http_client, HttpxClient
    ), "Client.http_client should be of type HttpxClient."


def test_init_aiohttp() -> None:
    """
    Test that a Client initialized from an 'aiohttp' JSON uses AioHttpClient.
    """
    client = Client.load_from_file("dumped_clients/aiohttp.json")
    assert isinstance(
        client.http_client, AioHttpClient
    ), "Client.http_client should be of type AioHttpClient."


def test_init_nonsense() -> None:
    """
    Test that initializing a Client with an unsupported client type
    raises InvalidClientTypeException.
    """
    with pytest.raises(InvalidClientTypeException):
        Client.load_from_file("dumped_clients/nonsense_http_client.json")
