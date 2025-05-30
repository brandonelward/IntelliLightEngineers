import os
import shutil
import traci
import pandas as pd
import streamlit as st
import pyautogui

#Launches the SUMO system using user-defined parameters
def runSimulation(simFile, outFile, stepCount, gui, sumoHome):

    st.session_state.simStatus = "In Progress"

    print("sumoHome = " + str(st.session_state.sumoHome))

    sumo_mode = ""
    if gui:
        sumo_mode="sumo-gui"
    else:
        sumo_mode="sumo"

    configure(sumoHome)

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

    if gui:
        #Clean the images directory
        folder = "images/"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

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

        if gui: #Assume that if the gui is running, generate a heatmap
            takeScreenshot(imagesFolder="images/", step=step)


        with empty:
            st.write(f"step {step+1}/{stepCount}.")

    traci.close()
    st.write("Simulation Complete!")
    
    df = pd.DataFrame(data)
    df.to_csv(outFile, index=False)

    st.session_state.simStatus = "Finished"

    return df


def takeScreenshot(imagesFolder, step):
    filename = os.path.join(imagesFolder, f"screenshot_{step:04}.png")
    print(f"Taking screenshot {step}...")

    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

    print(f"Saved: {filename}")

#Configures SUMO environment variables
def configure(sumoHome):
    sumo_home = sumoHome.replace("/", "//")

    os.environ["SUMO_HOME"] = sumo_home
    return
