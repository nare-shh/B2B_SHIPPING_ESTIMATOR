"""
Unit tests for services.
"""
import pytest
from src.services.shipping_charge_service import DeliverySpeed
from src.core.exceptions import NotFoundError, ValidationError


class TestWarehouseService:
    """Test suite for WarehouseService."""
    
    def test_find_nearest_warehouse(self, services, repositories):
        """Test finding nearest warehouse to seller."""
        # Seller 1 is in Andheri, Mumbai
        # Warehouse 1 is in Mumbai Central
        warehouse, distance = services.warehouse.find_nearest_warehouse(seller_id=1)
        
        assert warehouse.warehouse_id == 1  # Mumbai warehouse
        assert 0 < distance < 50  # Should be very close
    
    def test_seller_not_found(self, services):
        """Test error when seller doesn't exist."""
        with pytest.raises(NotFoundError, match="Seller with ID 999 not found"):
            services.warehouse.find_nearest_warehouse(seller_id=999)
    
    def test_get_warehouse(self, services):
        """Test getting warehouse by ID."""
        warehouse = services.warehouse.get_warehouse(warehouse_id=1)
        
        assert warehouse.warehouse_id == 1
        assert warehouse.name == "Mumbai Central Warehouse"
    
    def test_warehouse_not_found(self, services):
        """Test error when warehouse doesn't exist."""
        with pytest.raises(NotFoundError, match="Warehouse with ID 999 not found"):
            services.warehouse.get_warehouse(warehouse_id=999)


class TestShippingChargeService:
    """Test suite for ShippingChargeService."""
    
    def test_calculate_from_warehouse_standard(self, services):
        """Test shipping calculation with standard delivery."""
        result = services.shipping_charge.calculate_from_warehouse(
            warehouse_id=1,  # Mumbai
            customer_id=1,   # Pune (~120 km)
            product_id=1,    # Rice 5kg
            delivery_speed="standard"
        )
        
        assert result.shipping_charge > 0
        assert result.transport_mode == "Truck"  # 100-500km range
        assert result.delivery_cost.speed == "standard"
        assert result.delivery_cost.base_charge == 10.0
        assert result.delivery_cost.extra_charge == 0.0
    
    def test_calculate_from_warehouse_express(self, services):
        """Test shipping calculation with express delivery."""
        result = services.shipping_charge.calculate_from_warehouse(
            warehouse_id=1,
            customer_id=1,
            product_id=1,  # 5kg product
            delivery_speed="express"
        )
        
        assert result.delivery_cost.speed == "express"
        assert result.delivery_cost.base_charge == 10.0
        assert result.delivery_cost.extra_charge == 6.0  # 1.2 * 5kg
    
    def test_invalid_delivery_speed(self, services):
        """Test error for invalid delivery speed."""
        with pytest.raises(ValidationError, match="Invalid delivery speed"):
            services.shipping_charge.calculate_from_warehouse(
                warehouse_id=1,
                customer_id=1,
                product_id=1,
                delivery_speed="instant"  # Not supported
            )
    
    def test_warehouse_not_found(self, services):
        """Test error when warehouse doesn't exist."""
        with pytest.raises(NotFoundError, match="Warehouse with ID 999 not found"):
            services.shipping_charge.calculate_from_warehouse(
                warehouse_id=999,
                customer_id=1,
                product_id=1,
                delivery_speed="standard"
            )
    
    def test_customer_not_found(self, services):
        """Test error when customer doesn't exist."""
        with pytest.raises(NotFoundError, match="Customer with ID 999 not found"):
            services.shipping_charge.calculate_from_warehouse(
                warehouse_id=1,
                customer_id=999,
                product_id=1,
                delivery_speed="standard"
            )
    
    def test_product_not_found(self, services):
        """Test error when product doesn't exist."""
        with pytest.raises(NotFoundError, match="Product with ID 999 not found"):
            services.shipping_charge.calculate_from_warehouse(
                warehouse_id=1,
                customer_id=1,
                product_id=999,
                delivery_speed="standard"
            )
    
    def test_calculate_total(self, services):
        """Test complete shipping calculation."""
        result = services.shipping_charge.calculate_total(
            seller_id=1,     # Mumbai seller
            customer_id=1,   # Pune customer
            product_id=1,    # Rice 5kg
            delivery_speed="standard"
        )
        
        assert result.shipping_charge > 0
        assert result.nearest_warehouse is not None
        assert result.nearest_warehouse.warehouse_id == 1  # Mumbai warehouse
        assert result.breakdown is not None
    
    def test_different_transport_modes(self, services):
        """Test that different distances use different transport modes."""
        # Short distance: Mumbai warehouse to Pune customer (~120 km) = Truck
        result1 = services.shipping_charge.calculate_from_warehouse(
            warehouse_id=1, customer_id=1, product_id=5, delivery_speed="standard"
        )
        assert result1.transport_mode == "Truck"
        
        # Long distance: Mumbai warehouse to Kochi customer (~1350 km) = Aeroplane
        result2 = services.shipping_charge.calculate_from_warehouse(
            warehouse_id=1, customer_id=4, product_id=5, delivery_speed="standard"
        )
        assert result2.transport_mode == "Aeroplane"


class TestDeliverySpeed:
    """Test DeliverySpeed enum."""
    
    def test_standard_value(self):
        """Test standard delivery speed."""
        assert DeliverySpeed.STANDARD.value == "standard"
    
    def test_express_value(self):
        """Test express delivery speed."""
        assert DeliverySpeed.EXPRESS.value == "express"
    
    def test_parse_from_string(self):
        """Test parsing from string."""
        assert DeliverySpeed("standard") == DeliverySpeed.STANDARD
        assert DeliverySpeed("express") == DeliverySpeed.EXPRESS
