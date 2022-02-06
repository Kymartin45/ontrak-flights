from dotenv import dotenv_values
from flask import Flask
import requests
import json

app = Flask(__name__)
config = dotenv_values('.env')

AVIATION_STACK_API_KEY = config.get('AVIATION_STACK_API_KEY')

@app.route('/')
def getFlightData():
    url = 'http://api.aviationstack.com/v1/flights'
    params = {'access_key': AVIATION_STACK_API_KEY}    
    
    req = requests.get(url, params=params)
    res = json.loads(req.text)
    data = json.dumps(res, indent=4)

    with open('flightData.json', 'w') as outfile:
        outfile.write(data)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

