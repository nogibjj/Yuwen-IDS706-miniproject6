# Yuwen-Cai-week5-mini-repo  

[![cicd](https://github.com/nogibjj/Yuwen-IDS706-miniproject5/actions/workflows/cicd.yml/badge.svg)](https://github.com/nogibjj/Yuwen-IDS706-miniproject5/actions/workflows/cicd.yml)  

This is a repo for course 706_Data_Engineering Week 6 Mini Project. This objective was to Design a complex SQL query for a MySQL database and explain the results.

# Purpose
- Create a MYSQL database in Cloud platform
- Perform a complex query operation


## Preparation
1. Format code with Python black by using `make format`

2. Lint code with Ruff by using `make lint`. 

3. Test code by using `make test`


## Code Location
You can find all the relevant code in Python with SQL database in main.py

Snippets of some SQL functions are excerpted below:

For the "CRUD" with database part:

### connect 
```python
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
```

### create
```python
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
```

### insert
```python
def insert_user(conn, username, email):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)",
                        (username, email))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
```

### update
```python
def update_user_email(conn, username, new_email):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email=? WHERE username=?",
                        (new_email, username))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
```

### delete
```python
def delete_user(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
```


All the functions are tested in test_main.py

### Two Query Function
1. select all users from the database
2. choose the person with shortest email

### result:
Result Running main.py:
![Alt text](<test_result.png>)

Result Running make test:
![Alt text](<main_result.png>)
