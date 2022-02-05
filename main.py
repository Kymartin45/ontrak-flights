from flask import Flask
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values('.env')

FLIGHT_API_KEY = config.get('FLIGHT_API_KEY')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

