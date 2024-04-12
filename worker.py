from flask import Flask,request
import argparse
import threading 
import time
import pika
import mysql.connector
import json
import signal
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


mydb = mysql.connector.connect(
  host= "localhost",
  user= "root",
  password= "",
  database= "G2"
)
from scraper import *
def closeConn(signum, frame):
    connection.close()
    mydb.close()

signal.signal(signal.SIGINT, closeConn)
app = Flask(__name__) 
busy = 0
t = None
def scrapingWork(content):
    '''
    Parameters:
    Product title
    ('Simple','Load More','Pagination','Custom')
    '''
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

@app.route('/poll')
def polling():
    if t == None:
        return "1"
    else:
        if t.is_alive() == True:
            return "0"
        else:
            return "1"
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