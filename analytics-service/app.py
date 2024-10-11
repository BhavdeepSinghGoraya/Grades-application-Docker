import mysql.connector
from pymongo import MongoClient
import time
from mysql.connector import Error

def connect_with_retry(retries=5, delay=5):
    while retries > 0:
        try:
            connection = mysql.connector.connect(
                    host="mysql",  
                    user="user",
                    password="password",
                    database="grades_db"
            )
            if connection.is_connected():
                print("Connected to MySQL")
                return connection
        except Error as e:
            print(f"Error: {e}, retrying in {delay} seconds...")
            time.sleep(delay)
            retries -= 1
    raise Exception("Could not connect to MySQL after retries")

mysql_conn = connect_with_retry()

# MySQL connection
mysql_conn = mysql.connector.connect(
    host="mysql",  
    user="user",
    password="password",
    database="grades_db"
)

cursor = mysql_conn.cursor()
cursor.execute("SELECT MAX(grade), MIN(grade), AVG(grade) FROM grades")
result = cursor.fetchone()
max_grade, min_grade, avg_grade = result

# MongoDB connection
client = MongoClient("mongodb://mongo-db:27017/")
db = client.analytics_db
stats_collection = db.grade_statistics

# Write data to MongoDB
stats_collection.insert_one({
    "max_grade": max_grade,
    "min_grade": min_grade,
    "avg_grade": avg_grade
})

# Close connections
cursor.close()
mysql_conn.close()
client.close()
