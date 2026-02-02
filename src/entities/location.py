"""
Location entity representing geographic coordinates.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    """
    Represents a geographic location with latitude and longitude.
    
    Attributes:
        lat: Latitude in degrees (-90 to 90)
        lng: Longitude in degrees (-180 to 180)
    """
    lat: float
    lng: float
    
    def __post_init__(self):
        """Validate coordinates are within valid ranges."""
        if not -90 <= self.lat <= 90:
            raise ValueError(f"Latitude must be between -90 and 90, got {self.lat}")
        if not -180 <= self.lng <= 180:
            raise ValueError(f"Longitude must be between -180 and 180, got {self.lng}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {"lat": self.lat, "long": self.lng}
