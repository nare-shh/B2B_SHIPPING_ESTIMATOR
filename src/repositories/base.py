"""
Base repository with generic CRUD operations using in-memory storage.
"""
from typing import TypeVar, Generic, Dict, Optional, List
from abc import ABC, abstractmethod

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository providing CRUD operations with in-memory storage.
    
    This pattern allows easy swapping to a database implementation later
    by changing the storage mechanism while keeping the interface the same.
    """
    
    def __init__(self):
        self._store: Dict[int, T] = {}
    
    @abstractmethod
    def _get_id(self, entity: T) -> int:
        """Extract the ID from an entity. Must be implemented by subclasses."""
        pass
    
    def add(self, entity: T) -> T:
        """
        Add an entity to the store.
        
        Args:
            entity: The entity to add
            
        Returns:
            The added entity
        """
        entity_id = self._get_id(entity)
        self._store[entity_id] = entity
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Retrieve an entity by its ID.
        
        Args:
            entity_id: The unique identifier
            
        Returns:
            The entity if found, None otherwise
        """
        return self._store.get(entity_id)
    
    def get_all(self) -> List[T]:
        """
        Retrieve all entities from the store.
        
        Returns:
            List of all entities
        """
        return list(self._store.values())
    
    def update(self, entity: T) -> Optional[T]:
        """
        Update an existing entity.
        
        Args:
            entity: The entity with updated values
            
        Returns:
            The updated entity if found, None otherwise
        """
        entity_id = self._get_id(entity)
        if entity_id in self._store:
            self._store[entity_id] = entity
            return entity
        return None
    
    def delete(self, entity_id: int) -> bool:
        """
        Delete an entity by its ID.
        
        Args:
            entity_id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        if entity_id in self._store:
            del self._store[entity_id]
            return True
        return False
    
    def exists(self, entity_id: int) -> bool:
        """Check if an entity exists by ID."""
        return entity_id in self._store
    
    def count(self) -> int:
        """Return the total number of entities in the store."""
        return len(self._store)
    
    def clear(self) -> None:
        """Clear all entities from the store."""
        self._store.clear()
