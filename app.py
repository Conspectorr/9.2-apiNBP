from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_exchange_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    return data[0]["rates"]

@app.route("/", methods=["GET", "POST"])
def currency_calculator():
    rates = get_exchange_rates()
    
    if request.method == "POST":
        selected_currency = request.form["currency"]
        amount = float(request.form["amount"])
        
        selected_rate = next((rate for rate in rates if rate["code"] == selected_currency), None)
        if selected_rate:
            cost_pln = amount * float(selected_rate["ask"])
            return render_template("calculator.html", rates=rates, selected_currency=selected_currency, amount=amount, cost_pln=cost_pln)
    
    return render_template("calculator.html", rates=rates)

if __name__ == "__main__":
    app.run(debug=True)
