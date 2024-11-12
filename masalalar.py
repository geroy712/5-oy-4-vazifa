import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="autosalon_db", user="username", password="password", host="localhost"
)
conn.autocommit = True  

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS avtomobillar (
        id SERIAL PRIMARY KEY,
        nomi VARCHAR(100) NOT NULL,
        model TEXT,
        yil INTEGER,
        narx NUMERIC(12, 2),
        mavjudmi BOOL DEFAULT TRUE
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS clientlar (
        id SERIAL PRIMARY KEY,
        ism VARCHAR(50) NOT NULL,
        familiya VARCHAR(50),
        telefon CHAR(13),
        manzil TEXT
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS buyurtmalar (
        id SERIAL PRIMARY KEY,
        avtomobil_id INTEGER REFERENCES avtomobillar(id),
        client_id INTEGER REFERENCES clientlar(id),
        sana DATE NOT NULL,
        umumiy_narx NUMERIC(12, 2)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS xodimlar (
        id SERIAL PRIMARY KEY,
        ism VARCHAR(50) NOT NULL,
        lavozim VARCHAR(50),
        maosh NUMERIC(10, 2)
    );
""")


cur.execute("""
    ALTER TABLE clientlar
    ADD COLUMN email VARCHAR(100);
""")

cur.execute("""
    ALTER TABLE clientlar
    RENAME COLUMN ism TO ismi;
""")

cur.execute("""
    ALTER TABLE clientlar
    RENAME TO mijozlar;
""")

cur.execute("""
    INSERT INTO avtomobillar (nomi, model, yil, narx)
    VALUES 
    ('Chevrolet', 'Spark', 2020, 8500.00),
    ('Tesla', 'Model 3', 2023, 40000.00);
""")

cur.execute("""
    INSERT INTO mijozlar (ismi, familiya, telefon, manzil, email)
    VALUES 
    ('Ali', 'Valiyev', '+998901234567', 'Toshkent', 'ali@example.com'),
    ('Laylo', 'Xudoyberdiyeva', '+998907654321', 'Samarqand', 'laylo@example.com');
""")

cur.execute("""
    INSERT INTO buyurtmalar (avtomobil_id, client_id, sana, umumiy_narx)
    VALUES 
    (1, 1, '2024-11-01', 8500.00),
    (2, 2, '2024-11-05', 40000.00);
""")

cur.execute("""
    INSERT INTO xodimlar (ism, lavozim, maosh)
    VALUES 
    ('Akmal', 'Sotuvchi', 1500.00),
    ('Zarina', 'Menejer', 1800.00);
""")


cur.execute("""
    UPDATE xodimlar
    SET ism = 'Rustam'
    WHERE id = 1;
""")
cur.execute("""
    UPDATE xodimlar
    SET ism = 'Gulnoza'
    WHERE id = 2;
""")


cur.execute("""
    DELETE FROM xodimlar
    WHERE id = 1;
""")

cur.execute("SELECT * FROM avtomobillar;")
print("Avtomobillar:", cur.fetchall())

cur.execute("SELECT * FROM mijozlar;")
print("Mijozlar:", cur.fetchall())

cur.execute("SELECT * FROM buyurtmalar;")
print("Buyurtmalar:", cur.fetchall())

cur.execute("SELECT * FROM xodimlar;")
print("Xodimlar:", cur.fetchall())

cur.close()
conn.close()
