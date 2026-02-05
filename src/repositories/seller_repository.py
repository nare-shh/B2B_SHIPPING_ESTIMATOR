"""
Seller repository for managing seller data.
"""
from src.repositories.base import BaseRepository
from src.entities.seller import Seller


class SellerRepository(BaseRepository[Seller]):
    """
    Repository for Seller entities.
    
    Provides CRUD operations for sellers (Kirana stores) with in-memory storage.
    """
    
    def _get_id(self, entity: Seller) -> int:
        """Extract seller_id from Seller entity."""
        return entity.seller_id
    
    def find_by_name(self, name: str) -> list[Seller]:
        """
        Find sellers by name (partial match, case-insensitive).
        
        Args:
            name: The name to search for
            
        Returns:
            List of matching sellers
        """
        name_lower = name.lower()
        return [
            seller for seller in self._store.values()
            if name_lower in seller.name.lower()
        ]
