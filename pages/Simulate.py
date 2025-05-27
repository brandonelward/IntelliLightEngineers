import streamlit as st
import os
import Simulation

fp = os.path.dirname(__file__)

# user inputs
sumo_upload_entry = st.file_uploader(label="Upload Sumo Files (.sumocfg, .xml)")
if sumo_upload_entry is not None:

    save_path = os.path.join(os.path.join(fp, '../generated'), sumo_upload_entry.name)
    with open(save_path, "wb") as f:
        f.write(sumo_upload_entry.getbuffer())
    
    # Display the saved file path
    st.write(f"File saved at: {save_path}")


available_configs = os.listdir(os.path.join(fp, '../generated'))
available_configs = [sumocnfg for sumocnfg in available_configs if sumocnfg.endswith(".sumocfg")]
sumo_config_entry = st.selectbox(label="Sumo Config Filename (.sumocfg)", options=available_configs)



sim_duration_entry = st.number_input(label="Duration of simulation (max: 5000 timesteps)", min_value=10, max_value=5000, step=10)
#sim_period_entry = st.number_input(label="Time Periods", min_value=2, max_value=50, step=1)
output_filename_entry = st.text_input(label="Output data file name")
gui_toggle = st.checkbox("Generate Heatmap (open GUI while running)")

submit_button = st.button("Simulate!")

if submit_button:
    simFile = "generated/" + sumo_config_entry

    if len(output_filename_entry) <= 1:
        #if no outputFileName, output won't be called " .csv"
        split = sumo_config_entry.split(".")
        print(split)
        outFile = split[0]
    else:
        outFile = output_filename_entry

    
    dur = sim_duration_entry
    gui = gui_toggle
    sumohome = st.session_state.sumoHome

    simdata = Simulation.runSimulation(simFile=simFile, outFile=outFile, stepCount=dur, gui=gui, sumoHome=sumohome)

    st.session_state.simdata = simdata