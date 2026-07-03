# main.py

"""                     Main
    Acts as the main program that stores links to all other tables.
This will guide the user to the various tables in which each table will perform
its own requests. Once the user finsihes on a specific table is is returned here. 
"""

from config import TABLES

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


def main_menu():
    while True:
        print("\n" + "="*85)
        print("     Welcome to the Arcane Keeper's Database")
        print("="*85)
        print("Please select a table to review.")
        
        for i, t in enumerate(TABLES, 1):
            print(f"{i:2}. {t.upper()}")
        print(" 0. Exit")
        print("="*85)
        print("Crafted in Python by Chad Carmickle • June 2026")

        try:
            choice = int(input("\nSelect table: "))
            if choice == 0:
                print("👋 Goodbye!")
                break
            if 1 <= choice <= len(TABLES):
                table = TABLES[choice-1]
                
                # Table routing
                if table == "customers":
                    customers_menu()
                elif table == "employees":
                    employees_menu()
                elif table == "inventory":
                    inventory_menu()
                elif table == "loan":
                    loan_menu()
                elif table == "products":
                    products_menu()
                elif table == "purchaseorder":
                    purchaseorder_menu()
                elif table == "rentals":
                    rentals_menu()
                elif table == "salestransaction":
                    salestransaction_menu()
                elif table == "supplier":
                    supplier_menu()
                elif table == "transactionitem":
                    transactionitem_menu()
                else:
                    print(f"\n⚠️  {table.upper()} is not implemented yet.")
            else:
                print("Invalid choice.")
        except:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main_menu()