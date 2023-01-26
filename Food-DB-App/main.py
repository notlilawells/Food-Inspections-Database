import datatier
import pymssql
import math
import sys

############################################
# main
#
print('** Welcome to the Food Inspections app **')
print()

# Connecting to the database
servername = 'lilawells.database.windows.net'
login = 'ReadWriteUser'
pwd = 'nu!cs2022'
dbname = 'Food-Inspections'

try:
  dbConn = pymssql.connect(server=servername,
                           user=login,
                           password=pwd,
                           database=dbname)
  print("** You're now connected to the Food Inspections database **")

  print()
  print('A bit about your command options...')
  print()

  # Commands 1 through 8 
  print('Cmd 0: Information about the database and inputs')
  print('Cmd 1: Number of inspections and food establishments in the DB')
  print('Cmd 2: % of inspections in the database by inspection result')
  print('Cmd 3: Info on stores by store type')
  print('Cmd 4: Stores that failed inspection by store type')
  print('Cmd 5: Info on a stores inspections by store ID')
  print('Cmd 6: Look up stores that failed inspection by zip code')
  print('Cmd 7: Look up stores that passed inspection by zip code')
  print('Cmd 8: Find what % of store types passed inspection by zip code')
  print("Cmd 9: Find what % of a store's inspections it passed, failed, etc. by inputting the store ID")

except Exception as err:
  print("Error:", err)
  print("failed to connect :-(")
  sys.exit()
finally:
  print()

# Defining the DB cursor
dbCursor = dbConn.cursor()
  
# Printing command prompt
cmd = input('Please enter a command (1-9, x to exit): ')

