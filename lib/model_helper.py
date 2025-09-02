import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from validation import rmse_validation, mae_validation, r2_validation
import pickle
import joblib
from datetime import datetime

FIG_OUT_PATH = "./out/"

''' params:
- garage: garage name to select dataset from
- start/end_date: start and end date to select dataset from
- partition_details: deterministic/random and/or starting/last weeks if selecting partitioned dataset
    - expected to be "d_last", "d_starting", or "r"
- partition: training/test/validation dataset to choose from
'''
def load_and_format_data(garage, start_date, end_date, partition_details:str=None, partition=None):
     # read data
    data_loc = f"../datasets/{garage.replace(" ","_")}/{start_date}_{end_date}"
    if partition_details:
        data_loc += "_partitioned_" + partition_details + ".pkl"
    else:
        data_loc += "_set.pkl"

    garage_data_by_week = []
    with open(data_loc, "rb") as f:
        loaded_data = pickle.load(f)
        if partition_details:
            garage_data_by_week = loaded_data[partition] 
        else:
            garage_data_by_week = loaded_data
    
    # normalize all values in dfs to populate x_data and y_data
    x_data = []
    y_data = []
    start_dates = []
    ind = 0
    for df in garage_data_by_week:
        mon_to_thurs = df[df['timestamp'].dt.weekday != 4]
        ts = mon_to_thurs["timestamp"].iloc[0]
        start_dates.append(ts)
        monday = ts - pd.Timedelta(days=ts.weekday())
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)

        x_data.append((mon_to_thurs["timestamp"] - monday).dt.total_seconds() / 60)
        y_data.append(mon_to_thurs["fullness"])
        ind += 1
    return (x_data, y_data, start_dates)

def test_and_eval(garage, start_dates, x_data, y_data, model, model_weights=[]):
## plot predictions and expected values
    current_time_str = datetime.now().strftime("%m-%d-%Y_%I:%M_%p")

    # generate x_stream from start of monday to end of thursday
    x_end = pd.Timedelta(days=4).total_seconds() / 60
    all_x_vals = np.linspace(0, x_end, num=1000)
    
    for i in range(len(x_data)):
        plt.scatter(x_data[i], y_data[i], alpha=0.5, label=f'{start_dates[i]}')
        if len(model_weights) != 0:
            plt.scatter(x_data[i], model(pd.Series(x_data[i]), *model_weights), color='black', alpha=0.5)
        else:
            plt.scatter(x_data[i], model(x_data[i]), color='black', alpha=0.5)


    # plt.scatter(x_data, y_data, color='blue', alpha=0.5, label='raw data')
    # plt.scatter(x_data, model(pd.Series(x_data), *model_weights), color='orange', alpha=0.5, label='model values')
    if len(model_weights) != 0:
        plt.plot(all_x_vals, model(all_x_vals, *model_weights), color='red')
    else:
        plt.plot(all_x_vals, model(all_x_vals.reshape(-1, 1)), color='red')
    
    plt.xlabel('Time (minutes)')
    plt.ylabel('Fullness')
    plt.title(f'Predictions and Actual Fullness for {garage}')
    plt.legend(loc='upper right', bbox_to_anchor=(1.45, 1))
    plt.savefig(FIG_OUT_PATH + f"{current_time_str}_{garage}_{start_dates[0].strftime('%Y-%m-%d')}_plot.png", bbox_inches="tight")
    plt.show()

## plot difference plot using y_data in stat params
    for i in range(len(x_data)):
        y_pred = None
        if len(model_weights) != 0:
            y_pred = model(pd.Series(x_data[i]), *model_weights)
        else:
            y_pred = model(x_data[i]).flatten()
        plt.scatter(x_data[i], y_pred-y_data[i], alpha=0.5, label=f'{start_dates[i]}')

    plt.plot(all_x_vals, np.zeros_like(all_x_vals), color='red')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Difference (prediction - actual)')
    plt.title(f'Difference between predicted and actual fullness for {garage}')
    plt.legend(loc='upper right', bbox_to_anchor=(1.45, 1))
    plt.savefig(FIG_OUT_PATH + f"{current_time_str}_{garage}_{start_dates[0].strftime('%Y-%m-%d')}_residual.png", bbox_inches="tight")
    plt.show()

## compute stats
    flat_x_data = list(itertools.chain.from_iterable(x_data))
    y_pred = None
    if len(model_weights) != 0:
        y_pred = model(pd.Series(flat_x_data), *model_weights)
    else:
        y_pred = model(flat_x_data).flatten()
    stat_params = list(itertools.chain.from_iterable(y_data)), y_pred

    print(f"{garage} stats")
    print(f"r^2: {r2_validation(*stat_params)}")
    print(f"rmse: {mae_validation(*stat_params)}")
    print(f"mae: {rmse_validation(*stat_params)}\n\n")

def format_for_model(input:list):
    return np.array(input).reshape(-1, 1)

def export_models(model_name, full_models, partition_models):
    base_file_path = f"../models/{model_name}/"
    # export fully trained model
    with open(base_file_path + f"{model_name}.pkl", "wb") as f:
        pickle.dump(full_models, f)
    print("wrote fully trained models")

    # export partition trained models
    with open(base_file_path + f"{model_name}_p.pkl", "wb") as f:
        pickle.dump(partition_models, f)
    print("wrote partition trained models")

def export_models_with_joblib(model_name, full_models, partition_models):
    base_file_path = f"../joblib_models/{model_name}/"
    # export fully trained model
    joblib.dump(full_models, base_file_path + f"{model_name}.pkl")
    print("wrote fully trained models with joblib")

    # export partition trained models
    joblib.dump(partition_models, base_file_path + f"{model_name}_p.pkl")
    print("wrote partition trained models with joblib")