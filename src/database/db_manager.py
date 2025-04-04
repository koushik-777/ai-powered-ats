import sqlite3
import os

class DBManager:
    def __init__(self, db_path='recruitment.db'):
        # Ensure the path is absolute
        self.db_path = db_path
        self.initialize_db()
    
    def initialize_db(self):
        """Initialize the database with required tables"""
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables using schema
        with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as schema_file:
            schema_sql = schema_file.read()
            cursor.executescript(schema_sql)
        
        conn.commit()
        conn.close()
        
        print(f"Database initialized at {self.db_path}")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            conn.commit()
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    
    def insert_record(self, table, data):
        """Insert a record into the specified table"""
        placeholders = ', '.join(['?'] * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            record_id = cursor.lastrowid
            conn.commit()
            return record_id
        except Exception as e:
            conn.rollback()
            print(f"Error inserting record: {e}")
            return None
        finally:
            conn.close()
    
    def update_record(self, table, record_id, data):
        """Update a record in the specified table"""
        set_clause = ', '.join([f"{column} = ?" for column in data.keys()])
        values = tuple(data.values()) + (record_id,)
        
        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating record: {e}")
            return False
        finally:
            conn.close()