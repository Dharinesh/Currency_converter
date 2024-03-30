from flask import Flask, render_template, request
import requests
from currency_info import CURRENCY_INFO

app = Flask(__name__, static_folder='static')

# List of supported currencies
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "CHF", "CNY", "HKD", "NZD", "SEK", "KRW", "SGD", "NOK", "MXN", "RUB", "ZAR", "TRY", "BRL", "TWD", "DKK", "PLN", "THB", "IDR", "HUF", "CZK", "ILS", "CLP", "PHP", "AED", "COL", "SAR", "MYR", "RON", "BGN", "HRK", "ISK"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the form data
        base_currency = request.form["base_currency"]
        target_currency = request.form["target_currency"]
        amount = float(request.form["amount"])

        # Call the conversion function
        converted_amount = convert_currency(amount, base_currency, target_currency)

        # Pass the result to the template
        return render_template("index.html", currencies=SUPPORTED_CURRENCIES, result=converted_amount)

    # Render the template with default values
    return render_template("index.html", currencies=SUPPORTED_CURRENCIES, result=None)

def convert_currency(amount, from_currency, to_currency):
    # API endpoint URL
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Get the conversion rate
        conversion_rate = data["rates"][to_currency]

        # Calculate the converted amount
        converted_amount = amount * conversion_rate

        return converted_amount
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    app.run(debug=True)