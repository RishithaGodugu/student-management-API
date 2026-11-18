# import mysql.connector 

# def get_connection():
#     connection=mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="512503",
#         database="student_db"
#     )

#     return connection

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    connection=mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return connection