# The while loop
while cmd != "x":
  # cmd 0 - info on db and inputs
  if cmd == "0":
    print() # adding a space btw cmd & output 
    sql0_p1 = """
              SELECT COUNT(Stores.Store_ID)
              FROM Stores; 
              """
    sql0_p2 = """
              SELECT COUNT(Inspection_ID)
              FROM Inspections;
              """

    sql0_p3 = """
              SELECT MIN(Inspection_Year), MAX(Inspection_Year) 
              FROM Inspections; 
              """
    row = datatier.select_one_row(dbConn, sql0_p1, [])
    num_stores = row[0]

    row1 = datatier.select_one_row(dbConn, sql0_p2, [])
    num_inspections = row1[0]

    dbCursor.execute(sql0_p3)
    yrs = dbCursor.fetchone()
    
    start_yr = yrs[0]
    end_yr = yrs[1]

    print('The food inspections database contains information on', f"{num_stores:,}", 'stores and', f"{num_inspections:,}", 'inspections in Chicago from', start_yr, 'to', end_yr, ". All data was downloaded and compiled from the City of Chicago's data portal. The data was collected by Chicago's Department of Public Health’s Food Protection Program using a standardized procedure. Their procedures and findings were then overseen and approved by a State of Illinois Licensed Environmental Health Practitioner (LEHP). Please visit the Chicago data portal at data.cityofchicago.org for more information on data collection procedures.")
  
  # cmd 1 - number of inspections and food establishments
  elif cmd == "1":
    # SQL for number of inspections and number of stores
    sql1_pt1 = """
               SELECT COUNT(Inspection_ID) FROM Inspections;
               """
    
    sql1_pt2 = """
               SELECT COUNT(Store_ID) FROM Stores;
               """

    # Using python to read the SQL
    row = datatier.select_one_row(dbConn, sql1_pt1, [])
    print("# of inspections", ":", f"{row[0]:,}")

    row = datatier.select_one_row(dbConn, sql1_pt2, [])
    print("# of food establishments", ":", f"{row[0]:,}")

  # cmd 2 - % of inspection results in DB by inspection type
  elif cmd == "2":
    
    # SQL for % of inspections by inspection type
    sql2_p1 = """
              SELECT COUNT(Inspection_ID) FROM Inspections;
              """

    sql2_p2 = """
              SELECT COUNT(Inspection_ID) FROM Inspections
               INNER JOIN Inspection_Results 
                  ON Inspections.Result_ID = Inspection_Results.Result_ID
               GROUP BY Inspection_Results.Result_ID; 
              """
    
    total = datatier.select_one_row(dbConn, sql2_p1, [])
    denom = total[0]

    dbCursor.execute(sql2_p2)
    rows = dbCursor.fetchall()

    # Printing the results with Python
    a = []
    for row in rows:
      a.append(round(row[0] / denom * 100, 2))

    print('% of inspections that passed', ':', str(a[0]) + '%')
    print('% of inspections that failed', ':', str(a[1]) + '%')
    print('% of inspections that passed with conditions', ':', str(a[2]) + '%')
    print('% of inspections that had no entry', ':', str(a[3]) + '%')
    print('% of inspections that were not ready', ':', str(a[4]) + '%')
    print('% of inspections that were out of business', ':', str(a[5]) + '%')

  # cmd 3 - enter store type
  # return id, name, zip, number of inspections
  elif cmd == "3":
    # cmd description
    print('** Input a store type to get the store ID, name, zip code, and number of inspections for each store in that type **')
    print() # adding a line btw command description & input
    type = input('Input the type of a food establishment (e.g. %Restaurant%): ')
    print() # adding a lin btw input & output
    sql3 = """
           SELECT Stores.Store_ID, Store_Name, Store_Type, COUNT(Inspection_ID)
             FROM Stores
            INNER JOIN Store_Types
               ON Stores.Store_Type_ID = Store_Types.Store_Type_ID
            INNER JOIN Inspections
               ON Stores.Store_ID = Inspections.Store_ID 
            INNER JOIN Inspection_Results
               ON Inspections.Result_ID = Inspection_Results.Result_ID
            WHERE Store_Type LIKE %s
         GROUP BY Stores.Store_ID, Store_Name, Store_Type;
           """

    dbCursor.execute(sql3, (type))
    rows = dbCursor.fetchall()

    if len(rows) == 0:
      print("No stores found in that type, try one from the following: ")
      print('  Restaurant')
      print('  Grocery Store')
      print('  School')
      print('  Hospital')
      print('  Daycare')

    else:
      more = "this can be anything but no"
      i = 0
      page = 1
      total = math.ceil(len(rows)/10)
      while more != "no" and more != "n":
        end = i + 10
        if end > len(rows):
          end = len(rows)
          for row in rows[i:end]:
            print(row[0], ':', row[1], ":", row[2], ': (# of inspections)', row[3])
          print()
          more = "no"
        else:
          for row in rows[i:end]:
            print(row[0], ':', row[1], ":", row[2], ': (# of inspections)', row[3])
          print()
          more = input("Display more? [yes/no]  [" + str(page) + ' of ' + str(total) + '] ') 
          i = i + 10
          page = page + 1

  # cmd 4 = input store type
  # returns stores in that type that failed inspections
  elif cmd == "4":
    # cmd description 
    print('** Input a store type to find stores in that type that failed inspection **')
    print() # adding a space btw cmd description and input 
    store_type = input('Input a store type (ex. %Restaurant%): ')
    print() # adding a space btw input & output 

    # SQL for output 
    sql4 = """
           SELECT Inspections.Store_ID, Store_Name, Zip_Code, Results
           FROM Inspections
           INNER JOIN Stores
           ON Inspections.Store_ID = Stores.Store_ID
           INNER JOIN Inspection_Results
           ON Inspections.Result_ID = Inspection_Results.Result_ID 
           INNER JOIN Store_Types
           ON Stores.Store_Type_ID = Store_Types.Store_Type_ID 
           WHERE Store_Type LIKE %s
           GROUP BY Inspections.Store_ID, Store_Name, Zip_Code, Results;
           """

    # Reading and printing output
    dbCursor.execute(sql4, store_type)
    rows = dbCursor.fetchall()
    
    if len(rows) == 0:
      print("No stores found in that type, try one from the following: ")
      print('  Restaurant')
      print('  Grocery Store')
      print('  School')
      print('  Hospital')
      print('  Daycare')

    elif len(rows) <= 10:
      for row in rows:
        print(row[0], ":", row[1], ":", row[2], ':', row[3])
    else:
      more = "this can be anything but no"
      i = 0
      page = 1
      total = math.ceil(len(rows)/10)
      while more != "no" and more != "n":
        end = i + 10
        if end > len(rows):
          end = len(rows)
          for row in rows[i:end]:
            print(row[0], ":", row[1], ':', row[2], ":", row[3])
          more = "no"
        else:
          for row in rows[i:end]:
            print(row[0], ":", row[1], ':', row[2], ":", row[3])
          print()
          more = input("Display more? [yes/no]  [" + str(page) + ' of ' + str(total) + '] ') 
          i = i + 10
          page = page + 1

  # cmd 5 - input store id
  # outputs info on store and its inspections
  elif cmd == "5":
    # cmd description 
    print('** Input a store ID to get information on that store and its inspections **')
    print() # adding a space btw cmd description and input 
    id = input('Enter a store ID (ex. 1 or 2): ')

    if int(id) < 0: # if input is negative 
      print('Invalid input (must be positive). Try any number from zero to 31362 instead.')
    elif int(id) > 31362: # invalid input 
      print('Input outside range of store IDs. Try any number from zero to 31362 instead.')
    else: # valid input 

      # SQL for the output 
      sql5_p1 = """
                SELECT Store_ID, Store_Type, Store_Name, License_Number, Address, Zip_Code
                FROM Stores
                INNER JOIN Store_Types
                ON Stores.Store_Type_ID = Store_Types.Store_Type_ID
                WHERE Stores.Store_ID = %s;
                """
      sql5_p2 = """
                SELECT COUNT(Inspection_ID)
                FROM Inspections
                INNER JOIN Stores
                ON Inspections.Store_ID = Stores.Store_ID
                WHERE Stores.Store_ID = %s;
                """
  
      sql5_p3 = """
                SELECT Inspection_Year, Inspection_Type, Results
                FROM Inspection_Results
                INNER JOIN Inspections
                ON Inspection_Results.Result_ID = Inspections.Result_ID 
                INNER JOIN Inspection_Types
                ON Inspections.Inspection_Type_ID = Inspection_Types.Inspection_Type_ID
                WHERE Store_ID = %s;
                """
  
      # Reading and displaying the results with Python
      dbCursor.execute(sql5_p1, (id))
      rows = dbCursor.fetchall()
  
      dbCursor.execute(sql5_p2, (id))
      rows2 = dbCursor.fetchall()
  
      dbCursor.execute(sql5_p3, (id))
      rows3 = dbCursor.fetchall()
  
      if len(rows) == 0:
        print("No store found")
      else:
        for row in rows:
          print()
          print('Store ID', ':', row[0])
          print('Store type', ':', row[1])
          print('Store name', ':', row[2])
          print('License number', ':', row[3])
          print('Address', ':', row[4])
          print('Zip code', ':', row[5])
          print()
  
      if len(rows2) == 0:
        print("No inspections found")
      else:
        for row in rows2:
          print('Inspections')
          print('Number of inspections', ':', row[0])
  
      if len(rows3) == 0:
        print("No results found")
      else:
        print('Inspection details:')
        for row in rows3:
          print('  ', row[0], ':', row[1], ':', row[2])

  # cmd 6 - input Chicago zip code
  # outputs stores in that zip code that failed inspection
  elif cmd == "6":
    # cmd description
    print('** Look up stores that failed inspection by zip code **')
    print() # adding a space btw cmd description & input
    zip = input('Input a Chicago zip code (ex. 60657): ')
    print()

    # checking for valid input 
    if int(zip) < 0: # invalid input
      print('Invalid zip code (must be positive)')
    elif len(zip) != 5:
      print("Invalid zip code (must have five numbers)")
    else: # if input is valid 

      #SQL for cmd 6
      sql6 = """
             SELECT DISTINCT Stores.Store_ID, Store_Name, Address, Results
             FROM Stores 
             INNER JOIN Inspections 
             ON Stores.Store_ID = Inspections.Store_ID
             INNER JOIN Inspection_Results 
             ON Inspections.Result_ID = Inspection_Results.Result_ID
             WHERE Zip_Code = %s AND Inspections.Result_ID = 2;
             """
      dbCursor.execute(sql6, (zip))
      rows = dbCursor.fetchall()
      
      if len(rows) == 0: # if no results 
        print("No stores found, try inputting a zip code that starts with a six and a zero.")
        print('Here are a few to choose from:')
        print('  60657')
        print('  60645')
        print('  60601')
        print('  60659')
        print('  60617')
        print()

        # offering to expand search
        expand = input("Alter search? [yes/no] ")
        
        if expand != 'no' and expand != 'n':
          quant = input("How much do you want to add or subtract from your input zip code (ex. +1, -1)? ")
          print()
          # expanding the zip code input
          zip_expanded = int(zip) + int(quant)
          
          if zip_expanded < 0:
            print('Invalid input (zip code must be positive), try again.')
          else: 
            dbCursor.execute(sql6, (zip_expanded))
            rows = dbCursor.fetchall()
    
            # adding an if/else statement for printing
            if len(rows) == 0:
              print("We expanded the zip code input but still can't find any stores in", zip, 'or (when altered)', zip_expanded, "so, try again.")
              
           # paging and displaying more
            else:
              more = "this can be anything but no"
              i = 0
              page = 1
              total = math.ceil(len(rows)/10)
              while more != "no" and more != "n":
                end = i + 10
                if end > len(rows):
                  end = len(rows)
                  for row in rows[i:end]:
                    print(row[0], ":", row[1], ':', row[2], ":", row[3])
                  print()
                  more = "no"
                else:
                  for row in rows[i:end]:
                    print(row[0], ":", row[1], ':', row[2], ":", row[3])
                  print()
                  more = input("Display more? [yes/no]  [" + str(page) + ' of ' + str(total) + '] ') 
                  i = i + 10
                  page = page + 1
  
      # paging and displaying more
      else:
        more = "this can be anything but no"
        i = 0
        page = 1
        total = math.ceil(len(rows)/10)
        while more != "no" and more != "n":
          end = i + 10
          if end > len(rows):
            end = len(rows)
            for row in rows[i:end]:
              print(row[0], ":", row[1], ':', row[2], ":", row[3])
            print()
            more = "no"
          else:
            for row in rows[i:end]:
              print(row[0], ":", row[1], ':', row[2], ":", row[3])
            print()
            more = input("Display more? [yes/no]  [" + str(page) + ' of ' + str(total) + '] ') 
            i = i + 10
            page = page + 1


  # cmd 7 - input Chicago zip code
  # outputs stores in that zip code that passed inspection
  elif cmd == "7":
    # cmd description
    print('** Look up stores that passed inspection by zip code **')
    print() # adding a space btw cmd description & input 
    zip_pass = input('Input a Chicago zip code (ex. 60657): ')
    print() # adding a space btw input & output 

    
    if int(zip_pass) < 0: # invalid input
      print('Invalid zip code (must be positive)')
    elif len(zip_pass) != 5:
      print("Invalid zip code (must have five numbers)")
    else: # if input is valid 

      # SQL for cmd 7
      sql7 = """
             SELECT DISTINCT Stores.Store_ID, Store_Name, Address, Results
             FROM Stores 
             INNER JOIN Inspections 
             ON Stores.Store_ID = Inspections.Store_ID
             INNER JOIN Inspection_Results 
             ON Inspections.Result_ID = Inspection_Results.Result_ID
             WHERE Zip_Code = %s AND Inspections.Result_ID = 1;
             """
      dbCursor.execute(sql7, (zip_pass))
      rows = dbCursor.fetchall()
  
      if len(rows) == 0: # if no results 
        print("No stores found, try inputting a zip code that starts with a six and a zero.")
        print('Here are a few to choose from:')
        print('  60657')
        print('  60645')
        print('  60601')
        print('  60659')
        print('  60617')
        print()

        # offering to expand search
        expand = input("Alter search? [yes/no] ")
        
        if expand != 'no' and expand != 'n':
          quant = input("How much do you want to add or subtract from your input zip code (ex. +1, -1)? ")
          print()
          # expanding the zip code input
          zip_pass_expanded = int(zip_pass) + int(quant)
          
          if zip_pass_expanded < 0:
            print('Invalid input (zip code must be positive), try again.')
          else: 
            dbCursor.execute(sql7, (zip_pass_expanded))
            rows = dbCursor.fetchall()
    
            # adding an if/else statement for printing
            if len(rows) == 0:
              print("We expanded the zip code input but still can't find any stores in", zip_pass, 'or (when altered)', zip_pass_expanded, "so, try again.")
              
           # paging and displaying more
            else:
              more = "this can be anything but no"
              i = 0
              page = 1
              total = math.ceil(len(rows)/10)
              while more != "no" and more != "n":
                end = i + 10
                if end > len(rows):
                  end = len(rows)
                  for row in rows[i:end]:
                    print(row[0], ":", row[1], ':', row[2], ":", row[3])
                  print()
                  more = "no"
                else:
                  for row in rows[i:end]:
                    print(row[0], ":", row[1], ':', row[2], ":", row[3])
                  print()
                  more = input("Display more? [yes/no]  [" + str(page) + ' of ' + str(total) + '] ') 
                  i = i + 10
                  page = page + 1
  
      # paging and displaying more
      else:
        more = "this can be anything but no"
        i = 0
        page = 1
        total = math.ceil(len(rows)/10)
        while more != "no" and more != "n":
          end = i + 10
          if end > len(rows):
            end = len(rows)
            for row in rows[i:end]:
              print(row[0], ":", row[1], ':', row[2], ":", row[3])
            print()
            more = "no"
          else:
            for row in rows[i:end]:
              print(row[0], ":", row[1], ':', row[2], ":", row[3])
            print()
            more = input("Display more? [yes/no]  [" + str(page) + ' of ' + str(total) + '] ') 
            i = i + 10
            page = page + 1
            
  # cmd 8 - input zip code
  # outputs % of passed insp by store type
  elif cmd == "8":
    # cmd description
    print('** Input zip code to find % of stores that passed inspection by store type **')
    print() # adding a space btw cmd description & input 
    zip = input('Input a Chicago zip code (ex. 60657): ')
    print() # adding a space btw input & output 

    if int(zip) < 0: # invalid input
      print('Invalid zip code (must be positive)')
    elif len(zip) != 5: # invalid input
      print("Invalid zip code (must have five numbers)")
    else: # valid input 

      # SQL for part 8 
      store_cats = """
                   SELECT Store_Type
                   FROM Store_Types;
                   """
      sql8 = """
             SELECT Store_Type, CAST((COUNT(Inspection_ID)) AS FLOAT)
             FROM Store_Types
             INNER JOIN Stores
             ON Store_Types.Store_Type_ID = Stores.Store_Type_ID 
             INNER JOIN Inspections
             ON Stores.Store_ID = Inspections.Store_ID
             WHERE Zip_Code = %s
             GROUP BY Store_Type;
             """
      
      sql8_p1 = """
             SELECT Store_Type, CAST((COUNT(Inspection_ID)) AS FLOAT)
             FROM Store_Types
             INNER JOIN Stores
             ON Store_Types.Store_Type_ID = Stores.Store_Type_ID 
             INNER JOIN Inspections
             ON Stores.Store_ID = Inspections.Store_ID
             WHERE Zip_Code = %s AND Result_ID = 1
             GROUP BY Store_Type;
             """
      
      dbCursor.execute(sql8, (zip))
      rows = dbCursor.fetchall()

      dbCursor.execute(sql8_p1, (zip))
      rows2 = dbCursor.fetchall() 
      
      dbCursor.execute(store_cats)
      categories = dbCursor.fetchall()  

      if len(rows) == 0: # if no results 
        print("No stores found, try again and try inputting a zip code that starts with a six and a zero.")
        print('Here are a few to choose from:')
        print('  60657')
        print('  60645')
        print('  60601')
        print('  60659')
        print('  60617')

      # displaying results 
      else:

        # putting the results into dictionaries 
        denom_dict = {tup[0]: tup[1] for tup in rows}
        numerator_dict = {tup[0]: tup[1] for tup in rows2}
        # printing the results 
        for cat in denom_dict:
          if cat not in numerator_dict:
            print(cat)
            print('  ', '0 % of inspections in this type passed')
            print()
          else: 
            i = round((numerator_dict[cat]/denom_dict[cat])*100, 2)
            print(cat)
            print('  ', i, '% of inspections in this type passed')
            print()

  elif cmd == "9":
    # cmd description
    id = input('Input a store ID to see what % of inspections that store passed, failed, etc.) ')
    print() # adding space btw input & output
    
    if int(id) < 0: # if input is negative 
      print('Invalid input (must be positive). Try any number from zero to 31362 instead.')
    elif int(id) > 31362: # invalid input 
      print('Input outside range of store IDs. Try any number from zero to 31362 instead.')
    else: # valid input

      sql9_p1 = """
                SELECT COUNT(Inspection_ID)
                FROM Inspections 
                WHERE Store_ID = %s; 
                """
      sql9_p2 = """
                SELECT COUNT(Inspection_ID), Results
                FROM Inspections
                INNER JOIN Inspection_Results
                ON Inspections.Result_ID = Inspection_Results.Result_ID
                WHERE Store_ID = %s
                GROUP BY Results;
                """
      dbCursor.execute(sql9_p1, (id))
      denom_tups = dbCursor.fetchall()
      denom = denom_tups[0][0] # denominator of later calc

      dbCursor.execute(sql9_p2, (id))
      rows = dbCursor.fetchall()

      if len(rows) == 0: # if no results
        print("Looks like this store hasn't had an inspection yet! Try again.")
      else: # if we have results 
        print('This store had', denom, 'inspections. Of those, the results are as follows: ')
        for row in rows: 
          print(round((row[0]/denom)*100, 2), '%', ':', row[1])
      
  else:
    print("**Error, unknown command, try again...")

  print()
  cmd = input("Please enter a command (1-9, x to exit): ")

print()
print("** Done **")

# closing the connection to the database
dbConn.close()