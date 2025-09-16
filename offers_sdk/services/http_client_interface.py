"""
Interface for HTTP clients used by the Offers SDK.

Defines required methods for synchronous and asynchronous HTTP operations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from .api_response import APIResponse


class IHttpClient(ABC):
    """
    Abstract base class for HTTP clients used in the SDK.
    """

    @abstractmethod
    async def async_get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Perform an asynchronous HTTP GET request.

        Args:
            url: URL to send the GET request to.
            params: Optional query parameters.
            headers: Optional HTTP headers.

        Returns:
            APIResponse: The result of the HTTP request.
        """
        pass

    @abstractmethod
    async def async_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Perform an asynchronous HTTP POST request.

        Args:
            url: URL to send the POST request to.
            data: Optional JSON payload.
            headers: Optional HTTP headers.

        Returns:
            APIResponse: The result of the HTTP request.
        """
        pass

    @abstractmethod
    def sync_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Perform a synchronous HTTP POST request.

        Args:
            url: URL to send the POST request to.
            data: Optional JSON payload.
            headers: Optional HTTP headers.

        Returns:
            APIResponse: The result of the HTTP request.
        """
        pass
