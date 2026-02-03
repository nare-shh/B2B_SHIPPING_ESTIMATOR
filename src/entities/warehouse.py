"""
Warehouse entity representing storage/distribution centers.
"""
from dataclasses import dataclass
from src.entities.location import Location


@dataclass
class Warehouse:
    """
    Represents a warehouse in the distribution network.
    
    Sellers drop products at the nearest warehouse, and items
    are shipped from the warehouse to customers.
    
    Attributes:
        warehouse_id: Unique identifier for the warehouse
        location: Geographic location of the warehouse
        name: Optional warehouse name/identifier
    """
    warehouse_id: int
    location: Location
    name: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "warehouseId": self.warehouse_id,
            "warehouseLocation": self.location.to_dict(),
            "name": self.name
        }
