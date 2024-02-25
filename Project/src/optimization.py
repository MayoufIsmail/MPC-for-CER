import numpy as np
from scipy.optimize import minimize
from scipy.sparse import csc_matrix

def PV_chrg(NetGen_t, BattCap_t, BattCapMax, MaxBattIo, Action_t):
    if Action_t == 1 and NetGen_t >= 0:
        return min(NetGen_t, BattCapMax - BattCap_t, MaxBattIo)
    else:
        return 0

def Grid_chrg(NetGen_t, BattCap_t, BattCapMax, MaxBattIo, Action_t):
    if Action_t == 1 and NetGen_t < 0:
        return min(BattCapMax - BattCap_t, MaxBattIo)
    else:
        return 0

def Dischrg_To_Load(NetGen_t, BattCap_t, MaxBattIo, Action_t):
    if Action_t == 0 and NetGen_t < 0:
        return min(-NetGen_t, BattCap_t, MaxBattIo)
    else:
        return 0

def Grid_To_Load(NetGen_t, Action_t):
    if (Action_t == 0 and NetGen_t < 0) or (Action_t == 1 and NetGen_t <= 0):
        return -NetGen_t
    else:
        return 0

def cost_function(x):
    return np.sum(x)

# Convert constraints to sparse matrix format
#sparse_constraints = [csc_matrix(con['jac'](np.ones(horizon), *con['args'])) for con in constraints]

# Solve optimization problem with sparse constraints
#res = minimize(objective, np.ones(horizon), bounds=bounds, constraints=sparse_constraints)

def MPC(PV_chrg, Grid_chrg, Dischrg_To_Load, Grid_To_Load, NetGen, BattCapMax, BattCap, MaxBattIo, Action,
        cost_function, constraints, horizon, **kwargs):
    bounds = [(0, 1) for _ in range(horizon)]  # Bounds for decision variables

    # Define objective function
    def objective(x):
        return cost_function(x)

    # Solve optimization problem
    res = minimize(objective, np.ones(horizon), bounds=bounds, constraints=constraints)

    # Convert constraints to sparse matrix format
    sparse_constraints = [csc_matrix(con['jac'](np.ones(horizon), *con['args'])) for con in constraints]

    # Extract optimal input
    optimal_input = res.x

    return optimal_input
