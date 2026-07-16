# tables/employees.py

"""*********************** Employees ***********************
Stores information about employees who work at The Arcane Keeper. 
It keeps track of employee details, job roles, contact information, 
hire dates, and other information needed to manage staff.

************************************************************************
"""

from utils import make_request, print_table
from config import BASE_URL

TABLE = "employees"           
ID_FIELD = "EMPLOYEEID"      

def get_all():
    resp = make_request("GET", f"{BASE_URL}/{TABLE}")
    return resp.json().get("items", []) if resp else []

def get_one(record_id):
    resp = make_request("GET", f"{BASE_URL}/{TABLE}/{record_id}")
    return resp.json() if resp else None

def add_record():
    print("\n--- Add New Record to Employees Table ---")
    print("Columns: FIRSTNAME, LASTNAME, HOURLYRATE, ADDRESS, JOBTITLE, DEPARTMENT, ROLE,")
    print("(EMPLOYEEID is auto-generated)\n")

    data = {}
    fields = ["FIRSTNAME", "LASTNAME", "HOURLYRATE", "ADDRESS", "JOBTITLE", 
              "DEPARTMENT", "ROLE"]
    
    examples = {
        "FIRSTNAME": "Example: John",
        "LASTNAME": "Example: Snow",
        "HOURLYRATE": "Example: 25.0",
        "ADDRESS": "Example: 1212 The Wall",
        "JOBTITLE": "Example: Commander",
        "DEPARTMENT": "Example: Management",
        "ROLE": "Example: Short Descrption"
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
        resp = make_request("POST", f"{BASE_URL}/employees/", data)
        if resp:
            print("✅ Record added to customers successfully!")
    else:
        print("No data entered.")

    print("\n********************************* Now displaying updated database ********************************* \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)

def update_record(): 
    print("\n Now Displaying Records available to update: \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)

    print("\n*********** Enter the column to update in the Employees Table ***********")
    print("(EMPLOYEEID is auto-generated | Link may be left blank. )\n")
    try:
        rid = input(f"{ID_FIELD} to update: ").strip()
        print("Please wait...\n")


        record = get_one(rid)
        print("\n")
        print(record.keys())
        print("\n")

        if not record:
            print("Record not found.")
            return
        
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
                        record[field] = value 
                    except Exception as e:
                        print(f"Invalid input: {e}")

        resp = make_request("PUT", f"{BASE_URL}/{TABLE}/{rid}", record)

        if resp:
            print(f"✅ Record {rid} updated!")

    except:
        print("Invalid input")
    
    print("\n********************************* Now displaying updated database ********************************* \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records) 

def delete_record(): 
    print("\n Now Displaying Records to delete: \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)

    try:
        rid = input(f"\n{ID_FIELD} to delete: ").strip()
        if input(f"Delete record {rid}? (y/n): ").lower() == 'y':
            resp = make_request("DELETE", f"{BASE_URL}/{TABLE}/{rid}")
            if resp:
                print(f"✅ Record {rid} deleted!")
                get_all()
    except:
        print("Invalid ID")

    print("\n********************************* Now displaying updated database ********************************* \n") 
    records = get_all()
    print(f"Found {len(records)} record(s)")
    print_table(records)


def employees_menu():                     
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