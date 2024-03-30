from flask import Flask, render_template, request
import requests

app = Flask(__name__, static_folder='static')

SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "CHF", "CNY", "HKD", "NZD", "SEK", "KRW", "SGD", "NOK", "MXN", "RUB", "ZAR", "TRY", "BRL", "TWD", "DKK", "PLN", "THB", "IDR", "HUF", "CZK", "ILS", "CLP", "PHP", "AED", "COL", "SAR", "MYR", "RON", "BGN", "HRK", "ISK"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        base_currency = request.form["base_currency"]
        target_currency = request.form["target_currency"]
        amount = float(request.form["amount"])

        converted_amount = convert_currency(amount, base_currency, target_currency)

        return render_template("index.html", currencies=SUPPORTED_CURRENCIES, result=converted_amount)

    return render_template("index.html", currencies=SUPPORTED_CURRENCIES, result=None)

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        conversion_rate = data["rates"][to_currency]
        converted_amount = amount * conversion_rate

        return converted_amount
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
