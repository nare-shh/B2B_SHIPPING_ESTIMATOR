"""
Customer entity representing a buyer in the marketplace.
"""
from dataclasses import dataclass
from src.entities.location import Location


@dataclass
class Customer:
    """
    Represents a customer (buyer) in the B2B marketplace.
    
    Attributes:
        customer_id: Unique identifier for the customer
        name: Customer's name
        phone: Contact phone number
        location: Geographic location for delivery
    """
    customer_id: int
    name: str
    phone: str
    location: Location
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "customerId": self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "location": self.location.to_dict()
        }
