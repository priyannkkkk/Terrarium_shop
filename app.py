from flask import Flask, render_template , request , session, redirect, url_for, jsonify
from data import PREMADE_TERRARIUMS, VESSELS, PLANTS, SUBSTRATES 
from datetime import datetime 

app = Flask(__name__)
# --- CRITICAL CONFIGURATION ---
app.secret_key = 'a_very_secret_and_unique_key_for_terranova_2025' 
# ------------------------------

# --- CORE LOGIC: Helper function to add premade item to session ---
def _add_premade_item_to_cart_logic(item_id):
    """Handles product lookup and adds the item to the cart session."""
    if 'cart' not in session:
        session['cart'] = []

    # Safe lookup based on index (item_id - 1)
    product_index = item_id - 1
    
    if 0 <= product_index < len(PREMADE_TERRARIUMS):
        product = PREMADE_TERRARIUMS[product_index]
    else:
        # Fallback lookup for unexpected IDs
        product = next((p for p in PREMADE_TERRARIUMS if int(p.get('id', 0)) == item_id), None)

    if product:
        cart_item = {
            'id': product['id'],
            'type': 'premade',
            'name': product['name'],
            'price': product['price'],
            'quantity': 1
        }
        session['cart'].append(cart_item)
        session.modified = True 
        return len(session['cart'])
    
    return len(session.get('cart', [])) # Return current count if product not found

# --- Context Processor ---
@app.context_processor
def inject_global_vars():
    show_intro = (request.endpoint == 'home' and request.method == 'GET')
    cart_count = len(session.get('cart', []))
    
    return {
        'now': datetime.now(), 
        'cart_count': cart_count,
        'show_intro': show_intro
    }

# --- PRIMARY ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html', products=PREMADE_TERRARIUMS)

@app.route('/customize')
def customize():
    return render_template(
        'customize.html',
        vessels=VESSELS,
        plants=PLANTS,
        substrates=SUBSTRATES
    )

@app.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    total = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

# --- PREMADE ITEM MANAGEMENT ---

# 1. AJAX Endpoint (Used by "Add to Cart" button - No Refresh)
@app.route('/add-premade-to-cart-ajax/<int:item_id>', methods=['POST'])
def add_premade_to_cart_ajax(item_id):
    current_count = len(session.get('cart', []))
    new_count = _add_premade_item_to_cart_logic(item_id)
    
    if new_count > current_count:
        return jsonify({'success': True, 'cart_count': new_count}), 200
    
    return jsonify({'success': False, 'message': 'Product not added'}), 400

# 2. Buy Now Endpoint (Used by "Buy Now" button - Redirects to cart)
@app.route('/buy-now/<int:item_id>')
def buy_now(item_id):
    _add_premade_item_to_cart_logic(item_id) 
    return redirect(url_for('view_cart'))

# 3. Non-AJAX Fallback (Used only for redirecting with anchor if AJAX fails)
@app.route('/add-premade-to-cart/<int:item_id>')
def add_premade_to_cart(item_id):
    _add_premade_item_to_cart_logic(item_id) 
    return redirect(url_for('shop', _fragment=f'product-{item_id}')) 

# --- CART MANAGEMENT ---

@app.route('/remove-from-cart/<int:index>')
def remove_from_cart(index):
    if 'cart' in session:
        cart = session['cart']
        if 0 <= index < len(cart):
            cart.pop(index)
            session.modified = True
            
    return redirect(url_for('view_cart'))

@app.route('/clear-cart')
def clear_cart():
    if 'cart' in session:
        session['cart'] = []
        session.modified = True 
    return redirect(url_for('view_cart'))

# Route for the final checkout process
@app.route('/checkout-complete')
def checkout_complete():
    # 1. Clear the cart session to simulate order placement
    if 'cart' in session:
        # We don't use cart.clear() because session['cart'] might not exist
        session['cart'] = []
        session.modified = True 
        
    # 2. Render the Thank You page
    return render_template('thank_you.html')


# --- CUSTOM ITEM MANAGEMENT ---

@app.route('/build-summary', methods=['POST'])
def build_summary():
    single_fields = ['growing_medium', 'drainage_layer', 'hardscape_stones']
    multi_fields = ['plants[]', 'care[]', 'accessories[]']
    
    all_components = []
    total_price_inr = 0.0
    vessel_name = "Custom Build"
    
    for field in single_fields:
        item_data_str = request.form.get(field) 
        if not item_data_str:
            return redirect(url_for('customize')) 
        try:
            name, price_str = item_data_str.split('|')
            price_inr = float(price_str)
            all_components.append({'name': name, 'price_inr': price_inr}) 
            total_price_inr += price_inr
            if field == single_fields[0]:
                vessel_name = name
        except (ValueError, IndexError):
            return redirect(url_for('customize')) 
    
    for field in multi_fields:
        for item_data_str in request.form.getlist(field):
            try:
                name, price_str = item_data_str.split('|')
                price_inr = float(price_str)
                all_components.append({'name': name, 'price_inr': price_inr})
                total_price_inr += price_inr
            except (ValueError, IndexError):
                continue 

    custom_item = {
        'type': 'custom',
        'components': all_components, 
        'total_price_inr': total_price_inr,
        'name': f"Custom Terrarium: {vessel_name}..."
    }
    
    session['last_custom_build'] = custom_item
    return render_template('summary.html', item=custom_item)


@app.route('/add-custom-to-cart', methods=['GET'])
def add_custom_to_cart():
    custom_item = session.pop('last_custom_build', None) 
    
    if not custom_item:
        return redirect(url_for('customize')) 

    cart_item = {
        'type': custom_item['type'],
        'name': custom_item['name'],
        'price': custom_item['total_price_inr'], 
        'quantity': 1
    }

    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(cart_item)
    session.modified = True
    
    return redirect(url_for('view_cart'))


# Note: Add this function below your existing cart routes (e.g., after clear_cart)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')