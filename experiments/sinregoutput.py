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
        date_start = pd.to_datetime("2025-03-10 12:00:00 AM")
        date_end = pd.to_datetime("2025-03-14 12:00:00 AM")
        
        # Adjust this path if necessary
        wdir = os.getcwd()
        data_folder_dir = os.path.join(wdir, "../scrape/out/")
        
        # Load and filter data
        all_data = load_data(data_folder_dir)
        
        # Convert timestamp column to datetime if it's not already
        all_data['timestamp'] = pd.to_datetime(all_data['timestamp'])
        
        north_data = all_data[all_data['garage name'] == "North Garage"]
        north_data = north_data[(north_data['timestamp'] >= date_start) & (north_data['timestamp'] <= date_end)]
        
        # Convert timestamps to minutes after date_start
        north_data['time'] = (north_data['timestamp'] - date_start).dt.total_seconds() / 60
        
        x_data = north_data['time']
        y_data = north_data['fullness']
        
        # Initial guess for the fitting parameters
        initial_guess = [50, 0.005, 500, 50]
        
        # Perform the curve fit
        params, _ = curve_fit(sinusoidal_model, x_data, y_data, p0=initial_guess)
        return params
    except Exception as e:
        print(f"Error in get_sinusoidal_params: {str(e)}")
        # Return default parameters if there's an error
        return np.array([50, 0.005, 500, 50])