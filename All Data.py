import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data
pv_data = pd.read_csv(r"C:\Users\Ismail\OneDrive\Documents\WiWi 23 24\Coordination of Distributed Resources in Renewable Energy Systems\Project\data\PV_data_15min.csv") # PV output in watts
load_data = pd.read_csv(r"C:\Users\Ismail\OneDrive\Documents\WiWi 23 24\Coordination of Distributed Resources in Renewable Energy Systems\Project\data\Load_data_15min.csv") # Load consumption in watts

# Convert data to numeric
pv_data['data.PV'] = pd.to_numeric(pv_data['data.PV']) # Replace '<column_name>' with the actual column name containing PV output
load_data['data.Load'] = pd.to_numeric(load_data['data.Load']) # Replace '<column_name>' with the actual column name containing load consumption
#net_gen[t] = pv_data.iloc[t]['data.PV'] - load_data.iloc[t]['data.Load']
time_steps = len(pv_data) # Number of time steps (assuming it's the same for both PV and load data)

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
discharge = np.zeros(time_steps) # Battery power to load or grid
pv_charge = np.zeros(time_steps) # PV power to charge battery
export = np.zeros(time_steps) # PV power to grid
imported = np.zeros(time_steps) # Grid power imported

# Main loop
for t in range(time_steps):
    net_gen[t] = pv_data.iloc[t]['data.PV'] - load_data.iloc[t]['data.Load'] # Net generation at time t
    if ctrl_action[t] == 1: # Charge
        if net_gen[t] >= 0: # Surplus PV
            grid_to_load[t] = 0 # No grid power to load
            grid_charge[t] = 0 # No grid power to charge battery
            discharge[t] = 0 # No battery power to load or grid
            pv_charge[t] = min(net_gen[t], batt_cap_max - batt_cap[t], max_batt_io) # PV power to charge battery
            export[t] = net_gen[t] - pv_charge[t] # PV power to grid
        if net_gen[t] < 0: # Deficit PV
            grid_to_load[t] = -net_gen[t] # Grid power to load
            discharge[t] = 0 # No battery power to load or grid
            pv_charge[t] = 0 # No PV power to charge battery
            export[t] = 0 # No PV power to grid
            grid_charge[t] = min(batt_cap_max - batt_cap[t], max_batt_io) # Grid power to charge battery
    if ctrl_action[t] == 0: # Discharge
        if net_gen[t] >= 0: # Surplus PV
            grid_to_load[t] = 0 # No grid power to load
            grid_charge[t] = 0 # No grid power to charge battery
            discharge[t] = 0 # No battery power to load or grid
            pv_charge[t] = 0 # No PV power to charge battery
            export[t] = net_gen[t] # PV power to grid
        if net_gen[t] < 0: # Deficit PV
            grid_to_load[t] = -net_gen[t] # Grid power to load
            grid_charge[t] = 0 # No grid power to charge battery
            pv_charge[t] = 0 # No PV power to charge battery
            export[t] = 0 # No PV power to grid
            discharge[t] = min(-net_gen[t], batt_cap[t], max_batt_io) # Battery power to load or grid
    batt_cap[t+1] = batt_cap[t] + pv_charge[t] + grid_charge[t] - discharge[t] # State of charge at time t+1
    imported[t] = grid_to_load[t] + grid_charge[t] # Grid power imported at time t

# Plotting
plt.figure(figsize=(10, 6))

# Plot PV output, load consumption, and net generation
plt.plot(pv_data['data.PV'], label='PV Output')
plt.plot(load_data['data.Load'], label='Load Consumption')
plt.plot(net_gen, label='Net Generation')

# Plot battery charge/discharge
plt.plot(pv_charge, label='PV Charge')
plt.plot(grid_charge, label='Grid Charge')
plt.plot(discharge, label='Discharge')

# Plot grid import/export
plt.plot(imported, label='Grid Import')
plt.plot(export, label='PV Export')

plt.xlabel('Time Step')
plt.ylabel('Power (W)')
plt.title('BSS Operation')
plt.legend()
plt.grid(True)
plt.show()
