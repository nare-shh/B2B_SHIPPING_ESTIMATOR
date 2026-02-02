"""
Seed data for the shipping charge estimator.

This module provides sample data to demonstrate the API functionality.
In production, this would be replaced with database migrations/fixtures.
"""
from src.entities import Customer, Seller, Product, Warehouse, Location
from src.entities.product import Dimensions


def seed_data(repositories) -> None:
    """
    Seed the repositories with sample data.
    
    Creates sample customers, sellers, products, and warehouses
    for demonstration purposes.
    
    Args:
        repositories: The Repositories container
    """
    # ========== WAREHOUSES ==========
    # Major distribution centers across India
    warehouses = [
        Warehouse(
            warehouse_id=1,
            location=Location(lat=19.0760, lng=72.8777),  # Mumbai
            name="Mumbai Central Warehouse"
        ),
        Warehouse(
            warehouse_id=2,
            location=Location(lat=28.7041, lng=77.1025),  # Delhi
            name="Delhi Distribution Center"
        ),
        Warehouse(
            warehouse_id=3,
            location=Location(lat=12.9716, lng=77.5946),  # Bangalore
            name="Bangalore Logistics Hub"
        ),
        Warehouse(
            warehouse_id=4,
            location=Location(lat=22.5726, lng=88.3639),  # Kolkata
            name="Kolkata Warehouse"
        ),
        Warehouse(
            warehouse_id=5,
            location=Location(lat=13.0827, lng=80.2707),  # Chennai
            name="Chennai Shipping Center"
        ),
    ]
    
    for warehouse in warehouses:
        repositories.warehouse.add(warehouse)
    
    # ========== SELLERS (Kirana Stores) ==========
    sellers = [
        Seller(
            seller_id=1,
            name="Sharma General Store",
            location=Location(lat=19.1136, lng=72.8697)  # Andheri, Mumbai
        ),
        Seller(
            seller_id=2,
            name="Kumar Kirana",
            location=Location(lat=28.6139, lng=77.2090)  # Central Delhi
        ),
        Seller(
            seller_id=3,
            name="Bangalore Mart",
            location=Location(lat=12.9352, lng=77.6245)  # Koramangala
        ),
        Seller(
            seller_id=4,
            name="Southern Groceries",
            location=Location(lat=13.0569, lng=80.2425)  # Chennai
        ),
        Seller(
            seller_id=5,
            name="Eastern Provisions",
            location=Location(lat=22.5958, lng=88.2636)  # Howrah, Kolkata
        ),
    ]
    
    for seller in sellers:
        repositories.seller.add(seller)
    
    # ========== CUSTOMERS ==========
    customers = [
        Customer(
            customer_id=1,
            name="Rahul Verma",
            phone="+91-9876543210",
            location=Location(lat=18.5204, lng=73.8567)  # Pune
        ),
        Customer(
            customer_id=2,
            name="Priya Singh",
            phone="+91-9876543211",
            location=Location(lat=26.9124, lng=75.7873)  # Jaipur
        ),
        Customer(
            customer_id=3,
            name="Amit Patel",
            phone="+91-9876543212",
            location=Location(lat=23.0225, lng=72.5714)  # Ahmedabad
        ),
        Customer(
            customer_id=4,
            name="Deepa Nair",
            phone="+91-9876543213",
            location=Location(lat=9.9312, lng=76.2673)  # Kochi
        ),
        Customer(
            customer_id=5,
            name="Suresh Reddy",
            phone="+91-9876543214",
            location=Location(lat=17.3850, lng=78.4867)  # Hyderabad
        ),
    ]
    
    for customer in customers:
        repositories.customer.add(customer)
    
    # ========== PRODUCTS ==========
    products = [
        Product(
            product_id=1,
            name="Rice (5kg Pack)",
            price=350.0,
            weight_kg=5.0,
            dimensions=Dimensions(length=30, width=20, height=10)
        ),
        Product(
            product_id=2,
            name="Cooking Oil (5L)",
            price=650.0,
            weight_kg=4.5,
            dimensions=Dimensions(length=20, width=15, height=30)
        ),
        Product(
            product_id=3,
            name="Wheat Flour (10kg)",
            price=450.0,
            weight_kg=10.0,
            dimensions=Dimensions(length=40, width=25, height=12)
        ),
        Product(
            product_id=4,
            name="Sugar (2kg)",
            price=90.0,
            weight_kg=2.0,
            dimensions=Dimensions(length=20, width=15, height=8)
        ),
        Product(
            product_id=5,
            name="Tea (500g Premium)",
            price=280.0,
            weight_kg=0.5,
            dimensions=Dimensions(length=10, width=8, height=15)
        ),
    ]
    
    for product in products:
        repositories.product.add(product)
