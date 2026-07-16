# tables/purchaseorder.py

"""*********************** Purchase Order ***********************
Records orders placed with suppliers to replenish inventory. 
Each purchase order tracks which supplier fulfilled the order, 
the order date, total cost, and current order status.

************************************************************************
"""
from tables.supplier import get_all as get_all_supplier
from utils import make_request, print_table, parse_joindate
from config import BASE_URL

TABLE = "purchaseorder"           
ID_FIELD = "PURCHASEORDERID"      

def get_all():
    resp = make_request("GET", f"{BASE_URL}/{TABLE}")
    return resp.json().get("items", []) if resp else []

def get_one(record_id):
    resp = make_request("GET", f"{BASE_URL}/{TABLE}/{record_id}")
    return resp.json() if resp else None

def add_record():
    print("\n--- Add New Record to Transaction Item Table ---")
    print("Columns: SupplierID, Order Date, Delivery Date, Total Amount, Status, Notes")
    print("(PurchaseOrderID is auto-generated)\n")
    print("Available Suppliers")
    supplier = get_all_supplier()
    print_table(supplier)
    print("\n**************************************************************************************************************************")

    data = {}
    fields = ["SUPPLIERID", "ORDERDATE", "DELIVERYDATE", "TOTALAMOUNT", "STATUS", "NOTES" ]
    
    examples = {
        "SUPPLIERID":     "Example: Select the supplier above:",
        "ORDERDATE":      "Example: Date of Supply Ordered: (YYYY-MM-DD) | (MM-DD-YYYY).",
        "DELIVERYDATE":   "Example: Date of Supply Delivered: (YYYY-MM-DD) | (MM-DD-YYYY). (Press Enter if not yet delivered:)",
        "TOTALAMOUNT":    "Example: Total Cost.",
        "STATUS":         "Example: Order Placed, In Transit, Out for Delivery, Delivered.",
        "NOTES":          "Example: Short desc"
    }

    for field in fields:
            value = input(f"{field} ({examples[field]}): ").strip()
            if not value:
                continue

            if field == "ORDERDATE":
                parsed = parse_joindate(value)
                if parsed is None:
                    print(f"{field} must be a valid date like YYYY-MM-DD")
                    return
                data[field] = parsed
                continue

            if field == "DELIVERYDATE":
                if value.upper() in ("NULL", "NONE"):
                    data[field] = None
                else:
                    parsed = parse_joindate(value)
                    if parsed is None:
                        print(f"{field} must be a valid date like YYYY-MM-DD or NULL")
                        return
                    data[field] = parsed
                continue

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
        print(); 


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


def purchaseorder_menu():                     
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