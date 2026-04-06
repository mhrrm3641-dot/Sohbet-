import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '../data/vouchers.db')

def export_unused_codes():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM vouchers WHERE is_used = 0")
    codes = cursor.fetchall()
    
    with open("satis_bekleyen_kodlar.txt", "w") as f:
        for c in codes:
            f.write(f"{c[0]}\n")
    
    print(f"{len(codes)} adet kod 'satis_bekleyen_kodlar.txt' dosyasına yazıldı.")
    conn.close()

if __name__ == "__main__":
    export_unused_codes()
