from flask import Flask, flash, redirect, render_template, request
from dotenv import dotenv_values
import requests
import json
import os

app = Flask(__name__)
config = dotenv_values('.env')

AVIATION_STACK_API_KEY = config.get('AVIATION_STACK_API_KEY')

@app.route('/')
def getFlightData():
    url = 'http://api.aviationstack.com/v1/flights'
    search_flight_num = request.args.get('get-flight-by-id')
    
    if search_flight_num == '':
        flash('Please search for a flight using the flight number')
        return redirect('/', code=302)  # successful redirect 
    
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        'flight_number': search_flight_num
    }
     
    # req = requests.get(url, params=params) 
    # res = json.loads(req.text)
    # data = json.dumps(res)
    
    # with open('flightData.json', 'w') as outfile:
    #     outfile.write(data)
    return render_template('index.html')

app.route('/my-flight', methods=['GET', 'POST'])
def getFlightById():
    return render_template('myFlight.html')
    

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8000)

