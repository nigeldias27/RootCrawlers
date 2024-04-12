# RootCrawlers

## Features

- Scraping information from the web takes a great deal of time if code is written for each website manually and is executed sequentially. Hence the distributed master-slave approach is taken to execute a standard set of scrapers simultaneously.
  If needed, an option is available to execute custom scraper code.
- Segregation of Appraisal and Discovery stages by passing the scraped data to a message queue (RabbitMQ) for consumers to retrieve contact details while scrapers continue executing. 
- Contact details are retrieved by looking for social media links and email ids in text part of the html since they are typically at the footer of product page. If it does not return the details, it crawls the website for subsequent website links to check.
- Contacting the companies by sending automated emails. At a given interval, the system rechecks if the contacted company has still not registered with G2 and resends an email.
- Creation of a GUI interface to allow admin/users to easily access and edit any part of the system.

## Project Directory and File Info

- **GUI:** Consists of all the streamlit code.
  
  1. **gui.py:** Home page of the streamlit app where the user can send scrapers for execution and where the user can view all the scraped content.
  2. **pages/Config.py:** Allows a user to update the contents of the config.json file
  3. **pages/Add.py:** Adds a new scraper to the data.csv file.
- **master.py:** Distributes the scrapers among all the available workers.
- **worker.py:** Executes the scraper by filling in the parameters from standard scrapers in scraper.py or execute custom scraper. The scraped content i.e the generally available product name or website is sent moreInfo.py using a message queue (RabbitMQ)
- **scraper.py:** Standard scraper codes such as click on load more button, pagination button until all the content is retrieved.
- **moreinfo.py:** Information received from the message queue is passed like the website link is then crawled for subsequent links in the html text content until the contact info is received. The contact info is then stored in a relational database(MySQL).
- **emailService.py:** Code to send an automated email
- **lastContacted.py:** Code to check when the company has last contacted interval has been exceeded and the company has not registered their product yet on G2 to resend an email.

## Installation and Setup

1. Clone the Repo.
2. Installing the required libraries:
   `pip -r requirements.text`
3. Install chromedrivers from https://chromedriver.chromium.org for selenium
4. Install rabbitmq from https://www.rabbitmq.com/docs/download
5. Install mysql and run the create.sql script to create the database and table.
6. Change the mysql connector info at Line 10 in moreinfo.py, at Line 17 in worker.py and at Line 90 and 103 in GUI/gui.py .(Soon to be added to the config file)
7. Change the email info in emailService.py .(Soon to be added to the config file)

## How to Run

1. Start rabbitmq
   On macos `brew services start rabbitmq`
   To stop: `brew services stop rabbitmq`
1. Run the moreinfo.py
   `python3.10 moreinfo.py`
1. Running worker nodes
   `python3.10 worker.py <port no>`
   Note: Make sure to add the worker urls in config.json file.
1. Running master node
   `python3.10 master.py 8001`
1. Run Streamlit GUI Interface
   `python3.10 -m streamlit run gui.py`

- Run Email Service
  `python3.10 emailService.py`

## Future Work

- Experimenting with the use of LLMs on scraped data to increase the accuracy of finding contact details.
- Creating bots to contact Companies through methods other than email such as social media websites.
- Checking for new products from companies that have registered before.
- Once a critical mass of company responses are received, analytics can be performed to find the cause for the lack of visibility.
