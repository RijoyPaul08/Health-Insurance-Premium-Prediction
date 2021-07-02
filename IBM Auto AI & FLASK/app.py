
import numpy as np
from flask import Flask, request, jsonify, render_template
import requests

import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "_oeMprisZeAZ4QbKZ4LZP9CJphNowwDuiqrkh7l9iSkg"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}
#age_data,gender_data,bmi_data,children_data,smoker_data,region_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    
    age_data =request.form['age']
    gender_data=request.form['gender']
    bmi_data = request.form['bmi']
    children_data = request.form['children']
    smoker_data = request.form['smoker']
    region_data = request.form['region']


    t = [[int(age_data),gender_data,float(bmi_data),int(children_data),smoker_data,region_data]]
    print(t)
    #[age_data,gender_data,bmi_data,children_data,smoker_data,region_data]
    payload_scoring = {"input_data": [{"fields": [["age","sex","bmi","children","smoker","region"]], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d95524c0-a82a-476a-b99d-868cb0598712/predictions?version=2021-06-26', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    #print("",Scoring response)
    #print("Display1",response_scoring)
    #print("Display2",response_scoring.json())
    pred_response = response_scoring.json()
    #print("Display3",pred_response)
    
    pred_Outputvalue = pred_response['predictions'][0]['values'][0][0]
    pred_Outputvalue=str(round(pred_Outputvalue, 2))
    pred_Outputvalue='Rs. '+pred_Outputvalue
    print("Output Predicted",pred_Outputvalue)
    
    
    #pred_Outputvalue = pred_response.predictions[0].values[0][0]
    #print("Display5",pred_Outputvalue)
  
    return render_template('index.html', prediction_text=pred_Outputvalue)


if __name__ == "__main__":
    app.run(debug=False)