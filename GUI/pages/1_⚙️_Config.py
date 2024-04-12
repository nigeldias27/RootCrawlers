import streamlit as st
import json

st.set_page_config(page_title="Config", page_icon="⚙️")

st.title("Edit Config file")

with open("../config.json") as configFile:
    configFile=json.loads(configFile.read())
    newProductTimeout = st.text_input("Enter New Product Timeout:(Days)",value=str(configFile['newProductTimeout']))
    workerAlivenessTimout = st.text_input("Worker Aliveness Timeout:(Seconds)",value=str(configFile['workerAlivenessTimout']))
    pollInterval = st.text_input("Enter Poll Interval(Seconds)",value=str(configFile['pollInterval']))
    workers = st.text_input("Enter URL of all workers separated by ,",value=','.join(configFile['workers']))
    add = st.button("Update")
    if add:
        with open("../config.json", "w") as outfile: 
            json.dump({"newProductTimeout":int(newProductTimeout),
                    "workerAlivenessTimout":int(workerAlivenessTimout),
                    "pollInterval":int(pollInterval),
                    'workers':workers.split(',')}, outfile)