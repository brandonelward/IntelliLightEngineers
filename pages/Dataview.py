import streamlit as st
import os
import pandas as pd
import plotly.express as px
from CV import CV

#https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-a-dataframe-based-on-column-values

outputFolderPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output"
possiblefiles = os.listdir(outputFolderPath)

fileSelector = st.selectbox("Which file would you like to view: ", possiblefiles)

def load_data(filename):
    df = pd.read_csv(os.path.join(outputFolderPath, filename))
    return df

def DrawSingleVehicleDistance(df, vehicleID, col):
    with col:
        distanceData = df.loc[df["vehicle_id"] == vehicleID, "distance_traveled"]
        st.markdown(f"Distance (Vehicle {vehicleID})")
        st.line_chart(distanceData, x_label="Simulation Step", y_label="Distance Travelled (meters)")

def DrawSingleVehicleNoise(df, vehicleID, col):
    with col:
        noiseData = df.loc[df["vehicle_id"] == vehicleID, "noise_emissions"]
        st.markdown(f"Noise (Vehicle {vehicleID}):")
        st.bar_chart(noiseData, x_label="Simulation Step", y_label="Noise Emission (dB)")

def DrawSingleVehicleCO2(df, vehicleID, col):
    with col:
        co2Data = df.loc[df["vehicle_id"] == vehicleID, "co2_emissions"]
        st.markdown(f"CO2 Emission (Vehicle {vehicleID}):")
        st.bar_chart(co2Data, x_label="Simulation Step", y_label="CO2 Emission (mg)")

def DrawSingleVehicleWaiting(df, vehicleID, col):
    with col:
        waitingTimeData = df.loc[df["vehicle_id"] == vehicleID, "waiting_time"]
        st.markdown(f"Waiting Time (Vehicle {vehicleID}):")
        st.bar_chart(waitingTimeData, x_label="Simulation Step", y_label="Waiting Time (seconds)")

def DrawComparisonChart(df, vehicle_ids, column, title, y_label):
    st.subheader(title)
    chart_data = pd.DataFrame()
    for vid in vehicle_ids:
        data = df.loc[df["vehicle_id"] == vid, ["step", column]].set_index("step")
        chart_data[f"Vehicle {vid}"] = data[column]
    st.line_chart(chart_data, y_label=y_label)

if fileSelector:
    df = load_data(fileSelector)
    unique_vehicle_ids = df['vehicle_id'].unique()

    # 1. General Simulation Insights
    st.header("General Simulation Insights")
    generate_general_button = st.button("Generate General Insights")

    if generate_general_button:
        st.subheader("General Insights:")
        col_gen1, col_gen2 = st.columns(2)
        with col_gen1:
            if 'emission_class' in df.columns:
                st.subheader("Emission Class Distribution")
                emission_counts = df['emission_class'].value_counts()
                fig_emission = px.pie(emission_counts, names=emission_counts.index, values=emission_counts.values, title='Emission Class Breakdown')
                st.plotly_chart(fig_emission)
            else:
                st.info("Emission class data not available.")

            if 'waiting_time' in df.columns and 'step' in df.columns:
                st.subheader("Average Waiting Time Over Time")
                avg_wait_time = df.groupby('step')['waiting_time'].mean()
                st.line_chart(avg_wait_time, y_label="Average Waiting Time (seconds)")
            else:
                st.info("Waiting time data not available.")

        with col_gen2:
            if 'co2_emissions' in df.columns and 'step' in df.columns:
                st.subheader("Average CO2 Emissions Over Time")
                avg_co2 = df.groupby('step')['co2_emissions'].mean()
                st.line_chart(avg_co2, y_label="Average CO2 Emissions (mg)")
            else:
                st.info("CO2 emissions data not available.")

            if 'time_loss' in df.columns:
                st.subheader("Total Time Loss")
                total_time_loss = df['time_loss'].sum()
                st.metric("Total Time Loss (Total for all vehicles)", f"{total_time_loss:.2f} seconds")
            else:
                st.info("Time loss data not available.")

    # 2. Single Vehicle Analysis
    st.header("Single Vehicle Analysis")
    single_vehicle_id = st.selectbox("Choose a VehicleID to analyse:", unique_vehicle_ids)
    generate_single_button = st.button("Generate Single Vehicle Graphs")

    if generate_single_button:
        st.markdown(f"### Analysing Vehicle {single_vehicle_id}:")
        col_sv1, col_sv2 = st.columns(2)
        if single_vehicle_id in df['vehicle_id'].values:
            DrawSingleVehicleDistance(df, single_vehicle_id, col_sv1)
            DrawSingleVehicleCO2(df, single_vehicle_id, col_sv2)
            DrawSingleVehicleNoise(df, single_vehicle_id, col_sv1)
            DrawSingleVehicleWaiting(df, single_vehicle_id, col_sv2)
        else:
            st.warning(f"Vehicle ID '{single_vehicle_id}' not found in the selected data.")

    # 3. Compare Multiple Vehicles
    st.header("Compare Multiple Vehicles")
    selected_vehicle_ids = st.multiselect("Choose VehicleIDs to compare:", unique_vehicle_ids)

    if selected_vehicle_ids:
        st.subheader("Comparison of Vehicle Metrics")
        DrawComparisonChart(df, selected_vehicle_ids, "speed", "Speed Comparison", "Speed (m/s)")
        DrawComparisonChart(df, selected_vehicle_ids, "co2_emissions", "CO2 Emission Comparison", "CO2 Emission (mg)")
        DrawComparisonChart(df, selected_vehicle_ids, "noise_emissions", "Noise Emission Comparison", "Noise Emission (dB)")
        DrawComparisonChart(df, selected_vehicle_ids, "waiting_time", "Waiting Time Comparison", "Waiting Time (seconds)")
        DrawComparisonChart(df, selected_vehicle_ids, "distance_traveled", "Distance Travelled Comparison", "Distance Travelled (meters)")


    #Add Heatmaps
    st.header("Heatmaps")
    heatmapButton = st.button("Generate Heatmap")
    heatmapPath = "heatmap.png"
    vidPath=""
    detect = CV.Detect()

    if heatmapButton:
        if len(os.listdir("images/")) <= 0:
            with st.empty():
                st.write("No images were taken, you should enable heatmap generation in Simulate")
        else:
            with st.empty():
                st.write("Generating Heatmap")
                detect.generate_detection_heatmap_from_images(image_dir="images/",output_path=heatmapPath)
                heatmapImage = st.image(heatmapPath)
