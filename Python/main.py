import csv
import MySQL
import MongoDB


def calculate_disperse(values, average):
    """
    Function to calculate standard deviation
    :param values: sample values
    :param average: mathematical expectation
    :return: standard deviation
    """
    quadratic_deviation = []
    for value in values:
        quadratic_deviation.append((average - value) ** 2)
    return sum(quadratic_deviation) / len(quadratic_deviation)


def calculate_expected_value(values):
    """
    Function to calculate mathematical expectation
    :param values: sample values
    :return: mathematical expectation
    """
    return sum(values) / len(values)


def calculate_results(results_dict):
    """
    Function to display the disperse and the expected value calculation process
    :param results_dict: Dictionary containing the results of all tests for one database
    """
    print("Calculating results...")
    print("///////////////////////////////////////////////////////////////////////////////////////")
    db = results_dict['db']
    results = results_dict['results']
    for result in results:
        print(f"{db} - {result['name']}")
        expected_value = calculate_expected_value(result['values'])
        print(f"Expected value - {expected_value}")
        print(f"Disperse - {calculate_disperse(result['values'], expected_value)}")
        print("///////////////////////////////////////////////////////////////////////////////////////")


def array_to_dict(array):
    """
    Function to convert values from a two-dimensional array to a dictionary
    :param array: two-dimensional array
    :return: dictionary
    """
    return [{"FirstName": item[0],
             "Surname": item[1],
             "Stipend": item[2],
             "Stream": item[3],
             "AvgMark": item[4],
             "Grade": item[5],
             "Class": item[6]} for item in array]


def read_csv(namefile):
    """
    Function to get values from CSV-file
    :param namefile: CSV-file name
    :return: values from CSV-file in 2D array
    """
    rows = []
    with open(namefile, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)
    return rows


def menu():
    print("This is an automated tool for testing CRUD operations on MySQL and MongoDB databases.")
    print("Reading dataset from CSV-file...")
    data = read_csv("data.csv")
    mysql_results = MySQL.menu(data)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    dict_data = array_to_dict(data)
    mongodb_results = MongoDB.menu(dict_data)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    calculate_results(mysql_results)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    calculate_results(mongodb_results)


if __name__ == '__main__':
    menu()
