import joblib
import numpy as np
from flask import Flask, request, jsonify, render_template
import pandas as pd
import random

app = Flask(__name__)
# Load saved models
knn_model = joblib.load('models/nate_knn.sav')

# Dictionary of all loaded models
loaded_models = {
    'knn': knn_model
}


# Function to decode predictions
def decode(pred):
    if pred == 1: return 'Exit'
    else: return 'Stay'


@app.route('/')
def home():
    first = request.args.get('first')
    return render_template('index.html', first=first)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/pred')
def pred():
    return render_template('predict.html')


@app.route("/getimage")
def get_img():
    return "/static/img/2.jpg"


@app.route('/predict', methods=['POST'])
def predict():

    # List values received from index
    values = [x for x in request.form.values()]
    print(values)
    # new_array - input to models
    new_array = np.array(values).reshape(1, -1)
    print(new_array)
    print(values)
    
    # Key names for customer dictionary custd
    cols = ['CreditScore',
            'Geography',
            'Gender',
            'Age',
            'Tenure',
            'Balance',
            'NumOfProducts',
            'HasCrCard',
            'IsActiveMember',
            'EstimatedSalary']

    print(cols)
    # Create customer dictionary
    custd = {}
    for k, v in zip(cols, values):
        custd[k] = v

    # Convert 1 or 0 to Yes or No  
    yn_val = ['HasCrCard', 'IsActiveMember']
    for val in yn_val:
        if custd[val] == '1': custd[val] = 'Yes'
        else: custd[val] = 'No'

    # save predictiond to the list
    predl = []
    for m in loaded_models.values():
        predl.append(decode(m.predict(new_array)[0]))

    if predl[0] == "Exit":
        my_list = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"]
        recommendations_list = random.sample(my_list, 2)
        recommendations = "Recommendations"
        recod_1 = recommendations_list[0]
        recod_2 = recommendations_list[1]
    else:
        recommendations = " "
        recod_1 = " "
        recod_2 = " "

    shape_img= "/static/img/2.jpg"       
    return render_template("predict.html",
                           pred_out=f"This customer will {predl[0]} \
                           in your branch",
                           recommendations=recommendations,
                           recod_1=recod_1, recod_2=recod_2,
                           shape_img=shape_img)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)
