import streamlit as st

#overview
#setup page
#simulate page
#dataview page

st.title("Help Page")
st.header("Project Overview", divider=True)
st.markdown('''
This dashboard is designed to be a user friendly wrapper for the Simulation of Urban MObility (SUMO) suite of tools. The user is able to generate a simulation scenario with a selection of pre-generated maps. Then, the user will simulate the scenario with customisable parameters. Graphs and visualisations will be used to demonstrate the data gathered from the simulation.
''')
st.header("Pages", divider=True)
st.subheader("Setup")
st.markdown('''
1. Select one of the maps in the Simulation Map dropdown.
2. Give the scenario a recognisable name.
3. Click the Generate File button.
            
This will create a file that is stored locally and accessable through the Simulate page.
''')
st.subheader("Simulate")
st.markdown('''
1. Select the file generated from the Setup page.
2. Choose how long the simulation lasts.
3. Give the data a recognisable name.
4. If you want to watch the simulation in real-time, check the Simulation GUI checkbox.
            
This will give you a .csv file stored locally containing data gathered from the simulation. This data is accessable through the Data page.
''')
st.subheader("Data")
st.markdown('''
1. Select the file generated from the Simulate page.
2. Click the Generate Graphs button.
            
This will show graphs that use data from the chosen file.
''')