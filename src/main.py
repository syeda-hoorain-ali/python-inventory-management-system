import sys
from inventory import Inventory
from utils import add_product_menu, file_operations_menu, get_input, print_header, remove_expired_menu, restock_product_menu, search_menu, sell_product_menu

def main_menu():
    """Main menu of the inventory management system."""
    inventory = Inventory()
    
    while True:
        print_header("Inventory Management System")
        print("1. Add new product")
        print("2. Sell product")
        print("3. Restock product")
        print("4. Search/view products")
        print("5. File operations (save/load)")
        print("6. Remove expired products")
        print("7. Exit")
        
        choice = get_input("\nEnter choice (1-7): ", int, lambda x: 1 <= x <= 7, "Please enter 1-7.")
        
        if choice == 1:
            add_product_menu(inventory)
        elif choice == 2:
            sell_product_menu(inventory)
        elif choice == 3:
            restock_product_menu(inventory)
        elif choice == 4:
            search_menu(inventory)
        elif choice == 5:
            file_operations_menu(inventory)
        elif choice == 6:
            remove_expired_menu(inventory)
        elif choice == 7:
            print("\nThank you for using the Inventory Management System!")
            sys.exit(0)


if __name__ == "__main__":
    main_menu() 
