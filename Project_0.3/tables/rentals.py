# tables/rentals.py

"""***********************  rentals ***********************
Stores information about magical items available for rental. 
It records rental periods, associated customers, fees, return dates, 
and the status of each rental to ensure rented items are properly managed.

************************************************************************
"""

from tables.transactionitem import get_all as get_all_transactionitem
from utils import make_request, print_table, parse_joindate
from utils import make_request, print_table
from config import BASE_URL

TABLE = "rentals"           
ID_FIELD = "RENTALSID"      

def get_all():
    resp = make_request("GET", f"{BASE_URL}/{TABLE}")
    return resp.json().get("items", []) if resp else []

def get_one(record_id):
    resp = make_request("GET", f"{BASE_URL}/{TABLE}/{record_id}")
    return resp.json() if resp else None

def add_record():
    print("\n--- Add New Record to Loan Table ---")
    print("Columns:Transaction ID, Rental Start date, Rental Due date, Rental Return date, Rental Rate per day, Late Fee amount.  ")
    print("(LoanID is auto-generated)\n")

    print("Available Transction ID")
    transactionID = get_all_transactionitem()
    print_table(transactionID)
    print() 
    print("\n**************************************************************************************************************************")

    data = {}
    fields = [
        "TRANSACTIONITEMID",
        "RENTALSTARTDATE",
        "RENTALDUEDATE",
        "RENTALRETURNDATE",
        "RENTALRATEPERDAY",
        "LATEFEEAMOUNT",
 
    ]

    examples = {
        "TRANSACTIONITEMID":      "Example: ID of Transction. ",
        "RENTALSTARTDATE":    "Example: Rental start date (YYYY-MM-DD). ",
        "RENTALDUEDATE":      "Example: Rental due date (YYYY-MM-DD). 3 months for standard rental: ",
        "RENTALRETURNDATE":   "Example: Rental Date product returned",
        "RENTALRATEPERDAY":   "Example: Rental rate per day.",
        "LATEFEEAMOUNT":      "Example: Full amount of late fee.",

    }

    for field in fields:
        value = input(f"{field} ({examples[field]}): ").strip()
        if not value:
            continue

        if field in ("RENTALSTARTDATE", "RENTALDUEDATE"):
            parsed = parse_joindate(value)
            if parsed is None:
                print(f"{field} must be a valid date like YYYY-MM-DD")
                return
            data[field] = parsed
            continue

        if field == "RENTALRETURNDATE":
            if value.upper() in ("NULL", "NONE"):
                data[field] = None
            else:
                parsed = parse_joindate(value)
                if parsed is None:
                    print(f"{field} must be a valid date like YYYY-MM-DD or NULL")
                    return
                data[field] = parsed
            continue

        try:
            if value.isdigit():
                data[field] = int(value)
            elif "." in value and value.replace(".", "", 1).isdigit():
                data[field] = float(value)
            else:
                data[field] = value
        except Exception:
            data[field] = value

    if data:
        resp = make_request("POST", f"{BASE_URL}/{TABLE}/", data)
        if resp:
            print("✅ Record added to loan table successfully!")
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

    print("\n********************************* Now displaying updated database ********************************* \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)

def rentals_menu():                     
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