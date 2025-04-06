import os
import sys
import traci
import pandas as pd
import streamlit as st

def runSimulation(simFile, outFile, stepCount, periods):

    st.session_state.simStatus = "In Progress"

    configure()

    if (".sumocfg" not in simFile):
        simFile = simFile + ".sumocfg"

    if (".csv" not in outFile):
        outFile = outFile + ".csv"
    
    data = {
        "step": [],
        "vehicle_id": [],
        "speed": [],
        "acceleration": [],
        "distance_traveled": [],
    }

    traci.start(["sumo", "-c", simFile])

    st.write(f"step 0/{stepCount}.")

    for step in range(stepCount):
        traci.simulationStep()

        #do data collection
        stepUpdate = st.write(f"step {step+1}/{stepCount}.")

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

    traci.close()
    
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
