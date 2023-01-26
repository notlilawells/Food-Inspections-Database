import pymssql
import sys

servername = 'lilawells.database.windows.net'
login = 'ReadWriteUser'
pwd = 'nu!cs2022'
dbname = 'Food-Inspections'

print('**Trying to connect to Food-Inspections in Microsoft Azure cloud...')
print()

try:
  dbConn = pymssql.connect(server=servername,
                           user=login,
                           password=pwd,
                           database=dbname)
  print("**connected!")
except Exception as err:
  print("Error:", err)
  print("failed to connect :-(")
  sys.exit()
finally:
  print()

# additional code here

sql = """
      SELECT COUNT(Inspection_ID) FROM Inspections;
      SELECT COUNT(Store_ID) FROM Stores;
      """

dbCursor = dbConn.cursor()
dbCursor.execute(sql)
row = dbCursor.fetchone()

print('# of inspections: ', row[0])

dbCursor.nextset()  # skip to next result

row = dbCursor.fetchone()
print('# of food establishments: ', row[0])

print()
print('**Done')
dbConn.close()