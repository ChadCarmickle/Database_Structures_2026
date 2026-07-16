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

from tables.customers import get_all as get_all_customers
from tables.products import get_all as get_all_products
from tables.inventory import get_all as get_all_inventory
from tables.employees import get_all as get_all_employees

from utils import make_request, print_table, parse_joindate
from config import BASE_URL

def perform_sale():
    
    sale_success = True
    print("\n--- Perform a Sale ---")
    print("This will walk you through creating a new sale from start to finish.\n")


    # ---------- Step 1: Create the order (SALESTRANSACTION) ----------

    print("Available Customers:")
    print_table(get_all_customers())

    customer_id = input("\nCUSTOMERID for this sale: ").strip()

    customers = get_all_customers()

    customer_record = None

    for customer in customers:
        if int(customer["customerid"]) == int(customer_id):
            customer_record = customer
            break

    if not customer_record:
        print("❌ Customer not found.")
        return


    print("\nAvailable Employees:")
    print_table(get_all_employees())

    employee_id = input("\nEMPLOYEEID handling this sale: ").strip()


    trans_date = input("Transaction date (YYYY-MM-DD): ").strip()
    parsed_date = parse_joindate(trans_date)

    payment_status = input("Payment Status (Paid, Unpaid, Rented): ").strip()
    payment_method = input("Payment Method (Gold, Ledger-wisp): ").strip()
    status = input("Status (Pending, Authorized, Settled, Declined): ").strip()


    order_data = {
        "CUSTOMERID": int(customer_id),
        "EMPLOYEEID": int(employee_id),
        "TRANSACTIONDATE": parsed_date,
        "PAYMENTSTATUS": payment_status,
        "PAYMENTMETHOD": payment_method,
        "STATUS": status,
        "TOTALAMOUNT": 0
    }


    print("\nCreating order...")

    resp = make_request(
        "POST",
        f"{BASE_URL}/salestransaction/",
        order_data
    )


    if not resp:
        print("❌ Failed to create the order. Aborting sale.")
        return


    order_record = resp.json()

    transaction_id = order_record["transactionid"]

    print("✅ Order created!")
    print(f"Transaction ID: {transaction_id}")



    # ---------- Step 2: Add products to TRANSACTIONITEM ----------

    print("\nAvailable Products:")
    products = get_all_products()
    print_table(products)


    product_id = input("\nPRODUCTID being purchased: ").strip()
    quantity = int(input("Quantity: "))


    # Find product price
    unit_price = 0

    for product in products:
        if int(product["productid"]) == int(product_id):
            unit_price = float(product["baseprice"])
            break


    if unit_price == 0:
        print("❌ Product not found.")
        return

    # Apply customer discount
    discount = float(customer_record.get("discount", 0) or 0)

    # Calculate totals
    line_total = quantity * unit_price * (1 - discount / 100)

    total_amount = line_total


    item_data = {
        "SALESTRANSACTIONID": transaction_id,
        "PRODUCTID": int(product_id),
        "QUANTITY": quantity,
        "UNITPRICE": unit_price,
        "DISCOUNT": discount,
        "LINETOTAL": line_total
    }


    print("\nAdding item...")


    item_resp = make_request(
        "POST",
        f"{BASE_URL}/transactionitem/",
        item_data
    )


    if not item_resp:
        print("❌ Failed to add transaction item.")
        return


    print("✅ Product added to sale!")



    # ---------- Step 3: Update Inventory ----------

    print("\nUpdating inventory...")


    inventory = get_all_inventory()

    inventory_found = False

    for item in inventory:

        if str(item["productid"]) == str(product_id):

            inventory_found = True

            current_quantity = int(item["quantityonhand"])
            new_quantity = current_quantity - quantity


            if new_quantity < 0:
                print("❌ Not enough inventory.")
                return


            inventory_id = item["inventoryid"]


            inventory_update = {
                "INVENTORYID": inventory_id,
                "PRODUCTID": item["productid"],
                "LASTADJUSTEDBYEMPLOYEEID": employee_id,
                "QUANTITYONHAND": new_quantity,
                "REORDERLEVEL": item["reorderlevel"],
                "LASTRESTOCKDATE": item["lastrestockdate"],
                "NOTES": item["notes"]
            }


            resp = make_request(
                "PUT",
                f"{BASE_URL}/inventory/{inventory_id}",
                inventory_update
            )


            if resp:
                print("✅ Inventory updated!")
            else:
                print("❌ Inventory update failed.")
                sale_success = False


            break
    if not inventory_found:
        print("❌ Product not found in inventory.")
        sale_success = False



    # ---------- Step 4: Update Sale Total ----------


    sale_update = {
        "TOTALAMOUNT": total_amount
    }


    resp = make_request(
        "PUT",
        f"{BASE_URL}/salestransaction/{transaction_id}",
        sale_update
    )


    if resp:
        print(f"✅ Sale total updated: ${total_amount:.2f}")
    else:
        print("❌ Sale total update failed.")
        sale_success = False



    # ---------- Step 5: Update Customer Balance ----------

    print("\nUpdating customer balance...")

    current_balance = float(customer_record.get("balance", 0) or 0)

    new_balance = current_balance + total_amount


    customer_update = {
        "FIRSTNAME": customer_record["firstname"],
        "LASTNAME": customer_record["lastname"],
        "OCCUPATION": customer_record.get("occupation"),
        "MAGICFIELD": customer_record.get("magicfield"),
        "JOINDATE": customer_record.get("joindate"),
        "DISCOUNT": customer_record.get("discount"),
        "MEMBERSHIPLEVEL": customer_record.get("membershiplevel"),
        "NOTES": customer_record.get("notes"),
        "BALANCE": new_balance
    }


    resp = make_request(
        "PUT",
        f"{BASE_URL}/customers/{customer_id}",
        customer_update
    )


    if resp:
        print(f"✅ Customer balance updated: ${new_balance:.2f}")
    else:
        print("❌ Customer update failed.")
        sale_success = False



 # ---------- Sale Complete ----------

    print("\n================================")

    if sale_success:
        print("✅ SALE COMPLETED SUCCESSFULLY")
    else:
        print("⚠️ SALE COMPLETED WITH ERRORS")

    print(f"Transaction ID: {transaction_id}")
    print(f"Total Amount: ${total_amount:.2f}")
    print("================================")

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