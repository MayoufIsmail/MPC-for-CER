# utils.py

import numpy as np
import pandas as pd

def load_data(file_path, parse_dates=None):
    """
    Load data from a CSV file using pandas.

    Parameters:
    - file_path (str): Path to the CSV file.
    - parse_dates (list, optional): List of column names to parse as dates.

    Returns:
    - pd.DataFrame: Loaded data.
    """
    return pd.read_csv(file_path, parse_dates=parse_dates)

def calculate_net_generation(pv_data, load_data):
    """
    Calculate the net generation by subtracting load from PV generation.

    Parameters:
    - pv_data (pd.DataFrame): DataFrame with PV generation data.
    - load_data (pd.DataFrame): DataFrame with load data.

    Returns:
    - pd.Series: Net generation.
    """
    return pv_data["PV_gen"] - load_data["data.Load"]

def create_constraints(constraint_functions, *args):
    """
    Create constraints for optimization.

    Parameters:
    - constraint_functions (list): List of constraint functions.
    - args (tuple): Additional arguments to be passed to each constraint function.

    Returns:
    - list: List of constraint dictionaries.
    """
    constraints = [{'type': 'eq', 'fun': constraint, 'args': args} for constraint in constraint_functions]
    return constraints

def print_optimal_input(optimal_input):
    """
    Print or display the optimal input.

    Parameters:
    - optimal_input (ndarray): Optimal input values.

    Returns:
    - None
    """
    print("Optimal Input:", optimal_input)

# Add more utility functions as needed
