import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix
from optimization import PV_chrg, Grid_chrg, Dischrg_To_Load, Grid_To_Load, cost_function, MPC

# Load data
load_data = pd.read_csv(r"C:\Users\Ismail\OneDrive\Documents\WiWi 23 24\Coordination of Distributed Resources in Renewable Energy Systems\Project\data\Load_data_15min.csv", parse_dates=["Time"])
PV_data = pd.read_csv(r"C:\Users\Ismail\OneDrive\Documents\WiWi 23 24\Coordination of Distributed Resources in Renewable Energy Systems\Project\data\PV_data_15min.csv", parse_dates=["Time"])

# Extract relevant columns
NetGen = PV_data["data.PV"] - load_data["data.Load"]

# Other parameters
horizon = len(NetGen)
BattCapMax = 12  # kWh
BattCapVar = np.ones(horizon) * 1.2  # Initial State of Charge (kWh)
MaxBattIo = 9  # kW

# Define constraints functions
def pv_chrg_constraint(x):
    return [PV_chrg(NetGen[t], BattCapVar[t], BattCapMax, MaxBattIo, x[t]) for t in range(horizon)]

def dischrg_to_load_constraint(x):
    return [Dischrg_To_Load(NetGen[t], BattCapVar[t], MaxBattIo, x[t]) for t in range(horizon)]

# Define constraints
constraints = [
    {'type': 'eq', 'fun': pv_chrg_constraint},  # PV Charging constraint
    {'type': 'eq', 'fun': dischrg_to_load_constraint},  # Discharge to Load constraint
]


sparse_constraints = [csc_matrix(con.get('jac', np.eye(horizon))(np.ones(horizon), *con['args'])) for con in constraints]


# Solve optimization problem with sparse constraints
res = minimize(objective, np.ones(horizon), bounds=bounds, constraints=sparse_constraints)
# Call MPC function with constraints
optimal_input = MPC(PV_chrg, Grid_chrg, Dischrg_To_Load, Grid_To_Load, NetGen, BattCapMax, BattCapVar, MaxBattIo, np.ones(horizon), cost_function, constraints, horizon, method='trust-constr')

# Display results or perform further actions based on optimal input
print("Optimal Input:", optimal_input)
