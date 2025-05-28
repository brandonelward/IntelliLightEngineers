import os
import sys
import traci
import pandas as pd
import streamlit as st
from database import create_database

# Initialise the database file when this module is loaded
create_database.initialise_database()

#Launches the SUMO system using user-defined parameters
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
        "position_x": [],
        "position_y": [],
        "co2_emissions": [],
        "noise_emissions": [],
        "waiting_time": [],
        "lane_id": [],
        "emission_class": [],
        "time_loss": []
    }

    traci.start([sumo_mode, "-c", simFile])

    step=0

    empty = st.empty()

    for step in range(stepCount):
        traci.simulationStep()
        
        vehicle_ids = traci.vehicle.getIDList()
        for vehicle in vehicle_ids:
            speed = traci.vehicle.getSpeed(vehicle)
            acceleration = traci.vehicle.getAcceleration(vehicle)
            distance = traci.vehicle.getDistance(vehicle)
            position = traci.vehicle.getPosition(vehicle)
            co2 = traci.vehicle.getCO2Emission(vehicle)
            noise = traci.vehicle.getNoiseEmission(vehicle)
            wait = traci.vehicle.getWaitingTime(vehicle)
            lane_id = traci.vehicle.getLaneID(vehicle)
            emis_class = traci.vehicle.getEmissionClass(vehicle)
            time_loss = traci.vehicle.getTimeLoss(vehicle)

            # Store data
            data["step"].append(step)
            data["vehicle_id"].append(vehicle)
            data["speed"].append(speed)
            data["acceleration"].append(acceleration)
            data["distance_traveled"].append(distance)
            data["position_x"].append(position[0])
            data["position_y"].append(position[1])
            data["co2_emissions"].append(co2)
            data["noise_emissions"].append(noise)
            data["waiting_time"].append(wait)
            data["lane_id"].append(lane_id)
            data["emission_class"].append(emis_class)
            data["time_loss"].append(time_loss)

        with empty:
            st.write(f"step {step+1}/{stepCount}.")

    traci.close()
    st.write("Simulation Complete!")
    
    df = pd.DataFrame(data)
    df.to_csv(outFile, index=False) # Save to CSV


    simulation_name_for_db = os.path.splitext(os.path.basename(outFile))[0]

    if not df.empty:
        st.write(f"Saving simulation data to database table '{simulation_name_for_db}'...")
        create_database.save_dataframe_to_new_table(df, simulation_name_for_db)
    else:
        st.warning("No simulation data was generated or collected to save to the database.")


    st.session_state.simStatus = "Finished"

    return df


#Configures SUMO environment variables
def configure():
    sumo_home = "C:\\Users\\brand\\Documents\\SUMO"
    os.environ["SUMO_HOME"] = sumo_home
    return
