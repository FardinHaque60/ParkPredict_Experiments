from flask import Flask, jsonify
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from experiments.sinusodial_regression import get_sinusoidal_params

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask API Test"

@app.route('/weights', methods=['GET'])
def weights_endpoint():
    """
    Simple endpoint to return the sinusoidal regression weights.
    """
    # Grab params from the function
    params = get_sinusoidal_params()  #numpy array
    
    # Convert them to a list so they can be JSON-serialized
    return jsonify({
        "sinusoidal_regression_weights": params.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)