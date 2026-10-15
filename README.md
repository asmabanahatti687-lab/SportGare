⚽ SportGear – Sports & Fitness E-Commerce Website (Streamlit Edition)
A complete, modern, responsive, and feature-rich SportGear E-Commerce Web Application built using Python and Streamlit for selling sports equipment, fitness accessories, gym products, and sportswear.

🌟 Key Features
Interactive Catalog & Multi-Filtering:

Live search bar by product name or category.

Dynamic category selector (Gym Equipment, Fitness Accessories, Sports Shoes, Sportswear, Cricket, Football, Badminton, Yoga).

Price range slider and minimum star-rating filters.

Shopping Cart & Secure Checkout Simulator:

Quantity management bound to live stock inventory levels.

Automatic subtotal, shipping, and tax calculations.

Promo code support (Try code SPORT20 for a 20% discount).

Mock payment gateway options (Credit/Debit Card, UPI/NetBanking, Cash on Delivery).

User Authentication & Order History:

Customer account creation and login with client-side validation.

Order history tracking showing status badges for past purchases.

Wishlist management.

Admin Management Dashboard:

Secure Admin Role-Based Access Control (admin@sportgear.com / admin123).

Product CRUD operations (Add new products, update stock quantities, remove items).

Overview of all customer orders.

🚀 Installation and Setup Instructions
Follow these steps to run the application locally on your machine:

Prerequisites
Python 3.8 or higher installed on your computer.

pip (Python package manager).

Step 1: Clone or Download the Project
Ensure you have saved your Python application code as app.py in your project folder.

Step 2: Install Dependencies
Open your terminal, command prompt, or IDE terminal and run the following command to install Streamlit and Pandas:

Bash
pip install streamlit pandas
Step 3: Run the Streamlit Application
Execute the following command inside your project directory:

Bash
streamlit run app.py
Step 4: Access the Website
Once running, Streamlit will automatically open your default browser to the local URL (typically http://localhost:8501).

🔐 Testing & Default Credentials
Customer Access: Register a new account via the Login / Register page or browse as a guest.

Administrator Access:

Go to the Login / Register tab.

Enter Email: admin@sportgear.com

Enter Password: admin123

This unlocks the Admin Dashboard tab in the navigation menu to manage inventory and view orders.

📂 Project Structure
Plaintext
sportgear/
│
├── app.py           # Main Streamlit application containing frontend, backend logic, and mock database
└── README.md        # Project documentation and setup guide# SportGare
