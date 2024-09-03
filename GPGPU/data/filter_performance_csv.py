import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os  
from matplotlib.ticker import PercentFormatter
from scipy.optimize import curve_fit
base_path = '/home/cc/power/data/cpu_performance/'
# List of second header values you are interested in
desired_columns = ['Time','EXEC','INST','PhysIPC%', 'CFREQ', 'READ', 'WRITE', 'Proc Energy (Joules)', 'DRAM Energy (Joules)', 'UncFREQ (Ghz)']

# Function to filter and overwrite a CSV file
def filter_csv(file_path):
    # Read the CSV file with a two-row header
    df = pd.read_csv(file_path, header=[0, 1], on_bad_lines='skip')
    # Filter columns based on specified headers
    filtered_df = df.loc[:, (df.columns.get_level_values(0) == 'System') & (df.columns.get_level_values(1).isin(desired_columns))]
    # Save the filtered DataFrame back to CSV, overwriting the original file
    filtered_df.to_csv(file_path, index=False)

# Walk through each directory and subdirectory in the base_path
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.csv'):
            # Full path to the file
            full_file_path = os.path.join(root, file)
            # Filter the CSV file and overwrite
            filter_csv(full_file_path)