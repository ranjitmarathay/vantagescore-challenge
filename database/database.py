import sqlite3
import os
from datetime import datetime

def get_db():
    db_path = "./../database.db"  # path to your regular database
    if os.getenv("TEST_ENV"):
        db_path = ":memory:"  # use an in-memory database for tests
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def create_tables(conn, testing=False):
  try:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            address TEXT NOT NULL,
            unit TEXT,
            property_value INTEGER,
            year_built INTEGER,
            bed INTEGER,
            bath INTEGER,
            sleeps INTEGER,
            sqft INTEGER,
            lot_size INTEGER,
            description TEXT,
            image_url TEXT,
            url TEXT,
            last_updated TEXT,
            nightly_rate REAL,
            property_type TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT
      );
    """)

    if testing:
        print("inserting temporary data")
        data = [{
            "title": "Test Property",
            "address": "123 Test St",
            "unit": "A",
            "property_value": 100000,
            "year_built": 2022,
            "bed": 2,
            "bath": 1,
            "sleeps": 4,
            "sqft": 1000,
            "lot_size": 1000,
            "description": "Test description",
            "image_url": "https://example.com/",
            "url": "https://example.com/",
            "last_updated": datetime.now().isoformat(),
            "nightly_rate": 200,
            "property_type": "Duplex"
        }, {
            "title": "Test Property 3",
            "address": "456 Test St",
            "unit": "B",
            "property_value": 175000,
            "year_built": 1990,
            "bed": 3,
            "bath": 2,
            "sleeps": 6,
            "sqft": 1300,
            "lot_size": 1000,
            "description": "Test description",
            "image_url": "https://example.com/",
            "url": "https://example.com/",
            "last_updated": datetime.now().isoformat(),
            "nightly_rate": 400,
            "property_type": "Single Family Home"

        }]
        insert_stmt = '''
            INSERT INTO properties 
            (title, address, unit, property_value, year_built, bed, bath, sleeps, sqft, lot_size, description, image_url, url, last_updated, nightly_rate, property_type) 
            VALUES 
            (:title, :address, :unit, :property_value, :year_built, :bed, :bath, :sleeps, :sqft, :lot_size, :description, :image_url, :url, :last_updated, :nightly_rate, :property_type)
        '''
        for item in data:
            cursor.execute(insert_stmt, item)

    # cursor.execute("SELECT * FROM properties")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print("Retrieved row:", row)
    conn.commit()
  except Exception as e:
      print(f"An error occurred: {e}")
      raise
