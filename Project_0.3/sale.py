# tables/sales.py

"""*********************** Sales ***********************
Executes the multi-step "Perform a Sale" transaction. Unlike the other
table modules, this file doesn't manage a single table — it coordinates
several tables together as one logical transaction:

    1. Create a record in salestransaction (the order)
    2. Create one or more records in transactionitem (the line items)
    3. Update inventory to remove the products sold
    4. Update the customer's balance with the order total

If any step fails partway through, we should decide how to handle
rollback/cleanup (to be added once the individual steps are working).

************************************************************************
"""

from tables.customers import get_all as get_all_customers, get_one as get_one_customer
from tables.products import get_all as get_all_products
from tables.inventory import get_all as get_all_inventory
from tables.employees import get_all as get_all_employees

from utils import make_request, print_table, parse_joindate
from config import BASE_URL


def perform_sale():
    print("\n--- Perform a Sale ---")
    print("This will walk you through creating a new sale from start to finish.\n")

    # ---------- Step 1: Create the order (salestransaction) ----------
    print("Available Customers:")
    print_table(get_all_customers())

    customer_id = input("\nCUSTOMERID for this sale: ").strip()

    print("\nAvailable Employees:")
    print_table(get_all_employees())

    employee_id = input("\nEMPLOYEEID handling this sale: ").strip()

    trans_date = input("Transaction date (YYYY-MM-DD): ").strip()
    parsed_date = parse_joindate(trans_date)

    payment_status = input("Payment Status (Paid, Unpaid, Rented): ").strip()
    payment_method = input("Payment Method (Gold, Ledger-wisp): ").strip()
    status = input("Status (Pending, Authorized, Settled, Declined): ").strip()

    order_data = {
        "CUSTOMERID": int(customer_id) if customer_id.isdigit() else customer_id,
        "EMPLOYEEID": int(employee_id) if employee_id.isdigit() else employee_id,
        "TRANSACTIONDATE": parsed_date,
        "PAYMENTSTATUS": payment_status,
        "PAYMENTMETHOD": payment_method,
        "STATUS": status,
        "TOTALAMOUNT": 0,  # placeholder — will update once line items are totaled
    }

    print("\nCreating order...")
    resp = make_request("POST", f"{BASE_URL}/salestransaction/", order_data)

    if not resp:
        print("❌ Failed to create the order. Aborting sale.")
        return

    order_record = resp.json()
    print("✅ Order created!")
    print(f"Order record: {order_record}")
def sales_menu():
    while True:
        print("\n--- SALES ---")
        print("1. Perform a Sale")
        print("0. Back to Table List")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            perform_sale()
        elif choice == "0":
            break
        else:
            print("Invalid option.")