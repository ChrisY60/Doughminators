import qrcode
import os

def generate_qr_codes(num_tables):
    os.makedirs("qr_codes", exist_ok=True)
    base_url = "http://145.93.164.237:8080?table_id="  # Adjust for your server URL

    for table_id in range(1, num_tables + 1):
        url = f"{base_url}{table_id}"
        qr = qrcode.make(url)
        qr.save(f"qr_codes/table_{table_id}.png")
        print(f"Generated QR code for Table {table_id} at: qr_codes/table_{table_id}.png")

generate_qr_codes(10)