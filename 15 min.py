import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Data
pv_data = pd.read_csv(r"C:\Users\Ismail\OneDrive\Documents\WiWi 23 24\Coordination of Distributed Resources in Renewable Energy Systems\Project\data\PV_data_15min.csv") # PV output in watts
load_data = pd.read_csv(r"C:\Users\Ismail\OneDrive\Documents\WiWi 23 24\Coordination of Distributed Resources in Renewable Energy Systems\Project\data\Load_data_15min.csv") # Load consumption in watts

# Convert data to numeric
pv_data['data.PV'] = pd.to_numeric(pv_data['data.PV']) # Replace '<column_name>' with the actual column name containing PV output
load_data['data.Load'] = pd.to_numeric(load_data['data.Load']) # Replace '<column_name>' with the actual column name containing load consumption

# Number of time steps (assuming it's the same for both PV and load data)
time_steps = len(pv_data)

# BSS parameters
batt_cap_max = 12 * 1000 # Energy capacity in watt-hours
max_batt_io = 9 * 1000 # Maximum (dis-)charging power in watts
eff = 0.9 # Efficiency
batt_cap = np.zeros(time_steps + 1) # State of charge array
batt_cap[0] = 1.2 * 1000 # Initial state of charge in watt-hours

# Control action array
ctrl_action = np.random.choice([0, 1], size=time_steps) # Random charge/discharge actions

# Output arrays
net_gen = np.zeros(time_steps) # Net generation
grid_to_load = np.zeros(time_steps) # Grid power to load
grid_charge = np.zeros(time_steps) # Grid power to charge battery
discharge_to_load = np.zeros(time_steps) # Discharge power to load
discharge_to_grid = np.zeros(time_steps) # Discharge power to grid
imported = np.zeros(time_steps) # Imported power
pv_charge = np.zeros(time_steps) # PV power to charge battery

# Main loop
for t in range(time_steps):
    net_gen[t] = pv_data.iloc[t]['data.PV'] - load_data.iloc[t]['data.Load'] # Net generation at time t
    if ctrl_action[t] == 1: # Charge
        if net_gen[t] >= 0: # Surplus PV
            grid_to_load[t] = 0 # No grid power to load
            grid_charge[t] = 0 # No grid power to charge battery
            discharge_to_load[t] = 0 # No battery power to load
            discharge_to_grid[t] = 0 # No battery power to grid
            pv_charge[t] = min(net_gen[t], batt_cap_max - batt_cap[t], max_batt_io) # PV power to charge battery
        else: # Deficit PV
            grid_to_load[t] = -net_gen[t] # Grid power to load
            grid_charge[t] = 0 # No grid power to charge battery
            discharge_to_load[t] = min(-net_gen[t], batt_cap[t], max_batt_io) # Battery power to load
            discharge_to_grid[t] = 0 # No battery power to grid
    else: # Discharge
        if net_gen[t] >= 0: # Surplus PV
            grid_to_load[t] = 0 # No grid power to load
            grid_charge[t] = min(batt_cap_max - batt_cap[t], max_batt_io) # Grid power to charge battery
            discharge_to_load[t] = 0 # No battery power to load
            discharge_to_grid[t] = 0 # No battery power to grid
        else: # Deficit PV
            grid_to_load[t] = -net_gen[t] # Grid power to load
            grid_charge[t] = 0 # No grid power to charge battery
            discharge_to_load[t] = 0 # No battery power to load
            discharge_to_grid[t] = min(-net_gen[t], batt_cap[t], max_batt_io) # Battery power to grid
            
    # Battery capacity update
    batt_cap[t+1] = batt_cap[t] + pv_charge[t] + grid_charge[t] - discharge_to_load[t] - discharge_to_grid[t]
    
    # Imported power
    imported[t] = grid_to_load[t] + grid_charge[t]

# Cost-effective operation objective
electricity_rate = 0.12  # Assuming electricity rate of $0.12 per kWh
total_interval_cost = np.sum(imported * electricity_rate)

print("Total Interval Cost:", total_interval_cost)

# Plotting using Plotly
fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(x=np.arange(time_steps), y=pv_data['data.PV'], mode='lines', name='PV Output'))
fig.add_trace(go.Scatter(x=np.arange(time_steps), y=load_data['data.Load'], mode='lines', name='Load Consumption'))
fig.add_trace(go.Scatter(x=np.arange(time_steps), y=net_gen, mode='lines', name='Net Generation'))
fig.add_trace(go.Scatter(x=np.arange(time_steps), y=pv_charge, mode='lines', name='PV Charge'))
fig.add_trace(go.Scatter(x=np.arange(time_steps), y=grid_charge, mode='lines', name='Grid Charge'))
fig.add_trace(go.Scatter(x=np.arange(time_steps), y=discharge_to_load, mode='lines', name='Discharge to Load'))
fig.add_trace(go.Scatter(x=np.arange(time_steps), y=discharge_to_grid, mode='lines', name='Discharge to Grid'))
fig.add_trace(go.Scatter(x=np.arange(time_steps), y=imported, mode='lines', name='Imported Power'))

# Update layout
fig.update_layout(title='BSS Operation',
                  xaxis_title='Time Step',
                  yaxis_title='Power (W)',
                  legend_title='Data')

# Show plot
fig.show()
