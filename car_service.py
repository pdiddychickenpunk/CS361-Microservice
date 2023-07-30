# Author: Paul Adams

# Date: 7/30/23

# Description: This microservice recieves a JSON object within a request containing user choices
# from the partner application. This service returns the most highly rated car from the external
# dataset.

from flask import Flask, render_template, request, jsonify
import csv, json

app = Flask(__name__)
data_base_path = r'data\Car information.csv'
database = []

@app.route("/")
def display_data(data):
    return render_template('index.html')

@app.route("/get_car/", methods=['POST'])
def get_car():
    car_data = request.json
    # Retrieve and parse JSON data.
    print(car_data)
    car_type = car_data['car_type'].lower()
    fuel_type = car_data['fuel_type'].lower()
    price_range = car_data['price_range'].lower()
    fuel_efficiency_preferance = int(car_data['fuel_efficiency-preferance'])
    high_performance_preferance = int(car_data['high_performance-preferance'])
    reliability_preferance = int(car_data['reliability-preferance'])
    comfort_preferance = int(car_data['comfort-preferance'])

    # Price range is pipe separated, low|high. Get low price and high price.
    price_range = price_range.split("|")
    low_price = int(price_range[0])
    high_price = int(price_range[1])

    with open(data_base_path, "r", newline='', encoding='utf-8') as database_file:
        database_data = csv.reader(database_file)
        for row in database_data:
            database.append(row)

    print("Data Input:")
    print(car_data) # Display JSON data read in.
    print("---------------------------------------------------------")
    # Filter database down to only what user put as their values.
    user_database = []
    highest_rating = 0
    for row in database[1:]:
        database_car_name = row[0].lower()
        database_car_type = row[1].lower()
        database_fuel_type = row[2].lower()
        database_price = row[3]
        database_fuel_efficiency_rating = row[4]
        database_high_performance_rating = row[5]
        database_reliability_rating = row[6]
        database_comfort_rating = row[7]
        database_url = row[-2]
        # Validate no empty values were found. If so, we skip.
        if (database_car_name == '' or database_car_type == '' or database_fuel_type == '' or database_price == '' or database_fuel_efficiency_rating == '' or database_high_performance_rating == '' or database_reliability_rating == '' or database_comfort_rating == ''):
            continue

        # Convert database ratings and price to int.
        database_price = int(database_price)
        database_fuel_efficiency_rating = int(database_fuel_efficiency_rating)
        database_high_performance_rating = int(database_high_performance_rating)
        database_reliability_rating = int(database_reliability_rating)
        database_comfort_rating = int(database_comfort_rating)

        # Perform filter out net where data has to pass the below conditionals to be considered.
        if (car_type == database_car_type and fuel_type == database_fuel_type):
            pass

        if (database_car_type != car_type):
            continue

        elif (database_fuel_type != fuel_type):
            continue

        elif (database_price not in range(low_price, high_price + 1)):
            continue
        
        # The row of database data is acceptable for the user's choices. Proceed to calculate highest rating.
        else:
            rating = (database_fuel_efficiency_rating * fuel_efficiency_preferance) + (database_high_performance_rating * high_performance_preferance) + (database_reliability_rating * reliability_preferance) + (database_comfort_rating * comfort_preferance)

            if (rating > highest_rating):
                highest_rating = rating
                final_car = database_car_name
                final_car_type = database_car_type
                final_fuel_type = database_fuel_type
                final_price = database_price
                final_fuel_efficiency_rating = database_fuel_efficiency_rating
                final_high_performance_rating = database_high_performance_rating
                final_reliability_rating = database_reliability_rating
                final_comfort_rating = database_comfort_rating
                final_url = database_url

    # If highest rating is 0, that means we didn't find any database data to match with.
    # Set result and write JSON object to file.
    if (highest_rating == 0):
        highest_rating = "No matches found"
        car_choice = {'car': highest_rating}
        car_choice = json.dumps(car_choice)
        return car_choice


    # Write JSON response for partner application to import.
    car_choice = {

                'car': final_car,
                'car_type': final_car_type,
                'fuel_type': final_fuel_type,
                'price': final_price,
                'fuel_efficiency_rating': final_fuel_efficiency_rating,
                'high_performance_rating': final_high_performance_rating,
                'reliability_rating': final_reliability_rating,
                'comfort_rating': final_comfort_rating,
                'url': final_url
    }
    
    return car_choice


"""Attributions:

https://flexiple.com/python/python-get-current-directory/
https://stackoverflow.com/questions/17211188/how-to-create-a-timer-on-python
(second answer)
https://docs.python.org/3/library/csv.html
https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application
https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
(second answer)
https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files
https://stackoverflow.com/questions/10313001/is-it-possible-to-make-post-request-in-flask
(first answer)
https://pythonbasics.org/flask-http-methods/

"""