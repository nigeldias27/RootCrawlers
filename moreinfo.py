from bs4 import BeautifulSoup
from selenium import webdriver
import mysql.connector
import re
import pika
import time
from datetime import datetime
from datetime import timedelta

mydb = mysql.connector.connect(
  host= "localhost",
  user= "root",
  password= "",
  database= "G2"
)
browser=webdriver.Chrome()
def sendEmail(emailId):
    print("Sent email to",emailId)
def emailSocialLink(soup):
    links = soup.find_all('a')
    socialLinks = {}
    for data in soup(['style', 'script']):
        data.decompose()
    r =  ' '.join(soup.stripped_strings)
    emailList = re.findall(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",r)
    
    if len(emailList) != 0:
        socialLinks['emailId'] = emailList[0] 
    for a in links:
        try:
            if 'facebook' in a['href']:
                socialLinks['facebook'] = a['href']
            if 'twitter' in a['href']:
                socialLinks['twitter'] = a['href']
            if 'linkedin' in a['href']:
                socialLinks['linkedin'] = a['href']
            if 'instagram' in a['href']:
                socialLinks['instagram'] = a['href']
        except:
            continue        
    return socialLinks

def visitLink(URL,ProductName):
    ProductName = re.escape(ProductName)
    browser.get(URL)
    # Removing HTML tags
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()
    r =  ' '.join(soup.stripped_strings)
    # Search for social media links and emailIDs in the text of the html (Typically at the footer of product page)
    socialLinks = emailSocialLink(soup)
    # If no social links exist, crawl the website for website links to visit
    if len(socialLinks)==0:    
        websiteLinks = re.findall(r'https?://(?:www\.)?[a-zA-Z0-9./]+',r) #Get emailID
        if len(websiteLinks)!=0:
            visitLink(websiteLinks)
    else:
        #Add social links data to the database.
        #Send emailId and update counter
        mycursor = mydb.cursor()
        if socialLinks.get("emailId")!=None:
            sendEmail(socialLinks.get("emailId"))
        val = (ProductName,socialLinks.get("emailId"),socialLinks.get("instagram"),socialLinks.get("facebook"),socialLinks.get("linkedin"),socialLinks.get("twitter"),URL,(datetime.now() + timedelta(days=5) ).strftime('%Y-%m-%d %H:%M:%S'))
        mycursor.execute("insert into GA_Products(ProductName,emailId,instagram,facebook,linkedin,twitter,website,lastContacted) values(%s,%s,%s,%s,%s,%s,%s,%s)" , val)
        mydb.commit()
        mycursor.close()
        return re.findall(r'https?://(?:www\.)?[a-zA-Z0-9./]+',r) #Get website Link
    


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    try:
        visitLink(body.decode('utf-8').split(' ')[0],' '.join(body.decode('utf-8').split(' ')[1:]))
    except Exception as e:
        print(e)
    channel.basic_ack(method.delivery_tag)

print(' [*] Waiting for messages. To exit press CTRL+C')

#channel.basic_consume('hello',callback,auto_ack=False)
while True:
    method_frame, header_frame, body = channel.basic_get(queue='hello',auto_ack=False)
    if method_frame:
        print(" [x] Received %r" % body)
        try:
            visitLink(body.decode('utf-8').split(' ')[0],' '.join(body.decode('utf-8').split(' ')[1:]))
        except Exception as e:
            print(e)
        channel.basic_ack(method_frame.delivery_tag)
    else:
        time.sleep(1)
#channel.start_consuming()
mydb.close()