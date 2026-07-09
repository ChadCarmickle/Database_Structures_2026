# tables/inventory.py

"""*********************** Inventory ***********************
Tracks the quantity and location of every product in stock. 
This table helps monitor inventory levels, identify items that
need restocking, and maintain accurate records of available merchandise.

************************************************************************
"""
from tables.products import get_all as get_all_products
from utils import make_request, print_table, parse_joindate
from utils import make_request, print_table
from config import BASE_URL

TABLE = "inventory"           
ID_FIELD = "inventoryID"      

def get_all():
    resp = make_request("GET", f"{BASE_URL}/{TABLE}")
    return resp.json().get("items", []) if resp else []

def get_one(record_id):
    resp = make_request("GET", f"{BASE_URL}/{TABLE}/{record_id}")
    return resp.json() if resp else None

def add_record():
    print("\n--- Add New Record to Inventory Table ---")
    print("Columns: ProductID, LASTADJUSTEDBYEMPLOYEEID, QUANTITYONHAND, REORDERLEVEL, LASTRESTOCKDATE, NOTES	")
    print("(INVENTORYID is auto-generated)\n")

    print("--- Available Products ---")
    products = get_all_products()
    print_table(products)
    print()

    data = {}
    fields = ["PRODUCTID", "LASTADJUSTEDBYEMPLOYEEID", "QUANTITYONHAND", "REORDERLEVEL", "LASTRESTOCKDATE", 
              "NOTES"]
    
    examples = {
        "PRODUCTID":                "Example: Product ID of product: 2 - Health Potion: ",
        "LASTADJUSTEDBYEMPLOYEEID": "Example: Employee ID: Ex-705",
        "QUANTITYONHAND":           "Example: Amt Currently in stock",
        "REORDERLEVEL":             "Example: Amt required to re-order product. 100",
        "LASTRESTOCKDATE":          "Example: Date of last restock. MM/DD/YYYY",
        "NOTES":                    "Example: Short Descrption"
    }

    for field in fields:
        value = input(f"{field} ({examples[field]}): ").strip()

        if value:
            if field == "LASTRESTOCKDATE":
                parsed = parse_joindate(value)
                if parsed:
                    data[field] = parsed
                continue

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
        resp = make_request("POST", f"{BASE_URL}/inventory/", data)
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
        rid = input(f"{ID_FIELD} to update: ").strip()
        print("Fetching record to update...Please Wait...")

        record = get_one(rid)
        if not record:
            print("Record not found.")
            return

        record.pop("links", None)
        
        print("\n")
        print(record.keys())
        print("\n")

        print("Enter fields to update (type 'done' when finished):")

        while True:
            field = input("Field name (or 'done'): ").strip().lower()
            if field == "done":
                break
            if field not in record:
                print("Invalid field name.")
                continue

            value = input("New value: ").strip()
            if value:
                if value.isdigit():
                    record[field] = int(value)
                elif "." in value and value.replace(".", "", 1).isdigit():
                    record[field] = float(value)
                else:
                    record[field] = value

        resp = make_request("PUT", f"{BASE_URL}/{TABLE}/{rid}", record)
        if resp:
            print(f"✅ Record {rid} updated!")
    except Exception as e:
        print(f"Invalid input: {e}")
    
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

    print("\n********************************* Now displaying updated database ********************************* \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)

def inventory_menu():                  
    while True:
        print(f"\n--- {TABLE.upper()} TABLE ---")
        print("1. List All Records")
        print("2. Add New Record")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. View One Record")
        print("0. Back to Table List")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            print("Fetching records... Please wait...")
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
            try:
                rid = input(f"{ID_FIELD}: ").strip()
                record = get_one(rid)
                if record:
                    print("\n--- Record Details ---")
                    for k, v in record.items():
                        if k != 'links':
                            print(f"{k:20}: {v}")
            except:
                print("Invalid ID")

        elif choice == "0":
            break
        else:
            print("Invalid option.")