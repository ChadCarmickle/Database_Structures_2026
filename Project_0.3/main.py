# main.py

"""                     Main
    Acts as the main program that stores links to all other tables.
This will guide the user to the various tables in which each table will perform
its own requests. Once the user finishes on a specific table is returned here. 
"""

# Imports all other table menus.
from tables.customers import customers_menu
from tables.employees import employees_menu
from tables.inventory import inventory_menu
from tables.loan import loan_menu
from tables.products import products_menu
from tables.purchaseorder import purchaseorder_menu
from tables.rentals import rentals_menu
from tables.salestransaction import salestransaction_menu
from tables.supplier import supplier_menu
from tables.transactionitem import transactionitem_menu

# Imports the join-based reports.
from tables.sales_detailed_reports import sales_detail_report
from tables.inventory_supplier_report import inventory_supplier_report

# Maps table name -> menu function
TABLE_FUNCTIONS = {
    "customers": customers_menu,
    "employees": employees_menu,
    "inventory": inventory_menu,
    "loan": loan_menu,
    "products": products_menu,
    "purchaseorder": purchaseorder_menu,
    "rentals": rentals_menu,
    "salestransaction": salestransaction_menu,
    "supplier": supplier_menu,
    "transactionitem": transactionitem_menu,
}

# Groups tables into categories for display. Adjust groupings/order freely.
CATEGORIES = {
    "People":        ["customers", "employees", "supplier"],
    "Inventory":     ["products", "inventory"],
    "Transactions":  ["salestransaction", "transactionitem", "purchaseorder"],
    "Services":      ["loan", "rentals"],
}

# Reports listed after the table categories. Order here determines numbering.
REPORTS = [
    ("Display Sales Report      (Joins tables: SalesTransction + TransactionItem + Products + Customers.)", sales_detail_report),
    ("Inventory Report          (Joins Inventiory + Products + Supplier)", inventory_supplier_report),
]
 
def build_menu_order():
    """Flattens CATEGORIES into a single ordered list of table names,
    which determines the numbering shown to the user."""
    order = []
    for tables in CATEGORIES.values():
        order.extend(tables)
    return order


def print_menu(menu_order):
    print("\n" + "="*85)
    print("     Welcome to the Arcane Keeper's Database")
    print("="*85)
    print("Please select a table to review.")

    i = 1
    for category, tables in CATEGORIES.items():
        print(f"\n-- {category} --")
        for t in tables:
            print(f"{i:2}. {t.upper()}")
            i += 1

    # Prints reports menu. 
    print("\n-- Reports --")
    for label, _ in REPORTS:
        print(f"{i:2}. {label}")
        i += 1


    print("\n 0. Perform a Sale")
    print(" ` or type 'Exit' to close Application")
    print("="*85)
    print("Crafted in Python by Chad Carmickle • June-July 2026")


 
def main_menu():
    menu_order = build_menu_order()
    num_tables = len(menu_order)
    num_reports = len(REPORTS)
 
    while True:
        print_menu(menu_order)
 
        try:
            raw = input("\nSelect table: ").strip()
 
            if raw == "`" or raw.lower() == "exit":
                print("👋 Goodbye!")
                break
 
            choice = int(raw)
            if choice == 0:
                print("Not yet implemented")
                continue
            if 1 <= choice <= num_tables:
                table = menu_order[choice - 1]
                menu_func = TABLE_FUNCTIONS.get(table)
                if menu_func:
                    menu_func()
                else:
                    print(f"\n⚠️  {table.upper()} is not implemented yet.")
            elif num_tables < choice <= num_tables + num_reports:
                _, report_func = REPORTS[choice - num_tables - 1]
                report_func()
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid choice.")


if __name__ == "__main__":
    main_menu()