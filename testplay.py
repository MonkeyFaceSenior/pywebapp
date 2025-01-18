import mysql.connector

# Establish the connection
connection = mysql.connector.connect( host='homeysrv.local.lau.fm', port=3307, user='diary', password='Abc123321!', database='hannadiary')

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Execute a query
cursor.execute("hannadiary;")

# Fetch the result of the query
result = cursor.fetchone()
print("Connected to database:", result)

# Close the cursor and connection
cursor.close()
connection.close()


# Insert data into a table
cursor.execute("INSERT INTO diary (content, title) VALUES (%s, %s)", ("test 1", "test 2"))
connection.commit()  # Commit the changes to the database

# Retrieve data
cursor.execute("SELECT * FROM diary")
result = cursor.fetchall()
for row in result:
    print(row)
