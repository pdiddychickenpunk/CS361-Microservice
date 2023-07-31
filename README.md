# CS361-Microservice
Microservice for CS361. This service works for my partner's project. It recieves data from the partner application in JSON format. This program then parses that data, performs computation with that data, and returns data in JSON format to be picked up by the partner application.

# How to use this service

To use this service, you need to send a POST request to the service route responsible for sending back car data.

A JSON file must be provided to the request in the following format:

"car_type": "string value", "fuel_type": "string value", 
"price_range": "int value (low)|int value (high)", 
"fuel_efficiency-preferance":"int value", "high_performance-preferance":"int value", 
"reliability-preferance":"int value", "comfort-preferance":"int value"

An example call would be:

(using POST method) http://localhost:8001//get_car/

In the above example, you provide the JSON file as part of the request.

A response will be automatically sent by the service. Your application must automatically look for a response from the original request. The JSON data is in the response itself, so the JSON data must be retrieved
from that response.