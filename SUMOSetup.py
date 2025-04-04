#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
import traci
import pandas as pd

# 🚦 Configure SUMO Paths
sumo_home = "C:\\Program Files (x86)\\Eclipse\\Sumo"
os.environ["SUMO_HOME"] = sumo_home
tools = os.path.join(sumo_home, "tools")
sys.path.append(tools)

print("✅ SUMO path configured successfully!")

# 🚗 Start SUMO
sumo_binary = "sumo-gui"  # Use "sumo" for command-line mode
sumo_config = "simulation.sumocfg"
traci.start([sumo_binary, "-c", sumo_config])
print("✅ SUMO started successfully!")

# 📊 Data storage
data = {
    "step": [],
    "vehicle_id": [],
    "speed": [],
    "acceleration": [],
    "distance_traveled": [],
    "time_in_simulation": []
}

# Track when vehicles enter the simulation
vehicle_entry_time = {}

# ⏳ Run Simulation Loop
step = 0
while step < 100:  # Run for 100 steps
    traci.simulationStep()  # Advance simulation

    # Collect vehicle data
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle in vehicle_ids:
        speed = traci.vehicle.getSpeed(vehicle)
        acceleration = traci.vehicle.getAcceleration(vehicle)
        distance = traci.vehicle.getDistance(vehicle)

        # Record first appearance of vehicle
        if vehicle not in vehicle_entry_time:
            vehicle_entry_time[vehicle] = step

        time_in_simulation = step - vehicle_entry_time[vehicle]

        # Store data
        data["step"].append(step)
        data["vehicle_id"].append(vehicle)
        data["speed"].append(speed)
        data["acceleration"].append(acceleration)
        data["distance_traveled"].append(distance)
        data["time_in_simulation"].append(time_in_simulation)

    print(f"Step: {step}, Vehicles: {len(vehicle_ids)}")
    step += 1

print("✅ Simulation completed!")

# 💾 Save Data to CSV
df = pd.DataFrame(data)
df.to_csv("simulation_data.csv", index=False)
print("✅ Data saved to simulation_data.csv")


# In[ ]:




