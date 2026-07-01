# tables/products.py

"""*********************** Products ***********************
Stores all magical items sold by the shop, including books, potions,
 enchanted equipment, scrolls, and other merchandise. Each product 
 includes information such as its name, category, price, and stock availability.

************************************************************************
"""

from utils import make_request, print_table
from config import BASE_URL

TABLE = "products"      
ID_FIELD = "PRODUCTSID"  


def get_all():
    resp = make_request("GET", f"{BASE_URL}/{TABLE}")
    return resp.json().get("items", []) if resp else []


def get_one(record_id):
    resp = make_request("GET", f"{BASE_URL}/{TABLE}/{record_id}")
    return resp.json() if resp else None


def add():
    print(f"\n--- Add New Record to {TABLE.upper()} ---")
    print("Enter column names (type 'done' when finished)\n")

    data = {}

    while True:
        field = input("Column name (or 'done'): ").strip().upper()

        if field == "DONE":
            break

        value = input("Value: ").strip()

        if value:
            try:
                if value.isdigit():
                    data[field] = int(value)
                elif "." in value:
                    data[field] = float(value)
                else:
                    data[field] = value
            except:
                data[field] = value

    if data:
        resp = make_request("POST", f"{BASE_URL}/{TABLE}/", data)
        if resp:
            print("✅ Record added!")
    else:
        print("No data entered.")


def products_menu():
    while True:
        print(f"\n--- {TABLE.upper()} TABLE ---")
        print("1. List All Records")
        print("2. Add New Record")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. View One Record")
        print("0. Back")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            records = get_all()
            print(f"Found {len(records)} record(s)")
            print_table(records)

        elif choice == "2":
            add()

        elif choice == "3":
            rid = input(f"{ID_FIELD}: ").strip()

            data = {}

            while True:
                field = input("Field (or 'done'): ").strip().upper()

                if field == "DONE":
                    break

                value = input("New value: ").strip()

                if value:
                    data[field] = value

            if data:
                make_request("PUT", f"{BASE_URL}/{TABLE}/{rid}", data)
                print("✅ Updated.")

        elif choice == "4":
            rid = input(f"{ID_FIELD}: ").strip()

            if input("Delete? (y/n): ").lower() == "y":
                make_request("DELETE", f"{BASE_URL}/{TABLE}/{rid}")
                print("✅ Deleted.")

        elif choice == "5":
            rid = input(f"{ID_FIELD}: ").strip()

            record = get_one(rid)

            if record:
                for k, v in record.items():
                    if k != "links":
                        print(f"{k:20}: {v}")

        elif choice == "0":
            break

        else:
            print("Invalid option.")