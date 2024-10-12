import mysql.connector
from pymongo import MongoClient
import time
from mysql.connector import Error
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

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

def init_scheduler():
    print('--------------------------------------------------------')
    print('inside init schedular')
    print('--------------------------------------------------------')
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(process_stats,
                'interval',
                seconds=60)
    sched.start()


def process_stats():
    try:
        print('--------------------------------------------------------')
        print('inside process stats')
        print('--------------------------------------------------------')
        current_datetime = datetime.datetime.now()
        stats = {
            "max_grade": 0,
            "min_grade": 0,
            "avg_grade": 0,
            "timestamp": current_datetime
        }


        mysql_conn = connect_with_retry()
        cursor = mysql_conn.cursor()


        cursor.execute("SELECT MAX(grade), MIN(grade), AVG(grade) FROM grades")
        result = cursor.fetchone()
        max_grade, min_grade, avg_grade = result

        stats['max_grade'] = max_grade
        stats['min_grade'] = min_grade
        stats['avg_grade'] = float(avg_grade)

        # MongoDB connection
        client = MongoClient("mongodb://mongo-db:27017/")
        db = client.analytics_db
        stats_collection = db.grade_statistics

        # Inserting the stats into MongoDB with a timestamp
        stats_collection.insert_one(stats)

        print(f"Stats inserted into MongoDB at {current_datetime}")

    except Error as mysql_error:
        print(f"MySQL Error: {mysql_error}")
    except Exception as e:
        print(f"Error during stats processing: {e}")
    finally:
        # Ensure connections are closed properly
        if 'cursor' in locals():
            cursor.close()
        if 'mysql_conn' in locals() and mysql_conn.is_connected():
            mysql_conn.close()
        if 'client' in locals():
            client.close()
if __name__=='__main__':

    print("Starting analytics service...")
    mysql_conn = connect_with_retry()
    if mysql_conn:
        mysql_conn.close()
    init_scheduler()
    try:
        while True:
            time.sleep(60)  # Sleep for 1 minute to keep the service alive
    except (KeyboardInterrupt, SystemExit):
        print("Analytics service shutting down.")