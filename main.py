from flask import Flask, request, session, render_template, redirect, url_for
import requests

app = Flask("__main__")
app.secret_key = "your_secret_key"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["location"] = request.form.get("location")
        return redirect(url_for("result"))
    return render_template("index.html")


@app.route("/weather")
def result():
    location = session.get("location", "New York")

    BASE_URL = "https://api.weatherapi.com/v1/current.json"
    key = "5fe787d50629440eb7c00938241410"
    q = f"{location}"
        
    url = f"{BASE_URL}?q={q}&key={key}"
    try:
        response = requests.get(url)
        data = response.json()

        if "location" not in data or "current" not in data:
            print("Unexpected API response:", data)
            return redirect(url_for('home'))
        
        city = data["location"]["name"]
        region = data["location"]["region"]
        country = data["location"]["country"]
        current = data["current"]["condition"]["text"]
        wind_mph = data["current"]["wind_mph"]
        pressure_mb = data["current"]["pressure_mb"]
        humidity = data["current"]["humidity"]
        return render_template(
            "resultpg.html",
            city=city,
            region=region,
            country=country,
            current=current,
            wind_mph=wind_mph,
            pressure_mb=pressure_mb,
            humidity=humidity,
        )

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return render_template("errorpg.html")


if __name__ == "__main__":
    app.run(debug=True)
