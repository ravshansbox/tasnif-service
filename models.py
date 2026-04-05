from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "products"

    mxik: str = Field(primary_key=True)
    mxik_name_uz: Optional[str] = None
    mxik_name_ru: Optional[str] = None
    mxik_name_lat: Optional[str] = None
    label_for_check: Optional[int] = None
    international_code: Optional[str] = None
    use_package: Optional[int] = None
    created_at: Optional[int] = None
    update_at: Optional[int] = None
    label: Optional[int] = None
    cash_sale: Optional[int] = None

    # Relationship to packages
    packages: list["Package"] = Relationship(back_populates="product")


class Package(SQLModel, table=True):
    __tablename__ = "packages"

    code: int = Field(primary_key=True)
    mxik_code: str = Field(foreign_key="products.mxik")
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_lat: Optional[str] = None
    package_type: Optional[str] = None

    # Relationship to product
    product: Optional[Product] = Relationship(back_populates="packages")


class Group(SQLModel, table=True):
    __tablename__ = "groups"

    group_code: int = Field(primary_key=True)
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_lat: Optional[str] = None
