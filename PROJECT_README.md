# Inventory Management System

A robust Python-based Inventory Management System that can track different product types, handle stock operations, process sales, and persist data.

## Features

- **Multiple Product Types** - Support for Electronics, Grocery, and Clothing items with type-specific attributes
- **Stock Operations** - Add, sell, restock products with validation
- **Search Functionality** - Search by name or product type
- **Data Persistence** - Save and load inventory data to/from JSON files
- **Expired Product Management** - Track and remove expired grocery items
- **Interactive CLI** - User-friendly command-line interface
- **Custom Exception Handling** - Informative error messages for common issues

## Project Structure

- `product.py` - Contains the abstract Product class and subclasses (Electronics, Grocery, Clothing)
- `inventory.py` - Contains the Inventory class for managing collections of products
- `main.py` - Command-line interface for interacting with the inventory system
- `sample_data.py` - Script to create and save sample inventory data
- `test_inventory.py` - Unit tests for the system

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

1. Clone the repository or download the source code:
```
git clone https://github.com/syeda-hoorain-ali/python-inventory-management-system.git
```

2. Navigate to the project directory:
```
cd python-inventory-management-system
```

### Running the Application

Run the main script to start the interactive CLI:
```
python src/main.py
```

### Loading Sample Data

To create and save sample inventory data:
```
python sample_data.py
```

This creates a `sample_inventory.json` file that you can load from the application's File Operations menu.


## Usage Guide

### Main Menu

The system presents the following options when launched:

1. **Add new product** - Add a new Electronics, Grocery, or Clothing product
2. **Sell product** - Record a sale and reduce stock
3. **Restock product** - Add more units to existing stock
4. **Search/view products** - Search by name or type, or view all products
5. **File operations** - Save or load inventory data from files
6. **Remove expired products** - Remove expired grocery items from inventory
7. **Exit** - Exit the application

### Product Types and Attributes

1. **Electronics**
   - Product ID, Name, Price, Quantity
   - Brand, Warranty (years)

2. **Grocery**
   - Product ID, Name, Price, Quantity
   - Expiry Date
   - Expiration status checked automatically

3. **Clothing**
   - Product ID, Name, Price, Quantity
   - Size, Material

### Data Persistence

The system can save and load inventory data in JSON format. Files are stored in the project directory by default.

## Error Handling

The system includes custom exception handling for common scenarios:

- `InsufficientStockError` - Raised when trying to sell more items than available
- `DuplicateProductError` - Raised when adding a product with an ID that already exists
- `InvalidProductTypeError` - Raised when the product type is invalid or unsupported.
- Various value and format validation errors with helpful messages

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

