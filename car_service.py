# Author: Paul Adams

# Date: 7/30/23

# Description: This microservice recieves a JSON object within a request containing user choices
# from the partner application. This service returns the most highly rated car from the external
# dataset.

from flask import Flask, request
import csv, json

app = Flask(__name__)
data_base_path = r'data\Car information.csv'
database = []

@app.route("/")
def display_data():
    return "<p> Data will be sent.</p>"

@app.route("/get_car/", methods=['POST'])
def get_car():
    car_data = request.json
    # Retrieve and parse JSON data.
    car_type = car_data['car_type'].lower()
    fuel_type = car_data['fuel_type'].lower()
    price_range = car_data['price_range'].lower()
    fuel_efficiency_preference = int(car_data['fuel_efficiency-preference'])
    high_performance_preference = int(car_data['high_performance-preference'])
    reliability_preference = int(car_data['reliability-preference'])
    comfort_preference = int(car_data['comfort-preference'])

    # Price range is pipe separated, low|high. Get low price and high price.
    price_range = price_range.split("|")
    low_price = int(price_range[0])
    high_price = int(price_range[1])

    with open(data_base_path, "r", newline='', encoding='utf-8') as database_file:
        database_data = csv.reader(database_file)
        for row in database_data:
            database.append(row)

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
        if (database_car_name == '' or database_car_name == 'Car' or database_car_type == '' or database_car_type == 'Car Type' or database_fuel_type == '' or database_fuel_type == 'Fuel Type' or database_price == '' or database_price == 'Price' or database_fuel_efficiency_rating == '' or database_fuel_efficiency_rating == 'Fuel Efficiency Rating' or database_high_performance_rating == '' or database_high_performance_rating == 'High Performance Rating' or database_reliability_rating == '' or database_reliability_rating == 'Reliability rating' or database_comfort_rating == '' or database_comfort_rating == 'comfort rating' or database_url == '' or database_url == 'Link to website'):
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
            rating = (database_fuel_efficiency_rating * fuel_efficiency_preference) + (database_high_performance_rating * high_performance_preference) + (database_reliability_rating * reliability_preference) + (database_comfort_rating * comfort_preference)

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


if __name__ == '__main__':
    app.run(debug=True, port=8001)


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
https://www.geeksforgeeks.org/how-to-change-port-in-flask-app/#
Info from the .json() method for (requests?). https://github.com/psf/requests
https://languages.oup.com/google-dictionary-en
https://www.google.com/search?sca_esv=556432238&q=preference&si=ACFMAn-S_tFEbe5J-h2tG_x3DZ9e6V1iGTG1kym1dG9bJdUV4PAy8C7ZximM6KWNzo6HP5VS6ZaBrBcWYuY7N04ypjSwVf4_Euyb6OcC26VIZyrGqFyQuzU%3D&expnd=1&sa=X&sqi=2&ved=2ahUKEwiOxpaL1tiAAxXiPEQIHcm-C1oQ2v4IegQIGxBc&biw=1920&bih=923&dpr=1
(Google search to check spelling)
https://blog.apastyle.org/apastyle/2013/10/how-do-i-cite-a-search-in-apa-style.html#:~:text=Slightly%20Longer%20A%3A%20A%20search,or%20in%20the%20reference%20list.&text=what%20they%20did%20with%20the%20results.
https://www.seoquake.com/blog/google-search-param/#:~:text=URL%20Search&text=The%20latter%20does%20not%20require,interest%E2%80%9D(or%20as_q).
https://support.google.com/docs/answer/161768?hl=en&co=GENIE.Platform%3DDesktop
https://www.google.com/search?q=preference&oq=preference&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIKCAEQABixAxiABDIHCAIQABiABDIKCAMQABixAxiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIKCAkQLhjUAhiABNIBCDEyNjZqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

"""