from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    mxik = Column(String, primary_key=True)
    mxik_name_uz = Column(String)
    mxik_name_ru = Column(String)
    mxik_name_lat = Column(String)
    label_for_check = Column(Integer)
    international_code = Column(String)
    use_package = Column(Integer)
    created_at = Column(BigInteger)
    update_at = Column(BigInteger)
    label = Column(Integer)
    cash_sale = Column(Integer)

    packages = relationship("Package", back_populates="product")


class Package(Base):
    __tablename__ = "packages"

    code = Column(Integer, primary_key=True)
    mxik_code = Column(String, ForeignKey("products.mxik"))
    name_uz = Column(String)
    name_ru = Column(String)
    name_lat = Column(String)
    package_type = Column(String)

    product = relationship("Product", back_populates="packages")


class Group(Base):
    __tablename__ = "groups"

    group_code = Column(Integer, primary_key=True)
    name_uz = Column(String)
    name_ru = Column(String)
    name_lat = Column(String)
