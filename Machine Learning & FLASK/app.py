
import numpy as np
from flask import Flask, request, jsonify, render_template
import requests
import json
import pickle

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}
#age_data,gender_data,bmi_data,children_data,smoker_data,region_data

app = Flask(__name__)
model = pickle.load(open('Insurance.pkl','rb'))
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


    t = [[int(age_data),int(gender_data),float(bmi_data),int(children_data),int(smoker_data),int(region_data)]]
    print(t)
    #[age_data,gender_data,bmi_data,children_data,smoker_data,region_data]
  
    prediction = model.predict(t)
    print(prediction)
    prediction=str(round(prediction[0],2))
    print(prediction)
    return render_template('index.html', prediction_text=prediction)


if __name__ == "__main__":
    app.run()