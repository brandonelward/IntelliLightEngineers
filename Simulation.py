import os
import sys
import traci
import pandas as pd
import streamlit as st

def runSimulation(simFile, outFile, stepCount, gui):

    st.session_state.simStatus = "In Progress"

    sumo_mode = ""
    if gui:
        sumo_mode="sumo-gui"
    else:
        sumo_mode="sumo"

    configure()

    if (".sumocfg" not in simFile):
        simFile = simFile + ".sumocfg"

    if (".csv" not in outFile):
        outFile = outFile + ".csv"
    if ("output/" not in outFile):
        outFile = "output/" + outFile


    data = {
        "step": [],
        "vehicle_id": [],
        "speed": [],
        "acceleration": [],
        "distance_traveled": [],
    }

    traci.start([sumo_mode, "-c", simFile])

    step=0

    empty = st.empty()

    for step in range(stepCount):
        traci.simulationStep()

        #do data collection
        
        vehicle_ids = traci.vehicle.getIDList()
        for vehicle in vehicle_ids:
            speed = traci.vehicle.getSpeed(vehicle)
            acceleration = traci.vehicle.getAcceleration(vehicle)
            distance = traci.vehicle.getDistance(vehicle)

            # Store data
            data["step"].append(step)
            data["vehicle_id"].append(vehicle)
            data["speed"].append(speed)
            data["acceleration"].append(acceleration)
            data["distance_traveled"].append(distance)

        with empty:
            st.write(f"step {step+1}/{stepCount}.")

    traci.close()
    st.write("Simulation Complete!")
    
    df = pd.DataFrame(data)
    df.to_csv(outFile, index=False)

    st.session_state.simStatus = "Finished"

    return df

def configure():
    sumo_home = "C:\\Program Files (x86)\\Eclipse\\Sumo"
    os.environ["SUMO_HOME"] = sumo_home
    tools = os.path.join(sumo_home, "tools")
    sys.path.append(tools)
    return
