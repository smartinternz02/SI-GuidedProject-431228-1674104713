
from flask import Flask, render_template, request
import numpy as np
import pickle
import pandas as pd

# model = pickle.load(open(r"C:/Users/user/payments.pkl",'rb'))

app = Flask(__name__)

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "7nPw6r8tJxnZnPeATzKKr_2RwmleY94lY6TzsA7sFUK1"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route("/")
def about():
    return render_template('home.html')

@app.route("/home")
def about1():
    return render_template('home.html')

@app.route("/predict")      
def home1():
    return render_template('predict.html')

@app.route("/pred", methods=['POST','GET'])
def predict():
   x = [[x for x in request.form.values()]]
   print(x)
   # NOTE: manually define and pass the array(s) of values to be scored in the next line
   payload_scoring = {"input_data": [{"field": [["step","type","amount","oldbalanceOrg","newbalanceOrig","oldbalanceDest","newbalanceDest"]], "values":x}]}

   response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/45d58753-6745-46c3-a88f-36f5580cfd98/predictions?version=2022-06-27', json=payload_scoring,
   headers={'Authorization': 'Bearer ' + mltoken})
   predictions=response_scoring.json()
   pred = predictions['predictions'][0]['values'][0][0]
  
   print(pred[0])
   return render_template('submit.html', prediction_text=str(pred))

if __name__ == "__main__":
 app.run(debug=False)
