import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlmodel import Session, func, select
from starlette.types import ASGIApp, Receive, Scope, Send

from database import get_session
from models import Group, Product

load_dotenv()

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))


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
                new_headers = []
                charset_set = False
                for name, value in headers:
                    if name.lower() == b"content-type" and b"application/json" in value:
                        if b"charset" not in value:
                            value = value + b"; charset=utf-8"
                        charset_set = True
                    new_headers.append((name, value))

                if not charset_set:
                    for name, value in new_headers:
                        if (
                            name.lower() == b"content-type"
                            and b"application/json" in value
                        ):
                            break
                    else:
                        new_headers.append(
                            (b"content-type", b"application/json; charset=utf-8")
                        )

                message = {**message, "headers": new_headers}
            await send(message)

        await self.app(scope, receive, custom_send)


app = FastAPI()
app.add_middleware(CharsetMiddleware)


@app.get("/products")
def list_products(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    limit = min(limit, 1000)
    statement = select(Product).offset(skip).limit(limit)
    products = session.exec(statement).all()

    total = session.exec(select(func.count(Product.mxik))).one()

    return {
        "data": products,  # SQLModel objects auto-serialize!
        "meta": {
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total,
        },
    }


@app.get("/products/{mxik}")
def get_product(mxik: str, session: Session = Depends(get_session)):
    statement = select(Product).where(Product.mxik == mxik)
    product = session.exec(statement).first()
    if not product:
        return {"error": "Product not found"}
    return product


@app.get("/groups")
def list_groups(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    limit = min(limit, 1000)
    statement = select(Group).offset(skip).limit(limit)
    groups = session.exec(statement).all()

    total = session.exec(select(func.count(Group.group_code))).one()

    return {
        "data": groups,
        "meta": {
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
