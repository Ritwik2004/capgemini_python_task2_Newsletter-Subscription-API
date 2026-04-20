from flask import Flask, request, jsonify, render_template
import mysql.connector
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = Flask(__name__)

def DB_Connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/subscribe", methods=["POST"])
def addEmail():
    data = request.get_json()

    if "email" not in data:
        return jsonify({"error" : "Email is required"}), 400

    email = data["email"]

    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    connection = DB_Connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("INSERT INTO subscribers (email) VALUES (%s)", (email,))
        connection.commit()
        return jsonify({"message": "add to database successfully"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error" : "The email already exist"}), 400
    finally:
        cursor.close()
        connection.close()

@app.route("/updateEmail", methods=["PUT"])
def updateEmail():
    data = request.get_json()

    if not data or "oldEmail" not in data or "newEmail" not in data:
        return jsonify({"error": "oldEmail and newEmail are required"}), 400

    old_email = data["oldEmail"].strip().lower()
    new_email = data["newEmail"].strip().lower()

    if not is_valid_email(new_email):
        return jsonify({"error": "Invalid new email format"}), 400

    connection = DB_Connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE subscribers SET email = %s WHERE email = %s",
            (new_email, old_email)
        )
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Old email not found"}), 404

        return jsonify({"message": "Email updated successfully"}), 200

    except mysql.connector.IntegrityError:
        return jsonify({"error": "New email already exists"}), 409

    finally:
        cursor.close()
        connection.close()

@app.route("/unsubscribe", methods=["DELETE"])
def deleteEmail():
    data = request.get_json()

    if "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    email = data["email"]

    connection = DB_Connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM subscribers WHERE email = %s", (email,))
    connection.commit()

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify({"message": "Email not found"}), 404

    cursor.close()
    connection.close()
    return jsonify({"message": "Unsubscribed successfully"}), 200
    
@app.route("/subscribers", methods=["GET"])
def getSubscribersEmail():
    connection = DB_Connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT email FROM subscribers")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)