import streamlit as st

import Simulation

# user inputs
sumo_config_entry = st.text_input(label="Sumo Config Filename (.sumocfg)")
sim_duration_entry = st.number_input(label="Duration of simulation (timesteps)", min_value=10, max_value=500, step=10)
sim_period_entry = st.number_input(label="Time Periods", min_value=2, max_value=50, step=1)
output_filename_entry = st.text_input(label="Output data file (.csv)")

submit_button = st.button("Simulate!")

if submit_button:
    simFile = "simdata/" + sumo_config_entry
    outFile = output_filename_entry
    dur = sim_duration_entry
    period = sim_period_entry

    simData = Simulation.runSimulation(simFile=simFile, outFile=outFile, stepCount=dur, periods=period)

    st.session_state.simData = simData