import mysql.connector
import time
from datetime import datetime
mydb = mysql.connector.connect(
  host= "localhost",
  user= "root",
  password= "Leginsaid322$",
  database= "G2"
)
while True:
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM GA_Products order by lastContacted asc")

    myresult = mycursor.fetchone()

    mycursor.close()
    mostrecentDateTime= datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    dateTimeNow = datetime.now()
    time.sleep((mostrecentDateTime -dateTimeNow).total_seconds())

    sendemail()
    mycursor = mydb.cursor()

    sql = "UPDATE GA_Products SET lastContacted = DATE_ADD(lastContacted,INTERVAL 7 DAY) WHERE ProductName = '"+myresult[0]+"'"

    mycursor.execute(sql)

    mydb.commit()