"""
Asynchronous HTTP client using aiohttp.

Implements the IHttpClient interface to perform async GET/POST requests.
"""

from typing import Any, Dict, Optional
import asyncio
import aiohttp

from .api_response import APIResponse
from .http_client_interface import IHttpClient


class AioHttpClient(IHttpClient):
    """
    Async HTTP client using aiohttp for network calls.
    """

    async def async_get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        """
        Perform an asynchronous GET request.

        Args:
            url: Target URL.
            params: Optional query parameters.
            headers: Optional HTTP headers.

        Returns:
            APIResponse: Contains JSON data and HTTP status code.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    try:
                        data = await response.json(content_type=None)
                    except Exception:
                        data = {}
                    return APIResponse(data=data, status_code=response.status)
        except Exception as e:
            return APIResponse(data={"error": str(e)}, status_code=500)

    async def async_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        """
        Perform an asynchronous POST request.

        Args:
            url: Target URL.
            data: Optional JSON payload.
            headers: Optional HTTP headers.

        Returns:
            APIResponse: Contains JSON data and HTTP status code.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    try:
                        resp_data = await response.json(content_type=None)
                    except Exception:
                        resp_data = {}
                    return APIResponse(data=resp_data, status_code=response.status)
        except Exception as e:
            return APIResponse(data={"error": str(e)}, status_code=500)

    def sync_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        """
        Synchronous wrapper for async_post.

        Args:
            url: Target URL.
            data: Optional JSON payload.
            headers: Optional HTTP headers.

        Returns:
            APIResponse: Contains JSON data and HTTP status code.
        """
        return asyncio.run(self.async_post(url, data=data, headers=headers))
