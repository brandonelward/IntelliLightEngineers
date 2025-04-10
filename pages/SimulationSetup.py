import streamlit as st
import os
import xml.etree.cElementTree as ET

fp = os.path.dirname(__file__)

available_maps = os.listdir(os.path.join(fp, '../maps'))
available_maps = [sumocnfg for sumocnfg in available_maps if sumocnfg.endswith(".net.xml")]
map_select = st.selectbox(label="Simulation Map", options=available_maps)

sim_duration_entry = st.number_input(label="Duration of simulation (timesteps)", min_value=10, max_value=99999, step=10)

def WriteSimulationFile(simName, networkFile, duration):
    routes = GenerateRoutesFile(networkFile, duration, simName)

    config = ET.Element("configuration")
    
    input = ET.SubElement(config, "input")
    time = ET.SubElement(config, "time")
    report = ET.SubElement(config, "report")

    ET.SubElement(input, 'net-file value="' + networkFile + '"')
    ET.SubElement(input, 'route-files value="' + routes + '"')

    ET.SubElement(time, 'begin value="0"')
    ET.SubElement(time, 'end value="'+duration+'"')

    ET.SubElement(report, 'collision-output value="collisions.xml"')

    tree = ET.ElementTree(config)
    fileName = os.path.join(fp, simName+".sumocfg")
    tree.write(fileName)

    st.write("Simulation file generated. " + fileName)


def GenerateRoutesFile(networkFile, duration, outName):
    routesPath = os.path.join(fp, '\\generated\\'+ outName+".rou.xml")
    os.system("C:/Program Files (x86)/Eclipse/Sumo/tools/randomTrips.py -n "+ str(networkFile) +" -e "+ str(duration)+" -o "+str(routesPath))
    st.write("Routes file Generated! " + routesPath)
    return routesPath

generateButton = st.button("Generate File")

if generateButton:
    WriteSimulationFile(simName=map_select.strip(".net.xml"), networkFile=map_select, duration=sim_duration_entry)

