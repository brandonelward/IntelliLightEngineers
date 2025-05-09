import streamlit as st
import os
import pandas as pd

#https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values

outputFolderPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output"
possiblefiles = os.listdir(outputFolderPath)

fileSelector = st.selectbox("Which folder would you like to view: ", possiblefiles)

def DrawDistanceGraph(df, vehicleID):
    with col1:
        distanceData = df.loc[df["vehicle_id"] == vehicleID, "distance_traveled"]
        st.markdown("Distance")
        st.line_chart(distanceData, x_label="Simulation Step", y_label="Distance Travelled (meters)")

def DrawNoiseBarGraph(df, vehicleID):
    with col1:
        noiseData = df.loc[df["vehicle_id"] == vehicleID, "noise_emissions"]
        st.markdown("Noise:")
        st.bar_chart(noiseData, x_label="Simulation Step", y_label="Noise Emission (dB)")

def DrawCO2BarChart(df, vehicleID):
    with col2:
        co2Data = df.loc[df["vehicle_id"] == vehicleID, "co2_emissions"]
        st.markdown("CO2 Emission:")
        st.bar_chart(co2Data, x_label="Simulation Step", y_label="CO2 Emission (mg)")

def DrawWaitingTimeBarChart(df, vehicleID):
    with col2:
        waitingTimeData = df.loc[df["vehicle_id"] == vehicleID, "waiting_time"]
        st.markdown("Waiting time:")
        st.bar_chart(waitingTimeData, x_label="Simulation Step", y_label="Waiting Time (seconds)")


if fileSelector:
    df = pd.read_csv(os.path.join(outputFolderPath, fileSelector))
    uni_vehicle_ids = df['vehicle_id'].unique()

    vehicleIdSelector = st.selectbox("Choose VehicleID to analyse", uni_vehicle_ids)
    generateButton = st.button("Generate Graphs")

    if generateButton:
        st.markdown(f"Analysing Vehicle {vehicleIdSelector}:")
        col1, col2 = st.columns(2)
        if vehicleIdSelector in df['vehicle_id'].values:
            DrawDistanceGraph(df, vehicleIdSelector)
            DrawCO2BarChart(df, vehicleIdSelector)
            DrawNoiseBarGraph(df, vehicleIdSelector)
            DrawWaitingTimeBarChart(df, vehicleIdSelector)
        else:
            st.warning(f"Vehicle ID '{vehicleIdSelector}' not found in the selected data.")