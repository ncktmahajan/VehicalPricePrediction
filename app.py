from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input features from the form
        year = float(request.form['year'])
        present_price = float(request.form['present_price'])
        kms_driven = float(request.form['kms_driven'])
        fuel_type = request.form['fuel_type']
        seller_type = request.form['seller_type']
        transmission = request.form['transmission']
        owner = float(request.form['owner'])

        # Encode categorical variables
        if fuel_type == 'Petrol':
            fuel_type = 1
        elif fuel_type == 'Diesel':
            fuel_type = 0
        else:  # Assuming 'CNG'
            fuel_type = 2

        if seller_type == 'Individual':
            seller_type = 1
        else:  # Assuming 'Dealer'
            seller_type = 0

        if transmission == 'Manual':
            transmission = 1
        else:  # Assuming 'Automatic'
            transmission = 0

        # Create a feature array for prediction (7 features)
        features = np.array([[year, present_price, kms_driven, fuel_type, seller_type, transmission, owner]])

        # Make prediction
        prediction = model.predict(features)
        
        # Output result
        output = f'Estimated Selling Price: {prediction[0]:.2f} Lakh'

        return render_template('index.html', prediction_text=output)
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {e}')

if __name__ == "__main__":
    app.run(debug=True)
