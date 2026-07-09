#*************************** config.py ********************************
# Stores settings that the rest of your Python program can import and use.


BASE_URL = "https://oracleapex.com/ords/chad_db"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Referer": "https://oracleapex.com/ords/chad_db/",
}

TABLES = [
    "customers", "employees", "transactionitem", "inventory", "loan",
    "products", "purchaseorder", "rentals", "salestransaction", "supplier"
]