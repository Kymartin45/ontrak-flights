from flask import Flask, flash, redirect, render_template, request
from datetime import datetime
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
    now = datetime.now()
    curr_date = now.strftime('%Y-%m-%d') 
    
    url = 'http://api.aviationstack.com/v1/flights'
    search_flight_num = request.args.get('flight-number')
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        'flight_number': search_flight_num,
        'flight_date': curr_date    # not needed in long run when searching personal flight num (param CAN be used if user wants historical flight records)
    }
    
    req = requests.get(url, params=params)
    res = json.loads(req.text)
    airlines = res['data']
    
    airline_data = []
    for airline in airlines:
        airline_data.append({
            'flight_date': airline['flight_date'],
            'flight_status': airline['flight_status'],
            'airline_name': airline['airline']['name'],
            'departure_airport': airline['departure']['airport'],
            'arrival_airport': airline['arrival']['airport'],
            'flight_number': airline['flight']['number'],
            'active_flight': airline['live'],                
            'flight_latitude': airline['live']['latitude'],   # flights MUST be active/en-route in order to get lat, long
            'flight_longitude': airline['live']['longitude']
        })
        
    if search_flight_num == '':
        flash('Please search for a flight using the flight number', 'error')
        return redirect('/', code=302)
    
    return render_template('myFlight.html', airline_data = airline_data, date = curr_date)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8000)

