from contextlib import contextmanager
from typing import Generator
import psycopg2
from psycopg2.extras import RealDictCursor
from backend.config import settings

class Database:
    """Database connection manager"""
    
    @staticmethod
    @contextmanager
    def get_connection():
        """Get database connection with context manager"""
        conn = None
        try:
            conn = psycopg2.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                cursor_factory=RealDictCursor
            )
            yield conn
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def execute_query(query: str, params: tuple = None, fetch: str = "all"):
        """Execute a query and return results"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if fetch == "one":
                result = cursor.fetchone()
            elif fetch == "all":
                result = cursor.fetchall()
            else:
                result = None
            
            conn.commit()
            cursor.close()
            return result
    
    @staticmethod
    def execute_many(query: str, params_list: list):
        """Execute multiple queries"""
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            cursor.close()

db = Database()