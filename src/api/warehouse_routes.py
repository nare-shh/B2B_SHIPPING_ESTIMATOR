"""
Warehouse API routes.
"""
from fastapi import APIRouter, Query, Depends
from src.api.schemas import NearestWarehouseResponse, LocationResponse
from src.core.dependencies import get_services, Services


router = APIRouter(prefix="/warehouse", tags=["Warehouse"])


@router.get(
    "/nearest",
    response_model=NearestWarehouseResponse,
    summary="Get Nearest Warehouse",
    description="""
    Find the nearest warehouse to a seller's location.
    
    This endpoint:
    1. Fetches the seller's location
    2. Calculates distance to all warehouses using Haversine formula
    3. Returns the nearest warehouse
    """
)
async def get_nearest_warehouse(
    seller_id: int = Query(
        ...,
        alias="sellerId",
        description="Seller's unique identifier",
        ge=1
    ),
    product_id: int = Query(
        ...,
        alias="productId",
        description="Product's unique identifier (for context)",
        ge=1
    ),
    services: Services = Depends(get_services)
) -> NearestWarehouseResponse:
    """
    Get the nearest warehouse to a seller.
    
    Args:
        seller_id: The seller's ID
        product_id: The product ID (for context/future use)
        services: Injected services container
        
    Returns:
        NearestWarehouseResponse with warehouse details
    """
    warehouse, distance = services.warehouse.find_nearest_warehouse(seller_id)
    
    return NearestWarehouseResponse(
        warehouseId=warehouse.warehouse_id,
        warehouseLocation=LocationResponse(
            lat=warehouse.location.lat,
            lng=warehouse.location.lng
        ),
        distanceKm=distance,
        warehouseName=warehouse.name
    )
