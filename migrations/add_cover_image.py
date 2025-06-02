from app import db
import sqlite3

def upgrade():
    # SQLite veritabanına bağlan
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    # cover_image sütununu ekle
    cursor.execute('ALTER TABLE post ADD COLUMN cover_image VARCHAR(200)')
    
    # Değişiklikleri kaydet ve bağlantıyı kapat
    conn.commit()
    conn.close()

if __name__ == '__main__':
    upgrade() 