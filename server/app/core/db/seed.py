"""Database seeding utilities"""

from datetime import datetime
import logging
from enum import Enum
from typing import List, Dict, Any, Callable

import bcrypt
from sqlmodel import Session, select

from app.services.order.model import Order, OrderItem, OrderStatus, PaymentStatus
from app.services.product.model import Product, ProductCategory, ProductStatus

from .conn import engine
from .user import Vendor, Shopper, UserStatus

logger = logging.getLogger(__name__)


class SeedProfile(str, Enum):
    """Available seeding profiles"""

    MINIMAL = "minimal"
    TESTING = "testing"
    FULL_DEMO = "full_demo"


def create_password_hash(pswd: str) -> str:
    """Create a password hash from plaintext password"""
    pass_bytes = pswd.encode("utf-8")
    return bcrypt.hashpw(pass_bytes, bcrypt.gensalt()).decode("utf-8")


def get_minimal_vendors() -> List[Vendor]:
    """Return a minimal list of demo vendors"""
    return [
        Vendor(
            name="Tech Galaxy",
            phone_number="+1-555-123-4567",
            email="contact@techgalaxy.com",
            status=UserStatus.ACTIVE,
            rating=4.7,
            bank_info={"bank": "Chase", "account": "XXXX1234"},
            comission=10.0,
            specialty="Electronics",
            password_hash=create_password_hash("techpass123"),
            locations=[
                {
                    "type": "store",
                    "street": "Main Street",
                    "number": "123",
                    "zip_code": "10001",
                    "city": "New York",
                    "state": "NY",
                    "country": "USA",
                }
            ],
        ),
        Vendor(
            name="Fashion Avanue",
            phone_number="+1-555-987-6543",
            email="support@fashionavenue.com",
            status=UserStatus.ACTIVE,
            rating=4.5,
            bank_info={"bank": "Bank of America", "account": "XXXX5678"},
            comission=15.0,
            specialty="Clothing",
            password_hash=create_password_hash("fashion456"),
            locations=[
                {
                    "type": "warehouse",
                    "street": "Commerce Blvd",
                    "number": "789",
                    "zip_code": "90210",
                    "city": "Los Angeles",
                    "state": "CA",
                    "country": "USA",
                }
            ],
        ),
    ]


def get_minimal_shoppers() -> List[Shopper]:
    """Returns a minimal list of demo shoppers"""
    return [
        Shopper(
            name="John Doe",
            phone_number="+1-555-111-2222",
            email="john_doe@example.com",
            status=UserStatus.ACTIVE,
            password_hash=create_password_hash("johndoe123"),
            preferences={"theme": "dark", "notifications": True},
            payment_methods=[
                {"type": "credit_card", "last_four": "1234", "provider": "Visa"}
            ],
            wishlist=[1, 3, 5],
            search_history=["laptop", "smartphone", "headphones"],
            order_history=[10001, 10002],
            locations=[
                {
                    "type": "home",
                    "street": "Maple Avenue",
                    "number": "456",
                    "zip_code": "60007",
                    "city": "Chicago",
                    "state": "IL",
                    "country": "USA",
                }
            ],
        ),
        Shopper(
            name="Jane Smith",
            phone_number="+1-555-333-4444",
            email="jane_smith@example.com",
            status=UserStatus.ACTIVE,
            password_hash=create_password_hash("janesmith456"),
            preferences={"theme": "light", "notifications": False},
            payment_methods=[{"type": "paypal", "email": "jane.smith@example.com"}],
            wishlist=[2, 4],
            search_history=["dress", "shoes", "handbag"],
            order_history=[10003],
            locations=[
                {
                    "type": "work",
                    "street": "Tech Park",
                    "number": "789",
                    "complement": "Suite 200",
                    "zip_code": "94043",
                    "city": "Mountain View",
                    "state": "CA",
                    "country": "USA",
                }
            ],
        ),
    ]


