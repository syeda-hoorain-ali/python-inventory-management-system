import os
from datetime import datetime, timedelta
from typing import Callable, Literal, Optional
from src.exceptions import DuplicateProductError, InsufficientStockError, InvalidProductTypeError
from product import Electronics, Grocery, Clothing
from inventory import Inventory
from typing import TypeVar, Callable, Optional


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print a formatted header."""
    clear_screen()
    print("=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)
    print()


T = TypeVar('T')

def get_input(
    prompt: str, 
    type_func: Callable[[str], T], 
    validate_func: Optional[Callable[[T], bool]] = None, 
    error_msg: Optional[str] = None
    ) -> T:
    """Get and validate user input."""
    while True:
        try:
            value = type_func(input(prompt))
            if validate_func and not validate_func(value):
                print(error_msg or "Invalid input. Please try again.")
                continue
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid value.")


def add_product_menu(inventory: Inventory):
    """Menu for adding a new product."""
    print_header("Add New Product")
    
    # Product type selection
    print("\nSelect product type:")
    print("1. Electronics")
    print("2. Grocery")
    print("3. Clothing")
    
    product_type = get_input("Enter choice (1-3): ", int, lambda x: 1 <= x <= 3, "Please enter 1, 2, or 3.")
    
    # Common product details
    product_id = get_input("Enter product ID: ", str)
    name = get_input("Enter product name: ", str)
    price = get_input("Enter price: $", float, lambda x: x >= 0, "Price must be non-negative.")
    quantity = get_input("Enter initial quantity: ", int, lambda x: x >= 0, "Quantity must be non-negative.")
    
    try:
        if product_type == 1:
            brand = get_input("Enter brand: ", str)
            warranty = get_input("Enter warranty (years): ", int, lambda x: x >= 0, "Warranty must be non-negative.")
            product = Electronics(product_id, name, price, quantity, brand, warranty)
            
        elif product_type == 2:
            days_to_expiry = get_input("Enter days until expiry: ", int, lambda x: x >= 0, "Days must be non-negative.")
            expiry_date = (datetime.now() + timedelta(days=days_to_expiry)).date()
            product = Grocery(product_id, name, price, quantity, expiry_date)
            
        elif product_type == 3:
            size = get_input("Enter size (S/M/L/XL): ", str, lambda x: x in ['S', 'M', 'L', 'XL'], "Size must be one of S, M, L, XL.")
            material = get_input("Enter material: ", str)
            product = Clothing(product_id, name, price, quantity, size, material)
        
        else:
            raise InvalidProductTypeError("Invalid Product type")
        
        inventory.add_product(product)
        print("\nProduct added successfully!")
        
    except (DuplicateProductError, InvalidProductTypeError) as e:
        print(f"\nError: {e}")
    
    input("\nPress Enter to continue...")


def sell_product_menu(inventory: Inventory):
    """Menu for selling a product."""
    print_header("Sell Product")
    
    # List all products first
    products = inventory.list_all_products()
    if not products:
        print("No products in inventory.")
        input("\nPress Enter to continue...")
        return
    
    print("Available Products:")
    for i, product in enumerate(products, 1):
        print(f"{i}. {product.name} (ID: {product.product_id}) - {product.quantity_in_stock} in stock")
    
    try:
        choice = get_input(f"\nEnter product number (1-{len(products)}): ", 
                           int, lambda x: 1 <= x <= len(products), "Invalid product number.")
        
        product = products[choice-1]
        quantity = get_input(f"Enter quantity to sell (max {product.quantity_in_stock}): ", 
                             int, lambda x: 0 < x <= product.quantity_in_stock, 
                             f"Quantity must be between 1 and {product.quantity_in_stock}.")
        
        remaining = inventory.sell_product(product.product_id, quantity)
        print(f"\nSold {quantity} units of {product.name}. {remaining} units remaining in stock.")
        
    except (KeyError, InsufficientStockError) as e:
        print(f"\nError: {e}")
    
    input("\nPress Enter to continue...")


def restock_product_menu(inventory: Inventory):
    """Menu for restocking a product."""
    print_header("Restock Product")
    
    # List all products first
    products = inventory.list_all_products()
    if not products:
        print("No products in inventory.")
        input("\nPress Enter to continue...")
        return
    
    print("Products:")
    for i, product in enumerate(products, 1):
        print(f"{i}. {product.name} (ID: {product.product_id}) - {product.quantity_in_stock} in stock")
    
    try:
        choice = get_input("\nEnter product number (1-" + str(len(products)) + "): ", 
                           int, lambda x: 1 <= x <= len(products), "Invalid product number.")
        
        product = products[choice-1]
        quantity = get_input("Enter quantity to add: ", int, lambda x: x > 0, "Quantity must be positive.")
        
        new_stock = inventory.restock_product(product.product_id, quantity)
        print(f"\nAdded {quantity} units of {product.name}. New stock level: {new_stock}")
        
    except KeyError as e:
        print(f"\nError: {e}")
    
    input("\nPress Enter to continue...")


def search_menu(inventory: Inventory):
    """Menu for searching products."""
    while True:
        print_header("Search Products")
        print("1. Search by name")
        print("2. Search by product type")
        print("3. List all products")
        print("4. Back to main menu")
        
        choice = get_input("\nEnter choice (1-4): ", int, lambda x: 1 <= x <= 4, "Please enter 1-4.")
        
        if choice == 1:
            search_name(inventory)
        elif choice == 2:
            search_type(inventory)
        elif choice == 3:
            list_all(inventory)
        elif choice == 4:
            break


def search_name(inventory: Inventory):
    """Search products by name."""
    print_header("Search by Name")
    
    name = get_input("Enter name to search: ", str)
    products = inventory.search_by_name(name)
    
    if products:
        print(f"\nFound {len(products)} products matching '{name}':\n")
        for product in products:
            print(str(product))
            print("-" * 30)
    else:
        print(f"\nNo products found matching '{name}'.")
    
    input("\nPress Enter to continue...")


def search_type(inventory: Inventory):
    """Search products by type."""
    print_header("Search by Type")
    
    print("Select product type:")
    print("1. Electronics")
    print("2. Grocery")
    print("3. Clothing")
    
    type_choice = get_input("\nEnter choice (1-3): ", int, lambda x: 1 <= x <= 3, "Please enter 1-3.")
    
    type_name = ["Electronics", "Grocery", "Clothing"][type_choice - 1]
    products = inventory.search_by_type(type_name)
    
    if products:
        print(f"\nFound {len(products)} {type_name} products:\n")
        for product in products:
            print(str(product))
            print("-" * 30)
    else:
        print(f"\nNo {type_name} products found in inventory.")
    
    input("\nPress Enter to continue...")


def list_all(inventory: Inventory):
    """List all products in the inventory."""
    print_header("All Products")
    
    products = inventory.list_all_products()
    
    if products:
        print(f"Total: {len(products)} products\n")
        for product in products:
            print(str(product))
            print("-" * 30)
        
        total_value = inventory.total_inventory_value()
        print(f"\nTotal inventory value: ${total_value:.2f}")
    else:
        print("Inventory is empty.")
    
    input("\nPress Enter to continue...")


def file_operations_menu(inventory):
    """Menu for file operations."""
    while True:
        print_header("File Operations")
        print("1. Save inventory to file")
        print("2. Load inventory from file")
        print("3. Back to main menu")
        
        choice = get_input("\nEnter choice (1-3): ", int, lambda x: 1 <= x <= 3, "Please enter 1-3.")
        
        if choice == 1:
            save_inventory(inventory)
        elif choice == 2:
            load_inventory(inventory)
        elif choice == 3:
            break


def save_inventory(inventory: Inventory):
    """Save inventory to a file."""
    print_header("Save Inventory")
    
    filename = get_input("Enter filename to save (default: inventory.json): ", str)
    if not filename:
        filename = "inventory.json"
    
    if not filename.endswith(".json"):
        filename += ".json"
    
    try:
        inventory.save_to_file(filename)
        print(f"\nInventory saved to {filename} successfully!")
    except Exception as e:
        print(f"\nError saving inventory: {e}")
    
    input("\nPress Enter to continue...")


def load_inventory(inventory: Inventory):
    """Load inventory from a file."""
    print_header("Load Inventory")
    
    filename = get_input("Enter filename to load (default: inventory.json): ", str)
    if not filename:
        filename = "inventory.json"
    
    if not filename.endswith(".json"):
        filename += ".json"
    
    try:
        inventory.load_from_file(filename)
        print(f"\nInventory loaded from {filename} successfully!")
    except FileNotFoundError:
        print(f"\nFile {filename} not found.")
    except ValueError as e:
        print(f"\nError loading inventory: {e}")
    
    input("\nPress Enter to continue...")


def remove_expired_menu(inventory: Inventory):
    """Remove expired grocery products."""
    print_header("Remove Expired Products")
    
    expired = inventory.remove_expired_products()
    
    if expired:
        print(f"Removed {len(expired)} expired products:")
        for product in expired:
            if isinstance(product, Grocery):
                print(f"- {product.name} (expired on {product.expiry_date.strftime('%Y-%m-%d')})")
    else:
        print("No expired products found.")
    
    input("\nPress Enter to continue...")

