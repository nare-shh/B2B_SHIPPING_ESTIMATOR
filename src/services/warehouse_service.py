"""
Warehouse service for finding nearest warehouse.
"""
from typing import Optional, Tuple
from src.entities.warehouse import Warehouse
from src.entities.seller import Seller
from src.repositories.warehouse_repository import WarehouseRepository
from src.repositories.seller_repository import SellerRepository
from src.services.distance_calculator import DistanceCalculator
from src.core.exceptions import NotFoundError


class WarehouseService:
    """
    Service for warehouse-related business logic.
    
    Handles finding the nearest warehouse to a seller's location.
    """
    
    def __init__(
        self,
        warehouse_repo: WarehouseRepository,
        seller_repo: SellerRepository
    ):
        """
        Initialize the warehouse service.
        
        Args:
            warehouse_repo: Repository for warehouse data
            seller_repo: Repository for seller data
        """
        self._warehouse_repo = warehouse_repo
        self._seller_repo = seller_repo
    
    def find_nearest_warehouse(self, seller_id: int) -> Tuple[Warehouse, float]:
        """
        Find the nearest warehouse to a seller's location.
        
        Args:
            seller_id: The seller's unique identifier
            
        Returns:
            Tuple of (nearest warehouse, distance in km)
            
        Raises:
            NotFoundError: If seller not found or no warehouses exist
        """
        # Get the seller
        seller = self._seller_repo.get_by_id(seller_id)
        if not seller:
            raise NotFoundError(f"Seller with ID {seller_id} not found")
        
        # Get all warehouses
        warehouses = self._warehouse_repo.get_all()
        if not warehouses:
            raise NotFoundError("No warehouses available in the system")
        
        # Find the nearest warehouse
        nearest: Optional[Warehouse] = None
        min_distance = float('inf')
        
        for warehouse in warehouses:
            distance = DistanceCalculator.calculate(
                seller.location,
                warehouse.location
            )
            if distance < min_distance:
                min_distance = distance
                nearest = warehouse
        
        return nearest, min_distance
    
    def get_warehouse(self, warehouse_id: int) -> Warehouse:
        """
        Get a warehouse by ID.
        
        Args:
            warehouse_id: The warehouse's unique identifier
            
        Returns:
            The warehouse
            
        Raises:
            NotFoundError: If warehouse not found
        """
        warehouse = self._warehouse_repo.get_by_id(warehouse_id)
        if not warehouse:
            raise NotFoundError(f"Warehouse with ID {warehouse_id} not found")
        return warehouse
