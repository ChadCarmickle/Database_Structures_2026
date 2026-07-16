# tables/inventory_supplier_report.py

"""*********************** Inventory & Supplier Report ***********************
Joins: inventory + products + supplier

Since ORDS doesn't support sending raw SQL joins, this report fetches
each table individually and merges the records together in Python by
matching on their ID fields, showing current stock levels next to the
supplier who should be contacted for reordering.

************************************************************************
"""

from tables.products import get_all as get_all_products
from tables.inventory import get_all as get_all_inventory
from tables.supplier import get_all as get_all_supplier

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

def _to_number(value):
    """Safely converts a value to float for comparison; defaults to 0."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def inventory_supplier_report():
    """
    Shows current stock levels next to the supplier who should be
    contacted for reordering, instead of raw foreign key IDs.
    """
    print("\n--- Inventory & Supplier Report ---")
    print("Fetching data from inventory, products, supplier...")

    inventory = get_all_inventory()
    products = get_all_products()
    suppliers = get_all_supplier()

    if not inventory:
        print("No inventory records found.")
        return

    products_lookup = _index_by(products, "PRODUCTID")
    suppliers_lookup = _index_by(suppliers, "SUPPLIERID")

    report_rows = []

    for inv in inventory:
        inv = _normalize(inv)
        product_id = inv.get("PRODUCTID")
        quantity_on_hand = inv.get("QUANTITYONHAND", 0)
        reorder_level = inv.get("REORDERLEVEL", 0)

        product = products_lookup.get(product_id, {})
        supplier = suppliers_lookup.get(product.get("SUPPLIERID"), {})

        product_name = product.get("PRODUCTNAME", "Unknown")
        supplier_name = supplier.get("SUPPLIERNAME", "Unknown")
        supplier_contact = supplier.get("CONTACTINFO", "N/A")

        needs_reorder = "YES" if _to_number(quantity_on_hand) <= _to_number(reorder_level) else "No"

        report_rows.append({
            "PRODUCT": product_name,
            "QTYONHAND": quantity_on_hand,
            "REORDERLEVEL": reorder_level,
            "NEEDSREORDER": needs_reorder,
            "SUPPLIER": supplier_name,
            "CONTACT": supplier_contact,
        })

    print(f"\nFound {len(report_rows)} inventory record(s).\n")
    print_table(report_rows)
    continue_prompt()