# my_data = genfromtxt(csv_name, delimiter=',', dtype=None)
import pyodbc 
import os
        
server = 'lawdata.database.windows.net,1433'
database = 'CourtData'
username = os.getenv('LAW_DB_USER')
password = os.getenv('LAW_DB_PASS')
driver= '{ODBC Driver 17 for SQL Server}'
auth= 'ActiveDirectoryPassword'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';Authentication='+auth+';')
cursor = cnxn.cursor()
# os.environ['COURT_USER'] = 'AVADES01'
# os.environ['COURT_PASS'] = 'avades01'
# os.environ['LAW_DB_USER'] = 'dylan@albertazzilaw.com'
# os.environ['LAW_DB_PASS'] = 'Radtad234'
yay = 0