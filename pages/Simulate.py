import streamlit as st

import Simulation

# user inputs
sumo_config_entry = st.text_input(label="Sumo Config Filename (.sumocfg)")
sim_duration_entry = st.number_input(label="Duration of simulation (timesteps)", min_value=10, max_value=200, step=10)
#sim_period_entry = st.number_input(label="Time Periods", min_value=2, max_value=50, step=1)
output_filename_entry = st.text_input(label="Output data file (.csv)")
gui_toggle = st.checkbox("Simulation GUI")

submit_button = st.button("Simulate!")

if submit_button:
    simFile = "simdata/" + sumo_config_entry
    outFile = output_filename_entry
    dur = sim_duration_entry
    gui = gui_toggle

    simData = Simulation.runSimulation(simFile=simFile, outFile=outFile, stepCount=dur, gui=gui)

    st.session_state.simData = simData