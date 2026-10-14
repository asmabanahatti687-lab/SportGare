import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="SportGear | Sports & Fitness Store",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Sports Theme & UI Polish)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        width: 100%;
        background-color: #f97316;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #ea580c;
        color: white;
    }
    .product-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INITIALIZE SESSION STATE
# ---------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None  # Holds user email if logged in, or role ('admin')

if "cart" not in st.session_state:
    st.session_state.cart = {}  # Format: {product_id: quantity}

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "orders" not in st.session_state:
    st.session_state.orders = []

if "products" not in st.session_state:
    # Initial Mock Database for Products
    st.session_state.products = [
        {"id": 1, "name": "Pro Adjustable Dumbbell Set", "category": "Gym Equipment", "price": 149.99, "stock": 15, "rating": 4.8, "image": "🏋️‍♂️", "desc": "Compact adjustable weights from 5kg to 25kg."},
        {"id": 2, "name": "Heavy-Duty Olympic Barbell", "category": "Gym Equipment", "price": 220.00, "stock": 8, "rating": 4.9, "image": "🏋️", "desc": "Solid steel bar rated for up to 700 lbs."},
        {"id": 3, "name": "Resistance Loop Bands (Pack of 5)", "category": "Fitness Accessories", "price": 19.99, "stock": 45, "rating": 4.6, "image": "🎗️", "desc": "Durable latex bands with varying resistance levels."},
        {"id": 4, "name": "Smart Fitness Tracker Watch", "category": "Fitness Accessories", "price": 79.99, "stock": 20, "rating": 4.5, "image": "⌚", "desc": "Heart rate monitor, sleep tracking, and GPS."},
        {"id": 5, "name": "AirStride Running Shoes", "category": "Sports Shoes", "price": 89.99, "stock": 30, "rating": 4.7, "image": "👟", "desc": "Lightweight mesh upper with responsive cushioning."},
        {"id": 6, "name": "All-Weather Football", "category": "Football Equipment", "price": 29.99, "stock": 25, "rating": 4.4, "image": "⚽", "desc": "Stitched synthetic leather for superior touch."},
        {"id": 7, "name": "English Willow Cricket Bat", "category": "Cricket Equipment", "price": 179.99, "stock": 10, "rating": 4.9, "image": "🏏", "desc": "Grade 1 English willow designed for power strokes."},
        {"id": 8, "name": "Pro Carbon Badminton Racquet", "category": "Badminton Equipment", "price": 65.00, "stock": 18, "rating": 4.6, "image": "🏸", "desc": "Ultra-lightweight frame for high-speed smashes."},
        {"id": 9, "name": "Eco-Friendly Yoga Mat", "category": "Yoga and Exercise Products", "price": 24.99, "stock": 50, "rating": 4.8, "image": "🧘", "desc": "Non-slip texture with extra cushioning thickness."},
        {"id": 10, "name": "Dry-Fit Athletic Training Tee", "category": "Sportswear", "price": 22.50, "stock": 40, "rating": 4.3, "image": "👕", "desc": "Moisture-wicking breathable fabric."}
    ]

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & FILTERS
# ---------------------------------------------------------
st.sidebar.title("⚽ SportGear Hub")

# Authentication status display
if st.session_state.user:
    st.sidebar.success(f"Logged in as: **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
else:
    st.sidebar.info("Guest User")

st.sidebar.markdown("---")
nav_page = st.sidebar.radio("Navigation", ["Home / Catalog", "Shopping Cart", "My Wishlist", "My Orders", "Login / Register", "Admin Dashboard"])

# Catalog Filters in Sidebar (visible on Home)
selected_category = "All"
min_price, max_price = 0.0, 500.0
min_rating = 0.0
search_query = ""

if nav_page == "Home / Catalog":
    st.sidebar.markdown("### 🔍 Filters & Search")
    search_query = st.sidebar.text_input("Search Products", placeholder="e.g., Dumbbells, Cricket...")
    
    categories = ["All"] + list(set([p["category"] for p in st.session_state.products]))
    selected_category = st.sidebar.selectbox("Category", categories)
    
    max_db_price = max([p["price"] for p in st.session_state.products]) if st.session_state.products else 500.0
    min_price, max_price = st.sidebar.slider("Price Range ($)", 0.0, float(max_db_price), (0.0, float(max_db_price)))
    
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.5)

