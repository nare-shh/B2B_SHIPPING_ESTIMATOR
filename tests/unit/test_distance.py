"""
Unit tests for the Haversine distance calculator.
"""
import pytest
from src.services.distance_calculator import DistanceCalculator
from src.entities.location import Location


class TestDistanceCalculator:
    """Test suite for DistanceCalculator."""
    
    def test_same_location_returns_zero(self):
        """Distance between same location should be 0."""
        loc = Location(lat=28.7041, lng=77.1025)  # Delhi
        distance = DistanceCalculator.calculate(loc, loc)
        assert distance == 0.0
    
    def test_mumbai_to_delhi(self):
        """Test known distance: Mumbai to Delhi is ~1153 km."""
        mumbai = Location(lat=19.0760, lng=72.8777)
        delhi = Location(lat=28.7041, lng=77.1025)
        
        distance = DistanceCalculator.calculate(mumbai, delhi)
        
        # Allow 5% tolerance for Haversine approximation
        assert 1090 < distance < 1210
    
    def test_bangalore_to_chennai(self):
        """Test known distance: Bangalore to Chennai is ~290 km."""
        bangalore = Location(lat=12.9716, lng=77.5946)
        chennai = Location(lat=13.0827, lng=80.2707)
        
        distance = DistanceCalculator.calculate(bangalore, chennai)
        
        # Allow tolerance
        assert 275 < distance < 310
    
    def test_short_distance(self):
        """Test very short distance (within a city)."""
        # Andheri to Bandra in Mumbai (~10 km)
        andheri = Location(lat=19.1136, lng=72.8697)
        bandra = Location(lat=19.0544, lng=72.8402)
        
        distance = DistanceCalculator.calculate(andheri, bandra)
        
        assert 5 < distance < 15
    
    def test_long_distance_across_india(self):
        """Test long distance: Delhi to Kochi is ~2000+ km."""
        delhi = Location(lat=28.7041, lng=77.1025)
        kochi = Location(lat=9.9312, lng=76.2673)
        
        distance = DistanceCalculator.calculate(delhi, kochi)
        
        assert distance > 1900
        assert distance < 2200
    
    def test_calculate_from_coords(self):
        """Test convenience method with raw coordinates."""
        distance = DistanceCalculator.calculate_from_coords(
            lat1=19.0760, lng1=72.8777,  # Mumbai
            lat2=18.5204, lng2=73.8567   # Pune
        )
        
        # Mumbai to Pune is ~120 km
        assert 100 < distance < 150
    
    def test_symmetry(self):
        """Distance A→B should equal B→A."""
        mumbai = Location(lat=19.0760, lng=72.8777)
        delhi = Location(lat=28.7041, lng=77.1025)
        
        distance_ab = DistanceCalculator.calculate(mumbai, delhi)
        distance_ba = DistanceCalculator.calculate(delhi, mumbai)
        
        assert distance_ab == distance_ba
    
    def test_equator_crossing(self):
        """Test distance calculation crossing the equator."""
        north = Location(lat=10.0, lng=77.0)
        south = Location(lat=-10.0, lng=77.0)
        
        distance = DistanceCalculator.calculate(north, south)
        
        # ~2222 km (20 degrees * 111 km/degree)
        assert 2100 < distance < 2350
