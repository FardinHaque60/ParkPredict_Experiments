from flask import Flask, jsonify, request, render_template
import os
import sys
from datetime import datetime, timedelta
import numpy as np
import joblib
from typing import Dict, List, Optional
from sklearn.ensemble import RandomForestRegressor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from experiments.sinregoutput import get_sinusoidal_params, sinusoidal_model

app = Flask(__name__)

# In-memory storage for predictions history
prediction_history: List[Dict] = []

# Dictionary to store sinusoidal parameters for each garage
sinusoidal_params = {}

# List of all available garages
ALL_GARAGES = ["North Garage", "South Garage", "West Garage", "South Campus Garage"]

def load_sinusoidal_params():
    """
    Load sinusoidal parameters for all garages
    """
    global sinusoidal_params
    try:
        params = get_sinusoidal_params()
        # Update the global parameters with all available garages
        sinusoidal_params = params
        print(f"Successfully loaded sinusoidal parameters for garages: {', '.join(params.keys())}")
        return True
    except Exception as e:
        print(f"Error loading sinusoidal parameters: {str(e)}")
        return False

def get_minutes_from_week_start(timestamp: datetime) -> float:
    """
    Convert a timestamp to minutes from the start of the week (Monday 12 AM)
    """
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    
    week_start = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = week_start - timedelta(days=timestamp.weekday())
    minutes_diff = (timestamp - week_start).total_seconds() / 60
    return minutes_diff

def predict_sinusoidal(minutes: float, garage: str) -> float:
    """
    Make prediction using sinusoidal model for specified garage
    """
    try:
        if garage not in sinusoidal_params:
            raise ValueError(f"Predictions not available for {garage}. Currently only supporting: {', '.join(sinusoidal_params.keys())}")
        
        params = sinusoidal_params[garage]
        prediction = sinusoidal_model(minutes, *params)
        return float(prediction)
    except Exception as e:
        print(f"Error in predict_sinusoidal: {str(e)}")
        raise

@app.route('/')
def home():
    # Load models if not already loaded
    if not sinusoidal_params:
        load_success = load_sinusoidal_params()
        if not load_success:
            return render_template('error.html', 
                                message="Failed to load prediction models. Please try again later.")
    
    return render_template('index.html', 
                         all_garages=ALL_GARAGES,
                         available_garages=list(sinusoidal_params.keys()),
                         prediction_history=prediction_history[-5:])  # Show last 5 predictions

@app.route('/load_models', methods=['POST'])
def load_models_endpoint():
    try:
        success = load_sinusoidal_params()
        if not success:
            return jsonify({
                "error": "Failed to load models. Please check the server logs for details."
            }), 500
            
        return jsonify({
            "status": "success",
            "message": "Sinusoidal parameters loaded successfully",
            "available_garages": list(sinusoidal_params.keys())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not sinusoidal_params:
            success = load_sinusoidal_params()
            if not success:
                return jsonify({
                    "error": "Failed to load models. Please try again later."
                }), 500
        
        data = request.get_json()
        
        if 'timestamp' not in data:
            return jsonify({
                "error": "Missing required field: timestamp"
            }), 400
            
        if 'garage' not in data:
            return jsonify({
                "error": "Missing required field: garage"
            }), 400
            
        if data['garage'] not in sinusoidal_params:
            return jsonify({
                "error": f"Predictions not available for {data['garage']}. Currently only supporting: {', '.join(sinusoidal_params.keys())}"
            }), 400
        
        # Parse timestamp
        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            return jsonify({
                "error": "Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
            }), 400
        
        # Get minutes from week start
        minutes = get_minutes_from_week_start(timestamp)
        
        # Make prediction
        prediction = predict_sinusoidal(minutes, data['garage'])
        
        # Store prediction in history
        prediction_record = {
            "timestamp": data['timestamp'],
            "garage": data['garage'],
            "predicted_fullness": prediction,
            "prediction_time": datetime.now().isoformat()
        }
        prediction_history.append(prediction_record)
        
        return jsonify(prediction_record)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predictions', methods=['GET'])
def get_predictions():
    """
    Get all prediction history
    Optional query parameters:
    - limit: maximum number of predictions to return
    - start_date: filter predictions after this date
    - end_date: filter predictions before this date
    """
    try:
        limit = request.args.get('limit', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        filtered_predictions = prediction_history
        
        # Apply date filters if provided
        if start_date:
            start_date = datetime.fromisoformat(start_date)
            filtered_predictions = [p for p in filtered_predictions 
                                 if datetime.fromisoformat(p['timestamp']) >= start_date]
        
        if end_date:
            end_date = datetime.fromisoformat(end_date)
            filtered_predictions = [p for p in filtered_predictions 
                                 if datetime.fromisoformat(p['timestamp']) <= end_date]
        
        # Apply limit if provided
        if limit:
            filtered_predictions = filtered_predictions[-limit:]
        
        return jsonify({
            "count": len(filtered_predictions),
            "predictions": filtered_predictions
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predictions/<garage>', methods=['GET'])
def get_garage_predictions(garage):
    """
    Get prediction history for a specific garage
    """
    try:
        garage_predictions = [p for p in prediction_history if p['garage'] == garage]
        return jsonify({
            "garage": garage,
            "count": len(garage_predictions),
            "predictions": garage_predictions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weights', methods=['GET'])
def weights_endpoint():
    """
    Get the sinusoidal regression weights for all garages
    """
    try:
        return jsonify({
            "sinusoidal_regression_weights": {
                garage: params.tolist() 
                for garage, params in sinusoidal_params.items()
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5001)