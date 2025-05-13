class InsufficientStockError(Exception):
    """Exception raised when trying to sell more items than available in stock."""

class DuplicateProductError(Exception):
    """Exception raised when trying to add a product with an ID that already exists."""

class InvalidProductTypeError(Exception):
    """Exception raised when the product type is invalid or unsupported."""

