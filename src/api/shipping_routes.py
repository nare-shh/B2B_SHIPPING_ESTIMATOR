"""
Shipping charge API routes.
"""
from fastapi import APIRouter, Query, Depends
from src.api.schemas import (
    ShippingChargeResponse,
    ShippingBreakdown,
    DeliveryCostBreakdown,
    CalculateShippingRequest,
    TotalShippingResponse,
    WarehouseLocationResponse,
    LocationResponse
)
from src.core.dependencies import get_services, Services


router = APIRouter(prefix="/shipping-charge", tags=["Shipping"])


@router.get(
    "",
    response_model=ShippingChargeResponse,
    summary="Get Shipping Charge From Warehouse",
    description="""
    Calculate shipping charge from a specific warehouse to a customer.
    
    This endpoint:
    1. Calculates warehouse to customer distance
    2. Selects transport mode based on distance
    3. Computes shipping = distance × rate × product weight
    4. Adds delivery speed charges
    """
)
async def get_shipping_charge(
    warehouse_id: int = Query(
        ...,
        alias="warehouseId",
        description="Warehouse's unique identifier",
        ge=1
    ),
    customer_id: int = Query(
        ...,
        alias="customerId",
        description="Customer's unique identifier",
        ge=1
    ),
    product_id: int = Query(
        ...,
        alias="productId",
        description="Product's unique identifier",
        ge=1
    ),
    delivery_speed: str = Query(
        "standard",
        alias="deliverySpeed",
        description="Delivery speed: 'standard' or 'express'"
    ),
    services: Services = Depends(get_services)
) -> ShippingChargeResponse:
    """
    Calculate shipping charge from warehouse to customer.
    
    Args:
        warehouse_id: The warehouse ID
        customer_id: The customer ID
        product_id: The product ID
        delivery_speed: 'standard' or 'express'
        services: Injected services container
        
    Returns:
        ShippingChargeResponse with charge and breakdown
    """
    result = services.shipping_charge.calculate_from_warehouse(
        warehouse_id=warehouse_id,
        customer_id=customer_id,
        product_id=product_id,
        delivery_speed=delivery_speed
    )
    
    return ShippingChargeResponse(
        shippingCharge=result.shipping_charge,
        breakdown=ShippingBreakdown(
            distanceKm=result.distance_km,
            transportMode=result.transport_mode,
            transportCost=result.transport_cost,
            deliveryCost=DeliveryCostBreakdown(
                baseCharge=result.delivery_cost.base_charge,
                extraCharge=result.delivery_cost.extra_charge,
                total=result.delivery_cost.total,
                speed=result.delivery_cost.speed
            ),
            weightKg=result.weight_kg
        )
    )


@router.post(
    "/calculate",
    response_model=TotalShippingResponse,
    summary="Calculate Total Shipping Charge",
    description="""
    Calculate complete shipping charge from seller to customer.
    
    This is the main endpoint that:
    1. Finds the nearest warehouse to the seller
    2. Calculates shipping from that warehouse to customer
    3. Returns final shipping charge with warehouse details
    """
)
async def calculate_total_shipping(
    request: CalculateShippingRequest,
    services: Services = Depends(get_services)
) -> TotalShippingResponse:
    """
    Calculate total shipping charge including warehouse selection.
    
    Args:
        request: The calculation request with seller, customer, product, and speed
        services: Injected services container
        
    Returns:
        TotalShippingResponse with charge and warehouse info
    """
    result = services.shipping_charge.calculate_total(
        seller_id=request.sellerId,
        customer_id=request.customerId,
        product_id=request.productId,
        delivery_speed=request.deliverySpeed
    )
    
    breakdown = result.breakdown
    
    return TotalShippingResponse(
        shippingCharge=result.shipping_charge,
        nearestWarehouse=WarehouseLocationResponse(
            warehouseId=result.nearest_warehouse.warehouse_id,
            warehouseLocation=LocationResponse(
                lat=result.nearest_warehouse.location.lat,
                lng=result.nearest_warehouse.location.lng
            )
        ),
        breakdown=ShippingBreakdown(
            distanceKm=breakdown.distance_km,
            transportMode=breakdown.transport_mode,
            transportCost=breakdown.transport_cost,
            deliveryCost=DeliveryCostBreakdown(
                baseCharge=breakdown.delivery_cost.base_charge,
                extraCharge=breakdown.delivery_cost.extra_charge,
                total=breakdown.delivery_cost.total,
                speed=breakdown.delivery_cost.speed
            ),
            weightKg=breakdown.weight_kg
        )
    )
