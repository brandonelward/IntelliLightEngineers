import streamlit as st
import os
import pandas as pd

outputFolderPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output"
possiblefiles = os.listdir(outputFolderPath)


def DrawTrafFlowChart(filename):
    # Traffic flow line chart
    traf_flow_data = pd.read_csv(outputFolderPath+"/"+filename)["distance_traveled"]

    st.markdown("Traffic flow:")
    
    st.line_chart(traf_flow_data, x_label="Time period", y_label="Cars per period")

def DrawCongestionBarChart(filename):
    # Congestion level bar chart
    cong_data = pd.read_csv(outputFolderPath+"/"+filename)["speed"]

    st.markdown("Congestion Level:")

    st.bar_chart(cong_data, x_label="Time period", y_label="Avg. Idling Minutes/vehicle")

fileSelector = st.selectbox("Which folder would you like to view: ", possiblefiles)
generateButton = st.button("Generate Graphs")

if fileSelector and generateButton:
    DrawTrafFlowChart(fileSelector)
    DrawCongestionBarChart(fileSelector)

#Additional insights