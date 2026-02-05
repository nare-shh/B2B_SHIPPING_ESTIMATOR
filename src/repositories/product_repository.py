"""
Product repository for managing product data.
"""
from src.repositories.base import BaseRepository
from src.entities.product import Product


class ProductRepository(BaseRepository[Product]):
    """
    Repository for Product entities.
    
    Provides CRUD operations for products with in-memory storage.
    """
    
    def _get_id(self, entity: Product) -> int:
        """Extract product_id from Product entity."""
        return entity.product_id
    
    def find_by_price_range(self, min_price: float, max_price: float) -> list[Product]:
        """
        Find products within a price range.
        
        Args:
            min_price: Minimum price (inclusive)
            max_price: Maximum price (inclusive)
            
        Returns:
            List of products within the price range
        """
        return [
            product for product in self._store.values()
            if min_price <= product.price <= max_price
        ]
    
    def find_by_max_weight(self, max_weight_kg: float) -> list[Product]:
        """
        Find products under a maximum weight.
        
        Args:
            max_weight_kg: Maximum weight in kg
            
        Returns:
            List of products under the weight limit
        """
        return [
            product for product in self._store.values()
            if product.weight_kg <= max_weight_kg
        ]
