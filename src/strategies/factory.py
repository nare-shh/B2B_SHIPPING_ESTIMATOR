"""
Factory for selecting the appropriate shipping strategy based on distance.
"""
from typing import List
from src.strategies.base import ShippingStrategy
from src.strategies.mini_van import MiniVanStrategy
from src.strategies.truck import TruckStrategy
from src.strategies.aeroplane import AeroplaneStrategy


class ShippingStrategyFactory:
    """
    Factory class for selecting the appropriate shipping strategy.
    
    Uses the Factory pattern to encapsulate strategy selection logic
    based on distance. Strategies are registered in order of precedence.
    """
    
    def __init__(self):
        """Initialize with default strategies."""
        self._strategies: List[ShippingStrategy] = [
            MiniVanStrategy(),
            TruckStrategy(),
            AeroplaneStrategy()
        ]
    
    def get_strategy(self, distance_km: float) -> ShippingStrategy:
        """
        Get the appropriate shipping strategy for the given distance.
        
        Args:
            distance_km: The shipping distance in kilometers
            
        Returns:
            The appropriate ShippingStrategy for the distance
            
        Raises:
            ValueError: If no strategy is applicable (shouldn't happen with default config)
        """
        if distance_km < 0:
            raise ValueError(f"Distance cannot be negative: {distance_km}")
        
        for strategy in self._strategies:
            if strategy.is_applicable(distance_km):
                return strategy
        
        # Fallback to aeroplane for any distance not covered
        # This handles edge cases like exactly 500km
        return self._strategies[-1]
    
    def get_all_strategies(self) -> List[ShippingStrategy]:
        """Return all registered strategies."""
        return self._strategies.copy()
    
    def register_strategy(self, strategy: ShippingStrategy) -> None:
        """
        Register a new shipping strategy.
        
        Strategies are evaluated in order, so add them appropriately.
        
        Args:
            strategy: The strategy to register
        """
        self._strategies.append(strategy)
        # Sort by min_distance to ensure proper evaluation order
        self._strategies.sort(key=lambda s: s.min_distance)
