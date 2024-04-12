import streamlit as st
import csv
import re
st.title("Add Scraper")

website = st.text_input("Website")
typeOfScraper = st.selectbox('Type of scraper',('Simple','Load More','Pagination','Custom'))
productTag = st.text_input("Product Tag")
linkTag = st.text_input("Link Tag")
clickTag = st.text_input("Click Tag")
customScraper=''
if typeOfScraper =="Custom":
    customScraper = st.text_area("Custom Scraper")

submitbtn = st.button("Add")

if submitbtn:
    print([website,typeOfScraper,productTag,linkTag,clickTag,re.escape(customScraper)])
    with open("data.csv",'a') as fd:
        writer = csv.writer(fd)
        writer.writerow([False,"IDLE",website,typeOfScraper,productTag,linkTag,clickTag,re.escape(customScraper)])
    st.text("Record Added")