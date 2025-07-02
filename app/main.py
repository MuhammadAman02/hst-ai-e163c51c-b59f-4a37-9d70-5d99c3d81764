"""Main NiceGUI application with Apple Store interface."""

from nicegui import ui, app
from typing import List, Dict, Any, Optional
import requests
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("ui")

# Global state for cart and user
class AppState:
    def __init__(self):
        self.cart_items: List[Dict[str, Any]] = []
        self.current_user: Optional[Dict[str, Any]] = None
        self.selected_category: Optional[int] = None
        self.search_query: str = ""

app_state = AppState()

# API client functions
def api_request(method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """Make API request to backend."""
    base_url = f"http://{settings.host}:{settings.port}{settings.api_prefix}"
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return {"error": str(e)}

def get_categories() -> List[Dict[str, Any]]:
    """Get product categories."""
    result = api_request("GET", "/categories")
    return result if isinstance(result, list) else []

def get_products(category_id: Optional[int] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get products with optional filtering."""
    params = {}
    if category_id:
        params["category_id"] = category_id
    if search:
        params["search"] = search
    
    result = api_request("GET", "/products", params=params)
    return result if isinstance(result, list) else []

def add_to_cart(product_id: int, quantity: int = 1) -> bool:
    """Add product to cart."""
    result = api_request("POST", "/cart/add", json={"product_id": product_id, "quantity": quantity})
    return "error" not in result

def get_cart() -> Dict[str, Any]:
    """Get cart contents."""
    result = api_request("GET", "/cart")
    return result if isinstance(result, dict) else {"items": [], "total_amount": 0, "total_items": 0}

def create_order() -> bool:
    """Create order from cart."""
    result = api_request("POST", "/orders")
    return "error" not in result

# UI Components
def create_header():
    """Create application header."""
    with ui.header().classes('bg-gray-900 text-white shadow-lg'):
        with ui.row().classes('w-full items-center justify-between px-4'):
            # Logo and title
            with ui.row().classes('items-center'):
                ui.icon('apple', size='2rem').classes('text-white mr-2')
                ui.label('Apple Store').classes('text-xl font-bold')
            
            # Search bar
            with ui.row().classes('flex-1 max-w-md mx-8'):
                search_input = ui.input(placeholder='Search products...').classes('flex-1')
                search_input.on('keydown.enter', lambda: search_products(search_input.value))
                ui.button(icon='search', on_click=lambda: search_products(search_input.value)).classes('ml-2')
            
            # Cart and user actions
            with ui.row().classes('items-center'):
                cart_button = ui.button(icon='shopping_cart', on_click=show_cart).classes('mr-4')
                cart_badge = ui.badge('0', color='red').classes('absolute -top-2 -right-2')
                update_cart_badge()

def create_category_sidebar():
    """Create category sidebar."""
    with ui.column().classes('w-64 bg-gray-100 p-4 h-full'):
        ui.label('Categories').classes('text-lg font-bold mb-4')
        
        # All products option
        ui.button('All Products', on_click=lambda: filter_by_category(None)).classes('w-full mb-2 justify-start')
        
        # Category buttons
        categories = get_categories()
        for category in categories:
            ui.button(
                category['name'], 
                on_click=lambda c=category: filter_by_category(c['id'])
            ).classes('w-full mb-2 justify-start')

def create_product_grid(products: List[Dict[str, Any]]):
    """Create product grid display."""
    with ui.grid(columns=4).classes('gap-6 p-6 flex-1'):
        for product in products:
            create_product_card(product)

def create_product_card(product: Dict[str, Any]):
    """Create individual product card."""
    with ui.card().classes('w-full shadow-lg hover:shadow-xl transition-shadow cursor-pointer'):
        # Product image
        if product.get('image_url'):
            ui.image(product['image_url']).classes('w-full h-48 object-cover')
        else:
            with ui.element('div').classes('w-full h-48 bg-gray-200 flex items-center justify-center'):
                ui.icon('image', size='3rem').classes('text-gray-400')
        
        # Product info
        with ui.card_section():
            ui.label(product['name']).classes('text-lg font-semibold mb-2')
            ui.label(f"${product['price']:.2f}").classes('text-xl font-bold text-blue-600 mb-2')
            
            if product.get('description'):
                ui.label(product['description'][:100] + '...' if len(product['description']) > 100 else product['description']).classes('text-gray-600 text-sm mb-4')
            
            # Add to cart button
            ui.button(
                'Add to Cart', 
                icon='add_shopping_cart',
                on_click=lambda p=product: add_product_to_cart(p)
            ).classes('w-full bg-blue-600 text-white hover:bg-blue-700')

def create_cart_dialog():
    """Create cart dialog."""
    cart_data = get_cart()
    
    with ui.dialog() as cart_dialog, ui.card().classes('w-96'):
        ui.label('Shopping Cart').classes('text-xl font-bold mb-4')
        
        if not cart_data['items']:
            ui.label('Your cart is empty').classes('text-gray-500 text-center py-8')
        else:
            # Cart items
            for item in cart_data['items']:
                with ui.row().classes('w-full items-center justify-between mb-4 p-2 border-b'):
                    with ui.column().classes('flex-1'):
                        ui.label(item['product']['name']).classes('font-semibold')
                        ui.label(f"${item['product']['price']:.2f} x {item['quantity']}").classes('text-sm text-gray-600')
                    
                    ui.label(f"${item['product']['price'] * item['quantity']:.2f}").classes('font-bold')
            
            # Total
            ui.separator()
            with ui.row().classes('w-full justify-between items-center mt-4'):
                ui.label('Total:').classes('text-lg font-bold')
                ui.label(f"${cart_data['total_amount']:.2f}").classes('text-xl font-bold text-blue-600')
            
            # Checkout button
            ui.button(
                'Checkout', 
                on_click=lambda: checkout_cart(cart_dialog)
            ).classes('w-full mt-4 bg-green-600 text-white hover:bg-green-700')
        
        ui.button('Close', on_click=cart_dialog.close).classes('w-full mt-2')
    
    return cart_dialog

# Event handlers
def search_products(query: str):
    """Search products by query."""
    app_state.search_query = query
    app_state.selected_category = None
    refresh_products()

def filter_by_category(category_id: Optional[int]):
    """Filter products by category."""
    app_state.selected_category = category_id
    app_state.search_query = ""
    refresh_products()

def add_product_to_cart(product: Dict[str, Any]):
    """Add product to cart."""
    success = add_to_cart(product['id'])
    if success:
        ui.notify(f"Added {product['name']} to cart", type='positive')
        update_cart_badge()
    else:
        ui.notify("Failed to add product to cart", type='negative')

def show_cart():
    """Show cart dialog."""
    cart_dialog = create_cart_dialog()
    cart_dialog.open()

def checkout_cart(dialog):
    """Process checkout."""
    success = create_order()
    if success:
        ui.notify("Order placed successfully!", type='positive')
        update_cart_badge()
        dialog.close()
    else:
        ui.notify("Failed to place order", type='negative')

def update_cart_badge():
    """Update cart item count badge."""
    cart_data = get_cart()
    # This would need to be implemented with proper state management
    # For now, we'll just log the cart count
    logger.info(f"Cart has {cart_data.get('total_items', 0)} items")

def refresh_products():
    """Refresh product display."""
    # This would need to be implemented with proper UI state management
    # For now, we'll just log the refresh action
    logger.info(f"Refreshing products - category: {app_state.selected_category}, search: {app_state.search_query}")

# Main page
@ui.page('/')
def index():
    """Main Apple Store page."""
    ui.colors(primary='#1976d2')
    
    create_header()
    
    with ui.row().classes('w-full h-screen'):
        # Sidebar
        create_category_sidebar()
        
        # Main content
        with ui.column().classes('flex-1'):
            # Welcome section
            with ui.card().classes('w-full mb-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white'):
                with ui.card_section().classes('text-center py-8'):
                    ui.label('Welcome to Apple Store').classes('text-3xl font-bold mb-2')
                    ui.label('Discover the latest Apple products').classes('text-lg')
            
            # Products grid
            products = get_products()
            if products:
                create_product_grid(products)
            else:
                with ui.column().classes('flex-1 items-center justify-center'):
                    ui.label('No products available').classes('text-xl text-gray-500')

# Initialize sample data
def init_sample_data():
    """Initialize sample data for demonstration."""
    try:
        from app.core.database import get_db, create_tables
        from app.models import Category, Product
        from sqlalchemy.orm import Session
        
        # Create tables
        create_tables()
        
        # Add sample data
        with Session(bind=next(get_db()).bind) as db:
            # Check if data already exists
            existing_categories = db.query(Category).first()
            if existing_categories:
                return
            
            # Add categories
            categories = [
                Category(name="iPhone", description="Latest iPhone models", image_url="/static/images/iphone.jpg"),
                Category(name="iPad", description="Powerful tablets for work and play", image_url="/static/images/ipad.jpg"),
                Category(name="Mac", description="Desktop and laptop computers", image_url="/static/images/mac.jpg"),
                Category(name="Apple Watch", description="Smartwatch for health and fitness", image_url="/static/images/watch.jpg"),
                Category(name="AirPods", description="Wireless audio experience", image_url="/static/images/airpods.jpg"),
            ]
            
            for category in categories:
                db.add(category)
            
            db.commit()
            
            # Add products
            products = [
                # iPhones
                Product(name="iPhone 15 Pro", description="The ultimate iPhone with titanium design", price=999.00, category_id=1, stock_quantity=50),
                Product(name="iPhone 15", description="A total powerhouse", price=799.00, category_id=1, stock_quantity=75),
                Product(name="iPhone 14", description="As amazing as ever", price=699.00, category_id=1, stock_quantity=100),
                
                # iPads
                Product(name="iPad Pro 12.9\"", description="The ultimate iPad experience", price=1099.00, category_id=2, stock_quantity=30),
                Product(name="iPad Air", description="Serious performance. Serious fun.", price=599.00, category_id=2, stock_quantity=40),
                Product(name="iPad", description="The colorful, all‑screen iPad", price=329.00, category_id=2, stock_quantity=60),
                
                # Macs
                Product(name="MacBook Pro 16\"", description="Mind-blowing. Head-turning.", price=2499.00, category_id=3, stock_quantity=20),
                Product(name="MacBook Air 15\"", description="Impressively big. Impossibly thin.", price=1299.00, category_id=3, stock_quantity=35),
                Product(name="iMac 24\"", description="Makes a statement. Makes a splash.", price=1299.00, category_id=3, stock_quantity=25),
                
                # Apple Watch
                Product(name="Apple Watch Series 9", description="Smarter. Brighter. Mightier.", price=399.00, category_id=4, stock_quantity=80),
                Product(name="Apple Watch SE", description="A great deal to love.", price=249.00, category_id=4, stock_quantity=100),
                Product(name="Apple Watch Ultra 2", description="Next-level adventure.", price=799.00, category_id=4, stock_quantity=40),
                
                # AirPods
                Product(name="AirPods Pro (2nd gen)", description="Adaptive Audio. Now playing.", price=249.00, category_id=5, stock_quantity=120),
                Product(name="AirPods (3rd gen)", description="All-new design. Breakthrough sound.", price=179.00, category_id=5, stock_quantity=150),
                Product(name="AirPods Max", description="Computational audio. Listen, it's powerful.", price=549.00, category_id=5, stock_quantity=30),
            ]
            
            for product in products:
                db.add(product)
            
            db.commit()
            logger.info("Sample data initialized successfully")
            
    except Exception as e:
        logger.error(f"Failed to initialize sample data: {e}")

# Initialize sample data when module is imported
try:
    init_sample_data()
except Exception as e:
    logger.warning(f"Sample data initialization skipped: {e}")

__all__ = ["index"]