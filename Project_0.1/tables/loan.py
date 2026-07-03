## tables/loan.py

"""*********************** loan ***********************
Tracks magical items that have been loaned to customers for temporary use.
 It records who borrowed the item, when it was borrowed, its due date,
   return status, and any associated notes.

************************************************************************
"""
from tables.products import get_all as get_all_products
from tables.employees import get_all as get_all_employees
from tables.customers import get_all as get_all_customers
from tables.transactionitem import get_all as get_all_transactionitem


from utils import make_request, print_table, parse_joindate
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
    print("\n--- Add New Record to Loan Table ---")
    print("Columns: ProductID, EmployeeID, CustomerID, TransactionID, UnitPrice, LoanStartDate, LoanDueDate, LoanReturnDate, Latefee, LatefeeAmount, Status, Notes. ")
    print("(LoanID is auto-generated)\n")

    print("\n**************************************************************************************************************************")
    print("Available Products")
    products = get_all_products()
    print_table(products)

    print("Available Employees")
    employees = get_all_employees()
    print_table(employees)

    print("\nAvailable Customers:")
    customers = get_all_customers()
    print_table(customers)

    print("\nAvailable transaction-items:")
    transactionitem = get_all_transactionitem()
    print_table(transactionitem)
    print("\n**************************************************************************************************************************\n")

    data = {}
    fields = [
        "PRODUCTID",
        "EMPLOYEEID",
        "CUSTOMERID",
        "TRANSACTIONID",
        "UNITPRICE",
        "LOANSTARTDATE",
        "LOANDUEDATE",
        "LOANRETURNDATE",
        "LATEFEE",
        "LATEFEEAMOUNT",
        "STATUS",
        "NOTES",
        "SALESTRANSACTIONID",
        "QUANTITY",
        "DISCOUNT",
    ]

    examples = {
        "PRODUCTID":          "Example: ID of product. ",
        "EMPLOYEEID":         "Example: ID of employee handling the transaction. ",
        "CUSTOMERID":         "Example: ID of customer borrowing/buying. ",
        "TRANSACTIONID":      "Example: Transaction ID (e.g., 1-3). ",
        "UNITPRICE":          "Example: Amount per single item. ",
        "LOANSTARTDATE":      "Example: Loan start date (YYYY-MM-DD). ",
        "LOANDUEDATE":        "Example: Loan due date (YYYY-MM-DD). ",
        "LOANRETURNDATE":    "Example: Loan return date (YYYY-MM-DD) or NULL.",
        "LATEFEE":            "Example: Late fee flag/indicator (e.g., Yes/No or 0/1). ",
        "LATEFEEAMOUNT":      "Example: Late fee total amount (e.g., 10.00). ",
        "STATUS":            "Example: Current status (e.g., Borrowed, Returned, Overdue). ",
        "NOTES":              "Example: Short description/notes. ",
        "SALESTRANSACTIONID": "Example: Sales transaction id. ",
        "QUANTITY":           "Example: Amount being sold (integer). ",
        "DISCOUNT":           "Example: Discount% (e.g., 5 to 20). ",
    }

    for field in fields:
        value = input(f"{field} ({examples[field]}): ").strip()
        if not value:
            continue

        if field in ("LOANSTARTDATE", "LOANDUEDATE"):
            parsed = parse_joindate(value)
            if parsed is None:
                print(f"{field} must be a valid date like YYYY-MM-DD")
                return
            data[field] = parsed
            continue

        if field == "LOANRETURNDATE":
            if value.upper() in ("NULL", "NONE"):
                data[field] = None
            else:
                parsed = parse_joindate(value)
                if parsed is None:
                    print(f"{field} must be a valid date like YYYY-MM-DD or NULL")
                    return
                data[field] = parsed
            continue

        if field == "LATEFEE":
            if value.strip().lower() in ("yes", "y", "1", "true"):
                data[field] = 1
            elif value.strip().lower() in ("no", "n", "0", "false"):
                data[field] = 0
            else:
                print(f"{field} must be Yes/No or 0/1")
                return
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
        resp = make_request("POST", f"{BASE_URL}/loan/", data)
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