import streamlit as st
import os
import pandas as pd

#https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values

outputFolderPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output"
possiblefiles = os.listdir(outputFolderPath)

fileSelector = st.selectbox("Which folder would you like to view: ", possiblefiles)

def DrawDistanceGraph(df, vehicleID):
    with col1:
        # Traffic flow line chart
        distanceData = df["distance_traveled"]
        data = distanceData.loc[df["vehicle_id"] == vehicleID]

        st.markdown("Distance")
        
        st.line_chart(data, x_label="Time", y_label="Distance Travelled")

def DrawNoiseBarGraph(df, vehicleID):
    with col1:
        # Traffic flow line chart
        distanceData = df["noise_emissions"]
        data = distanceData.loc[df["vehicle_id"] == vehicleID]

        st.markdown("Noise:")
        
        st.bar_chart(data, x_label="Time", y_label="Noise Emission (db)")

def DrawCO2BarChart(df, vehicleID):
    with col2:
        # Congestion level bar chart
        co2Data = df["co2_emissions"]
        data = co2Data.loc[df["vehicle_id"] == vehicleID]

        st.markdown("CO2 Emission:")

        st.bar_chart(data, x_label="Time", y_label="CO2 Emission (mg)")

def DrawWaitingTimeBarChart(df, vehicleID):
    with col2:
        # Congestion level bar chart
        co2Data = df["waiting_time"]
        data = co2Data.loc[df["vehicle_id"] == vehicleID]

        st.markdown("Waiting time:")

        st.bar_chart(data, x_label="Simulation Time", y_label="Stationary Time (timesteps)")


if fileSelector:
    df = pd.read_csv(outputFolderPath+"/"+fileSelector)
    uni = df['vehicle_id'].unique()

    vehicleIdSelector = st.number_input(label = "Choose VehicleID to analyse", min_value=0, max_value=len(uni)-1)
    generateButton = st.button("Generate Graphs")

    if generateButton:
        st.markdown("Analysing Vehicle " + str(vehicleIdSelector) + ":")
        col1, col2 = st.columns(2)
        DrawDistanceGraph(df, vehicleIdSelector)
        DrawCO2BarChart(df, vehicleIdSelector)
        DrawNoiseBarGraph(df, vehicleIdSelector)
        DrawWaitingTimeBarChart(df, vehicleIdSelector)






