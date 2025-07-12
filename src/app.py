import os
from datetime import datetime
import logging
from io import BytesIO
import decimal

from flask import Flask, Response, redirect, request, render_template, send_file, send_from_directory, url_for, jsonify
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
import requests

import backend
from database import write_to_db
from applogs import applogs




app = Flask(__name__)

BG_COLOR = os.environ.get('BG_COLOR')
namespace = "abc"

#monitoring city request metrics
http_request_city_counter = Counter("http_requests_city", "city counter", ["city"])


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

            write_to_db(namespace)
                       
        except Exception as e:
            app.logger.error("searched location that does not exist")
            #return render_template("home.html", error="Location does not exist!")
            return render_template("home.html", error=f"{e}")

        return redirect(url_for("answer"))

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
