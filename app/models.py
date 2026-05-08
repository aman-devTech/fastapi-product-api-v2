from pydantic import BaseModel, EmailStr

# 📝 Product request schema (for POST/PUT - no id)
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


# ✅ Product response schema (for GET - includes id)
class Product(ProductCreate):
    id: int

    class Config:
        from_attributes = True   # ✅ must be inside model


# 📥 Data coming from user (request body)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 🔐 Login request schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

