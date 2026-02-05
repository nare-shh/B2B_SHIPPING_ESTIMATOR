"""
Customer repository for managing customer data.
"""
from src.repositories.base import BaseRepository
from src.entities.customer import Customer


class CustomerRepository(BaseRepository[Customer]):
    """
    Repository for Customer entities.
    
    Provides CRUD operations for customers with in-memory storage.
    """
    
    def _get_id(self, entity: Customer) -> int:
        """Extract customer_id from Customer entity."""
        return entity.customer_id
    
    def find_by_phone(self, phone: str) -> Customer | None:
        """
        Find a customer by phone number.
        
        Args:
            phone: The phone number to search for
            
        Returns:
            The customer if found, None otherwise
        """
        for customer in self._store.values():
            if customer.phone == phone:
                return customer
        return None
