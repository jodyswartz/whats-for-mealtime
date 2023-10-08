import pymongo


def insert(username, password, date, time, selected_name, selected_amount):
    # local
    #url = 'mongodb://  :  @localhost:27017'.format(username, password)
    # production
    url = f"mongodb+srv:// username : password @cluster0.m4cipub.mongodb.net/?tls=true&tlsAllowInvalidCertificates=true"
    client = pymongo.MongoClient(url)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    db = client['astro_journal']

    food_collection = db['food']
    # Production
    food_collection.insert_one( 'date': date,
                                'time': time,
                                'name': selected_name,
                                'amount': selected_amount )
