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
sim = st.Page("pages/Simulate.py", title="Simulate", icon="🔁")
simset = st.Page("pages/SimulationSetup.py", title="Setup", icon="🧰")
data = st.Page("pages/Dataview.py", title="Data", icon="📊")
#files = st.Page("pages/Files.py")



pages = [simset, sim, data]
pg = st.navigation(pages=pages)
pg.run()