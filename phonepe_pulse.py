import pandas as pd
import sqlite3
import streamlit as st
import plotly.express as px
import json
import numpy as np
#connect sqlite database
connect = sqlite3.connect('phonepe.db')
df = pd.read_sql_query("SELECT * from aggregated_name", connect)
 
#Create the dashboard
st.title("PhonePe Pulse Dashboard")
    
# User input
state = st.selectbox("Select a State", df['aggregate_name'].unique())
year = st.selectbox("Select a Year", df['year'].unique())
payment = st.selectbox("Select a payment", df['name'].unique())
     
# Filter user input data
filtered_df = df[(df['aggregate_name'] == state) & (df['year'] == year) & (df['name'] == payment)]
     
india_states = json.load(open("states_india.geojson", "r"))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]

df['scale']=np.log10(df['count']) 

fig = px.choropleth(
    df,
    locations="state_id",
    geojson=india_states,
    color="scale",
    hover_name="aggregate_name",
    hover_data=["count"],
    title="phonepe pulse data",
     )
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig, use_container_width=True)
