from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Literal

from src.exceptions import InsufficientStockError


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock
    
   
    def restock(self, amount: int):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._quantity_in_stock += amount

    
    def sell(self, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if quantity > self._quantity_in_stock:
            raise InsufficientStockError(f"Only {self._quantity_in_stock} units available")
        self._quantity_in_stock -= quantity

    
    def get_total_value(self):
        return self._price * self._quantity_in_stock
    
    
    def to_dict(self) -> dict[str, str | float]:
        """Convert product to dictionary for serialization."""
        return {
            "type": self.__class__.__name__,
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock
        }
    
    
    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, new_price: int):
        if new_price <= 0:
            raise ValueError("Price cannot be negative")
        self._price = new_price
    
    @property
    def quantity_in_stock(self):
        return self._quantity_in_stock

    
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    def __repr__(self) -> str:
        return f"Product(product_id={self._product_id}, name={self._name}, price={self._price}, quantity_in_stock={self._quantity_in_stock})"    




class Electronics(Product):
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, brand: str, warranty_years: float):
        super().__init__(product_id, name, price, quantity_in_stock)
        
        self._warranty_years = warranty_years
        self._brand = brand
        
    @property
    def warranty_years(self):
        return self._warranty_years
    
    @property
    def brand(self):
        return self._brand
    
    def to_dict(self) -> dict[str, str | float]:
        data = super().to_dict()
        data.update({
            "brand": self._brand,
            "warranty_years": self._warranty_years
        })
        return data
    
    
    def __str__(self) -> str:
        return f"Product ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}, Available stock: {self._quantity_in_stock}, Brand: {self._brand}, Warranty years: {self._warranty_years:.1f}"
    
    def __repr__(self) -> str:
        return f"Electronic(product_id={self._product_id}, name={self._name}, price={self._price}, quantity_in_stock={self._quantity_in_stock}, brand={self._brand}, warranty_years={self._warranty_years})"




class Grocery(Product):
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, expiry_date: date | str):
        super().__init__(product_id, name, price, quantity_in_stock)

        if isinstance(expiry_date, str):
            self._expiry_date = date.fromisoformat(expiry_date)
            # self._expiry_date = date.strftime(expiry_date, "%Y-%m-%d").date()
        else:
            self._expiry_date = expiry_date
        
    def is_expired(self) -> bool:
        return datetime.now() > self._expiry_date
    
    @property
    def expiry_date(self):
        return self._expiry_date
    
    def to_dict(self) -> dict[str, str | float]:
        data = super().to_dict()
        data.update({
            "expiry_date": self._expiry_date.isoformat(),
        })
        return data
        
    def __str__(self) -> str:
        expiry_date = self._expiry_date.strftime("%d-%m-%Y")
        return f"Product ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}, Available stock: {self._quantity_in_stock}, Expirydate: {expiry_date}"
    
    def __repr__(self) -> str:
        return f"Grocery(product_id={self._product_id}, name={self._name}, price={self._price}, quantity_in_stock={self._quantity_in_stock}, expiry_date={self._expiry_date})"
    
    
class Clothing(Product):
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, size: Literal['S', 'M', 'L', 'XL'], material: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        
        self._size = size
        self._material = material
        
    @property
    def size(self):
        return self._size
    
    @property
    def material(self):
        return self._material
    
    def to_dict(self) -> dict[str, str | float]:
        data = super().to_dict()
        data.update({
            "size": self._size,
            "material": self._material
        })
        return data
        
    def __str__(self) -> str:
        return f"Product ID: {self._product_id}, Name: {self._name}, Price: ${self._price:.2f}, Available stock: {self._quantity_in_stock},  Size: {self._size}, Material: {self._material}"
    
    def __repr__(self) -> str:
        return f"Clothing(product_id={self._product_id}, name={self._name}, price={self._price}, quantity_in_stock={self._quantity_in_stock}, size={self._size}, material={self._material})"
    
