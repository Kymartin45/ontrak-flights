from flask import Flask, flash, redirect, render_template, request
from dotenv import dotenv_values
import requests
import json
import os

app = Flask(__name__)
config = dotenv_values('.env')

AVIATION_STACK_API_KEY = config.get('AVIATION_STACK_API_KEY')

@app.route('/')
def flightHomePage():
    # req = requests.get(url, params=params) 
    # res = json.loads(req.text)
    # data = json.dumps(res, indent=4)
    
    # with open('flightData.json', 'w') as outfile:
    #     outfile.write(data)
    return render_template('index.html')

@app.route('/flight', methods=['GET', 'POST'])
def getFlightByNum():
    url = 'http://api.aviationstack.com/v1/flights'
    search_flight_num = request.args.get('flight-number')
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        'flight_number': search_flight_num
    }
    f = open('flightData.json') # temp read json file to avoid unecessary api req's
    data = json.load(f)
    airlines = data['data']
    
    airline_data = []
    for airline in airlines:
        airline_data.append({
            'flight_date': airline['flight_date'],
            'flight_status': airline['flight_status'],
            'airline_name': airline['airline']['name'],
            'flight_number': airline['flight']['number']
        })
        
    if search_flight_num == '':
        flash('Please search for a flight using the flight number')
        return redirect('/', code=302)
    
    return render_template('myFlight.html', airline_data = airline_data)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8000)

