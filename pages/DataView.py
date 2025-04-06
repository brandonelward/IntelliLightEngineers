import streamlit as st

def DrawTrafFlowChart(trafFlowData):
    # Traffic flow line chart    
    st.markdown("Traffic flow:")
    
    st.line_chart(trafFlowData, x_label="Time period", y_label="Cars per period")

def DrawCongestionBarChart(congData):
    # Congestion level bar chart
    st.markdown("Congestion Level:")

    st.bar_chart(congData, x_label="Time period", y_label="Avg. Idling Minutes/vehicle")

if (st.session_state.simStatus == "Finished"):
    traf_flow_data = st.session_state.simData["distance_traveled"]
    DrawTrafFlowChart(traf_flow_data)

    cong_data = st.session_state.simData["speed"]
    DrawCongestionBarChart(cong_data)

#Additional insights