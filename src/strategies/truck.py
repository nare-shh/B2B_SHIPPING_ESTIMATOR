"""
Truck shipping strategy for medium distances (100-500 km).
"""
from src.strategies.base import ShippingStrategy


class TruckStrategy(ShippingStrategy):
    """
    Shipping strategy for Truck transport.
    
    Applies to distances: 100-500 km
    Rate: 2 INR per km per kg
    """
    
    @property
    def min_distance(self) -> float:
        return 100
    
    @property
    def max_distance(self) -> float:
        return 500
    
    @property
    def rate_per_km_per_kg(self) -> float:
        return 2.0
    
    @property
    def mode_name(self) -> str:
        return "Truck"
