#Reviewed by Bronia

import os
from flask import Flask, Response, request, render_template, send_file, send_from_directory, url_for
from io import BytesIO
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from datetime import datetime
import logging
from applogs import applogs
import decimal
import requests
import boto3
import backend


app = Flask(__name__)

BG_COLOR=os.environ.get('BG_COLOR')

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
                       
        except Exception as e:
            app.logger.error("searched location that does not exist")
            return render_template("home.html", error="Location does not exist!")

        return render_template(
                "answer.html", location=location, country=country, days=days)

    return render_template("home.html", BG_COLOR=BG_COLOR)

@app.route("/dynamo", methods = ["POST"])
def dynamo():
    try: 
        dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")
        table = dynamodb.Table("Weather")

        table.put_item(
            Item={
                'location':location,
                'country':country,
                'day1': {
                    'Date':days[0].date,
                    'Day Temperature':decimal.Decimal(str(days[0].day_temp)),
                    'Night Temperature':decimal.Decimal(str(days[0].night_temp)),
                    'Average Humidity':days[0].humidity
                },
                'day2': {
                    'Date':days[1].date,
                    'Day Temperature':decimal.Decimal(str(days[1].day_temp)),
                    'Night Temperature':decimal.Decimal(str(days[1].night_temp)),
                    'Average Humidity':days[1].humidity
                },
                'day3': {
                    'Date':days[2].date,
                    'Day Temperature':decimal.Decimal(str(days[2].day_temp)),
                    'Night Temperature':decimal.Decimal(str(days[2].night_temp)),
                    'Average Humidity':days[2].humidity
                },
                'day4': {
                    'Date':days[3].date,
                    'Day Temperature':decimal.Decimal(str(days[3].day_temp)),
                    'Night Temperature':decimal.Decimal(str(days[3].night_temp)),
                    'Average Humidity':days[3].humidity
                },
                'day5': {
                    'Date':days[4].date,
                    'Day Temperature':decimal.Decimal(str(days[4].day_temp)),
                    'Night Temperature':decimal.Decimal(str(days[4].night_temp)),
                    'Average Humidity':days[4].humidity
                },
                'day6': {
                    'Date':days[5].date,
                    'Day Temperature':decimal.Decimal(str(days[5].day_temp)),
                    'Night Temperature':decimal.Decimal(str(days[5].night_temp)),
                    'Average Humidity':days[5].humidity
                },
                'day7': {
                    'Date':days[6].date,
                    'Day Temperature':decimal.Decimal(str(days[6].day_temp)),
                    'Night Temperature':decimal.Decimal(str(days[6].night_temp)),
                    'Average Humidity':days[6].humidity
                }
            })

    except Exception as e:
        return render_template("home.html", error=f"{e}")
    
    return render_template("home.html", error="Download succeeded!")


@app.route("/download_image", methods =["GET"])
def download_image():
    if request.method == "GET":
        try:
            url = "https://ws3eu88ri3.execute-api.eu-central-1.amazonaws.com/prod/michaelaviram/sky.png"
        
            binary = requests.get(url)
            image = BytesIO(binary.content)
            image.seek(0)

            return send_file(image, download_name=f"{location}'s sky.png", as_attachment=True)

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
