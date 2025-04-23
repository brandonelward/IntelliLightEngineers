import streamlit as st
import pandas as pd
import numpy as np



#session_state variable setup
if "simdata" not in st.session_state:
    st.session_state.simdata = pd.DataFrame()

if "simStatus" not in st.session_state:
    st.session_state.simStatus = "N/A"

simdata = pd.DataFrame()


#page navigation
sim = st.Page("pages/Simulate.py")
simset = st.Page("pages/SimulationSetup.py")
data = st.Page("pages/Dataview.py")
#files = st.Page("pages/Files.py")



pages = [sim, data, simset]
pg = st.navigation(pages=pages)
pg.run()