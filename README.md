```python
# Inputs: ctrl_action, pv[t], load[t], batt_cap_max, max_batt_io
# ctrl_action = [0, 1] charge/discharge

net_gen[t] = pv[t] - load[t]

if ctrl_action[t] == 1:  # charge
    if net_gen[t] >= 0:
        grid_to_load[t] = 0
        grid_charge[t] = 0
        discharge[t] = 0
        pv_charge[t] = min(net_gen[t], batt_cap_max - batt_cap[t], max_batt_io)
        export[t] = net_gen[t] - pv_charge[t]

    if net_gen[t] < 0:
        grid_to_load[t] = -net_gen[t]
        discharge[t] = 0
        pv_charge[t] = 0
        export[t] = 0
        grid_charge[t] = min(batt_cap_max - batt_cap[t], max_batt_io)

if ctrl_action[t] == 0:  # discharge
    if net_gen[t] >= 0:
        grid_to_load[t] = 0
        grid_charge[t] = 0
        discharge[t] = 0
        pv_charge[t] = 0
        discharge_to_load[t] = 0
        discharge_to_grid[t] = 0
        export = net_gen[t]

    if net_gen[t] < 0:
        grid_to_load[t] = -net_gen[t]
        grid_charge[t] = 0
        pv_charge[t] = 0
        export[t] = 0
        discharge_to_grid[t] = 0
        discharge_to_load[t] = min(-netgen[t], batt_cap[t], max_batt_io)

batt_cap[t + 1] = batt_cap[t] + pv_charge[t] + grid_charge[t] - discharge_to_load[t] - discharge_to_grid[t]
imported[t] = grid_to_load[t] + grid_charge[t]
```