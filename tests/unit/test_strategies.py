"""
Unit tests for shipping strategies.
"""
import pytest
from src.strategies import (
    MiniVanStrategy,
    TruckStrategy,
    AeroplaneStrategy,
    ShippingStrategyFactory
)


class TestMiniVanStrategy:
    """Test suite for MiniVanStrategy."""
    
    def test_properties(self):
        """Test strategy properties."""
        strategy = MiniVanStrategy()
        assert strategy.min_distance == 0
        assert strategy.max_distance == 100
        assert strategy.rate_per_km_per_kg == 3.0
        assert strategy.mode_name == "Mini Van"
    
    def test_applicability(self):
        """Test distance range applicability."""
        strategy = MiniVanStrategy()
        
        assert strategy.is_applicable(0)
        assert strategy.is_applicable(50)
        assert strategy.is_applicable(99.9)
        assert not strategy.is_applicable(100)
        assert not strategy.is_applicable(150)
    
    def test_cost_calculation(self):
        """Test cost calculation."""
        strategy = MiniVanStrategy()
        
        # 50 km, 2 kg → 50 * 3 * 2 = 300 INR
        result = strategy.calculate_cost(distance_km=50, weight_kg=2)
        
        assert result.transport_cost == 300.0
        assert result.transport_mode == "Mini Van"
        assert result.rate_per_km_per_kg == 3.0


class TestTruckStrategy:
    """Test suite for TruckStrategy."""
    
    def test_properties(self):
        """Test strategy properties."""
        strategy = TruckStrategy()
        assert strategy.min_distance == 100
        assert strategy.max_distance == 500
        assert strategy.rate_per_km_per_kg == 2.0
        assert strategy.mode_name == "Truck"
    
    def test_applicability(self):
        """Test distance range applicability."""
        strategy = TruckStrategy()
        
        assert not strategy.is_applicable(99)
        assert strategy.is_applicable(100)
        assert strategy.is_applicable(250)
        assert strategy.is_applicable(499.9)
        assert not strategy.is_applicable(500)
    
    def test_cost_calculation(self):
        """Test cost calculation."""
        strategy = TruckStrategy()
        
        # 200 km, 5 kg → 200 * 2 * 5 = 2000 INR
        result = strategy.calculate_cost(distance_km=200, weight_kg=5)
        
        assert result.transport_cost == 2000.0
        assert result.transport_mode == "Truck"


class TestAeroplaneStrategy:
    """Test suite for AeroplaneStrategy."""
    
    def test_properties(self):
        """Test strategy properties."""
        strategy = AeroplaneStrategy()
        assert strategy.min_distance == 500
        assert strategy.rate_per_km_per_kg == 1.0
        assert strategy.mode_name == "Aeroplane"
    
    def test_applicability(self):
        """Test distance range applicability."""
        strategy = AeroplaneStrategy()
        
        assert not strategy.is_applicable(499)
        assert strategy.is_applicable(500)
        assert strategy.is_applicable(1000)
        assert strategy.is_applicable(5000)
    
    def test_cost_calculation(self):
        """Test cost calculation."""
        strategy = AeroplaneStrategy()
        
        # 1000 km, 3 kg → 1000 * 1 * 3 = 3000 INR
        result = strategy.calculate_cost(distance_km=1000, weight_kg=3)
        
        assert result.transport_cost == 3000.0
        assert result.transport_mode == "Aeroplane"


class TestShippingStrategyFactory:
    """Test suite for ShippingStrategyFactory."""
    
    def test_get_mini_van_for_short_distance(self):
        """Factory returns MiniVan for 0-100 km."""
        factory = ShippingStrategyFactory()
        
        strategy = factory.get_strategy(50)
        
        assert isinstance(strategy, MiniVanStrategy)
    
    def test_get_truck_for_medium_distance(self):
        """Factory returns Truck for 100-500 km."""
        factory = ShippingStrategyFactory()
        
        strategy = factory.get_strategy(250)
        
        assert isinstance(strategy, TruckStrategy)
    
    def test_get_aeroplane_for_long_distance(self):
        """Factory returns Aeroplane for 500+ km."""
        factory = ShippingStrategyFactory()
        
        strategy = factory.get_strategy(800)
        
        assert isinstance(strategy, AeroplaneStrategy)
    
    def test_boundary_100km(self):
        """Test boundary at 100 km (should be Truck)."""
        factory = ShippingStrategyFactory()
        
        strategy = factory.get_strategy(100)
        
        assert isinstance(strategy, TruckStrategy)
    
    def test_boundary_500km(self):
        """Test boundary at 500 km (should be Aeroplane)."""
        factory = ShippingStrategyFactory()
        
        strategy = factory.get_strategy(500)
        
        assert isinstance(strategy, AeroplaneStrategy)
    
    def test_negative_distance_raises_error(self):
        """Negative distance should raise ValueError."""
        factory = ShippingStrategyFactory()
        
        with pytest.raises(ValueError, match="cannot be negative"):
            factory.get_strategy(-10)
    
    def test_zero_distance(self):
        """Zero distance should return MiniVan."""
        factory = ShippingStrategyFactory()
        
        strategy = factory.get_strategy(0)
        
        assert isinstance(strategy, MiniVanStrategy)
