"""
Authentication tests for the Offers SDK Client.

These tests cover:
1. Invalid refresh tokens.
2. Normal authentication flow.
3. Handling of repeated authentication requests within the API cooldown period.
"""

import pytest
from offers_sdk.client import Client
from offers_sdk.exceptions import AuthException, InvalidAPIRequestException


def test_wrong_refresh_token(client_type: str) -> None:
    """
    Test that using a wrong refresh token raises AuthException.

    Args:
        client_type: Type of HTTP client ('requests', 'httpx', or 'aiohttp').
    """
    with pytest.raises(AuthException):
        client = Client.load_from_file(
            f"dumped_clients/{client_type}_wrong_refresh_token.json"
        )
        client.retrieve_access_token()


def test_normal(client_type: str) -> None:
    """
    Test normal authentication flow.

    - Retrieves a valid access token.
    - Asserts that the token is set.
    - Saves the client state for reuse in subsequent tests.

    Args:
        client_type: Type of HTTP client ('requests', 'httpx', or 'aiohttp').
    """
    client = Client.load_from_file(f"dumped_clients/{client_type}.json")
    client.retrieve_access_token()  # Should complete without error.

    assert client.access_token, "Access token should be set after successful auth."

    # Save client state for further tests (avoiding repeated auth calls)
    client.save_to_file(f"dumped_clients/{client_type}_w_access_token.json")


def test_normal_second(client_type: str) -> None:
    """
    Test that attempting a second authentication within the cooldown period
    raises InvalidAPIRequestException (HTTP 400).

    Args:
        client_type: Type of HTTP client ('requests', 'httpx', or 'aiohttp').
    """
    with pytest.raises(InvalidAPIRequestException):
        client = Client.load_from_file(f"dumped_clients/{client_type}.json")
        client.retrieve_access_token()
