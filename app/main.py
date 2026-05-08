from fastapi import FastAPI
from app.database import engine
import app.database_model as database_model

from app.routers import product, auth


app = FastAPI()

# Create tables
database_model.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "welcome to the world of tech :)"


# Include routers
app.include_router(product.router)
app.include_router(auth.router)
