import time
import mysql.connector

ITERATIONS = 5


# GENERAL OPERATIONS
def insert(connection, cursor, values):
    """
    Function to add records to a table
    :param connection: database
    :param cursor: query processor
    :param values: two-dimensional array of values
    """
    sql = "INSERT INTO students (FirstName, Surname, Stipend, Stream, AvgMark, Grade, Class) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, values)
    connection.commit()


def read(cursor):
    """
    Function to read rows from a table
    :param cursor: query processor
    :return: number of rows in the table
    """
    sql = "SELECT * FROM students"
    cursor.execute(sql)
    return len(cursor.fetchall())


def update(connection, cursor, new_value):
    """
    Function to change rows in a table
    :param connection: database
    :param cursor: query processor
    :param new_value: the value to which the value in the row will be changed
    """
    sql = f"UPDATE students SET Stipend = {new_value}"
    cursor.execute(sql)
    connection.commit()


def clear(connection, cursor):
    """
    Function to delete rows in a table
    :param connection: database
    :param cursor: query processor
    """
    sql = "TRUNCATE TABLE students"
    cursor.execute(sql)
    connection.commit()


# TESTS

def test_delete(connection, cursor, values):
    """
    Function to test deleting records from a table
    :param connection: database
    :param cursor: query processor
    :param values: two-dimensional array of values
    :return: test results
    """
    results = []
    for i in range(ITERATIONS):
        print(f"Try #{i + 1}")
        start = time.time()
        clear(connection, cursor)
        diff_time = time.time() - start
        print(f"It takes {diff_time} s")
        results.append(diff_time)
        insert(connection, cursor, values)
    return results


def test_update(connection, cursor):
    """
    Function to test updating records in a table
    :param connection: database
    :param cursor: query processor
    :return: test results
    """
    new_values = [5000, 0, 3123, 200, 40000000]
    results = []
    for i in range(ITERATIONS):
        print(f"Try #{i + 1}")
        start = time.time()
        update(connection, cursor, new_values[i])
        diff_time = time.time() - start
        print(f"It takes {diff_time} s")
        results.append(diff_time)
    return results


def test_read(cursor):
    """
    Function to test reading records from a table
    :param cursor: query processor
    :return: test results
    """
    results = []
    for i in range(ITERATIONS):
        print(f"Try #{i + 1}")
        start = time.time()
        length = read(cursor)
        diff_time = time.time() - start
        print(f"{length} rows were read. It takes {diff_time} s")
        results.append(diff_time)
    return results


def test_create(connection, cursor, values):
    """
    Function to test writing records in a table
    :param connection: database
    :param cursor: query processor
    :param values: two-dimensional array of values
    :return: test results
    """

    results = []
    for i in range(ITERATIONS):
        clear(connection, cursor)
        print(f"Try #{i + 1}")
        start = time.time()
        insert(connection, cursor, values)
        diff_time = time.time() - start
        print(f"It takes {diff_time} s")
        results.append(diff_time)
    return results


# MISC

def create_table(cursor):
    """
    Function to create a table
    :param cursor: query processor
    """
    cursor.execute("DROP TABLE students")
    cursor.execute("CREATE TABLE students("
                   "StudentID int not null AUTO_INCREMENT,"
                   "FirstName varchar(100) NOT NULL,"
                   "Surname varchar(100) NOT NULL,"
                   "Stipend float,"
                   "Stream varchar(100) NOT NULL,"
                   "AvgMark float NOT NULL,"
                   "Grade varchar(1) NOT NULL,"
                   "Class int NOT NULL,"
                   "PRIMARY KEY (StudentID))")


def connect():
    """
    Function for connecting to the database
    :return: database
    """
    database = mysql.connector.connect(
        host="mysql",
        user="root",
        passwd="root",
        database="db",
        port="3306"
    )
    return database


def menu(data):
    """
    The function of displaying work with the database
    :param data: values
    :return: dictionary of test results
    """
    print("Connecting the MySQL database...")
    database = connect()
    cursor = database.cursor()
    print("Creating the students table...")
    create_table(cursor)

    print("///////////////////////////////////////////////////////////////////////////////////////")
    print("Test MySQL #1 - Creating")
    create_results = test_create(database, cursor, data)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    print("Test MySQL #2 - Reading")
    read_results = test_read(cursor)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    print("Test MySQL #3 - Updating")
    update_results = test_update(database, cursor)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    print("Test MySQL #4 - Deleting")
    delete_results = test_delete(database, cursor, data)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    database.close()
    return {
        "db": "MySQL",
        "results": [
            {
                "name": "Creating results",
                "values": create_results
            },
            {
                "name": "Reading results",
                "values": read_results
            },
            {
                "name": "Updating results",
                "values": update_results
            },
            {
                "name": "Deleting results",
                "values": delete_results
            }
        ]
    }
