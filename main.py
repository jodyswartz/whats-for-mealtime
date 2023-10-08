from flask import Flask, render_template, request
import os
import crud
import utils

app = Flask(__name__, static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def index():
    username = None
    password = None
    date = None
    time = None
    selected_datetime = None
    selected_amount = None
    options = utils.getFoodList()
    selected_name = None
    generated_mealtime = None

    generated_mealtime = utils.mealtime()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        date = request.form['date']
        time = request.form['time']
        selected_datetime = f"Date:  date , Time:  time "
        selected_amount = request.form['amount']
        selected_name = request.form['dropdown']

        if date is not None and time is not None and selected_name is not None and selected_amount is not None:
            crud.insert(username=username, password=password, date=date, time=time, selected_name=selected_name,
                        selected_amount=selected_amount)

    return render_template('index.html', generated_mealtime=generated_mealtime, selected_datetime=selected_datetime,
                           selected_amount=selected_amount, options=options, selected_name=selected_name)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
