import streamlit as st
import pandas as pd
import numpy as np
import os

#session_state variable setup
if "simdata" not in st.session_state:
    st.session_state.simdata = pd.DataFrame()

if "simStatus" not in st.session_state:
    st.session_state.simStatus = "N/A"

fp = os.path.dirname(__file__)
pagesFolder = os.path.join(os.path.dirname(fp), r"pages")
def custom_pagelinks():
    #print(os.path.join(pagesFolder, r"Simulate.py"))
    menu = st.Page(page= os.path.join(pagesFolder, r"menu.py"), title="Menu", icon="📃")
    sim = st.Page(page = os.path.join(pagesFolder, r"Simulate.py"), title="Simulate", icon="🔁")
    simset = st.Page(page = os.path.join(pagesFolder, r"SimulationSetup.py"), title="Setup", icon="🧰")
    data = st.Page(page = os.path.join(pagesFolder, r"Dataview.py"), title="Data", icon="📊")
    help = st.Page(page=os.path.join(pagesFolder, r"help.py"), title="Help", icon="❓")
    st.navigation(pages=[menu,simset,sim,data,help]).run()


logo = st.sidebar.image(image="logo.jpg", use_container_width=True)
custom_pagelinks()