# Apple Store Application

A modern, responsive e-commerce application for Apple products built with NiceGUI and FastAPI.

## Features

- 🛍️ **Product Catalog**: Browse Apple products by category
- 🔍 **Search**: Find products quickly with search functionality
- 🛒 **Shopping Cart**: Add products to cart and manage quantities
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔐 **User Authentication**: Secure user registration and login
- 📦 **Order Management**: Place orders and track purchase history
- 🎨 **Modern UI**: Clean, Apple-inspired design with NiceGUI

## Technology Stack

- **Frontend**: NiceGUI (Python-based UI framework)
- **Backend**: FastAPI (Modern Python web framework)
- **Database**: SQLAlchemy V2 with SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic V2 for data validation

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd apple-store
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Open your browser**:
   - Application: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

## Project Structure

```
apple-store/
├── app/
│   ├── core/           # Core application configuration
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic validation schemas
│   ├── services/       # Business logic layer
│   ├── api/           # FastAPI endpoints
│   └── main.py        # NiceGUI frontend application
├── data/              # Database files
├── requirements.txt   # Python dependencies
├── main.py           # Application entry point
└── README.md         # This file
```

## API Endpoints

### Products
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get product details
- `GET /api/categories` - List product categories

### Shopping Cart
- `POST /api/cart/add` - Add item to cart
- `GET /api/cart` - Get cart contents
- `DELETE /api/cart/{item_id}` - Remove item from cart

### Orders
- `POST /api/orders` - Create order from cart
- `GET /api/orders` - Get user order history

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

## Sample Data

The application automatically creates sample data including:
- 5 product categories (iPhone, iPad, Mac, Apple Watch, AirPods)
- 15+ sample products with realistic pricing
- Product descriptions and specifications

## Configuration

Key configuration options in `.env`:

- `DEBUG`: Enable debug mode (True/False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT signing key (change in production!)

## Development

### Adding New Products

1. Use the API endpoints to add new categories and products
2. Or modify the sample data in `app/main.py`

### Customizing the UI

The NiceGUI frontend is in `app/main.py`. Key components:
- `create_header()`: Navigation and search
- `create_product_grid()`: Product display
- `create_cart_dialog()`: Shopping cart interface

### Database Schema

The application uses SQLAlchemy V2 with these main models:
- `User`: Customer accounts
- `Category`: Product categories
- `Product`: Store inventory
- `CartItem`: Shopping cart items
- `Order` & `OrderItem`: Purchase records

## Production Deployment

1. **Set environment variables**:
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-secure-secret-key
   export DATABASE_URL=postgresql://user:pass@localhost/applestore
   ```

2. **Use a production database**:
   - PostgreSQL recommended for production
   - Update `DATABASE_URL` in environment

3. **Run with a production server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.