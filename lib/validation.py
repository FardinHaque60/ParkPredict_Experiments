import numpy as np

# calc rmse values by comparing predicted vals with raw_data['fullness']
# assuming raw_data is DataFrame with 'fullness' and normalized 'time' columns 
def rmse_validation(raw_data, predicted_vals):
    if len(raw_data) != len(predicted_vals):
        raise ValueError("Length of raw_data and predicted_vals must be the same.")

    # Calculate RMSE
    rmse = np.sqrt(np.mean((raw_data - predicted_vals) ** 2))
    return rmse