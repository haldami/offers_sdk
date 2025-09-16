"""
Offer model for the Offers SDK.

Represents a single offer for a product including price and stock information.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Offer:
    """
    Represents an offer for a product.

    Attributes:
        id: Unique identifier of the offer.
        price: Price of the offer in the smallest currency unit (e.g., cents).
        items_in_stock: Number of items currently in stock.
    """

    id: UUID
    price: int
    items_in_stock: int

    def __repr__(self) -> str:
        return (
            f"Offer(id={self.id!r}, price={self.price!r}, "
            f"items_in_stock={self.items_in_stock!r})"
        )
