import pymongo


def insert(username, password, date, time, selected_name, selected_amount):
    url = 'mongodb://{}:{}@localhost:27017'.format(username, password)
    client = pymongo.MongoClient(url)
    db = client['astro_journal']

    food_collection = db['food']
    food_collection.insert_one({'date': date,
                                'time': time,
                                'name': selected_name,
                                'amount': selected_amount})
