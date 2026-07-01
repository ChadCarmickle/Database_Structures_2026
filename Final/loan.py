## tables/loan.py

"""*********************** loan ***********************
Tracks magical items that have been loaned to customers for temporary use.
 It records who borrowed the item, when it was borrowed, its due date,
   return status, and any associated notes.

************************************************************************
"""

from utils import make_request, print_table
from config import BASE_URL

TABLE = "loan"           
ID_FIELD = "LOANID"      

def get_all():
    resp = make_request("GET", f"{BASE_URL}/{TABLE}")
    return resp.json().get("items", []) if resp else []

def get_one(record_id):
    resp = make_request("GET", f"{BASE_URL}/{TABLE}/{record_id}")
    return resp.json() if resp else None

def add_record():
    print(f"\n--- Add New Record to {TABLE.upper()} ---")
    print("Enter fields (type 'done' when finished):\n")

    data = {}
    while True:
        field = input("Field name (or 'done'): ").strip()
        if field.lower() == "done":
            break
        value = input(f"Value for '{field}': ").strip()
        
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
            print(f"✅ Record added to {TABLE.upper()} successfully!")
    else:
        print("No data entered.")

def loan_menu():                     
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
            try:
                rid = input(f"{ID_FIELD} to update: ").strip()
                print("Enter fields to update (type 'done' when finished):")
                data = {}
                while True:
                    field = input("Field name (or 'done'): ").strip()
                    if field.lower() == 'done': break
                    value = input("New value: ").strip()
                    if value:
                        data[field] = value
                if data:
                    resp = make_request("PUT", f"{BASE_URL}/{TABLE}/{rid}", data)
                    if resp:
                        print(f"✅ Record {rid} updated!")
            except:
                print("Invalid input")

        elif choice == "4":
            try:
                rid = input(f"{ID_FIELD} to delete: ").strip()
                if input(f"Delete record {rid}? (y/n): ").lower() == 'y':
                    resp = make_request("DELETE", f"{BASE_URL}/{TABLE}/{rid}")
                    if resp:
                        print(f"✅ Record {rid} deleted!")
            except:
                print("Invalid ID")

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