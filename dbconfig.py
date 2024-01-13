import mysql.connector

# Change to your database credentials
db_conf = {
    "host" : "localhost",
    "user" : "root",
    "password" : "password",
    "database" : "AIRC_Kids_Game"
}

connection = mysql.connector.connect(**db_conf)
connection.autocommit = True

# Cursor will always return dictionary type as its easier to manage than indexes
# Buffered prevents unread results errors by always auto fetching all rows after select statements
cursor = connection.cursor(dictionary=True, buffered=True)
