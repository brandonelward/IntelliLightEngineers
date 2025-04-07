import streamlit as st
import os

def GetFilesInFolder(folderName):
    files = os.listdir(folderName)

    st.title("Files in " + folderName + ":")
    for file in files:
        if file.endswith(".sumocfg"):
            st.write(".SUMOCFG FILE: " + file)
        else:
            st.write(file)


folderSelector = st.selectbox("Which folder would you like to view: ", ("Simdata", "Output"))



GetFilesInFolder(folderSelector)
