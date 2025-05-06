import streamlit as st
import os

fp = os.path.dirname(__file__)
pagesFolder = os.path.join(os.path.dirname(fp), r"pages")

col1, col2, col3 = st.columns(3)
def pageLinks():
    st.page_link(page=os.path.join(pagesFolder, r"SimulationSetup.py"), icon="🧰", use_container_width=True)
    st.page_link(page=os.path.join(pagesFolder, r"Simulate.py"), icon="🔁", use_container_width=True)
    st.page_link(page=os.path.join(pagesFolder, r"Dataview.py"), icon="📊", use_container_width=True)
    st.page_link(page=os.path.join(pagesFolder, r"help.py"), icon="❓", use_container_width=True)
with col1:
    st.write(' ')
with col3:
    st.write(' ')

with col2:
    logo = st.image(image="logo.jpg", width=256)
    pageLinks()