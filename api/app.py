from flask import Flask, jsonify, request
import os
import sys
from datetime import datetime, timedelta
import numpy as np
import joblib
from typing import Dict, List, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from experiments.sinregoutput import get_sinusoidal_params

app = Flask(__name__)

# In-memory storage for predictions history
prediction_history: List[Dict] = []

def get_minutes_from_week_start(timestamp: datetime) -> float:
    """
    Convert a timestamp to minutes from the start of the week (Monday 12 AM)
    """
    # Convert timestamp to datetime if it's a string
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    
    week_start = timestamp - timedelta(days=timestamp.weekday(), 
                                     hours=timestamp.hour,
                                     minutes=timestamp.minute,
                                     seconds=timestamp.second,
                                     microseconds=timestamp.microsecond)
    minutes_diff = (timestamp - week_start).total_seconds() / 60
    return minutes_diff

def predict_sinusoidal(minutes: float) -> float:
    """
    Make prediction using sinusoidal model
    """
    try:
        params = get_sinusoidal_params()
        # Use the sinusoidal model function
        return float(sinusoidal_model(minutes, *params))
    except Exception as e: 
        print(f"Error in predict_sinusoidal: {str(e)}")
        # Return a default prediction if there's an error
        return 50.0  # Default to 50% fullness

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "message": "ParkPredict API",
        "endpoints": {
            "/predict": "POST - Get parking prediction",
            "/predictions": "GET - Get prediction history",
            "/predictions/<garage>": "GET - Get predictions for specific garage",
            "/weights": "GET - Get model weights"
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Validate input
        if not all(k in data for k in ['timestamp', 'garage', 'model']):
            return jsonify({
                "error": "Missing required fields",
                "required_fields": ["timestamp", "garage", "model"]
            }), 400
        
        # Parse timestamp
        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            return jsonify({
                "error": "Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
            }), 400
        
        # Validate garage
        valid_garages = ["North Garage", "South Garage", "West Garage", "South Campus Garage"]
        if data['garage'] not in valid_garages:
            return jsonify({
                "error": "Invalid garage",
                "valid_garages": valid_garages
            }), 400
        
        # Get minutes from week start
        minutes = get_minutes_from_week_start(timestamp)
        
        # Get prediction
        if data['model'] == 'sinusoidal':
            prediction = predict_sinusoidal(minutes)
        else:
            return jsonify({
                "error": "Unsupported model type",
                "supported_models": ["sinusoidal"]
            }), 400
        
        # Store prediction in history
        prediction_record = {
            "timestamp": data['timestamp'],
            "garage": data['garage'],
            "predicted_fullness": float(prediction),
            "model_used": data['model'],
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
    Get the sinusoidal regression weights
    """
    try:
        params = get_sinusoidal_params()
        return jsonify({
            "sinusoidal_regression_weights": params.tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)