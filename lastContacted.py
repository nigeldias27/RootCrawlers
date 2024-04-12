import mysql.connector
import time
from datetime import datetime
# Resends the mail if timeout is passed and the product is not on G2 yet.
mydb = mysql.connector.connect(
  host= "localhost",
  user= "root",
  password= "",
  database= "G2"
)
while True:
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM GA_Products order by lastContacted asc")

    myresult = mycursor.fetchone()

    mycursor.close()
    mostrecentDateTime= datetime.strptime(myresult[-1], '%Y-%m-%d %H:%M:%S')
    dateTimeNow = datetime.now()
    time.sleep((mostrecentDateTime -dateTimeNow).total_seconds())
    # TODO add function to actually send the mail when needed
    sendemail()
    mycursor = mydb.cursor()

    sql = "UPDATE GA_Products SET lastContacted = DATE_ADD(lastContacted,INTERVAL 7 DAY) WHERE ProductName = '"+myresult[0]+"'"

    mycursor.execute(sql)

    mydb.commit()