def get_minimal_products() -> List[Product]:
    """Retun a minimal list of products for demo vendors"""
    # Products for Tech Galaxy (vendor_id = 1)
    tech_galaxy_products = [
        Product(
            name="Premium Laptop",
            price=999.99,
            description="High-performance laptop with 16GB RAM and 512GB SSD",
            category=ProductCategory.ELECTRONICS,
            tags=["laptop", "computer", "premium"],
            sku="TG-LAPTOP-001",
            vendor_id=1,  # Tech Galaxy
            rating=4.8,
            stock=25,
            status=ProductStatus.ACTIVE,
            created_at=datetime.utcnow(),
            views_count=120,
            sales_count=17,
            discount_percentage=0.0,
        ),
        Product(
            name="Wireless Earbuds",
            price=89.99,
            description="Noise-cancelling wireless earbuds with 24-hour battery life",
            category=ProductCategory.ELECTRONICS,
            tags=["audio", "earbuds", "wireless"],
            sku="TG-AUDIO-002",
            vendor_id=1,  # Tech Galaxy
            rating=4.5,
            stock=50,
            status=ProductStatus.ACTIVE,
            created_at=datetime.utcnow(),
            views_count=85,
            sales_count=12,
            discount_percentage=5.0,
        ),
        Product(
            name="Smart Watch",
            price=199.99,
            description="Fitness and health tracking smartwatch with heart rate monitor",
            category=ProductCategory.ELECTRONICS,
            tags=["wearable", "fitness", "smartwatch"],
            sku="TG-WATCH-003",
            vendor_id=1,  # Tech Galaxy
            rating=4.6,
            stock=30,
            status=ProductStatus.ACTIVE,
            created_at=datetime.utcnow(),
            views_count=95,
            sales_count=8,
            discount_percentage=0.0,
        ),
    ]

    # Products for Fashion Avenue (vendor_id = 2)
    fashion_avenue_products = [
        Product(
            name="Designer Jeans",
            price=79.99,
            description="Premium denim jeans with modern fit",
            category=ProductCategory.CLOTHING,
            tags=["jeans", "denim", "fashion"],
            sku="FA-JEAN-001",
            vendor_id=2,  # Fashion Avenue
            rating=4.7,
            stock=40,
            status=ProductStatus.ACTIVE,
            created_at=datetime.utcnow(),
            views_count=110,
            sales_count=22,
            discount_percentage=0.0,
        ),
        Product(
            name="Summer Dress",
            price=59.99,
            description="Lightweight floral pattern summer dress",
            category=ProductCategory.CLOTHING,
            tags=["dress", "summer", "floral"],
            sku="FA-DRESS-002",
            vendor_id=2,  # Fashion Avenue
            rating=4.9,
            stock=15,
            status=ProductStatus.ACTIVE,
            created_at=datetime.utcnow(),
            views_count=150,
            sales_count=14,
            discount_percentage=10.0,
        ),
        Product(
            name="Leather Jacket",
            price=149.99,
            description="Classic leather jacket with modern styling",
            category=ProductCategory.CLOTHING,
            tags=["jacket", "leather", "outerwear"],
            sku="FA-JACKET-003",
            vendor_id=2,  # Fashion Avenue
            rating=4.8,
            stock=10,
            status=ProductStatus.ACTIVE,
            created_at=datetime.utcnow(),
            views_count=75,
            sales_count=6,
            discount_percentage=0.0,
        ),
    ]

    # Combine all products
    return tech_galaxy_products + fashion_avenue_products


