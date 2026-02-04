"""
Aeroplane shipping strategy for long distances (500+ km).
"""
import math
from src.strategies.base import ShippingStrategy


class AeroplaneStrategy(ShippingStrategy):
    """
    Shipping strategy for Aeroplane transport.
    
    Applies to distances: 500+ km
    Rate: 1 INR per km per kg
    """
    
    @property
    def min_distance(self) -> float:
        return 500
    
    @property
    def max_distance(self) -> float:
        return math.inf
    
    @property
    def rate_per_km_per_kg(self) -> float:
        return 1.0
    
    @property
    def mode_name(self) -> str:
        return "Aeroplane"
