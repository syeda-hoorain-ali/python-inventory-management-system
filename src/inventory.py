from datetime import datetime
import json
from src.exceptions import DuplicateProductError, InsufficientStockError
from product import Clothing, Electronics, Grocery, Product


class Inventory:
    """Class to manage a collection of products."""
    def __init__(self):
        self._products: dict[str, Product] = {}  # Dictionary with product_id as key and product object as value
    
    @property
    def total_products(self):
        return len(self._products)
    
    def add_product(self, product: Product):
        """Add a product to the inventory."""
        if product.product_id in self._products:
            raise DuplicateProductError(f"Product with ID {product.product_id} already exists")
        self._products[product.product_id] = product
    
    
    def remove_product(self, product_id: str):
        """Remove a product from the inventory by ID."""
        if product_id not in self._products:
            raise KeyError(f"No product with ID {product_id} exists in inventory")
        del self._products[product_id]
    
    
    def search_by_name(self, name: str) -> list[Product]:
        """Search for products by name (case-insensitive partial match)."""
        return [
            product for product in self._products.values() 
            if name.lower() in product.name.lower()
        ]


    def search_by_type(self, product_type: str) -> list[Product]:
        """Search for products by type."""
        products: list[Product] = []
        
        for product in self._products.values():
            if product.__class__.__name__.lower() == product_type.lower():
                products.append(product)
        
        return products 


    def list_all_products(self) -> list[Product]:
        """Return a list of all products in inventory."""
        return list(self._products.values())
    
    
    def sell_product(self, product_id: str, quantity: int):
        """Sell a given quantity of a product."""
        if product_id not in self._products:
            raise KeyError(f"No product with ID {product_id} exists in inventory")
        
        product = self._products[product_id]
        try:
            remaining = product.sell(quantity)
            return remaining
        except InsufficientStockError as e:
            raise InsufficientStockError(f"Cannot sell product {product.name}: {str(e)}")


    def restock_product(self, product_id: str, quantity: int):
        """Restock a given quantity of a product."""
        if product_id not in self._products:
            raise KeyError(f"No product with ID {product_id} exists in inventory")
        
        product = self._products[product_id]
        return product.restock(quantity)


    def total_inventory_value(self):
        """Calculate the total value of all products in inventory."""
        return sum([product.get_total_value() for product in self._products.values()])

    
    def remove_expired_products(self):
        """Remove all expired grocery products from inventory."""
        expired_products: list[Product] = []
        
        # Find expired products
        for product_id, product in list(self._products.items()):
            if isinstance(product, Grocery) and product.is_expired():
                expired_products.append(product)
                del self._products[product_id]
        
        return expired_products
    
    
    def save_to_file(self, filename: str):
        """Save the inventory to a JSON file."""
        data = [product.to_dict() for product in self._products.values()]
        
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
            

    def load_from_file(self, filename: str):
        """Load inventory from a JSON file."""

        product_classes = {
            "Electronics": Electronics,
            "Clothing": Clothing,
            "Grocery": Grocery,
        }

        try:
            with open(filename, 'r') as file:
                json_products: list[dict] = json.load(file)
            
                # Clear current inventory
                self._products = {}
                
                for product in json_products:
                    product_type = product.pop("type", '')
                    
                    if product_type in product_classes:
                        product_class = product_classes[product_type]
                        
                        if "expiry_date" in product:
                            product["expiry_date"] = datetime.fromisoformat(product['expiry_date'])
                        
                        self.add_product(product_class(**product))
                    else:
                        raise ValueError(f"Unknown product type: {product_type}")
        
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Invalid inventory file format: {str(e)}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found") 
        
               



