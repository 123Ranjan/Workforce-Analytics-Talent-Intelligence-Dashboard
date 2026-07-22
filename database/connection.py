# database/connection.py

import psycopg2
import pandas as pd
from database.config import DB_CONFIG

def get_connection():
    """Get PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def run_query(query):
    """Execute SQL query and return results as DataFrame using psycopg2 directly"""
    conn = get_connection()
    try:
        # Use cursor to execute and fetch data
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Fetch all data
        data = cursor.fetchall()
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        cursor.close()
        return df
    finally:
        conn.close()

def test_connection():
    """Test database connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False