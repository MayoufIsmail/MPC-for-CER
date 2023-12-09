class EnergySystem:
    def __init__(self, batt_cap_max, max_batt_io):
        self.batt_cap_max = batt_cap_max
        self.max_batt_io = max_batt_io
        self.batt_cap = 0
        self.net_gen = 0
        self.imported = 0
        self.grid_to_load = 0
        self.grid_charge = 0
        self.discharge = 0
        self.pv_charge = 0
        self.export = 0
        self.discharge_to_load = 0
        self.discharge_to_grid = 0

    def calculate_net_gen(self, pv, load):
        self.net_gen = pv - load

    def charge_operation(self, ctrl_action):
        if ctrl_action == 1:  # Charge
            if self.net_gen >= 0:
                self.grid_to_load = 0
                self.grid_charge = 0
                self.discharge = 0
                self.pv_charge = min(self.net_gen, self.batt_cap_max - self.batt_cap, self.max_batt_io)
                self.export = self.net_gen - self.pv_charge
            if self.net_gen < 0:
                self.grid_to_load = -self.net_gen
                self.discharge = 0
                self.pv_charge = 0
                self.export = 0
                self.grid_charge = min(self.batt_cap_max - self.batt_cap, self.max_batt_io)

    def discharge_operation(self, ctrl_action):
        if ctrl_action == 0:  # Discharge
            if self.net_gen >= 0:
                self.grid_to_load = 0
                self.grid_charge = 0
                self.discharge = 0
                self.pv_charge = 0
                self.discharge_to_load = 0
                self.discharge_to_grid = 0
                self.export = self.net_gen
            if self.net_gen < 0:
                self.grid_to_load = -self.net_gen
                self.grid_charge = 0
                self.pv_charge = 0
                self.export = 0
                self.discharge_to_grid = 0
                self.discharge_to_load = min(-self.net_gen, self.batt_cap, self.max_batt_io)

    def update_battery_capacity(self):
        self.batt_cap += self.pv_charge + self.grid_charge - self.discharge_to_load - self.discharge_to_grid

        if self.batt_cap > self.batt_cap_max:
            self.batt_cap = self.batt_cap_max
        elif self.batt_cap < 0:
            self.batt_cap = 0

    def update_imported_power(self):
        self.imported = self.grid_to_load + self.grid_charge
