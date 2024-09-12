from flask import Flask, render_template, request
from forms import PredictForm
import requests
import json

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3'  # Replace with a secure, randomly generated key

@app.route('/', methods=('GET', 'POST'))
def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.validate_on_submit():
        # Replace the hardcoded Bearer token with your actual IAM API key
        
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "eyJraWQiOiIyMDI0MDkwMjA4NDIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02NjgwMDBYNjFPIiwiaWQiOiJJQk1pZC02NjgwMDBYNjFPIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiZWE2ZTJlNjQtYmM4Mi00YThhLTkwODAtOGI0YjQ5NDI1YjlhIiwiaWRlbnRpZmllciI6IjY2ODAwMFg2MU8iLCJnaXZlbl9uYW1lIjoiUGFyaW4iLCJmYW1pbHlfbmFtZSI6IkFjaGFyeWEiLCJuYW1lIjoiUGFyaW4gQWNoYXJ5YSIsImVtYWlsIjoiYWNoYXJ5YXBhcmluMDVAZ21haWwuY29tIiwic3ViIjoiYWNoYXJ5YXBhcmluMDVAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoiYWNoYXJ5YXBhcmluMDVAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjY4MDAwWDYxTyIsIm5hbWUiOiJQYXJpbiBBY2hhcnlhIiwiZ2l2ZW5fbmFtZSI6IlBhcmluIiwiZmFtaWx5X25hbWUiOiJBY2hhcnlhIiwiZW1haWwiOiJhY2hhcnlhcGFyaW4wNUBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiMDY3N2QwZjNlMTMxNGE5NDhmNTRiZjliOWRkY2YwM2MiLCJmcm96ZW4iOnRydWV9LCJpYXQiOjE3MjYxNDc0NzEsImV4cCI6MTcyNjE1MTA3MSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9vaWRjL3Rva2VuIiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.rHERHX0hnhakztF7Fd16DgNu1RRj_0En1O82HdQILOUvSKpRa4L45Uki7N4IWnm6RduQQxgGm_lDH0VO8ZbTNj4YrxoMgnO0sRnO58Wrhu9OyNssEPM3av0Xg4iK9Pychje5sssCaCgL_m1a_PNzeK1sSFnngBtKKygqNGZD67WVa2ua3n7clELjv_HNlCTBF2ZDCbqs8o4Cq-CuTcbnvsox210JLll6Bnzh6LDjUjiJRTjLxdB9unKLfU8oQmTfzS30FPFDArqTx73q93vWmHF1LcfzWPC79b1fA6U_xk_kmYNfytHZp_mvqAuRHYjHphj4lsor_tKZKivXCrTHCw"}

        # Gather user inputs from the form
        userInput = [
            form.burnRate.data,
            form.revenue.data,
            form.customerAcquisitionCost.data,
            form.customerLifetimeValue.data,
            form.monthlyRecurringRevenue.data,
            form.churnRate.data,
            form.marketGrowthRate.data,
            form.marketingSpend.data,
            form.rdSpend.data,
            form.profitMargin.data,
            form.averageEmployeeSalary.data
        ]

        # Define the payload for scoring
        payload_scoring = {
            "input_data": [{
                "fields": [
                    "burnRate", "revenue", "customerAcquisitionCost",
                    "customerLifetimeValue", "monthlyRecurringRevenue", "churnRate",
                    "marketGrowthRate", "marketingSpend", "rdSpend",
                    "profitMargin", "averageEmployeeSalary"
                ],
                "values": [userInput]
            }]
        }

        # Make the POST request to the IBM Watson API
        response_scoring = requests.post(
            "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b1c2c67c-442c-4fba-8545-d59df83f7bd7/predictions",
            json=payload_scoring,
            headers=header
        )

        # Parse the JSON response
        output = response_scoring.json()

        # Extract the prediction from the response
        prediction = output.get("predictions", [])

        if prediction:
            estimated_annual_profit = round(prediction[0]["values"][0][0], 2)
            form.abc = estimated_annual_profit  # Store the prediction in the form

        return render_template('index.html', form=form)

    return render_template('index.html', form=form)

@app.route('/chat')
def chat():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
