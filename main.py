import sqlite3
import requests
from datetime import datetime
import json

def fetch_and_store_sales_data(from_date, to_date):
    API_CONFIG = {
        'app_key': 'srd2neaq1xg7bzc6uyk5jmwv98o4tpfh',
        'app_secret': 'fd08934c5224af4c975015e599d60a74bf857b4a',
        'access_token': '0442e1ee9899bc3806f1a40be490af4ec5c6602a',
        'restID': '51wok2zxnsad'
    }
    
    base_url = "http://api.petpooja.com/V1/orders/get_sales_data/"
    params = {
        "app_key": API_CONFIG["app_key"],
        "app_secret": API_CONFIG["app_secret"],
        "access_token": API_CONFIG["access_token"],
        "restID": API_CONFIG["restID"],
        "from_date": from_date,
        "to_date": to_date
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        sales_data = response.json()

        if not sales_data.get('Records'):
            print("No sales data found.")
            return False, "No sales data received from API"

        conn = sqlite3.connect("sales_database.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_number TEXT,
                sale_date TEXT,
                transaction_time TEXT,
                sale_amount REAL,
                tax_amount REAL,
                discount_amount REAL,
                round_off REAL,
                net_sale REAL,
                payment_mode TEXT,
                order_type TEXT,
                transaction_status TEXT
            )
        """)

        for sale in sales_data.get('Records', []):
            # print(f"Inserting sale: {sale}")  # Debugging each sale entry
            try:
                receipt_number = sale.get("Receipt number", "")
                sale_date = sale.get("Receipt Date", "")
                transaction_time = sale.get("Transaction Time", "")
                sale_amount = float(sale.get("Invoice amount", 0))
                tax_amount = float(sale.get("Tax amount", 0))
                discount_amount = float(sale.get("Discount amount", 0))
                round_off = float(sale.get("Round Off", 0))
                net_sale = float(sale.get("Net sale", 0))
                payment_mode = sale.get("Payment Mode", "")
                order_type = sale.get("Order Type", "")
                transaction_status = sale.get("Transaction status", "")

                cursor.execute("""
                    INSERT INTO sales_data (
                        receipt_number,
                        sale_date,
                        transaction_time,
                        sale_amount,
                        tax_amount,
                        discount_amount,
                        round_off,
                        net_sale,
                        payment_mode,
                        order_type,
                        transaction_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    receipt_number,
                    sale_date,
                    transaction_time,
                    sale_amount,
                    tax_amount,
                    discount_amount,
                    round_off,
                    net_sale,
                    payment_mode,
                    order_type,
                    transaction_status
                ))
            except sqlite3.Error as e:
                print("SQL Error:", e)

        conn.commit()
        cursor.close()
        conn.close()

        return True, "Data successfully fetched and stored"

    except requests.exceptions.RequestException as e:
        return False, f"API Error: {str(e)}"
    except sqlite3.Error as e:
        return False, f"Database Error: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"

if __name__ == "__main__":
    success, message = fetch_and_store_sales_data(from_date="2025-01-20 23:59:59", to_date="2025-01-30 23:59:59")
    print(message)