from flask import Flask, render_template, request, jsonify
from forms import PredictForm
from forms import ChatForm
import requests
import json

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
    form = ChatForm()  # Initialize the form
    if request.method == 'POST' and form.validate_on_submit():
        message = form.message.data
        document = request.files.get('document')

        # Prepare request to the AI model
        url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        body = {
            "input": f"""<|system|>
            You are Granite Chat, an AI language model developed by IBM...
            <|assistant|>
            {message}
            """,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 900,
                "repetition_penalty": 1.05
            },
            "model_id": "ibm/granite-13b-chat-v2",
            "project_id": "acaf9312-4593-4343-b3c4-3ddd33f7f9e3",
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
            "Authorization": "Bearer NEW_ACCESS_TOKEN"  # Replace with your actual token
        }

        # Make the request to the AI model
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # Raise an error for HTTP errors
            data = response.json()
            
            result = data.get('results', [{}])[0].get('generated_text', 'No response received')
            return render_template('chat.html', form=form, response=result)  # Pass the result to the template
        except requests.exceptions.RequestException as e:
            return render_template('chat.html', form=form, error=f'An error occurred: {str(e)}')
    
    return render_template('chat.html', form=form)  # Render the template with the form

if __name__ == '__main__':
    app.run(debug=True)