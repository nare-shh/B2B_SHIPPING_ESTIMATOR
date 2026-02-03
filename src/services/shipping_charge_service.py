"""
Shipping charge service for calculating shipping costs.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from src.entities.warehouse import Warehouse
from src.entities.customer import Customer
from src.entities.product import Product
from src.repositories.warehouse_repository import WarehouseRepository
from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository
from src.services.distance_calculator import DistanceCalculator
from src.services.warehouse_service import WarehouseService
from src.strategies.factory import ShippingStrategyFactory
from src.strategies.base import ShippingCostResult
from src.core.exceptions import NotFoundError, ValidationError


class DeliverySpeed(str, Enum):
    """Supported delivery speed options."""
    STANDARD = "standard"
    EXPRESS = "express"


@dataclass
class DeliveryCost:
    """Delivery speed cost breakdown."""
    base_charge: float
    extra_charge: float
    total: float
    speed: str


@dataclass
class ShippingChargeResult:
    """Complete shipping charge result with detailed breakdown."""
    shipping_charge: float
    distance_km: float
    transport_mode: str
    transport_cost: float
    delivery_cost: DeliveryCost
    weight_kg: float


@dataclass
class TotalShippingResult:
    """Result for total shipping calculation including warehouse info."""
    shipping_charge: float
    nearest_warehouse: Warehouse
    distance_km: float
    breakdown: ShippingChargeResult


class ShippingChargeService:
    """
    Service for calculating shipping charges.
    
    Combines transport mode selection (based on distance) with
    delivery speed charges to calculate the total shipping cost.
    
    Shipping Formula:
        transport_cost = distance × rate × weight
        delivery_cost = base_charge + (extra_per_kg × weight for express)
        total = transport_cost + delivery_cost
    """
    
    # Delivery speed charges
    BASE_COURIER_CHARGE = 10.0  # INR
    EXPRESS_EXTRA_PER_KG = 1.2  # INR per kg
    
    def __init__(
        self,
        warehouse_repo: WarehouseRepository,
        customer_repo: CustomerRepository,
        product_repo: ProductRepository,
        warehouse_service: WarehouseService,
        strategy_factory: Optional[ShippingStrategyFactory] = None
    ):
        """
        Initialize the shipping charge service.
        
        Args:
            warehouse_repo: Repository for warehouse data
            customer_repo: Repository for customer data
            product_repo: Repository for product data
            warehouse_service: Service for warehouse operations
            strategy_factory: Factory for shipping strategies (optional)
        """
        self._warehouse_repo = warehouse_repo
        self._customer_repo = customer_repo
        self._product_repo = product_repo
        self._warehouse_service = warehouse_service
        self._strategy_factory = strategy_factory or ShippingStrategyFactory()
    
    def _validate_delivery_speed(self, speed: str) -> DeliverySpeed:
        """
        Validate and parse delivery speed.
        
        Args:
            speed: The delivery speed string
            
        Returns:
            DeliverySpeed enum value
            
        Raises:
            ValidationError: If speed is not supported
        """
        try:
            return DeliverySpeed(speed.lower())
        except ValueError:
            valid_speeds = [s.value for s in DeliverySpeed]
            raise ValidationError(
                f"Invalid delivery speed '{speed}'. "
                f"Supported speeds: {valid_speeds}"
            )
    
    def _calculate_delivery_cost(
        self,
        speed: DeliverySpeed,
        weight_kg: float
    ) -> DeliveryCost:
        """
        Calculate delivery speed charges.
        
        Standard: 10 INR base
        Express: 10 INR base + 1.2 INR per kg
        
        Args:
            speed: The delivery speed
            weight_kg: Product weight in kg
            
        Returns:
            DeliveryCost with breakdown
        """
        base_charge = self.BASE_COURIER_CHARGE
        extra_charge = 0.0
        
        if speed == DeliverySpeed.EXPRESS:
            extra_charge = self.EXPRESS_EXTRA_PER_KG * weight_kg
        
        return DeliveryCost(
            base_charge=base_charge,
            extra_charge=round(extra_charge, 2),
            total=round(base_charge + extra_charge, 2),
            speed=speed.value
        )
    
    def calculate_from_warehouse(
        self,
        warehouse_id: int,
        customer_id: int,
        product_id: int,
        delivery_speed: str
    ) -> ShippingChargeResult:
        """
        Calculate shipping charge from a specific warehouse to customer.
        
        Args:
            warehouse_id: The warehouse ID
            customer_id: The customer ID
            product_id: The product ID
            delivery_speed: 'standard' or 'express'
            
        Returns:
            ShippingChargeResult with detailed breakdown
            
        Raises:
            NotFoundError: If any entity not found
            ValidationError: If delivery speed is invalid
        """
        # Validate delivery speed
        speed = self._validate_delivery_speed(delivery_speed)
        
        # Get entities
        warehouse = self._warehouse_repo.get_by_id(warehouse_id)
        if not warehouse:
            raise NotFoundError(f"Warehouse with ID {warehouse_id} not found")
        
        customer = self._customer_repo.get_by_id(customer_id)
        if not customer:
            raise NotFoundError(f"Customer with ID {customer_id} not found")
        
        product = self._product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with ID {product_id} not found")
        
        # Calculate distance
        distance_km = DistanceCalculator.calculate(
            warehouse.location,
            customer.location
        )
        
        # Get transport strategy and calculate transport cost
        strategy = self._strategy_factory.get_strategy(distance_km)
        transport_result: ShippingCostResult = strategy.calculate_cost(
            distance_km,
            product.weight_kg
        )
        
        # Calculate delivery speed cost
        delivery_cost = self._calculate_delivery_cost(speed, product.weight_kg)
        
        # Total shipping charge
        total_charge = transport_result.transport_cost + delivery_cost.total
        
        return ShippingChargeResult(
            shipping_charge=round(total_charge, 2),
            distance_km=distance_km,
            transport_mode=transport_result.transport_mode,
            transport_cost=transport_result.transport_cost,
            delivery_cost=delivery_cost,
            weight_kg=product.weight_kg
        )
    
    def calculate_total(
        self,
        seller_id: int,
        customer_id: int,
        product_id: int,
        delivery_speed: str
    ) -> TotalShippingResult:
        """
        Calculate total shipping charge from seller to customer.
        
        This is the main method that:
        1. Finds the nearest warehouse to the seller
        2. Calculates shipping from that warehouse to customer
        3. Returns complete result with warehouse details
        
        Args:
            seller_id: The seller ID
            customer_id: The customer ID
            product_id: The product ID
            delivery_speed: 'standard' or 'express'
            
        Returns:
            TotalShippingResult with shipping charge and warehouse info
            
        Raises:
            NotFoundError: If any entity not found
            ValidationError: If delivery speed is invalid
        """
        # Validate product exists first (for better error messages)
        product = self._product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product with ID {product_id} not found")
        
        # Find nearest warehouse to seller
        nearest_warehouse, seller_to_warehouse_distance = \
            self._warehouse_service.find_nearest_warehouse(seller_id)
        
        # Calculate shipping from warehouse to customer
        shipping_result = self.calculate_from_warehouse(
            warehouse_id=nearest_warehouse.warehouse_id,
            customer_id=customer_id,
            product_id=product_id,
            delivery_speed=delivery_speed
        )
        
        return TotalShippingResult(
            shipping_charge=shipping_result.shipping_charge,
            nearest_warehouse=nearest_warehouse,
            distance_km=shipping_result.distance_km,
            breakdown=shipping_result
        )
