# experiments/sinregoutput.py
import os
import sys
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# So Python can find ../lib/data_load.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))
from data_load import load_data

def sinusoidal_model(x, A, B, C, D):
    """Example sinusoidal function for curve fitting."""
    return A * np.sin(B * x + C) + D

def get_sinusoidal_params():
    """
    Computes the sinusoidal regression weights (params) using your stored CSV data
    in the same way as your notebook.
    """
    try:
        date_start = pd.to_datetime("2025-04-13 12:00:00 AM")
        date_end = pd.to_datetime("2025-04-26 12:00:00 AM")
        
        # Get the absolute path to the data directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_folder_dir = os.path.join(current_dir, "..", "scrape", "out")
        
        if not os.path.exists(data_folder_dir):
            raise FileNotFoundError(f"Data directory not found at: {data_folder_dir}")
        
        # Load and filter data
        try:
            all_data = load_data(data_folder_dir=data_folder_dir, date_start=date_start, date_end=date_end)
        except Exception as e:
            raise RuntimeError(f"Failed to load data: {str(e)}")
        
        if all_data is None or all_data.empty:
            raise ValueError("No data loaded from the data directory")
        
        # Convert timestamp column to datetime if it's not already
        all_data['timestamp'] = pd.to_datetime(all_data['timestamp'])
        
        # Get unique garage names
        garage_names = all_data['garage name'].unique()
        if len(garage_names) == 0:
            raise ValueError("No garage data found in the dataset")
        
        # Dictionary to store parameters for each garage
        garage_params = {}
        
        # Process each garage
        for garage in garage_names:
            # Filter data for this garage
            garage_data = all_data[all_data['garage name'] == garage]
            if garage_data.empty:
                print(f"Warning: No data found for {garage}")
                continue
                
            # Filter by date range
            garage_data = garage_data[(garage_data['timestamp'] >= date_start) & 
                                    (garage_data['timestamp'] <= date_end)]
            if garage_data.empty:
                print(f"Warning: No data found for {garage} between {date_start} and {date_end}")
                continue
            
            # Convert timestamps to minutes after date_start
            garage_data['time'] = (garage_data['timestamp'] - date_start).dt.total_seconds() / 60
            
            x_data = garage_data['time']
            y_data = garage_data['fullness']
            
            if len(x_data) < 4:  # Need at least 4 points for curve fitting
                print(f"Warning: Not enough data points for {garage}. Found {len(x_data)} points.")
                continue
            
            # Initial guess for the fitting parameters
            initial_guess = [50, 0.005, 500, 50]
            
            # Perform the curve fit
            try:
                params, _ = curve_fit(sinusoidal_model, x_data, y_data, p0=initial_guess)
                garage_params[garage] = params
                print(f"Successfully fitted model for {garage}")
            except Exception as e:
                print(f"Warning: Failed to fit model for {garage}: {str(e)}")
                continue
        
        if not garage_params:
            raise ValueError("No models could be fitted for any garage")
            
        return garage_params
            
    except Exception as e:
        print(f"Error in get_sinusoidal_params: {str(e)}")
        # Return default parameters for North Garage if there's an error
        return {"North Garage": np.array([50, 0.005, 500, 50])}