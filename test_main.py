import unittest
import main

class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        self.conn = main.connect_to_rds()
        self.new_db_name = 'test_employee_database'

    def tearDown(self):
        if self.conn:
            cursor = self.conn.cursor()
            drop_db_query = f"DROP DATABASE IF EXISTS {self.new_db_name};"
            cursor.execute(drop_db_query)
            self.conn.close()

    def test_connect_to_rds(self):
        self.assertIsNotNone(self.conn)

    def test_create_database(self):
        cursor = self.conn.cursor()
        main.create_database(self.conn, self.new_db_name)
        cursor.execute(f"USE {self.new_db_name};")
        cursor.execute("SELECT 1;")  # Execute a simple query to have a result set.
        result = cursor.fetchone()
        self.assertIsNotNone(result, "Failed to create the database")
        if result:
            self.assertEqual(result[0], 1)  # Verify the query result.


    def test_create_tables(self):
        main.create_database(self.conn, self.new_db_name)
        cursor = self.conn.cursor()
        cursor.execute(f"USE {self.new_db_name};")
        main.create_tables(self.conn)
        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor.fetchall()]
        self.assertIn('departments', tables)
        self.assertIn('employees', tables)

    def test_insert_sample_data(self):
        main.create_database(self.conn, self.new_db_name)
        cursor = self.conn.cursor()
        cursor.execute(f"USE {self.new_db_name};")
        main.create_tables(self.conn)
        main.insert_sample_data(self.conn)
        cursor.execute("SELECT COUNT(*) FROM departments;")
        department_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM employees;")
        employee_count = cursor.fetchone()[0]
        self.assertEqual(department_count, 4)
        self.assertEqual(employee_count, 7)

    def test_execute_complex_query(self):
        main.create_database(self.conn, self.new_db_name)
        cursor = self.conn.cursor()
        cursor.execute(f"USE {self.new_db_name};")
        main.create_tables(self.conn)
        main.insert_sample_data(self.conn)
        results = main.execute_complex_query(self.conn)
        self.assertEqual(len(results), 7)

if __name__ == '__main__':
    unittest.main()
