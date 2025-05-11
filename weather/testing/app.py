#Reviewed by Bronia

from flask import Flask
from flask import request
from flask import render_template
import backend

app = Flask(__name__)

@app.route("/",methods =["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            data = request.form['data']
            result = backend.main(data)

            location = result.location
            country = result.country
            days = result.days

        except Exception:
            return render_template("home.html", error="Location does not exist!")        

        return render_template("answer.html", location=location,\
            country=country, days=days)

    return render_template("home.html")

@app.errorhandler(404)
def handle_page_not_found(e):
    return render_template("page_not_found.html")

@app.errorhandler(500)
def handle_no_connection(e):
    return render_template("no_connection.html")


if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0")
