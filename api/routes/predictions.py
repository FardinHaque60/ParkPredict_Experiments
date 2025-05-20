from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from api.models.sinusoidal import predict_sinusoidal
from api.utils.time_utils import get_minutes_from_week_start
from api.utils.state import sinusoidal_params
from api.routes.main import load_sinusoidal_params

predictions_bp = Blueprint('predictions', __name__)

# In-memory storage for predictions history
prediction_history = []

@predictions_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Ensure models are loaded
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
        prediction = predict_sinusoidal(minutes, data['garage'], sinusoidal_params)
        
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

@predictions_bp.route('/predictions', methods=['GET'])
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

@predictions_bp.route('/predictions/<garage>', methods=['GET'])
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