import streamlit as st
import os

fp = os.path.dirname(__file__)
pagesFolder = os.path.join(os.path.dirname(fp), r"pages")

col1, col2, col3 = st.columns(3)
def pageLinks():
    setup = st.page_link(page=os.path.join(pagesFolder, r"SimulationSetup.py"), icon="🧰")
    sim = st.page_link(page=os.path.join(pagesFolder, r"Simulate.py"), icon="🔁")
    data = st.page_link(page=os.path.join(pagesFolder, r"Dataview.py"), icon="📊")
    help = st.page_link(page=os.path.join(pagesFolder, r"help.py"), icon="❓")
with col1:
    st.write(' ')
with col3:
    st.write(' ')
    
with col2:
    logo = st.image(image="logo.jpg", width=200)
    pageLinks()