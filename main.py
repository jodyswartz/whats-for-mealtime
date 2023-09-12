from flask import Flask, render_template, request
from datetime import datetime
import pymongo

app = Flask(__name__, static_folder='static')

client = pymongo.MongoClient('mongodb://admin:S2h36m78h54@localhost:59292')
db = client['astro_journal']

food_collection = db['food']


def getFoodList():
    file_path = "foodlist.txt"

    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()

            lines = file_contents.splitlines()

            data_array = []
            for line in lines:
                data_array.append(line)

            return data_array

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def mealtime():
    current_time = datetime.now().time()
    general_mealtime = "What's for "

    breakfast_start = datetime(1900, 1, 1, 6, 0, 0).time()
    breakfast_end = datetime(1900, 1, 1, 10, 59, 59).time()

    brunch_start = datetime(1900, 1, 1, 11, 0, 0).time()
    brunch_end = datetime(1900, 1, 1, 11, 59, 59).time()

    lunch_start = datetime(1900, 1, 1, 12, 0, 0).time()
    lunch_end = datetime(1900, 1, 1, 14, 0, 0).time()

    dinner_start = datetime(1900, 1, 1, 18, 0, 0).time()
    dinner_end = datetime(1900, 1, 1, 22, 0, 0).time()

    late_night_start = datetime(1900, 1, 1, 22, 0, 0).time()
    late_night_end = datetime(1900, 1, 1, 23, 59, 0).time()

    if breakfast_start <= current_time <= breakfast_end:
        return general_mealtime + " Breakfast?"
    elif brunch_start <= current_time <= brunch_end:
        return general_mealtime + " Brunch?"
    elif lunch_start <= current_time <= lunch_end:
        return general_mealtime + " Lunch?"
    elif dinner_start <= current_time <= dinner_end:
        return general_mealtime + " Dinner?"
    elif late_night_start <= current_time <= late_night_end:
        return "Late Night Meal?"
    else:
        return "Feeling for a Snack?"


@app.route('/', methods=['GET', 'POST'])
def index():
    date = None
    time = None
    selected_datetime = None
    selected_amount = None
    options = getFoodList()
    selected_name = None
    generated_mealtime = None

    generated_mealtime = mealtime()

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        selected_datetime = f"Date: {date}, Time: {time}"
        selected_amount = request.form['amount']
        selected_name = request.form['dropdown']
        
        if date is not None and time is not None and selected_name is not None and selected_amount is not None:
            food_collection.insert_one({'date': date,
                                        'time': time,
                                        'name': selected_name,
                                        'amount': selected_amount})

    return render_template('index.html', generated_mealtime=generated_mealtime, selected_datetime=selected_datetime,
                           selected_amount=selected_amount, options=options, selected_name=selected_name)

if __name__ == '__main__':
    app.run(debug=True)