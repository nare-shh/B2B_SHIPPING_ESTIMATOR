"""
Dependency injection for FastAPI.

This module provides singleton instances of repositories and services
that are injected into API routes.
"""
from functools import lru_cache
from dataclasses import dataclass
from src.repositories import (
    CustomerRepository,
    SellerRepository,
    ProductRepository,
    WarehouseRepository
)
from src.services.warehouse_service import WarehouseService
from src.services.shipping_charge_service import ShippingChargeService
from src.strategies.factory import ShippingStrategyFactory
from src.data.seed import seed_data


@dataclass
class Repositories:
    """Container for all repository instances."""
    customer: CustomerRepository
    seller: SellerRepository
    product: ProductRepository
    warehouse: WarehouseRepository


@dataclass
class Services:
    """Container for all service instances."""
    warehouse: WarehouseService
    shipping_charge: ShippingChargeService


# Singleton instances
_repositories: Repositories | None = None
_services: Services | None = None


def get_repositories() -> Repositories:
    """
    Get the singleton Repositories instance.
    
    Initializes repositories and seeds data on first call.
    
    Returns:
        Repositories container with all repository instances
    """
    global _repositories
    
    if _repositories is None:
        _repositories = Repositories(
            customer=CustomerRepository(),
            seller=SellerRepository(),
            product=ProductRepository(),
            warehouse=WarehouseRepository()
        )
        # Seed initial data
        seed_data(_repositories)
    
    return _repositories


def get_services() -> Services:
    """
    Get the singleton Services instance.
    
    Initializes services on first call.
    
    Returns:
        Services container with all service instances
    """
    global _services
    
    if _services is None:
        repos = get_repositories()
        
        warehouse_service = WarehouseService(
            warehouse_repo=repos.warehouse,
            seller_repo=repos.seller
        )
        
        shipping_charge_service = ShippingChargeService(
            warehouse_repo=repos.warehouse,
            customer_repo=repos.customer,
            product_repo=repos.product,
            warehouse_service=warehouse_service,
            strategy_factory=ShippingStrategyFactory()
        )
        
        _services = Services(
            warehouse=warehouse_service,
            shipping_charge=shipping_charge_service
        )
    
    return _services


def reset_dependencies() -> None:
    """Reset all singleton instances. Useful for testing."""
    global _repositories, _services
    _repositories = None
    _services = None
