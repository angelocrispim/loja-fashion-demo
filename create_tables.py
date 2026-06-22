from database import Base, engine

# importar todos os models
from models.user import User
from models.product import Product, ProductImage
from models.employee import Employee
from models.order import Order
from models.order_item import OrderItem
from models.cash_flow import CashFlow
from models.sale import Sale, SaleItem
from models.financial_transaction import FinancialTransaction
from models.cash_closing import CashClosing

Base.metadata.create_all(bind=engine)

print("✅ Tabelas criadas com sucesso!")