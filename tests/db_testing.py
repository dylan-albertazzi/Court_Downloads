# import mysql.connector
# from mysql.connector import errorcode
import datetime
from datetime import datetime as dt
from datetime import timezone

import pyodbc
server = 'lawdata.database.windows.net,1433'
database = 'CourtData'
username = 'dylan@albertazzilaw.com'
password = 'Radtad234'
driver= '{ODBC Driver 17 for SQL Server}'
auth= 'ActiveDirectoryPassword'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';Authentication='+auth+';')
cursor = cnxn.cursor()

cursor.execute("""
select * from DocketRecords
""")



rows = cursor.fetchall()
with cnxn:
  cursor.execute("""
  insert into DocketRecords(CaseNo, Description, FileDate, County, CaseType, CreateDateUtc, CourtCaseId) values (?,?,?,?,?,?,?)""", '101','test', datetime.date(2019,12,3),'test','test', dt.now(timezone.utc),'3433')
  cnxn.commit()


#Insert row code completed, now implement into scraper code