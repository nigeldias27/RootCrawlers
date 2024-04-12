import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
from datetime import date
import datetime
import json
import re
import pika
import mysql.connector

def soupfind(soup, tag):
    tagList = tag.split("|")
    typeOfTag = tagList[0]
    tagVal = tagList[1]
    tagEle = tagList[2] if len(tagList)==3 else None
    if typeOfTag =="CLASS_NAME":
        return soup.find_all(tagEle,class_= tagVal)
    elif typeOfTag =="ID":
        return soup.find_all(tagEle,id= tagVal)
    elif typeOfTag =="CSS_SELECTOR":
        return soup.select(tagVal)
def seleniumfind(browser, tag):
    tagList = tag.split("|")
    typeOfTag = tagList[0]
    tagVal = tagList[1]
    if typeOfTag =="CLASS_NAME":
        return browser.find_element(By.CLASS_NAME, tagVal)
    elif typeOfTag == "CSS_SELECTOR":
        return browser.find_element(By.CSS_SELECTOR,tagVal)
    elif typeOfTag == "XPATH":
        return browser.find_element(By.XPATH,tagVal)
    elif typeOfTag == "ID":
        return browser.find_element(By.ID,tagVal)
    elif typeOfTag == "NAME":
        return browser.find_element(By.NAME,tagVal)
    elif typeOfTag == "TAG_NAME":
        return browser.find_element(By.TAG_NAME,tagVal)
    elif typeOfTag == "LINK_TEXT":
        return browser.find_element(By.LINK_TEXT,tagVal)
    elif typeOfTag == "PARTIAL_LINK_TEXT":
        return browser.find_element(By.PARTIAL_LINK_TEXT,tagVal)
    

def checkG2Product(product,mydb):
    r = requests.get('https://data.g2.com/api/v1/products?filter[name]="'+product.replace(" ","+")+'"',headers={'Authorization':"Token b79944ecab1dbbfab91806e5b2e4856cf81d217dc8699e4da812af618130ccec"})
    g2Data = json.loads(r.text)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM GA_Products where ProductName='"+re.escape(product)+"'")

    myresult = mycursor.fetchall()

    if len(g2Data['data']) ==0 and len(myresult)==0:
        return False
    else:
        return True

def createFullURL(URL,href):
    if href[0] =="/":
        if URL[0:4] =="http":
            return '/'.join(URL.split("/")[0:3])+href
        else:
            return URL.split("/")[0]+href
    elif "http://" not in href and "https://" not in href:
        return "http://"+href
    else:
        return href
    



def plainwebscraper(URL,productElement,mydb,channel,linkElement=None):
    # Simple Web Scraping from a single page
    browser=webdriver.Chrome()
    browser.get(URL)
    soup = BeautifulSoup( browser.page_source , 'html.parser')
    if linkElement!=None:
        productLinkComboList = zip(soupfind(soup,productElement),soupfind(soup,linkElement))
        for productLink in productLinkComboList:
            productName = productLink[0].get_text()
            websiteLink = productLink[1].get_text()
            print(productName,websiteLink)
            if checkG2Product(productName,mydb)==False:
                    print(productName,websiteLink)
                    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=(createFullURL(linkElement,websiteLink)+' '+productName).encode('utf-8'))
    else:
        for productName in soupfind(soup,productElement):
            productName = productName.get_text()
            r = requests.get("https://autocomplete.clearbit.com/v1/companies/suggest?query="+productName.replace(" ","+"))
            websiteLink = r[0]['domain'] if r.length !=0 else ''
            print(productName,websiteLink)
    browser.close()


def loadMorewebscraper(URL,loadMoreButton,productElement,mydb,channel):
    # Keep clicking on the load more button until all the products are retrieved.
    browser=webdriver.Chrome()
    browser.get(URL)
    while(True):
        try:
            time.sleep(5)
            button = seleniumfind(browser,loadMoreButton)
            ActionChains(browser).scroll_to_element(button).click(button).perform()
        except:
            break
    time.sleep(5)
    soup = BeautifulSoup( browser.page_source , 'html.parser')
    for productText in soupfind(soup,productElement):
        productLink = productText.find("a",href=True)
        productLink = createFullURL(URL,productLink['href'])
        productText = productText.get_text()
        print(productText,productLink)
        if checkG2Product(productText,mydb)==False:
                    print(productText,productLink)
                    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=(productLink+' '+productText).encode('utf-8'))
    browser.close()


def paginationwebscraper(URL,paginationButton,productElement,mydb,channel):
    #Retrive all info on current page then move to next.
    browser=webdriver.Chrome()
    browser.get(URL)
    while(True):
        try:
            time.sleep(5)
            soup = BeautifulSoup( browser.page_source , 'html.parser')
            for productText in soupfind(soup,productElement):
                productLink = productText.find("a",href=True)
                productLink = createFullURL(URL,productLink['href'])
                productText = productText.get_text()
                if checkG2Product(productText,mydb)==False:
                    print(productText,productLink)
                    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=(productLink+' '+productText).encode('utf-8'))
                    
            
            button = seleniumfind(browser,paginationButton)
            ActionChains(browser).scroll_to_element(button).click(button).perform()
        except Exception as e:
            print(e)
            break
    browser.close()


#def linkedInScraper():
#def twitterScraper():

#plainwebscraper("https://growthlist.co/b2b-startups/","td","td")
#loadMorewebscraper("https://www.gartner.com/reviews/market/ai-augmented-software-testing-tools")
def customScraperWrapper(productText,productLink,mydb,channel):
    if checkG2Product(productText,mydb)==False:
        print(productText,productLink)
        channel.basic_publish(exchange='',
            routing_key='hello',
            body=(productLink+' '+productText).encode('utf-8'))

def customScraper(customScraperText,mydb,channel):
    exec(customScraperText)
