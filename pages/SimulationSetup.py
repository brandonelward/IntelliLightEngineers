import streamlit as st
import os
import xml.etree.cElementTree as ET

fp = os.path.dirname(__file__)

mapsFolder = os.path.join(os.path.dirname(fp), r"maps")
generatedFolder = os.path.join(os.path.dirname(fp), r"generated")

available_maps = os.listdir(generatedFolder)
available_maps = [sumocnfg for sumocnfg in available_maps if sumocnfg.endswith(".net.xml")]
map_select = st.selectbox(label="Simulation Map", options=available_maps)

simFileName = st.text_input(label="Scenario File Name")

#sim_duration_entry = st.number_input(label="Duration of simulation (timesteps)", min_value=10, max_value=99999, step=10)

def WriteSimulationFile(simName, networkFile, duration):
    routes = GenerateRoutesFile(networkFile, duration, simName)

    config = ET.Element("configuration")
    
    input = ET.SubElement(config, "input")
    time = ET.SubElement(config, "time")
    report = ET.SubElement(config, "report")

    ET.SubElement(input, 'net-file value="' + networkFile + '"')
    ET.SubElement(input, 'route-files value="' + str(routes) + '"')

    ET.SubElement(time, 'begin value="0"')
    ET.SubElement(time, 'end value="'+str(duration)+'"')

    ET.SubElement(report, 'collision-output value="collisions.xml"')

    tree = ET.ElementTree(config)
    fileName = os.path.join(generatedFolder, simName+".sumocfg")
    tree.write(fileName)

    st.write("Simulation file generated. " + fileName)


def GenerateRoutesFile(networkFile, duration, outName):
    routesPath = os.path.join(generatedFolder, outName+".trips.xml")
    randomTripsPath = os.path.join(os.path.dirname(fp), r"tools/randomTrips.py")
    inputNetFile = os.path.join(generatedFolder, networkFile)
    returnValue = os.system("python " + randomTripsPath + " -n "+ str(inputNetFile) +" -e "+ str(duration) + " -r "+ str(routesPath))
    st.write("Return Value: " + str(returnValue))
    st.write("Routes file Generated! " + str(routesPath))
    return routesPath

generateButton = st.button("Generate File")

if generateButton:
    filename=""
    if len(simFileName)  > 0:
        filename = simFileName
    else:
        filename = map_select.strip(".net.xml")

    with st.empty():
        WriteSimulationFile(simName=filename, networkFile=map_select, duration=5000)

