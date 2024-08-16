import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, Customer, Product, Order, OrderItem
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope='module')
def engine():
    # Load the database URL from environment variables
    DATABASE_URL = os.getenv('DATABASE_URL')
    return create_engine(DATABASE_URL)

@pytest.fixture(scope='module')
def tables(engine):
    # Create all tables in the database
    Base.metadata.create_all(engine)
    yield
    # Drop all tables after tests are completed
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine, tables):
    # Create a new database session for a test
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    # Rollback and close the session after each test
    session.rollback()
    session.close()

def test_customer_insertion(session):
    # Insert a customer with the required email field
    customer = Customer(id=1, name='Test Customer', email='test@example.com')
    session.add(customer)
    session.commit()

    # Query the database to verify the insertion
    result = session.query(Customer).filter_by(name='Test Customer').first()
    assert result is not None
    assert result.name == 'Test Customer'
    assert result.email == 'test@example.com'

def test_order_insertion(session):
    # Insert another customer with the required email field
    customer = Customer(id=2, name='Another Customer', email='another@example.com')
    session.add(customer)
    session.commit()

    # Insert an order associated with the customer
    order = Order(customer_id=2)
    session.add(order)
    session.commit()

    # Query the database to verify the order insertion
    result = session.query(Order).filter_by(customer_id=2).first()
    assert result is not None