def get_minimal_orders() -> List[Order]:
    """Return a minimal list of orders for demo data"""
    now = datetime.utcnow()
    week_ago = datetime(now.year, now.month, now.day - 7)

    orders = [
        # Order for John Doe (shopper_id=1)
        Order(
            shopper_id=1,
            status=OrderStatus.CONCLUDED,
            payment_method="credit_card",
            payment_status=PaymentStatus.CONFIRMED,
            delivery_location={
                "type": "home",
                "street": "Maple Avenue",
                "number": "456",
                "zip_code": "60007",
                "city": "Chicago",
                "state": "IL",
                "country": "USA",
            },
            shipping_method="Standard Shipping",
            tracking_number="TN78901234",
            estimated_delivery=datetime.utcnow(),
            subtotal=1089.98,
            tax_amount=108.99,
            shipping_cost=15.00,
            total_value=1213.97,
            created_at=week_ago,
            updated_at=week_ago,
            delivered_at=now,
            items=[],  # Will be populated after creation
        ),
        # Order for Jane Smith (shopper_id=2)
        Order(
            shopper_id=2,
            status=OrderStatus.IN_PROGRESS,
            payment_method="paypal",
            payment_status=PaymentStatus.CONFIRMED,
            delivery_location={
                "type": "work",
                "street": "Tech Park",
                "number": "789",
                "complement": "Suite 200",
                "zip_code": "94043",
                "city": "Mountain View",
                "state": "CA",
                "country": "USA",
            },
            shipping_method="Express Shipping",
            tracking_number="TN45678901",
            estimated_delivery=datetime(now.year, now.month, now.day + 2),
            discount_code="SUMMER10",
            discount_amount=6.00,
            subtotal=59.99,
            tax_amount=5.99,
            shipping_cost=8.50,
            total_value=68.48,
            created_at=now,
            updated_at=now,
            items=[],  # Will be populated after creation
        ),
    ]

    # Create order items
    order_items = [
        # Items for John's order (Premium Laptop and Wireless Earbuds)
        OrderItem(
            order_id=1,
            product_id=1,  # Premium Laptop
            quantity=1,
            unit_price=999.99,
            total_price=999.99,
        ),
        OrderItem(
            order_id=1,
            product_id=2,  # Wireless Earbuds
            quantity=1,
            unit_price=89.99,
            total_price=89.99,
        ),
        # Item for Jane's order (Summer Dress)
        OrderItem(
            order_id=2,
            product_id=5,  # Summer Dress
            quantity=1,
            unit_price=59.99,
            total_price=59.99,
        ),
    ]

    # Associate items with orders
    # Note: SQLModel will handle the bidirectional relationship
    orders[0].items = [order_items[0], order_items[1]]
    orders[1].items = [order_items[2]]

    return orders


# Registry of seed data generators by profile
SEED_REGISTRY: Dict[SeedProfile, Dict[Any, Callable]] = {
    SeedProfile.MINIMAL: {
        Vendor: get_minimal_vendors,
        Shopper: get_minimal_shoppers,
        Product: get_minimal_products,
        Order: get_minimal_orders,
    },
    SeedProfile.TESTING: {
        # To be added
    },
    SeedProfile.FULL_DEMO: {
        # To be added
    },
}


def table_is_empty(session: Session, model) -> bool:
    """Check if a table is empty"""
    return session.exec(select(model)).first() is None


def seed_database(profile: SeedProfile = SeedProfile.MINIMAL):
    """
    Seed the database with initial data if empty

    Args:
        profile: The seeding profile to use. Controls the amount and type of data.
    """

    if profile not in SEED_REGISTRY:
        logger.warning("Seed profile '%s' not found, using MINIMAL instead", profile)
        profile = SeedProfile.MINIMAL

    seed_generators = SEED_REGISTRY[profile]
    if not seed_generators:
        logger.warning("No seed generators found for profile '%s'", profile)

    # Define seeding order to handle relationships correctly
    # Entities with no dependencies come before entities with dependencies
    seeding_order = [Vendor, Shopper, Product, Order]

    with Session(engine) as session:
        for model in seeding_order:
            if model not in seed_generators:
                continue

            generator_function = seed_generators[model]
            model_name = model.__name__

            # Check if table is empty and seed if needed
            if table_is_empty(session, model):
                logger.info("Seeding %s table...", model_name)
                items = generator_function()
                for item in items:
                    session.add(item)
                session.commit()
                logger.info("Added %d %s items", len(items), model_name)
            else:
                logger.info(
                    "%s table already contains data, skipping seeding", model_name
                )

    logger.info("Database seeding complete")
