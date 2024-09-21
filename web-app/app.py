from flask import Flask, render_template, request, jsonify
from forms import PredictForm
from forms import ChatForm
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3'  # Replace with a secure, randomly generated key

@app.route('/', methods=('GET', 'POST'))
def startApp():
    form = PredictForm()
    return render_template('index.html')

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()  # Form instance created outside the if-else block
    if request.method == "GET":
        return render_template("predict.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            # Replace the hardcoded Bearer token with your actual IAM API key
            header = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + "vznVGGOpyc-4aTXxPbUEazfI4fw8aFafdeFgk_QkVySd"
            }

            # Gather user inputs from the form
            userInput = [
                form.age.data,
                form.contract_length.data,
                form.customer_id.data,
                form.gender.data,
                form.last_interaction.data,
                form.payment_delay.data,
                form.subscription_type.data,
                form.support_calls.data,
                form.tenure.data,
                form.total_spend.data,
                form.usage_frequency.data
            ]

            # Define the payload for scoring
            payload_scoring = {
                "input_data": [{
                    "fields": [
                        "age", "contract_length", "customer_id", "gender", "last_interaction",
                        "payment_delay", "subscription_type", "support_calls", "tenure",
                        "total_spend", "usage_frequency"
                    ],
                    "values": [userInput]
                }]
            }

            # Make the POST request to the IBM Watson API
            response_scoring = requests.post(
                "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/customerchurnpredictor/predictions?version=2021-05-01",
                json=payload_scoring,
                headers=header
            )

            # Parse the JSON response
            output = response_scoring.json()

            # Extract the prediction from the response
            prediction = output.get("predictions", [])

            if prediction:
                churn_prediction = round(prediction[0]["values"][0][0], 2)
                form.churn_result = churn_prediction  # Store the prediction in the form

            return render_template('predict.html', form=form)
        
        # If form validation fails, re-render the template with error messages
        return render_template('predict.html', form=form, errors=form.errors)
    
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    response_text = ""  # Initialize a variable to hold the response
    error_message = ""  # Initialize a variable to hold any error message

    if request.method == "GET":
        return render_template("chat.html", response=response_text, error=error_message)  # Render the initial form

    # Handle POST request
    elif request.method == "POST":
        message = request.form.get('message')
        document = request.files.get('document')

        # Prepare request to the AI model
        url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        body = {
            "input": f"""<|system|>
            You are Granite Chat, an AI language model developed by IBM. You are a cautious assistant. You carefully follow instructions. You are helpful and harmless and you follow ethical guidelines and promote positive behavior. You always respond to greetings (for example, hi, hello, g'day, morning, afternoon, evening, night, what's up, nice to meet you, sup, etc) with "Hello! I am Granite Chat, created by IBM. How can I help you today?". Please do not say anything else and do not start a conversation.
            <|assistant|>
            {message}
            """,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 900,
                "repetition_penalty": 1.05
            },
            "model_id": "ibm/granite-13b-chat-v2",
            "project_id": "c66b34f5-b590-4197-96aa-37b821f93631",
            "moderations": {
                "hap": {
                    "input": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {
                            "remove_entity_value": True
                        }
                    },
                    "output": {
                        "enabled": True,
                        "threshold": 0.5,
                        "mask": {
                            "remove_entity_value": True
                        }
                    }
                }
            }
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJraWQiOiIyMDI0MDkwMjA4NDIiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02NjgwMDBYNjFPIiwiaWQiOiJJQk1pZC02NjgwMDBYNjFPIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiZjhkNTFlNjUtYzJlMy00YzZjLTg1MTEtZTU2MGFkMjMzY2M5IiwiaWRlbnRpZmllciI6IjY2ODAwMFg2MU8iLCJnaXZlbl9uYW1lIjoiUGFyaW4iLCJmYW1pbHlfbmFtZSI6IkFjaGFyeWEiLCJuYW1lIjoiUGFyaW4gQWNoYXJ5YSIsImVtYWlsIjoiYWNoYXJ5YXBhcmluMDVAZ21haWwuY29tIiwic3ViIjoiYWNoYXJ5YXBhcmluMDVAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoiYWNoYXJ5YXBhcmluMDVAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjY4MDAwWDYxTyIsIm5hbWUiOiJQYXJpbiBBY2hhcnlhIiwiZ2l2ZW5fbmFtZSI6IlBhcmluIiwiZmFtaWx5X25hbWUiOiJBY2hhcnlhIiwiZW1haWwiOiJhY2hhcnlhcGFyaW4wNUBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiYmFjN2E4NzUxZWU5NDk4NTk4NGFhMGZiNmM1N2YzOWQiLCJpbXNfdXNlcl9pZCI6IjEyNjkyMTg3IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyNzQ4MTIyIn0sImlhdCI6MTcyNjg3ODk3NiwiZXhwIjoxNzI2ODgyNTc2LCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL29pZGMvdG9rZW4iLCJncmFudF90eXBlIjoidXJuOmlibTpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTphcGlrZXkiLCJzY29wZSI6ImlibSBvcGVuaWQiLCJjbGllbnRfaWQiOiJkZWZhdWx0IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.kqsGFkFTCVjRb5aVHNZeY0FAxKQUfoH4UoGu7a11chettqlEq0UNHBHCfhp5ZlTay6eVATFZROiAbklzB1hc81n0pgnImCN8f4INbUhorDLBIvRhLPrCpEbNEg6Yy0uLlKGfVNdVwEgPle3ACKLAIMMQSxDx36t-lnSH1SqE4PQhtwVjQUtp2HrxwecsTJNtcmFGPgm7aLLoOwms8g38xNuNeshZ-xRPB8Bh_t2BjJOA9FVYVS2bgST5HCmJrJWjo0gx1lvut5iMSHqQzdV5efpuXNi7YIsGMufaxkCHHxpDdrEdn9Q-lyGtc5RXT_0iY4W-oUPIa7yPXbvv4UT8oQ"
        }

        # Make the request to the AI model
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # Raise an error for HTTP errors
            data = response.json()

            result = data.get('results', [{}])[0].get('generated_text', 'No response received')
            
            # Log the response
            logging.info(f'Response from Granite AI: {result}')

            # Set response_text to display in the form
            response_text = result
        except requests.exceptions.RequestException as e:
            error_message = f'An error occurred: {str(e)}'
            logging.error(error_message)  # Log the error

    return render_template('chat.html', response=response_text, error=error_message)  # Render the template with the response

if __name__ == '__main__':
    app.run(debug=True)