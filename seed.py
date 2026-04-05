import json
import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine
from models import Product, Package, Group

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL)


def seed():
    with open("data/products.json") as f:
        products_data = json.load(f)

    with open("data/groups.json") as f:
        groups_response = json.load(f)

    with Session(engine) as session:
        # Seed products + packages
        for item in products_data:
            product = Product(
                mxik=item["mxik"],
                mxik_name_uz=item.get("mxikNameUz"),
                mxik_name_ru=item.get("mxikNameRu"),
                mxik_name_lat=item.get("mxikNameLat"),
                label_for_check=item.get("labelForCheck"),
                international_code=item.get("internationalCode"),
                use_package=item.get("usePackage"),
                created_at=item.get("createdAt"),
                update_at=item.get("updateAt"),
                label=item.get("label"),
                cash_sale=item.get("cashSale"),
            )
            session.add(product)

            for pkg in item.get("packages", []):
                package = Package(
                    code=pkg["code"],
                    mxik_code=pkg["mxikCode"],
                    name_uz=pkg.get("nameUz"),
                    name_ru=pkg.get("nameRu"),
                    name_lat=pkg.get("nameLat"),
                    package_type=pkg.get("packageType"),
                )
                session.add(package)

        # Seed groups
        for item in groups_response.get("data", []):
            group = Group(
                group_code=item["groupCode"],
                name_uz=item.get("nameUZ"),
                name_ru=item.get("nameRU"),
                name_lat=item.get("nameLAT"),
            )
            session.add(group)

        session.commit()

    print("Seed complete!")


if __name__ == "__main__":
    seed()
