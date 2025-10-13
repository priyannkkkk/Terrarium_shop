import csv
import os

# --- CRITICAL: Function to load data from CSV ---
def load_products_from_csv(file_path):
    """
    Loads product data from the terra.csv format and maps columns
    to the required Flask application keys.
    """
    products = []
    
    # --- MISSING DEFINITION FIX ---
    # Path is RELATIVE to the data.py file. This line calculates the absolute path.
    absolute_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
    # --- END MISSING DEFINITION FIX ---
    
    if not os.path.exists(absolute_path):
        print(f"Error: Product data file not found at {absolute_path}")
        return products

    try:
        with open(absolute_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for index, row in enumerate(reader):
                product_id = index + 1
                try:
                    product = {
                        'id': product_id,
                        # MAPPING: 'Name' -> 'name'
                        'name': row.get('Name', f'Unnamed Product {product_id}').strip(),
                        
                        # MAPPING: 'Sale Price' -> 'price' (The price used in cart/display)
                        'price': float(row.get('Sale Price', '0').replace(',', '').strip()), 
                        
                        # NEW MAPPING: Include original_price for discount display
                        'original_price': float(row.get('Original Price (₹)', '0').replace(',', '').strip()),
                        
                        # MAPPING: 'Short Description' -> 'description'
                        'description': row.get('Short Description', 'A lovely terrarium.').strip(),
                        
                        # MAPPING: 'image_url' -> 'image'
                        'image': row.get('image_url', 'default.jpg').strip()
                    }
                    products.append(product)
                except Exception as e:
                    print(f"Warning: Failed to process row {product_id}. Error: {e}. Skipping.")
            
    except Exception as e:
        print(f"An error occurred while reading the CSV: {e}")

    return products

# --- CENTRALIZED PRODUCT DATA LIST ---
# FIX: Updated file path to the new CSV
CSV_FILE_PATH = 'product_detail/terra.csv' 

PREMADE_TERRARIUMS = load_products_from_csv(CSV_FILE_PATH)

# --- Customization Options (Still hardcoded) ---
VESSELS = [
    {'name': 'Classic Jar (Small)', 'price': 15.00},
    {'name': 'Geometric Glass', 'price': 25.00},
    {'name': 'Open Bowl (Large)', 'price': 30.00}
]

PLANTS = [
    {'name': 'Fittonia (Red)', 'price': 8.00},
    {'name': 'Moss Mat', 'price': 5.00},
    {'name': 'Small Succulent Mix', 'price': 7.50}
]

SUBSTRATES = [
    {'name': 'Drainage Layer + Soil', 'price': 5.00},
    {'name': 'Sand & Grit Mix', 'price': 4.00}
]

# Fallback in case of zero products loaded
if not PREMADE_TERRARIUMS:
    print("WARNING: Using hardcoded fallback products as CSV loading failed or resulted in zero products.")
    PREMADE_TERRARIUMS = [
        {'id': 1, 'name': 'The Misty Rainforest (Fallback)', 'price': 45.00, 'description': 'Lush closed ecosystem. (Fallback Data)', 'image': 'misty.jpg'},
        {'id': 2, 'name': 'Desert Dune (Fallback)', 'price': 35.50, 'description': 'Open terrarium with succulent cacti. (Fallback Data)', 'image': 'desert.jpg'},
    ]