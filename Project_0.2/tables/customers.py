# tables/inventory.py

"""*********************** Customers ***********************

    Stores information about customers who shop at The Arcane Keeper. 
It includes personal details, magical specialization, membership level,
discounts, join date, and notes used to manage customer relationships.

************************************************************************
"""

from utils import make_request, print_table, parse_joindate
from config import BASE_URL
import json

TABLE = "customers"           
ID_FIELD = "CUSTOMERID"     

def get_all():
    resp = make_request("GET", f"{BASE_URL}/{TABLE}")
    return resp.json().get("items", []) if resp else []

def get_one(record_id):
    resp = make_request("GET", f"{BASE_URL}/{TABLE}/{record_id}")
    return resp.json() if resp else None

def add_record():
    print("\n--- Add New Record to Customers Table ---")
    print("Columns: FIRSTNAME, LASTNAME, OCCUPATION, MAGICFIELD, JOINDATE, DISCOUNT, MEMBERSHIPLEVEL, NOTES")
    print("(CUSTOMERID is auto-generated)\n")

    data = {}
    fields = ["FIRSTNAME", "LASTNAME", "OCCUPATION", "MAGICFIELD", "JOINDATE", 
              "DISCOUNT", "MEMBERSHIPLEVEL", "NOTES"]

    examples = {
        "FIRSTNAME": "Example: Hank",
        "LASTNAME": "Example: Hill",
        "OCCUPATION": "Example: Merchant",
        "MAGICFIELD": "Example: Fire",
        "JOINDATE": "Example: MM/DD/YYYY | YYYY-MM-DD",
        "DISCOUNT": "Example: 5, 10, 15, 20",
        "MEMBERSHIPLEVEL": "Example: Bronze, Silver, Gold, Platinum",
        "NOTES": "Example: Local Merchant specializes in Illusion Magic."
    }

    for field in fields:
        value = input(f"{field} ({examples[field]}): ").strip()

        if value:
            if field == "JOINDATE":
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
        resp = make_request("POST", f"{BASE_URL}/customers/", data)
        if resp:
            print("✅ Record added to customers successfully!")
    else:
        print("No data entered.")

def customers_menu():                     
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

                record = get_one(rid)
                print("\n")
                print(record.keys())
                print("\n")

                if not record:
                    print("Record not found.")
                    continue

                # Remove the links field (ORDS doesn't want it back)
                record.pop("links", None)

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
                        # Convert numbers if possible
                        if value.isdigit():
                            record[field] = int(value)
                        else:
                            try:
                                record[field] = float(value)
                            except ValueError:
                                if field == "JOINDATE":
                                    parsed = parse_joindate(value)
                                    if parsed:
                                        record[field] = parsed
                                else:
                                    record[field] = value

                resp = make_request("PUT", f"{BASE_URL}/{TABLE}/{rid}", record)

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

                    except Exception as e:
                        print(f"Error: {e}")

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