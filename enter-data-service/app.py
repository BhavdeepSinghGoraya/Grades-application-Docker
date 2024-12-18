import mysql.connector
import time
import jwt
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'Docker-Project-1'
# MySQL connection config (using environment variables)
def create_connection():
    return mysql.connector.connect(
        host="mysql",  
        user="user",
        password="password",
        database="grades_db"
    )
    

@app.route('/enter-data', methods=['GET','POST'])
# @token_required 
def enter_data():
    if (request.method=='GET'):

        return render_template('index.html')
    print(request.method)
    grade = int(request.form.get('grade'))
    student_name = request.form.get('student_name')
    print(grade)
    print(student_name)

    if not grade or not student_name:
        return jsonify({"error": "Invalid data"}), 400

    try:
        conn = create_connection()
        cursor = conn.cursor()
        print("Connected again")

        query = "INSERT INTO grades (grade, student_name) VALUES (%s, %s)"
        cursor.execute(query, (grade, student_name))
        conn.commit()

        flash("Data entered successfully!", "success") 
        return redirect(url_for('enter_data'))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"error": f"Failed to connect to database {err}"}), 500
    finally:
        if conn:
            conn.close()


@app.route('/')
def home():
    return "Enter Data service is running!"

if __name__ == '__main__':
    # Adding retry logic for the database connection
    retries = 5
    while retries > 0:
        try:
            conn = create_connection()
            if conn.is_connected():
                conn.close()
                print("Connected to MySQL successfully!")
                break
        except mysql.connector.Error:
            retries -= 1
            print(f"Could not connect to MySQL, retrying... {retries}")
            time.sleep(5)

    app.run(host="0.0.0.0", port=5001, debug=True)
