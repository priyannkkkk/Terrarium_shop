from flask import Flask, render_template , request , session, redirect, url_for, jsonify
from data import PREMADE_TERRARIUMS, VESSELS, PLANTS, SUBSTRATES 
from datetime import datetime 

app = Flask(__name__)
# --- CRITICAL CONFIGURATION ---
app.secret_key = 'a_very_secret_and_unique_key_for_terranova_2025' 
# ------------------------------

@app.context_processor
def inject_global_vars():
    # --- FINAL PERPETUAL INTRO LOGIC ---
    show_intro = False
    
    # CRITICAL CHECK: Show intro ONLY if the current function being run is 'home'.
    if request.endpoint == 'home' and request.method == 'GET':
        show_intro = True
    # -----------------------------------
    
    cart_count = len(session.get('cart', []))
    
    return {
        'now': datetime.now(), 
        'cart_count': cart_count,
        'show_intro': show_intro
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html', products=PREMADE_TERRARIUMS)

@app.route('/customize')
def customize():
    # Note: data.py lists are no longer strictly needed here, as customize.html uses hardcoded lists.
    return render_template(
        'customize.html',
        vessels=VESSELS,
        plants=PLANTS,
        substrates=SUBSTRATES
    )

# New Route to handle adding premade items to the cart
@app.route('/add-premade-to-cart/<int:item_id>')
def add_premade_to_cart(item_id):
    if 'cart' not in session:
        session['cart'] = []

    # Using the safer lookup based on item_id - 1 (index)
    product_index = item_id - 1
    
    if 0 <= product_index < len(PREMADE_TERRARIUMS):
        product = PREMADE_TERRARIUMS[product_index]
    else:
        # Fallback for unexpected IDs
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
        
        # *** CRITICAL FIX: Tell Flask the mutable session list has changed ***
        session.modified = True 
        
    # --- FIX: Redirect back to the product's anchor for smooth scrolling ---
    # We pass _fragment='product-X' to url_for, which generates a URL like /shop#product-X
    return redirect(url_for('shop', _fragment=f'product-{item_id}'))

from flask import Flask, render_template , request , session, redirect, url_for, jsonify # <-- CRITICAL: Import jsonify

# ... (rest of the file) ...

# --- NEW AJAX ROUTE: Add to Cart without redirect ---
@app.route('/add-premade-to-cart-ajax/<int:item_id>', methods=['POST'])
def add_premade_to_cart_ajax(item_id):
    if 'cart' not in session:
        session['cart'] = []

    # Using the safer lookup based on item_id - 1 (index)
    product_index = item_id - 1
    
    if 0 <= product_index < len(PREMADE_TERRARIUMS):
        product = PREMADE_TERRARIUMS[product_index]
    else:
        # Fallback for unexpected IDs
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
        
        # Return success and the new cart count in JSON format
        return jsonify({
            'success': True, 
            'cart_count': len(session['cart'])
        }), 200
    
    # Return failure if product not found
    return jsonify({'success': False, 'message': 'Product not found'}), 404

# ... (The existing add_premade_to_cart route is no longer strictly needed but can be left for the old 'Buy Now' button if you revert that link later. Let's focus on the AJAX part.)

# --- FIX 2B: New route for 'Buy Now' to redirect to cart ---
@app.route('/buy-now/<int:item_id>')
def buy_now(item_id):
    # Reuse the logic of add-to-cart
    add_premade_to_cart(item_id) 
    
    # Immediately redirect to the cart view for 'Buy Now' UX
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    total = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

# New Route to remove an item from the cart
@app.route('/remove-from-cart/<int:index>')
def remove_from_cart(index):
    if 'cart' in session:
        cart = session['cart']
        if 0 <= index < len(cart):
            cart.pop(index)
            session['cart'] = cart 
            
    return redirect(url_for('view_cart'))

# New Route to clear all items from the cart
@app.route('/clear-cart')
def clear_cart():
    if 'cart' in session:
        session['cart'] = []
        session.modified = True 
    return redirect(url_for('view_cart'))


# Route to handle Customizer form submission and show summary
@app.route('/build-summary', methods=['POST'])
def build_summary():
    
    # --- 1. Define all expected fields ---
    single_fields = ['growing_medium', 'drainage_layer', 'hardscape_stones']
    multi_fields = ['plants[]', 'care[]', 'accessories[]']
    
    all_components = []
    total_price_inr = 0.0 # Price is now accumulated directly in INR
    vessel_name = "Custom Build"
    
    # --- 2. Process Single-Select Fields (Radio Buttons) ---
    for field in single_fields:
        item_data_str = request.form.get(field) 
        
        if not item_data_str:
            return redirect(url_for('customize')) 

        try:
            name, price_str = item_data_str.split('|')
            price_inr = float(price_str)
            
            # Components are stored with their INR price
            all_components.append({'name': name, 'price_inr': price_inr}) 
            total_price_inr += price_inr
            
            if field == single_fields[0]:
                vessel_name = name
                
        except (ValueError, IndexError):
            return redirect(url_for('customize')) 
    
    # --- 3. Process Multi-Select Fields (Checkboxes) ---
    for field in multi_fields:
        multi_items = request.form.getlist(field)
        
        for item_data_str in multi_items:
            try:
                name, price_str = item_data_str.split('|')
                price_inr = float(price_str)
                
                # Components are stored with their INR price
                all_components.append({'name': name, 'price_inr': price_inr})
                total_price_inr += price_inr
                
            except (ValueError, IndexError):
                continue 

    # --- 4. Assemble Final Item Data ---
    
    custom_item = {
        'type': 'custom',
        'components': all_components, 
        'total_price_inr': total_price_inr,
        'name': f"Custom Terrarium: {vessel_name}..."
    }
    
    session['last_custom_build'] = custom_item
    
    # Render the summary page
    return render_template('summary.html', item=custom_item)


# Route to add the CUSTOM item to the cart from the summary page
@app.route('/add-custom-to-cart', methods=['GET'])
def add_custom_to_cart():
    custom_item = session.pop('last_custom_build', None) 
    
    if not custom_item:
        return redirect(url_for('customize')) 

    # Prepare cart item details
    cart_item = {
        'type': custom_item['type'],
        'name': custom_item['name'],
        # Use the stored INR price directly
        'price': custom_item['total_price_inr'], 
        'quantity': 1
    }

    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(cart_item)
    
    session.modified = True
    
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')