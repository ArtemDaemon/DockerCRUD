import pymongo
import time

ITERATIONS = 5
DOMAINS = ['172.18.0.2', '172.18.0.3', '172.18.0.4']
PORT = 27017


# GENERAL OPERATIONS
def create(collection, values):
    """
    Function to add documents to a collection
    :param collection: collection
    :param values: dict of values
    """
    collection.insert_many(values)


def read(collection):
    """
    Function to read documents from a collection
    :param collection: collection
    :return: number of rows in the table
    """
    cursor = collection.find({})
    return len(list(cursor))


def update(collection, value):
    """
    Function to change documents in a collection
    :param collection: collection
    :param value: the value to which the value in the document will be changed
    """
    collection.update_many(
        {},
        {'$set': {'Stipend': value}}
    )


def clear(collection):
    """
    Function to delete documents in a collection
    :param collection: collection
    """
    collection.delete_many({})


# TESTS
def test_create(collection, values):
    """
    Function to test writing documents in a collection
    :param collection: collection
    :param values: dict of values
    :return: test results
    """
    results = []
    for i in range(ITERATIONS):
        clear(collection)
        print(f"Try #{i + 1}")
        start = time.time()
        create(collection, values)
        diff_time = time.time() - start
        print(f"It takes {diff_time} s")
        results.append(diff_time)
    return results


def test_delete(collection, values):
    """
    Function to test deleting documents from a collection
    :param collection: collection
    :param values: dict of values
    :return: test results
    """
    results = []
    for i in range(ITERATIONS):
        print(f"Try #{i + 1}")
        start = time.time()
        clear(collection)
        diff_time = time.time() - start
        print(f"It takes {diff_time} s")
        results.append(diff_time)
        create(collection, values)
    return results


def test_read(collection):
    """
    Function to test reading documents from a collection
    :param collection: collection
    :return: test results
    """
    results = []
    for i in range(ITERATIONS):
        print(f"Try #{i + 1}")
        start = time.time()
        length = read(collection)
        diff_time = time.time() - start
        print(f"{length} rows were read. It takes {diff_time} s")
        results.append(diff_time)
    return results


def test_update(collection):
    """
    Function to test updating documents in a collection
    :param collection: collection
    :return: test results
    """
    new_values = [5000, 0, 3123, 200, 40000000]
    results = []
    for i in range(ITERATIONS):
        print(f"Try #{i + 1}")
        start = time.time()
        update(collection, new_values[i])
        diff_time = time.time() - start
        print(f"It takes {diff_time} s")
        results.append(diff_time)
    return results


def create_collection(db):
    """
    Function to create a collection
    :param db: database
    :return: created collection
    """
    collection = db['students']
    collection.drop()
    return db['students']


def menu(data):
    """
    The function of displaying work with the database
    :param data: values
    :return: dictionary of test results
    """
    print("Connecting the MongoDB database...")
    client = None
    for domain in DOMAINS:
        try:
            client = pymongo.MongoClient(
                host=[str(domain) + ":" + str(PORT)],
                serverSelectionTimeoutMS=3000,  # 3 second timeout
                username="root",
                password="example",
            )
            print("Server version:", client.server_info()["version"])
            break
        except pymongo.errors.ServerSelectionTimeoutError:
            continue

    db = client["database"]
    print("Creating the students collection...")
    collection = create_collection(db)

    print("///////////////////////////////////////////////////////////////////////////////////////")
    print("Test MongoDB #1 - Creating")
    create_results = test_create(collection, data)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    print("Test MongoDB #2 - Reading")
    read_results = test_read(collection)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    print("Test MongoDB #3 - Updating")
    update_results = test_update(collection)
    print("///////////////////////////////////////////////////////////////////////////////////////")
    print("Test MongoDB #4 - Deleting")
    delete_results = test_delete(collection, data)
    print("///////////////////////////////////////////////////////////////////////////////////////")

    return {
        "db": "MongoDB",
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
