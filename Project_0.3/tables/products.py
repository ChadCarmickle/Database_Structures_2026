# tables/products.py

"""*********************** Products ***********************
Stores all magical items sold by the shop, including books, potions,
 enchanted equipment, scrolls, and other merchandise. Each product 
 includes information such as its name, category, price, and stock availability.

************************************************************************
"""
from tables.supplier import get_all as get_all_supplier
from utils import make_request, print_table
from config import BASE_URL

TABLE = "products"      
ID_FIELD = "PRODUCTSID"  


def get_all():
    print("********************************* Now displaying updated database ********************************* ")
    resp = make_request("GET", f"{BASE_URL}/{TABLE}")
    return resp.json().get("items", []) if resp else []


def get_one(record_id):
    resp = make_request("GET", f"{BASE_URL}/{TABLE}/{record_id}")
    return resp.json() if resp else None


def add_record():
    print("\n--- Add New Record to Transaction Item Table ---")
    print("Columns: supplier_id, Product Name, Product Type, Volume, BasePrice")
    print("(ProductID is auto-generated)\n")

    print("\n**************************************************************************************************************************")
    print("--- Available Products ---")
    supplier = get_all_supplier()
    print_table(supplier)

    print("\n**************************************************************************************************************************\n")


    data = {}
    fields = ["SUPPLIERID", "PRODUCTNAME", "PRODUCTTYPE", "MAGICFIELD", "VOLUME", "BASEPRICE"]
    
    examples = {
        "SUPPLIERID":                    "Example: Sales ID of supplier 1-2",
        "PRODUCTNAME":                   "Example: Mana Potion",
        "PRODUCTTYPE":                   "Example: Potion",
        "MAGICFIELD":                    "Example: Consumable",
        "VOLUME":                        "Example: null if not a book.",
        "BASEPRICE":                     "Exemple: Price of single item."
    }

    for field in fields:
        value = input(f"{field} ({examples[field]}): ").strip()

        if value:
            try:
                if value.isdigit():
                    data[field] = int(value)
                elif "." in value and value.replace(".", "", 1).isdigit():
                    data[field] = float(value)
                else:
                    data[field] = value
            except:
                data[field] = value


    if data:
        resp = make_request("POST", f"{BASE_URL}/{TABLE}/", data)
        if resp:
            print("✅ Record added to customers successfully!")
    else:
        print("No data entered.")

    print("\n********************************* Now displaying updated database ********************************* \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)



def update_record(): 
    try:
        print("Fetching records... Please wait...")
        records = get_all()
        print(f"Found {len(records)} record(s)")
        print_table(records)


        rid = input(f"{ID_FIELD} to update: ").strip()
        existing = get_one(rid)
        if not existing:
            print("Record not found.")
            return
        print("Enter fields to update (type 'done' when finished):")
        data = {k: v for k, v in existing.items() if k != 'links'}
        while True:
            field = input("Field name (or 'done'): ").strip()
            if field.lower() == 'done': 
                break
            value = input("New value: ").strip()
            if value:
                matched_key = next((k for k in data if k.lower() == field.lower()), field)
                data[matched_key] = value
        resp = make_request("PUT", f"{BASE_URL}/{TABLE}/{rid}", data)
        if resp:
            print(f"✅ Record {rid} updated!")
    except Exception as e:
        print(f"⚠️ Error updating record: {e}")

    print("\n********************************* Now displaying updated database ********************************* \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)

def delete_record(): 
    try:
        rid = input(f"{ID_FIELD} to delete: ").strip()
        if input(f"Delete record {rid}? (y/n): ").lower() == 'y':
            resp = make_request("DELETE", f"{BASE_URL}/{TABLE}/{rid}")
            if resp:
                print(f"✅ Record {rid} deleted!")
    except:
        print("Invalid ID")

    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)


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
            add_record()

        elif choice == "3":
            update_record()

        elif choice == "4":
            delete_record() 

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