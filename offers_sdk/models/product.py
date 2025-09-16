"""
Product model for the Offers SDK.

Represents a product that can be registered with the Offers API.
"""

from dataclasses import dataclass
from uuid import UUID
from typing import Dict


@dataclass
class Product:
    """
    Represents a product.

    Attributes:
        id: Unique identifier of the product.
        name: Name of the product.
        description: Description of the product.
    """
    id: UUID
    name: str
    description: str

    def to_dict(self) -> Dict[str, str]:
        """
        Convert the Product instance into a dictionary suitable for API requests.

        Returns:
            Dictionary containing the product's id, name, and description.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description
        }

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id!r}, name={self.name!r}, "
            f"description={self.description!r})"
        )
