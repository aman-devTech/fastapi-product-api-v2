from sqlalchemy.orm import Session
import app.database_model as database_model
from app.utils.security import hash_password


def get_all(db: Session):
    return db.query(database_model.Product).all()


def get_by_id(db: Session, id: int):
    return db.query(database_model.Product)\
             .filter(database_model.Product.id == id)\
             .first()


def create(db: Session, product):
    new = database_model.Product(**product.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


def update(db: Session, db_product, product):
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    return db_product


def delete(db: Session, db_product):
    db.delete(db_product)
    db.commit()


def search_by_name(db: Session, name: str):
    return db.query(database_model.Product)\
             .filter(database_model.Product.name.contains(name))\
             .all()


def pagination(db: Session, page: int, limit: int):
    skip = (page - 1) * limit

    return db.query(database_model.Product)\
             .offset(skip)\
             .limit(limit)\
             .all()


def filter_by_price(db: Session, min_price: float):
    return db.query(database_model.Product)\
             .filter(database_model.Product.price >= min_price)\
             .all()


# User CRUD functions
def get_user_by_email(db: Session, email: str):
    return db.query(database_model.User).filter(database_model.User.email == email).first()


def create_user(db: Session, user: dict):
    hashed_password = hash_password(user["password"])
    db_user = database_model.User(
        email=user["email"],
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user