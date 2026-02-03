"""
Product entity representing items sold in the marketplace.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Dimensions:
    """Product dimensions in centimeters."""
    length: float
    width: float
    height: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "length": self.length,
            "width": self.width,
            "height": self.height
        }


@dataclass
class Product:
    """
    Represents a product in the marketplace.
    
    Attributes:
        product_id: Unique identifier for the product
        name: Product name
        price: Price in INR
        weight_kg: Weight in kilograms (used for shipping calculation)
        dimensions: Optional product dimensions
    """
    product_id: int
    name: str
    price: float
    weight_kg: float
    dimensions: Optional[Dimensions] = None
    
    def __post_init__(self):
        """Validate product attributes."""
        if self.price < 0:
            raise ValueError(f"Price cannot be negative, got {self.price}")
        if self.weight_kg <= 0:
            raise ValueError(f"Weight must be positive, got {self.weight_kg}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        result = {
            "productId": self.product_id,
            "name": self.name,
            "price": self.price,
            "weightKg": self.weight_kg
        }
        if self.dimensions:
            result["dimensions"] = self.dimensions.to_dict()
        return result
