"""
Mini Van shipping strategy for short distances (0-100 km).
"""
from src.strategies.base import ShippingStrategy


class MiniVanStrategy(ShippingStrategy):
    """
    Shipping strategy for Mini Van transport.
    
    Applies to distances: 0-100 km
    Rate: 3 INR per km per kg
    """
    
    @property
    def min_distance(self) -> float:
        return 0
    
    @property
    def max_distance(self) -> float:
        return 100
    
    @property
    def rate_per_km_per_kg(self) -> float:
        return 3.0
    
    @property
    def mode_name(self) -> str:
        return "Mini Van"
