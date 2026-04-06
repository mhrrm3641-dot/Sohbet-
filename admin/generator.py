import sqlite3
import secrets
import string
import os

# Veritabanı bağlantısı (Yoksa oluşturur)
db_path = os.path.join(os.path.dirname(__file__), '../data/vouchers.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vouchers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            is_used BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_codes(count=50):
    alphabet = string.ascii_uppercase + string.digits
    alphabet = alphabet.translate(str.maketrans('', '', '0OIL')) # Karışıklığı önle
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    generated = []
    for _ in range(count):
        # Örn: ABCD-1234-EFGH
        raw_code = ''.join(secrets.choice(alphabet) for _ in range(12))
        formatted_code = '-'.join([raw_code[i:i+4] for i in range(0, 12, 4)])
        
        try:
            cursor.execute("INSERT INTO vouchers (code) VALUES (?)", (formatted_code,))
            generated.append(formatted_code)
        except sqlite3.IntegrityError:
            continue # Kod çakışırsa pas geç
            
    conn.commit()
    conn.close()
    return generated

if __name__ == "__main__":
    init_db()
    new_codes = generate_codes(20)
    print(f"--- {len(new_codes)} Yeni Kod Üretildi ---")
    for c in new_codes:
        print(c)
