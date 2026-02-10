import mysql.connector
db = mysql.connector.connect(
    host="VECTRA",
    user="vectra\gopi",
    password="1234",
    database="gopi"
)
cursor = db.cursor()
cursor.execute("SELECT * FROM student ORDER BY 1 DESC LIMIT 5")
for row in cursor:
    print(row)
