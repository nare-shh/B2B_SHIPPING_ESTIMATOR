"""
Distance calculator using Haversine formula.
"""
import math
from src.entities.location import Location


class DistanceCalculator:
    """
    Calculates distances between geographic coordinates using the Haversine formula.
    
    The Haversine formula determines the great-circle distance between two points
    on a sphere given their longitudes and latitudes.
    
    Formula:
        a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
        c = 2 × atan2(√a, √(1−a))
        d = R × c
    
    Where R is the Earth's radius (approximately 6371 km).
    """
    
    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0
    
    @classmethod
    def calculate(cls, location1: Location, location2: Location) -> float:
        """
        Calculate the distance between two locations in kilometers.
        
        Args:
            location1: The first location
            location2: The second location
            
        Returns:
            Distance in kilometers, rounded to 2 decimal places
        """
        # Convert degrees to radians
        lat1 = math.radians(location1.lat)
        lat2 = math.radians(location2.lat)
        lon1 = math.radians(location1.lng)
        lon2 = math.radians(location2.lng)
        
        # Differences
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Haversine formula
        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = cls.EARTH_RADIUS_KM * c
        
        return round(distance, 2)
    
    @classmethod
    def calculate_from_coords(
        cls,
        lat1: float,
        lng1: float,
        lat2: float,
        lng2: float
    ) -> float:
        """
        Calculate distance from raw coordinates.
        
        Convenience method that accepts raw float coordinates.
        
        Args:
            lat1: Latitude of first point
            lng1: Longitude of first point
            lat2: Latitude of second point
            lng2: Longitude of second point
            
        Returns:
            Distance in kilometers
        """
        location1 = Location(lat=lat1, lng=lng1)
        location2 = Location(lat=lat2, lng=lng2)
        return cls.calculate(location1, location2)
