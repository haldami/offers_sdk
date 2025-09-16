"""
Synchronous and asynchronous HTTP client using requests.

Implements IHttpClient interface by leveraging `requests` for sync calls and
`asyncio.to_thread` for async calls.
"""

import requests
import asyncio
from typing import Any, Dict, Optional

from .http_client_interface import IHttpClient
from .api_response import APIResponse


class RequestsClient(IHttpClient):
    """
    HTTP client using the requests library.

    Provides both synchronous and asynchronous methods for compatibility.
    """

    def __init__(self) -> None:
        self.session = requests.Session()

    async def async_get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        return await asyncio.to_thread(self._get_sync, url, params, headers)

    async def async_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        return await asyncio.to_thread(self._post_sync, url, data, headers)

    def sync_post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> APIResponse:
        return self._post_sync(url=url, data=data, headers=headers)

    def _get_sync(
        self,
        url: str,
        params: Optional[Dict[str, Any]],
        headers: Optional[Dict[str, str]],
    ) -> APIResponse:
        try:
            resp = self.session.get(url, params=params, headers=headers)
            return APIResponse(
                data=resp.json() if resp.content else {},
                status_code=resp.status_code,
            )
        except requests.RequestException as e:
            return APIResponse(
                data={"error": str(e)},
                status_code=getattr(e.response, "status_code", -1),
            )

    def _post_sync(
        self,
        url: str,
        data: Optional[Dict[str, Any]],
        headers: Optional[Dict[str, str]],
    ) -> APIResponse:
        try:
            resp = self.session.post(url, json=data, headers=headers)
            return APIResponse(
                data=resp.json() if resp.content else {},
                status_code=resp.status_code,
            )
        except requests.RequestException as e:
            return APIResponse(
                data={"error": str(e)},
                status_code=getattr(e.response, "status_code", -1),
            )
