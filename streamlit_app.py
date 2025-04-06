import streamlit as st
import pandas as pd
import numpy as np



#session_state variable setup
if "simData" not in st.session_state:
    st.session_state.simData = pd.DataFrame()

if "simStatus" not in st.session_state:
    st.session_state.simStatus = "N/A"

simData = pd.DataFrame()


#page navigation
sim = st.Page("pages/Simulate.py")
simset = st.Page("pages/SimulationSetup.py")
data = st.Page("pages/Dataview.py")

pages = [sim, simset, data]
pg = st.navigation(pages=pages)
pg.run()