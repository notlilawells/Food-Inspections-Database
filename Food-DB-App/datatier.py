#
# datatier.py
#
# Executes SQL queries against the given database.
#
# Original author:
#   Prof. Joe Hummel
#   Northwestern University
#   CS 217, Fall 2022
#   Project 03
#
#import sqlite3
import pymssql


##################################################################
#
# select_one_row:
#
# Given a database connection and a SQL Select query,
# executes this query against the database and returns
# the first row retrieved by the query (or the empty
# tuple () if no data was retrieved). The query can
# be parameterized, in which case pass the values as
# a list via parameters; this parameter is optional.
#
# Returns: first row retrieved by the given query, or
#          () if no data was retrieved. If an error
#          occurs, a msg is output and None is returned.
#
def select_one_row(dbConn, sql, parameters=[]):
  dbCursor = dbConn.cursor()

  try:
    dbCursor.execute(sql, parameters)
    row = dbCursor.fetchone()
    if row is None:  # executed successfully, but no data was retrieved
      return ()
    else:
      return row

  except Exception as err:
    print("query failed:", err)
    return None

  finally:
    dbCursor.close()


##################################################################
#
# select_n_rows:
#
# Given a database connection and a SQL Select query,
# executes this query against the database and returns
# a list of rows retrieved by the query. If the query
# retrieves no data, the empty list [] is returned.
# The query can be parameterized, in which case pass
# the values as a list via parameters; this parameter
# is optional.
#
# Returns: a list of 0 or more rows retrieved by the
#          given query; if an error occurs a msg is
#          output and None is returned.
#
def select_n_rows(dbConn, sql, parameters=[]):
  dbCursor = dbConn.cursor()

  try:
    dbCursor.execute(sql, parameters)
    rows = dbCursor.fetchall()
    return rows

  except Exception as err:
    print("query failed:", err)
    return None

  finally:
    dbCursor.close()


##################################################################
#
# perform_action:
#
# Given a database connection and a SQL action query,
# executes this query and returns the # of rows
# modified; a return value of 0 means no rows were
# updated. Action queries are typically "insert",
# "update", "delete". The query can be parameterized,
# in which case pass the values as a list via
# parameters; this parameter is optional.
#
# Returns: the # of rows modified by the query; if an
#          error occurs a msg is output and -1 is
#          returned. Note that a return value of 0 is
#          not considered an error --- it means the
#          query did not change the database (e.g.
#          because the where condition was false?).
#
def perform_action(dbConn, sql, parameters=[]):
  dbCursor = dbConn.cursor()

  try:
    # try to execute, and if successful commit the changes
    # and return the # of rows modified by the query:
    dbCursor.execute(sql, parameters)
    dbConn.commit()
    return dbCursor.rowcount

  except Exception as err:
    # if it fails, print an error msg and return -1:
    print("query failed:", err)
    return -1

  finally:
    # cleanup code that gets executed either way:
    dbCursor.close()
