from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# DATABASE
from database import Base, engine

# MODELS
from models.user import User
from models.product import Product, ProductImage
from models.cart_item import CartItem
from models.order import Order
from models.order_item import OrderItem
from models.cash_flow import CashFlow
from models.employee import Employee
from models.cash_register import CashRegister
from models.sale import Sale, SaleItem
from models.financial_transaction import FinancialTransaction
from models.cash_closing import CashClosing
from models.contact_message import ContactMessage

# ROTAS
from routes.user import router as user_router
from routes.home import router as home_router
from routes.product import router as product_router
from routes.cart import router as cart_router
from routes.admin import router as admin_router
from routes.finance import router as finance_router
from routes.cash_register import router as cash_register_router
from routes import caixa
from routes.caixa import router as caixa_router

from routes.employee import router as employee_router


# ====================================
# APP
# ====================================

app = FastAPI()


# ====================================
# CRIAR TABELAS
# ====================================

Base.metadata.create_all(bind=engine)


# ====================================
# ARQUIVOS ESTÁTICOS
# ====================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ====================================
# ROTAS
# ====================================

app.include_router(home_router)

app.include_router(user_router)

app.include_router(product_router)

app.include_router(cart_router)

app.include_router(admin_router)

app.include_router(employee_router)

app.include_router(finance_router)

app.include_router(cash_register_router)

app.include_router(caixa.router)

app.include_router(caixa_router)