import streamlit as st
import pandas as pd
import requests
import mysql.connector
import threading
import time
import json

def sendRequests(request,df):

    r = requests.post("http://127.0.0.1:8001/allocateWork",json=request)
    print("Work Allocated!")
    masterAlive="0"
    while(masterAlive=="0"):
        r = requests.get("http://127.0.0.1:8001/poll")
        print(r.text)
        masterAlive=r.text
        with open('../config.json') as configFile:
            configFile=json.loads(configFile.read())
            time.sleep(configFile['pollInterval'])
    df.loc[df["Select to Run"] == True, 'State'] = 'COMPLETED'
    df.loc[df["Select to Run"] == True, 'Select to Run'] = False
    df.to_csv('data.csv',index=False)
    st.rerun()
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

result_dataFrame = pd.DataFrame(
            data={
                "ProductName": [],"emailId": [],"instagram": [],"instagram": [],"facebook": [],"linkedin": [],"twitter":[],"lastContacted":[]
            }
        )
st.markdown("# RootCrawlers")
st.markdown("## Key Websites")

csv = pd.read_csv('data.csv')
#csv.insert(0, 'State', 'IDLE')
#csv.insert(0, 'Select to Run', False)
#if 'data' not in st.session_state:
#    st.session_state['data'] = csv
edited_df = st.data_editor(csv)
col1, col2, col3,col4 = st.columns([.15,.18,.15,.55])
with col1:

    if st.button("⚡ Run"):
        print("Running")
        filteredDf = edited_df[edited_df['Select to Run']==True]
        request = filteredDf.drop(['State','Select to Run'], axis=1).to_json(orient = 'records',lines = False)
        edited_df.loc[edited_df["Select to Run"] == True, 'State'] = 'EXECUTING'
        edited_df.to_csv('data.csv',index=False)
#        st.session_state['data']['Select to Run'] = edited_df['Select to Run']
#        st.session_state['data'].loc[edited_df["Select to Run"] == True, 'State'] = 'EXECUTING'
        t = threading.Thread(target=sendRequests,args=(request,edited_df))
        t.start()
        print(request)
        print(edited_df)
        st.rerun()
with col2:
    if st.button("🚀 Run All"):
        edited_df.loc[:, 'Select to Run'] = 'True'
        edited_df.loc[:, 'State'] = 'EXECUTING'
        edited_df.to_csv('data.csv',index=False)
        t = threading.Thread(target=sendRequests,args=(request,edited_df))
        t.start()
        print(request)
        print(edited_df)
        st.rerun()
        print("Running all")
with col3:
    if st.button("💾 Save"):
        edited_df.to_csv("data.csv",index=False)
        print("Save")
with col4:
    if st.button("⟳ Refresh"):
        st.rerun()
st.markdown("## GA Products and their Contact Data")
cols1, cols2,cols3 = st.columns([.8,.1,.1])
with cols1:
    searchInput = st.text_input("Search by Product Name")
with cols2:
    st.markdown(' ### ')
    
    search = st.button("🔎")
    if search:
        mydb = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "Leginsaid322$",
    database= "G2"
    )
        result_dataFrame = pd.read_sql("SELECT * FROM GA_Products where ProductName LIKE '%"+searchInput+"%'",mydb)
        mydb.close()
        
with cols3:
    st.markdown('### ')
    refresh = st.button("⟳")
    if refresh:
        mydb = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "Leginsaid322$",
    database= "G2"
    )
        result_dataFrame = pd.read_sql("SELECT * FROM GA_Products",mydb)
        mydb.close()


st.dataframe(result_dataFrame)