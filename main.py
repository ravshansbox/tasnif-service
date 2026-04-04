from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send
from sqlalchemy.orm import Session

from database import get_db
from models import Group, Product


class CharsetMiddleware:
    """Ensure all JSON responses have charset=utf-8 for Safari compatibility."""
    
    def __init__(self, app: ASGIApp):
        self.app = app
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        async def custom_send(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                # Replace or add Content-Type with charset
                new_headers = []
                charset_set = False
                for name, value in headers:
                    if name.lower() == b"content-type" and b"application/json" in value:
                        if b"charset" not in value:
                            value = value + b"; charset=utf-8"
                        charset_set = True
                    new_headers.append((name, value))
                
                if not charset_set:
                    # Check if we should add it
                    for name, value in new_headers:
                        if name.lower() == b"content-type" and b"application/json" in value:
                            break
                    else:
                        new_headers.append((b"content-type", b"application/json; charset=utf-8"))
                
                message = {**message, "headers": new_headers}
            await send(message)
        
        await self.app(scope, receive, custom_send)


app = FastAPI()
app.add_middleware(CharsetMiddleware)


def product_to_dict(product: Product) -> dict:
    """Convert Product ORM object to dict, excluding SQLAlchemy internals."""
    return {
        "mxik": product.mxik,
        "mxik_name_uz": product.mxik_name_uz,
        "mxik_name_ru": product.mxik_name_ru,
        "mxik_name_lat": product.mxik_name_lat,
        "label_for_check": product.label_for_check,
        "international_code": product.international_code,
        "use_package": product.use_package,
        "created_at": product.created_at,
        "update_at": product.update_at,
        "label": product.label,
        "cash_sale": product.cash_sale,
    }


def group_to_dict(group: Group) -> dict:
    """Convert Group ORM object to dict."""
    return {
        "group_code": group.group_code,
        "name_uz": group.name_uz,
        "name_ru": group.name_ru,
        "name_lat": group.name_lat,
    }


@app.get("/products")
def list_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return [product_to_dict(p) for p in products]


@app.get("/products/{mxik}")
def get_product(mxik: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.mxik == mxik).first()
    if not product:
        return {"error": "Product not found"}
    return product_to_dict(product)


@app.get("/groups")
def list_groups(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    groups = db.query(Group).offset(skip).limit(limit).all()
    return [group_to_dict(g) for g in groups]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
