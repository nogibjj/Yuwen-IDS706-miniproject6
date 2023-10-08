import sqlite3

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

# Function to create the 'users' table if it doesn't exist
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
    except sqlite3.Error as e:
        print(e)

# Function to insert a new user into the database
def insert_user(conn, username, email):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)",
                        (username, email))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to retrieve a user by username
def get_user_by_username(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(e)

# Function to update a user's email by username
def update_user_email(conn, username, new_email):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email=? WHERE username=?",
                        (new_email, username))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to delete a user by username
def delete_user(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Query Function to retrieve all users
def select_all_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(e)

# Query Function to select person with shortest email
def select_person_with_shortest_email(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY LENGTH(email) ASC LIMIT 1")
        person = cursor.fetchone()
        return person
    except sqlite3.Error as e:
        print(e)

if __name__ == "__main__":
    database_file = "my_database.db"
    connection = create_connection(database_file)
    if connection:
        create_table(connection)

        # Create a new user
        insert_user(connection, "JohnDoe", "john@example.com")

        # Read a user
        user = get_user_by_username(connection, "JohnDoe")
        if user:
            print("User found:", user)

        # Update user email
        update_user_email(connection, "JohnDoe", "new_email@example.com")

        # Read the updated user
        updated_user = get_user_by_username(connection, "JohnDoe")
        if updated_user:
            print("Updated user:", updated_user)

        # Delete the user
        delete_user(connection, "JohnDoe")

        # user with shortest email
        insert_user(connection, "Apple", "a@example.com")
        insert_user(connection, "Banana", "Banana@example.com")
        insert_user(connection, "Orange", "ora@example.com")
        person = select_person_with_shortest_email(connection)

        if person:
            print("Person with the shortest email:")
            print("User ID:", person[0])
            print("Username:", person[1])
            print("Email:", person[2])
        else:
            print("No users in the database.")

        # select all users
        users = select_all_users(connection)

        for user in users:
            print("User ID:", user[0])
            print("Username:", user[1])
            print("Email:", user[2])

        connection.close()
