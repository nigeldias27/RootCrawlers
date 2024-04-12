from flask import Flask,request
import argparse
import threading 
import time
import pika
import mysql.connector
import json
import signal

# Make Connections
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


mydb = mysql.connector.connect(
  host= "localhost",
  user= "root",
  password= "",
  database= "G2"
)
#Import standard scraper functions from scraper.py
from scraper import *

def closeConn(signum, frame):
    connection.close()
    mydb.close()
#Close connection on Cntrl+C interrupt
signal.signal(signal.SIGINT, closeConn)
app = Flask(__name__) 
busy = 0
t = None
def scrapingWork(content):
    # Perform web scraping based on type
    try:
        print(content)
        if content['Type']== 'Simple':
            plainwebscraper(content['Website'],content['ProductTag'],mydb,channel,content['LinkTag'])
        elif content['Type']== 'Load More':
            loadMorewebscraper(content['Website'],content['ClickTag'],content['ProductTag'],mydb,channel)
        elif content['Type']== 'Pagination':
            paginationwebscraper(content['Website'],content['ClickTag'],content['ProductTag'],mydb,channel)
        elif content['Type']== 'Custom':
            customScraper(content['Custom Scraper'],mydb,channel)
    except Exception as e:
        print(e)
        return e

# ROUTES
# Check if the worker is busy
@app.route('/poll')
def polling():
    if t == None:
        return "1"
    else:
        if t.is_alive() == True:
            return "0"
        else:
            return "1"
# Async request to perform scraping action
@app.route('/scrape', methods = ['POST']) 
def scraper():
    global t
    content = request.json
    print(content)

    t = threading.Thread(target=scrapingWork,args=(content,))
    t.start()
    return "Successfully Allocated"



if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument("portno",type=int)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.portno)