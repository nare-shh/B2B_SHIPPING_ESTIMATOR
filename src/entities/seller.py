"""
Seller entity representing a vendor in the marketplace.
"""
from dataclasses import dataclass
from src.entities.location import Location


@dataclass
class Seller:
    """
    Represents a seller (Kirana store) in the B2B marketplace.
    
    Attributes:
        seller_id: Unique identifier for the seller
        name: Seller's store name
        location: Geographic location of the store
    """
    seller_id: int
    name: str
    location: Location
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "sellerId": self.seller_id,
            "name": self.name,
            "location": self.location.to_dict()
        }
