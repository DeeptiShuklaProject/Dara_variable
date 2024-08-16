from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Set up the database engine
engine = create_engine(DATABASE_URL)

# Define the Base class
Base = declarative_base()

# Define your models
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    orders = relationship('Order', back_populates='customer')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    order_items = relationship('OrderItem', back_populates='product')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('Customer', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='order_items')

# Create all tables
Base.metadata.create_all(engine)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_sample_data():
    # Create a new session
    session = SessionLocal()
    try:
        # Check for existing customers
        existing_customers = session.query(Customer).all()
        if not existing_customers:
            # Create sample customers
            customer1 = Customer(id=1, name='Customer 1', email='customer1@example.com')
            customer2 = Customer(id=2, name='Customer 2', email='customer2@example.com')

            # Create sample products
            product1 = Product(id=1, name='Product 1', price=1200.99)
            product2 = Product(id=2, name='Product 2', price=699.50)

            # Insert customers and products into the session
            session.add_all([customer1, customer2, product1, product2])
            session.commit()

            # Create sample orders
            order1 = Order(customer_id=customer1.id)
            order2 = Order(customer_id=customer2.id)

            # Add orders to the session and commit to save them
            session.add_all([order1, order2])
            session.commit()

            # Create sample order items
            order_item1 = OrderItem(order_id=order1.id, product_id=product1.id, quantity=1)
            order_item2 = OrderItem(order_id=order2.id, product_id=product2.id, quantity=2)

            # Insert order items into the session
            session.add_all([order_item1, order_item2])
            session.commit()

            print("Data initialized successfully!")
        else:
            print("Data already exists. Skipping initialization.")

    except IntegrityError as e:
        session.rollback()
        print(f"Integrity error occurred: {e}")

    finally:
        # Close the session
        session.close()

# Run the data initialization
add_sample_data()
