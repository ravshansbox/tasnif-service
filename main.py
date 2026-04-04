from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import get_db
from models import Group, Product

app = FastAPI()


@app.get("/products")
def list_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()


@app.get("/products/{mxik}")
def get_product(mxik: str, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.mxik == mxik).first()


@app.get("/groups")
def list_groups(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Group).offset(skip).limit(limit).all()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
