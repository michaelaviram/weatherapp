import os
from datetime import datetime
import logging
from io import BytesIO
import decimal

from flask import Flask, Response, redirect, request, render_template, send_file, send_from_directory, url_for, jsonify
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
import mysql.connector
import requests

import backend
from applogs import applogs




app = Flask(__name__)

BG_COLOR=os.environ.get('BG_COLOR')

#monitoring city request metrics
http_request_city_counter = Counter("http_requests_city", "city counter", ["city"])

def get_db_connection():
    """
    Establishes a connection to the MySQL database using environment variables.
    Expected environment variables:
      - MYSQL_HOST
      - MYSQL_DB
      - MYSQL_USER
      - MYSQL_PASSWORD
    """
    host = os.environ.get("MYSQL_HOST")
    database = os.environ.get("MYSQL_DB")
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_ROOT_PASSWORD")

    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        app.logger.error(f"Error connecting to MySQL: {e}")
    return None


@app.route("/dbtest")
def db_test():
    """
    A simple endpoint to test the MySQL connection.
    Executes a query to get the current time from the database.
    """
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to MySQL database"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT NOW();")
        current_time = cursor.fetchone()
        return jsonify({
            "message": "Successfully connected to MySQL!",
            "current_time": current_time[0]
        })
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


@app.route("/", methods =["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            data = request.form['data']            
            result = backend.main(data)

            global location 
            location = result.location
            http_request_city_counter.labels(city=location).inc()
            
            global country
            country = result.country
 
            global days
            days = result.days 
                       
        except Exception as e:
            app.logger.error("searched location that does not exist")
            return render_template("home.html", error="Location does not exist!")

        return redirect(url_for("answer"))

    print(db_test())


    return render_template("home.html", BG_COLOR=BG_COLOR)



@app.route("/answer", methods =["GET"])
def answer():
    try:
        return render_template(
                "answer.html", location=location, country=country, days=days)

    except Exception as e:
        return render_template("home.html", error=f"{e}")

@app.route("/metrics", methods =["GET"])
def metrics():
    if request.method == "GET":
        try:
            return Response(generate_latest())
        except Exception as e:
            return render_template("home.html", error=f"{e}")

@app.route("/history", methods =["GET"])
def history():
    if request.method == "GET":
        try:
            files = os.listdir("./history")
            files.sort(reverse=True)
            return render_template("history.html", files=files)
       
        except Exception as e:
            return render_template("home.html", error=f"{e}")

@app.route('/download_file/<path:filename>', methods=['GET'])
def download_file(filename):
    if request.method == "GET":
        try:
            return send_from_directory("./history", filename, as_attachment=True)
        except Exception as e:
            return render_template("home.html", error=f"{e}")


@app.errorhandler(404)
def handle_page_not_found(e):
    app.logger.critical("page not found")
    return render_template("page_not_found.html")

@app.errorhandler(500)
def handle_no_connection(e):
    app.logger.critical("no connection")
    return render_template("no_connection.html")


if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0")
