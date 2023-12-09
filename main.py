from energy_system import EnergySystem

def main():
    # Initialize Energy System
    energy_system = EnergySystem(batt_cap_max=100, max_batt_io=10)

    # Simulate Control Actions and Energy Flows
    energy_system.calculate_net_gen(pv=50, load=30)
    energy_system.charge_operation(ctrl_action=1)
    energy_system.update_battery_capacity()
    energy_system.update_imported_power()

    # Display Results
    print(f"Net Generation: {energy_system.net_gen}")
    print(f"Battery Capacity: {energy_system.batt_cap}")
    print(f"Imported Power: {energy_system.imported}")

if __name__ == "__main__":
    main()
