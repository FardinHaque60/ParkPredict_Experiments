import numpy as np

# calc rmse values by comparing predicted vals with raw_data['fullness']
# assuming raw_data and predicted_vals are lists with expected and predicted values respectively
def rmse_validation(raw_data, predicted_vals):
    if len(raw_data) != len(predicted_vals):
        raise ValueError("Length of raw_data and predicted_vals must be the same.")

    # Calculate RMSE
    rmse = np.sqrt(np.mean((np.array(raw_data, dtype=float) - np.array(predicted_vals, dtype=float)) ** 2))
    return rmse

def mae_validation(raw_data, predicted_vals):
    if len(raw_data) != len(predicted_vals):
        raise ValueError("Length of raw_data and predicted_vals must be the same.")

    # Calculate MAE
    mae = np.mean(np.abs(np.array(raw_data, dtype=float) - np.array(predicted_vals, dtype=float)))
    return mae

def r2_validation(raw_data, predicted_vals):
    if len(raw_data) != len(predicted_vals):
        raise ValueError("Length of raw_data and predicted_vals must be the same.")

    # Calculate R^2
    ss_res = np.sum((np.array(raw_data, dtype=float) - np.array(predicted_vals, dtype=float)) ** 2)
    ss_tot = np.sum((np.array(raw_data, dtype=float) - np.mean(raw_data, dtype=float)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return r2