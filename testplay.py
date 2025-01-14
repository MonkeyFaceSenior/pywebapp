import mysql.connector

# Establish the connection
connection = mysql.connector.connect(
    host='homeysrv.local.lau.fm', # For example, 'localhost' or an IP address
    user='your_username',  # Your MariaDB username
    password='your_password',  # Your MariaDB password
    database=''  # The name of the database to connect to
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Execute a query
cursor.execute("SELECT DATABASE();")

# Fetch the result of the query
result = cursor.fetchone()
print("Connected to database:", result)

# Close the cursor and connection
cursor.close()
connection.close()
