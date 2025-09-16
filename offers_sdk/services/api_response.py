"""
API Response model for the Offers SDK.

Represents the response from an HTTP request made by the SDK.
"""

from dataclasses import dataclass
from typing import Dict, Any, Union, List


@dataclass
class APIResponse:
    """
    Represents the result of an API call.

    Attributes:
        data: Parsed JSON response from the API.
        status_code: HTTP status code returned by the API.
    """

    data: Dict[str, Any]
    status_code: int

    def __repr__(self) -> str:
        return f"APIResponse(status_code={self.status_code!r}, data={self.data!r})"
