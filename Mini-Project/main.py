from flask import Flask, render_template, request
import csv
import matplotlib.pyplot as plt
import time
from io import BytesIO


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('reg.html')


@app.route('/submit', methods=['POST'])
def save_data():
    data1 = request.form['firstname']
    data2 = request.form['lastname']
    data3 = request.form['email']
    data4 = request.form['mobile']
    data5 = request.form['year']
    # data6 = request.form['password']
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data1, data2, data3, data4, data5])
    return 'Data saved successfully'

@app.route('/chart')
def index():
    # Read data from CSV file and count number of occurrences for each year
    year_count = {}
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            year = row[-1]
            if year in year_count:
                year_count[year] += 1
            else:
                year_count[year] = 1

    # Plot pie chart and save it to file
    labels = year_count.keys()
    sizes = year_count.values()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Year Data')
    plt.savefig('static/images/pie_chart.png')

    # Render HTML template and pass image URL to it

    return render_template('chart.html', image_url='static/images/pie_chart.png')


@app.route('/faq')
def faq():
    return render_template('faq.html')
def chatbot_response(message):
    var_time = time.ctime()
    qna = {
        "Hi" : "Hello",
        "hi" : "Hello",
        "Hello" : "Hi",
        "hello" : "Hi",
        "Hey" : "wassup",
        "hey" : "wassup",
        "what is your name" : "My name is ChatBot",
        "What is your name" : "My name is ChatBot",
        "how are you" : "I'am Fine, what about you",
        "How are you" : "I'am Fine, what about you",
        "I am fine" : "Ok",
        "i am fine" : "Ok",
        "Fine" : "Ok",
        "fine" : "Ok",
        "what is the time now" : var_time,
        "Bye" : "See you later",
        "bye" : "See you later",
        "ok" : "See you later",
        "Ok" : "See you later",
        
    }

    return qna.get(message, "I'm sorry, I didn't understand that.")
@app.route('/faq', methods=['POST'])
def get_bot_response():
    
    user_message = request.form['message']
    bot_response = chatbot_response(user_message)
    return render_template('faq.html', message=user_message, response=bot_response)


@app.route('/table')
def table():
    with open('data.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return render_template('table.html',data=data)
    

if __name__ == '__main__':
    app.run(debug=True)