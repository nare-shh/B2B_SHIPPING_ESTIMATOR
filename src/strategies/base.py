"""
Base shipping strategy interface.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ShippingCostResult:
    """Result of shipping cost calculation."""
    transport_cost: float
    distance_km: float
    weight_kg: float
    transport_mode: str
    rate_per_km_per_kg: float


class ShippingStrategy(ABC):
    """
    Abstract base class for shipping strategies.
    
    Implements the Strategy pattern for calculating shipping costs
    based on different transport modes (Mini Van, Truck, Aeroplane).
    
    Each strategy defines:
    - Distance range it applies to (min_distance, max_distance)
    - Rate per km per kg
    - Transport mode name
    """
    
    @property
    @abstractmethod
    def min_distance(self) -> float:
        """Minimum distance in km for this strategy (inclusive)."""
        pass
    
    @property
    @abstractmethod
    def max_distance(self) -> float:
        """Maximum distance in km for this strategy (exclusive, or inf)."""
        pass
    
    @property
    @abstractmethod
    def rate_per_km_per_kg(self) -> float:
        """Shipping rate in INR per km per kg."""
        pass
    
    @property
    @abstractmethod
    def mode_name(self) -> str:
        """Human-readable name of the transport mode."""
        pass
    
    def is_applicable(self, distance_km: float) -> bool:
        """
        Check if this strategy applies to the given distance.
        
        Args:
            distance_km: The distance in kilometers
            
        Returns:
            True if this strategy should be used for the distance
        """
        return self.min_distance <= distance_km < self.max_distance
    
    def calculate_cost(self, distance_km: float, weight_kg: float) -> ShippingCostResult:
        """
        Calculate the shipping cost for given distance and weight.
        
        Formula: cost = distance × rate × weight
        
        Args:
            distance_km: Distance in kilometers
            weight_kg: Product weight in kilograms
            
        Returns:
            ShippingCostResult with detailed breakdown
        """
        transport_cost = distance_km * self.rate_per_km_per_kg * weight_kg
        
        return ShippingCostResult(
            transport_cost=round(transport_cost, 2),
            distance_km=distance_km,
            weight_kg=weight_kg,
            transport_mode=self.mode_name,
            rate_per_km_per_kg=self.rate_per_km_per_kg
        )
