"""
Warehouse repository for managing warehouse data.
"""
from src.repositories.base import BaseRepository
from src.entities.warehouse import Warehouse


class WarehouseRepository(BaseRepository[Warehouse]):
    """
    Repository for Warehouse entities.
    
    Provides CRUD operations for warehouses with in-memory storage.
    """
    
    def _get_id(self, entity: Warehouse) -> int:
        """Extract warehouse_id from Warehouse entity."""
        return entity.warehouse_id
