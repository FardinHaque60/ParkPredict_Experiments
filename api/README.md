# ParkPredict API

A Flask-based API for predicting parking lot fullness using sinusoidal regression models.

## Project Structure

```
ParkPredict/api/
├── app.py                 # Main application entry point
├── models/               # Model-related code
│   └── sinusoidal.py     # Sinusoidal model logic and prediction functions
├── routes/               # API routes
│   ├── main.py          # Main routes (home, model loading)
│   └── predictions.py    # Prediction-related routes
├── utils/               # Utility functions
│   ├── time_utils.py    # Time conversion utilities
│   └── state.py         # Shared application state
├── templates/           # HTML templates
└── static/             # Static files (CSS, JS)
```

## Components

### Models
- `models/sinusoidal.py`: Contains the sinusoidal regression model implementation
  - `sinusoidal_model()`: The base sinusoidal function for curve fitting
  - `predict_sinusoidal()`: Makes predictions using the fitted model

### Routes
- `routes/main.py`: Handles main application routes
  - `/`: Home page with prediction interface
  - `/load_models`: Endpoint to load/reload prediction models
  - `/weights`: Endpoint to get model weights

- `routes/predictions.py`: Handles prediction-related routes
  - `/predict`: Makes predictions for a given timestamp and garage
  - `/predictions`: Gets prediction history with optional filtering
  - `/predictions/<garage>`: Gets prediction history for a specific garage

### Utils
- `utils/time_utils.py`: Time-related utility functions
  - `get_minutes_from_week_start()`: Converts timestamps to minutes from week start

- `utils/state.py`: Shared application state
  - Stores sinusoidal parameters for all garages

## API Endpoints

### GET /
- Returns the main prediction interface
- Automatically loads models if not already loaded

### POST /load_models
- Reloads the sinusoidal regression models
- Returns success status and available garages

### GET /weights
- Returns the sinusoidal regression weights for all garages

### POST /predict
- Makes a prediction for a given timestamp and garage
- Required fields:
  - `timestamp`: ISO format timestamp (YYYY-MM-DDTHH:MM:SS)
  - `garage`: Garage name
- Returns prediction record with timestamp, garage, and predicted fullness

### GET /predictions
- Gets prediction history
- Optional query parameters:
  - `limit`: Maximum number of predictions to return
  - `start_date`: Filter predictions after this date
  - `end_date`: Filter predictions before this date

### GET /predictions/<garage>
- Gets prediction history for a specific garage

## Running the API

1. Ensure you have the required dependencies installed
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. The API will be available at `http://localhost:5001`

## Dependencies
- Flask
- NumPy
- Pandas
- SciPy