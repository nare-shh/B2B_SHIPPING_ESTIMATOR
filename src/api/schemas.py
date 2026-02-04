"""
Pydantic schemas for API request/response models.

These schemas provide:
- Request validation
- Automatic OpenAPI documentation
- Response serialization
"""
from pydantic import BaseModel, Field
from typing import Optional


# ========== LOCATION SCHEMAS ==========

class LocationResponse(BaseModel):
    """Geographic location response."""
    lat: float = Field(..., description="Latitude in degrees")
    long: float = Field(..., description="Longitude in degrees", alias="lng")
    
    class Config:
        populate_by_name = True


# ========== WAREHOUSE SCHEMAS ==========

class WarehouseLocationResponse(BaseModel):
    """Warehouse location with ID."""
    warehouseId: int = Field(..., description="Unique warehouse identifier")
    warehouseLocation: LocationResponse = Field(..., description="Warehouse coordinates")


class NearestWarehouseResponse(BaseModel):
    """Response for nearest warehouse lookup."""
    warehouseId: int = Field(..., description="Nearest warehouse ID")
    warehouseLocation: LocationResponse = Field(..., description="Warehouse coordinates")
    distanceKm: Optional[float] = Field(None, description="Distance from seller in km")
    warehouseName: Optional[str] = Field(None, description="Warehouse name")


# ========== DELIVERY COST SCHEMAS ==========

class DeliveryCostBreakdown(BaseModel):
    """Delivery speed cost breakdown."""
    baseCharge: float = Field(..., description="Base courier charge in INR")
    extraCharge: float = Field(..., description="Extra charge for express delivery")
    total: float = Field(..., description="Total delivery cost")
    speed: str = Field(..., description="Delivery speed (standard/express)")


# ========== SHIPPING CHARGE SCHEMAS ==========

class ShippingBreakdown(BaseModel):
    """Detailed shipping cost breakdown."""
    distanceKm: float = Field(..., description="Distance in kilometers")
    transportMode: str = Field(..., description="Transport mode used")
    transportCost: float = Field(..., description="Transport cost in INR")
    deliveryCost: DeliveryCostBreakdown = Field(..., description="Delivery speed costs")
    weightKg: float = Field(..., description="Product weight in kg")


class ShippingChargeResponse(BaseModel):
    """Response for shipping charge calculation."""
    shippingCharge: float = Field(..., description="Total shipping charge in INR")
    breakdown: Optional[ShippingBreakdown] = Field(None, description="Cost breakdown")


class CalculateShippingRequest(BaseModel):
    """Request body for total shipping calculation."""
    sellerId: int = Field(..., description="Seller's unique identifier")
    customerId: int = Field(..., description="Customer's unique identifier")
    productId: int = Field(..., description="Product's unique identifier")
    deliverySpeed: str = Field(
        "standard",
        description="Delivery speed: 'standard' or 'express'"
    )


class TotalShippingResponse(BaseModel):
    """Response for total shipping calculation."""
    shippingCharge: float = Field(..., description="Total shipping charge in INR")
    nearestWarehouse: WarehouseLocationResponse = Field(..., description="Selected warehouse")
    breakdown: Optional[ShippingBreakdown] = Field(None, description="Detailed cost breakdown")


# ========== ERROR SCHEMAS ==========

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    statusCode: int = Field(..., description="HTTP status code")
