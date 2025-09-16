"""
HTTP client implementation using the httpx library.

Provides synchronous and asynchronous HTTP request methods by implementing
the IHttpClient interface.
"""

from typing import Any, Dict, Optional
import httpx
from .http_client_interface import IHttpClient
from .api_response import APIResponse


class HttpxClient(IHttpClient):
    """HTTP client using httpx supporting both asynchronous and synchronous calls."""

    async def async_get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        """Perform an asynchronous HTTP GET request.

        Args:
            url (str): The target URL.
            params (Optional[Dict[str, Any]]): Query parameters for the request.
            headers (Optional[Dict[str, str]]): HTTP headers to include.

        Returns:
            APIResponse: The response containing the status code and parsed JSON data.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                return APIResponse(
                    data=response.json() if response.content else {},
                    status_code=response.status_code,
                )
        except httpx.RequestError as exc:
            return APIResponse(data={"error": str(exc)}, status_code=500)

    async def async_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        """Perform an asynchronous HTTP POST request with JSON payload.

        Args:
            url (str): The target URL.
            data (Optional[Dict[str, Any]]): JSON data to send in the request body.
            headers (Optional[Dict[str, str]]): HTTP headers to include.

        Returns:
            APIResponse: The response containing the status code and parsed JSON data.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers)
                return APIResponse(
                    data=response.json() if response.content else {},
                    status_code=response.status_code,
                )
        except httpx.RequestError as exc:
            return APIResponse(data={"error": str(exc)}, status_code=500)

    def sync_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        """Perform a synchronous HTTP POST request with JSON payload.

        Args:
            url (str): The target URL.
            data (Optional[Dict[str, Any]]): JSON data to send in the request body.
            headers (Optional[Dict[str, str]]): HTTP headers to include.

        Returns:
            APIResponse: The response containing the status code and parsed JSON data.
        """
        try:
            with httpx.Client() as client:
                response = client.post(url, json=data, headers=headers)
                return APIResponse(
                    data=response.json() if response.content else {},
                    status_code=response.status_code,
                )
        except httpx.RequestError as e:
            return APIResponse(data={"error": str(e)}, status_code=500)
