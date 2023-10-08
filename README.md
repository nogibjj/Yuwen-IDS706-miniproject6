# Yuwen-Cai-week5-mini-repo  

[![cicd](https://github.com/nogibjj/Yuwen-IDS706-miniproject6/actions/workflows/cicd.yml/badge.svg)](https://github.com/nogibjj/Yuwen-IDS706-miniproject6/actions/workflows/cicd.yml)  

This is a repo for course 706_Data_Engineering Week 6 Mini Project. This objective was to Design a complex SQL query for a MySQL database and explain the results.

# Purpose
- Create a MYSQL database in Cloud platform
- Perform a complex query operation


## Preparation
1. Format code with Python black by using `make format`

2. Lint code with Ruff by using `make lint`. 

3. Test code by using `make test`

4. The database is created in AWS RDS with MYSQL.


## Code Location
You can find all the relevant code in Python with SQL database in main.py

Snippets of some SQL functions are excerpted below:

For the "CRUD" with database part:

### connect 
```python
def connect_to_rds():
    try:
        # Replace these variables with your own RDS information
        config = {
            'user': 'admin',
            'password': '***',
            'host': '***,
            'ssl_verify_identity': False,  
            # Enable SSL for a secure connection (recommended)
        }
        
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
```

### create database because RDS does not have a default one
```python
def create_database(conn, db_name):
    try:
        cursor = conn.cursor()
        create_db_query = f"CREATE DATABASE {db_name};"
        cursor.execute(create_db_query)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
```
### create 2 tables for complex query
# Function to create the 'departments' and 'employees' tables
def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                department_id INT AUTO_INCREMENT PRIMARY KEY,
                department_name VARCHAR(255) NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INT AUTO_INCREMENT PRIMARY KEY,
                employee_name VARCHAR(255) NOT NULL,
                department_id INT,
                FOREIGN KEY (department_id) REFERENCES departments(department_id)
            )
        ''')
        conn.commit()
    except mysql.connector.Error as e:
        print(e)

### insert sample employee sample data
```python
def insert_sample_data(conn):
    try:
        cursor = conn.cursor()
        # Insert departments
        cursor.execute("INSERT INTO departments (department_name)"
                       " VALUES ('HR'), ('Finance'), ('IT'), ('Marketing')")
        
        # Insert employees with department assignments
        cursor.execute("INSERT INTO employees (employee_name, department_id)"
                    " VALUES ('John Doe', 1), ('Jane Smith', 1),"
                    " ('Alice Johnson', 2),"
                    " ('Bob Anderson', 2), ('Charlie Brown', 3), "
                    "('David Wilson', 3), ('Eve Adams', 4)")
        
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
```

### Complex Query Function: complex SQL query retrieves information about employees and their associated departments, along with a count of employees within each department. 
```
def execute_complex_query(conn):
    try:
        cursor = conn.cursor()
        sql_query = """
        SELECT
            e.employee_id,
            e.employee_name,
            d.department_name,
            COUNT(*) OVER(PARTITION BY d.department_id) AS department_employee_count
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id;
        """
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        print(e)
```

### result:
Result Running main.py:
![Alt text](<main_result.png>)

Result Running test_main.py locally:
![Alt text](<test_result_local.png>)

Result Running make test in GitHub actions:
![Alt text](<test_result.png>)

