import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_db_connection():
    """
    Create a database connection to the MySQL database specified by the db_name.

    Returns
    -------
    connection : mysql.connector.connection.MySQLConnection
        The connection object to the database.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            # port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )

        print("MySQL Database connection successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    

if __name__ == '__main__':
    create_db_connection()