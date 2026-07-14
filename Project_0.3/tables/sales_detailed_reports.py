# tables/sales_detailed_reports.py

"""*********************** Sales Detail Report ***********************
Joins: salestransaction + transactionitem + products + customers

Since ORDS doesn't support sending raw SQL joins, this report fetches
each table individually and merges the records together in Python by
matching on their ID fields, producing one combined, human-readable
table of every line item ever sold.

************************************************************************
"""

from tables.customers import get_all as get_all_customers
from tables.products import get_all as get_all_products
from tables.transactionitem import get_all as get_all_transactionitem
from tables.salestransaction import get_all as get_all_salestransaction

from utils import continue_prompt
from utils import print_table


def _normalize(record):
    """Normalize keys to uppercase, handling both camelCase and lowercase from ORDS."""
    if not record:
        return {}
    normalized = {}
    for k, v in record.items():
        # Convert to uppercase, strip any weirdness
        key_upper = str(k).upper().strip()
        normalized[key_upper] = v
    return normalized

def _index_by(records, id_field):
    """Builds lookup dict. id_field should be uppercase."""
    lookup = {}
    for r in records:
        r = _normalize(r)
        rid = r.get(id_field.upper())          # Ensure uppercase
        if rid is not None:
            lookup[rid] = r
    return lookup


def sales_detail_report():
    """
    Shows every line item ever sold, alongside the customer who bought it
    and the product name/price, instead of raw foreign key IDs.
    """
    print("\n--- Sales Detail Report ---")
    print("Fetching data from salestransaction, transactionitem, products, customers...")

    sales = get_all_salestransaction()
    items = get_all_transactionitem()
    products = get_all_products()
    customers = get_all_customers()



    # Normalized debug
    norm_sales = [_normalize(s) for s in sales]
    norm_customers = [_normalize(c) for c in customers]

    customer_ids_in_sales = {s.get("CUSTOMERID") for s in norm_sales if s.get("CUSTOMERID") is not None}
    customer_ids = {c.get("CUSTOMERID") for c in norm_customers}


    if not items:
        print("No transaction items found.")
        return

    sales_lookup = _index_by(sales, "TRANSACTIONID")
    products_lookup = _index_by(products, "PRODUCTID")
    customers_lookup = _index_by(customers, "CUSTOMERID")

    report_rows = []

    for item in items:
        item = _normalize(item)
        sale_id = item.get("SALESTRANSACTIONID")
        product_id = item.get("PRODUCTID")
        quantity = item.get("QUANTITY", 0) or 0
        unit_price = item.get("UNITPRICE", 0) or 0
        discount = item.get("DISCOUNT", 0) or 0

        sale = sales_lookup.get(sale_id, {})
        product = products_lookup.get(product_id, {})
        
        # More robust customer lookup
        cust_id = sale.get("CUSTOMERID")
        customer = customers_lookup.get(cust_id, {}) if cust_id is not None else {}

        # Extra debug for this specific sale
        if cust_id:
            print(f"DEBUG: Sale {sale_id} -> CustomerID {cust_id} -> Found: {bool(customer)}")
        
        try:
            quantity_num = float(quantity)
            unit_price_num = float(unit_price)
            discount_num = float(discount)
        except (TypeError, ValueError):
            quantity_num = unit_price_num = discount_num = 0

        line_total = quantity_num * unit_price_num * (1 - discount_num / 100)

        customer_name = f"{customer.get('FIRSTNAME', '')} {customer.get('LASTNAME', '')}".strip() or "Unknown"
        product_name = product.get("PRODUCTNAME", "Unknown")

        report_rows.append({
            "SALEID": sale_id,
            "CUSTOMER": customer_name,
            "PRODUCT": product_name,
            "QTY": quantity,
            "UNITPRICE": unit_price,
            "DISCOUNT%": discount,
            "LINETOTAL": round(line_total, 2),
        })

    print(f"\nFound {len(report_rows)} line item(s) across all sales.\n")
    print_table(report_rows)
    continue_prompt()