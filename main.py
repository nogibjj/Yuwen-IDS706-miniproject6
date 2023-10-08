import mysql.connector

# Function to create a database connection
def connect_to_rds():
    try:
        # Replace these variables with your own RDS information
        config = {
            'user': 'admin',
            'password': 'hhxkHH0dBUcum2j49Xor',
            'host': 'miniproj-706.clddqsj3el9y.us-east-1.rds.amazonaws.com',
            'ssl_verify_identity': False,  
            # Enable SSL for a secure connection (recommended)
        }
        
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

# Manuual Create a database because rds does not provide a default one
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

# Function to execute a single written query
def execute_query(conn, query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

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

# Function to insert sample data into departments and employees tables
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

# Function to execute the complex SQL query
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

if __name__ == "__main__":
    conn = connect_to_rds()
    if conn:
        # Create a new database
        new_db_name = 'employee_database'
        create_database(conn, new_db_name)

        # Switch to the newly created database
        switch_db_query = f"USE {new_db_name};"
        execute_query(conn, switch_db_query)

        # Create tables and insert sample data
        create_tables(conn)
        insert_sample_data(conn)

        # Perform a complex query involving two tables
        result = execute_complex_query(conn)

        if result:
            for row in result:
                print(f"Department: {row[0]}, Employee Name: {row[1]}")
        else:
            print("No results.")

        conn.close()
