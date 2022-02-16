from flask import Flask, flash, redirect, render_template, request
from datetime import datetime
from dotenv import dotenv_values
import requests
import json
import os

app = Flask(__name__)
config = dotenv_values('.env')

AVIATION_STACK_API_KEY = config.get('AVIATION_STACK_API_KEY')
GEOAPIFY_API_KEY = config.get('GEOAPIFY_API_KEY')

now = datetime.now()
curr_date = now.strftime('%Y-%m-%d')

@app.route('/')
def flightHomePage():
    return render_template('index.html')

@app.route('/flight', methods=['GET', 'POST'])
def getFlightByNum(): 
    url = 'http://api.aviationstack.com/v1/flights'
    search_flight_num = request.args.get('flight-number')
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        'flight_number': search_flight_num,
    }
    r = requests.get(url, params=params)
    res = json.loads(r.text)
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
            'active_flight': airline['live']                # if live: return lat, long else null 
        })
        
    if search_flight_num == '':
        flash('Please search for a flight using the flight number', 'error')
        return redirect('/', code=302)
    
    return render_template('myFlight.html', airline_data = airline_data, date = curr_date)

@app.route('/flight/', methods=['GET'])
def renderMap():
    url = 'https://maps.geoapify.com/v1/staticmap'
    params = {
        'apiKey': GEOAPIFY_API_KEY,
        'style': 'klokantech-basic',
        'zoom': '4'
    }
    r = requests.get(url, params=params)    
    return render_template('map.html', map_src = r.url)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8000)

