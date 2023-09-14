from datetime import datetime


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