# ---------------------------------------------------------
# PAGE 1: HOME / CATALOG
# ---------------------------------------------------------
if nav_page == "Home / Catalog":
    # Hero Banner
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 2.5rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
            <h1 style="margin:0; font-size: 2.5rem;">🔥 Unleash Your Athletic Potential</h1>
            <p style="font-size: 1.1rem; color: #94a3b8; margin-top: 0.5rem;">Top-tier gym equipment, sportswear, and fitness accessories delivered to your door.</p>
        </div>
    """, unsafe_allow_html=True)

    # Filter Logic
    filtered_products = st.session_state.products
    if search_query:
        filtered_products = [p for p in filtered_products if search_query.lower() in p["name"].lower() or search_query.lower() in p["category"].lower()]
    if selected_category != "All":
        filtered_products = [p for p in filtered_products if p["category"] == selected_category]
    filtered_products = [p for p in filtered_products if min_price <= p["price"] <= max_price and p["rating"] >= min_rating]

    if not filtered_products:
        st.warning("No products found matching your search or filters. Try adjusting your criteria.")
    else:
        st.markdown(f"### Showing Products ({len(filtered_products)})")
        cols = st.cols(3)
        for idx, prod in enumerate(filtered_products):
            col = cols[idx % 3]
            with col:
                st.markdown(f"""
                    <div class="product-card">
                        <div style="font-size: 3rem; text-align: center;">{prod['image']}</div>
                        <h4 style="margin: 0.5rem 0 0.2rem 0;">{prod['name']}</h4>
                        <p style="color: #64748b; font-size: 0.85rem; margin: 0;">{prod['category']}</p>
                        <p style="font-weight: bold; color: #f97316; font-size: 1.2rem; margin: 0.5rem 0;">${prod['price']:.2f}</p>
                        <p style="font-size: 0.85rem; margin: 0;">⭐ {prod['rating']} | Stock: {prod['stock']}</p>
                        <p style="font-size: 0.9rem; color: #334155; margin: 0.5rem 0;">{prod['desc']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🛒 Add Cart", key=f"cart_{prod['id']}"):
                        if prod['stock'] > 0:
                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                            st.success(f"Added {prod['name']} to cart!")
                        else:
                            st.error("Out of stock!")
                with c2:
                    if st.button("❤️ Wishlist", key=f"wish_{prod['id']}"):
                        if prod not in st.session_state.wishlist:
                            st.session_state.wishlist.append(prod)
                            st.success("Added to Wishlist!")
                        else:
                            st.info("Already in Wishlist.")
                st.markdown("---")

# ---------------------------------------------------------
# PAGE 2: SHOPPING CART & CHECKOUT
# ---------------------------------------------------------
elif nav_page == "Shopping Cart":
    st.title("🛒 Your Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your shopping cart is empty. Explore our catalog to add items!")
    else:
        cart_subtotal = 0.0
        for prod_id, qty in list(st.session_state.cart.items()):
            prod = next((p for p in st.session_state.products if p["id"] == prod_id), None)
            if prod:
                item_total = prod["price"] * qty
                cart_subtotal += item_total
                
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                with col1:
                    st.write(f"**{prod['image']} {prod['name']}**")
                    st.caption(f"${prod['price']:.2f} each")
                with col2:
                    new_qty = st.number_input(f"Qty", min_value=1, max_value=prod['stock'], value=qty, key=f"qty_{prod_id}")
                    if new_qty != qty:
                        st.session_state.cart[prod_id] = new_qty
                        st.rerun()
                with col3:
                    st.write(f"**${item_total:.2f}**")
                with col4:
                    if st.button("Remove", key=f"rem_{prod_id}"):
                        del st.session_state.cart[prod_id]
                        st.rerun()
                st.markdown("---")
        
        # Order Summary & Checkout Section
        st.markdown("### Order Summary")
        shipping = 10.0 if cart_subtotal < 100 and cart_subtotal > 0 else 0.0
        tax = cart_subtotal * 0.08
        grand_total = cart_subtotal + shipping + tax
        
        st.write(f"**Subtotal:** ${cart_subtotal:.2f}")
        st.write(f"**Estimated Shipping:** ${shipping:.2f} *(Free over $100)*")
        st.write(f"**Tax (8%):** ${tax:.2f}")
        st.markdown(f"### **Final Total: ${grand_total:.2f}**")
        
        st.markdown("---")
        st.subheader("Secure Checkout")
        with st.form("checkout_form"):
            c1, c2 = st.columns(2)
            with c1:
                cust_name = st.text_input("Full Name", value="John Doe" if st.session_state.user else "")
                cust_email = st.text_input("Email Address", value=st.session_state.user if st.session_state.user else "")
                address = st.text_input("Street Address")
            with c2:
                city = st.text_input("City")
                state = st.text_input("State / Province")
                pin = st.text_input("PIN / Postal Code")
                phone = st.text_input("Contact Phone Number")
            
            payment_method = st.selectbox("Payment Method", ["Credit / Debit Card (Test Mode)", "UPI / NetBanking", "Cash on Delivery (COD)"])
            coupon = st.text_input("Discount Promo Code (Try SPORT20)")
            
            submitted = st.form_submit_button("Place Order Now")
            if submitted:
                discount = 0.2 * grand_total if coupon == "SPORT20" else 0.0
                final_paid = grand_total - discount
                
                # Validation
                if not cust_name or not cust_email or not address or not phone:
                    st.error("Please fill in all required delivery and contact fields.")
                else:
                    # Deduct stock
                    for prod_id, qty in st.session_state.cart.items():
                        for p in st.session_state.products:
                            if p["id"] == prod_id:
                                p["stock"] -= qty
                    
                    order_record = {
                        "order_id": f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "customer": cust_name,
                        "email": cust_email,
                        "items": dict(st.session_state.cart),
                        "total": final_paid,
                        "status": "Processing / Dispatched"
                    }
                    st.session_state.orders.append(order_record)
                    st.session_state.cart = {}  # Clear cart
                    
                    st.success(f"🎉 Order placed successfully! Your Order ID is **{order_record['order_id']}**.")
                    st.balloons()

# ---------------------------------------------------------
# PAGE 3: WISHLIST
# ---------------------------------------------------------
elif nav_page == "My Wishlist":
    st.title("❤️ My Wishlist")
    if not st.session_state.wishlist:
        st.info("Your wishlist is empty.")
    else:
        for idx, prod in enumerate(st.session_state.wishlist):
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.write(f"### {prod['image']} {prod['name']}")
                st.caption(prod['desc'])
            with c2:
                st.write(f"**Price:** ${prod['price']:.2f}")
            with c3:
                if st.button("Remove", key=f"del_wish_{idx}"):
                    st.session_state.wishlist.pop(idx)
                    st.rerun()
            st.markdown("---")

# ---------------------------------------------------------
# PAGE 4: ORDER HISTORY
# ---------------------------------------------------------
elif nav_page == "My Orders":
    st.title("📦 Order History & Tracking")
    if not st.session_state.orders:
        st.info("No past orders found.")
    else:
        for ord in st.session_state.orders:
            with st.container():
                st.markdown(f"""
                    <div style="background: white; padding: 1.2rem; border-radius: 8px; border-left: 5px solid #f97316; margin-bottom: 1rem;">
                        <h4>Order ID: {ord['order_id']}</h4>
                        <p style="margin:0; color: #64748b;">Date: {ord['date']} | Customer: {ord['customer']}</p>
                        <p style="margin:0.3rem 0; font-weight: bold; color: #0f172a;">Total Paid: ${ord['total']:.2f}</p>
                        <span style="background: #e2e8f0; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.85rem;">Status: {ord['status']}</span>
                    </div>
                """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 5: LOGIN / REGISTRATION
# ---------------------------------------------------------
elif nav_page == "Login / Register":
    st.title("🔐 Account Access")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email_in = st.text_input("Email / Username")
            pass_in = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Secure Login")
            
            if login_btn:
                # Demo admin backdoor or standard login validation
                if email_in == "admin@sportgear.com" and pass_in == "admin123":
                    st.session_state.user = "admin@sportgear.com"
                    st.success("Logged in as Administrator!")
                    st.rerun()
                elif email_in and len(pass_in) >= 6:
                    st.session_state.user = email_in
                    st.success(f"Welcome back, {email_in}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials or password too short.")
    
    with tab2:
        with st.form("reg_form"):
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email Address")
            reg_pass = st.text_input("Create Password", type="password")
            reg_cpass = st.text_input("Confirm Password", type="password")
            reg_btn = st.form_submit_button("Create Account")
            
            if reg_btn:
                if reg_pass != reg_cpass:
                    st.error("Passwords do not match.")
                elif len(reg_pass) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif not reg_email or "@" not in reg_email:
                    st.error("Please enter a valid email address.")
                else:
                    st.session_state.user = reg_email
                    st.success("Account successfully created and logged in!")
                    st.rerun()

# ---------------------------------------------------------
# PAGE 6: ADMIN DASHBOARD
# ---------------------------------------------------------
elif nav_page == "Admin Dashboard":
    st.title("⚙️ Admin Management Console")
    
    # Check if admin
    if st.session_state.user != "admin@sportgear.com":
        st.warning("⚠️ Access Denied. Please log in with admin credentials (`admin@sportgear.com` / `admin123`) via the Login page.")
    else:
        st.success("Welcome, Administrator. Full CRUD and inventory management controls active.")
        
        tab_inv, tab_add, tab_all_orders = st.tabs(["Manage Inventory", "Add New Product", "View All Orders"])
        
        with tab_inv:
            st.subheader("Current Stock Inventory")
            for idx, p in enumerate(st.session_state.products):
                c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
                with c1:
                    st.write(f"**{p['image']} {p['name']}**")
                    st.caption(f"Cat: {p['category']}")
                with c2:
                    new_stk = st.number_input("Stock", value=p['stock'], key=f"adm_stk_{p['id']}")
                    if new_stk != p['stock']:
                        p['stock'] = new_stk
                with c3:
                    st.write(f"Price: ${p['price']:.2f}")
                with c4:
                    if st.button("Delete", key=f"adm_del_{p['id']}"):
                        st.session_state.products.pop(idx)
                        st.rerun()
                st.markdown("---")
        
        with tab_add:
            st.subheader("Add New Product to Catalog")
            with st.form("new_prod_form"):
                p_name = st.text_input("Product Name")
                p_cat = st.selectbox("Category", [
                    "Gym Equipment", "Fitness Accessories", "Sports Shoes", 
                    "Sportswear", "Cricket Equipment", "Football Equipment", 
                    "Badminton Equipment", "Yoga and Exercise Products"
                ])
                p_price = st.number_input("Price ($)", min_value=0.01, value=29.99)
                p_stock = st.number_input("Initial Stock Quantity", min_value=1, value=20)
                p_rating = st.slider("Initial Rating", 1.0, 5.0, 4.5)
                p_icon = st.text_input("Emoji Icon", value="🏅")
                p_desc = st.text_area("Product Description")
                
                add_submit = st.form_submit_button("Publish Product")
                if add_submit:
                    if p_name and p_desc:
                        new_id = max([p["id"] for p in st.session_state.products]) + 1 if st.session_state.products else 1
                        new_item = {
                            "id": new_id,
                            "name": p_name,
                            "category": p_cat,
                            "price": p_price,
                            "stock": p_stock,
                            "rating": p_rating,
                            "image": p_icon,
                            "desc": p_desc
                        }
                        st.session_state.products.append(new_item)
                        st.success(f"Product '{p_name}' added successfully!")
                    else:
                        st.error("Please fill in product name and description.")
        
        with tab_all_orders:
            st.subheader("All Customer Orders")
            if not st.session_state.orders:
                st.info("No orders processed yet.")
            else:
                df_orders = pd.DataFrame(st.session_state.orders)....................................................................
                st.dataframe(df_orders, use_container_width=True)..