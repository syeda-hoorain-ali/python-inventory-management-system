from datetime import date, datetime, timedelta
from product import Electronics, Grocery, Clothing
from inventory import Inventory


def create_sample_inventory():
    """Create and return an inventory with sample products."""
    inventory = Inventory()
    
    # Add some electronics
    inventory.add_product(Electronics("E001", "Smartphone", 699.99, 15, "Apple", 1))
    inventory.add_product(Electronics("E002", "Laptop", 1299.99, 8, "Dell", 2))
    inventory.add_product(Electronics("E003", "Headphones", 149.99, 25, "Sony", 1))
    inventory.add_product(Electronics("E004", "Smart TV", 899.99, 5, "Samsung", 2))
    
    # Add some groceries with different expiry dates
    today = datetime.now().date()
    
    
    a = today + timedelta(days=7)
    
    
    inventory.add_product(Grocery("G001", "Milk", 3.49, 30, today + timedelta(days=7)))
    inventory.add_product(Grocery("G002", "Bread", 2.99, 25, today + timedelta(days=5)))
    inventory.add_product(Grocery("G003", "Eggs", 4.99, 20, today + timedelta(days=14)))
    inventory.add_product(Grocery("G004", "Cheese", 6.99, 15, today + timedelta(days=30)))
    # Add one expired item for testing
    inventory.add_product(Grocery("G005", "Yogurt", 1.99, 10, today - timedelta(days=1)))
    
    # Add some clothing
    inventory.add_product(Clothing("C001", "T-Shirt", 19.99, 50, "M", "Cotton"))
    inventory.add_product(Clothing("C002", "Jeans", 39.99, 30, "L", "Denim"))
    inventory.add_product(Clothing("C003", "Sweater", 49.99, 20, "S", "Wool"))
    inventory.add_product(Clothing("C004", "Jacket", 89.99, 15, "XL", "Polyester"))
    
    return inventory


def save_sample_data():
    """Create sample inventory and save it to a file."""
    inventory = create_sample_inventory()
    inventory.save_to_file("inventory.json")
    print(f"Sample inventory created with {inventory.total_products} products")
    print("Saved to 'inventory.json'")


if __name__ == "__main__":
    save_sample_data() 