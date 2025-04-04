import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Set up the dashboard title and description
st.set_page_config(page_title="AI Traffic Simulation Dashboard", layout="wide")
st.title("🚦 AI-Powered 3D City Traffic Simulation Dashboard")
st.markdown("An interactive dashboard to visualize traffic patterns, AI optimizations, and congestion analysis.")

# Sidebar for user inputs
sumo_config_entry = st.sidebar.text_input(label="Sumo Config Filename (.cfg)")
sim_duration_entry = st.sidebar.number_input(label="Duration of simulation (timesteps)", min_value=10, max_value=500, step=10)
output_filename_entry = st.sidebar.text_input(label="Output data file (.csv)")

submit_button = st.sidebar.button("Submit")
if submit_button:
    #set attributes
    #run the SUMO sim
    st.sidebar.write("Running sim for: " + output_filename_entry)


    


# Traffic flow line chart



# Congestion level bar chart




# Additional insights