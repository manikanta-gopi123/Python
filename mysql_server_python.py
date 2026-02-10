import pyodbc
db=pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};"
    "SERVER=VECTRA;"
    "DATABASE=gopi;"
    "Trusted_Connection=yes;")
mycursor=db.cursor()
mycursor.execute("use gopi")
mycursor.execute("select Top(5) * from gopi.dbo.Satish")

for i in mycursor:
    print(i)