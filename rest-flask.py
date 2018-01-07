from flask import Flask
from flask import request
import json
app = Flask(__name__)


@app.route('/')
def hello():
    return "Check Code of countries"

#for searching country code run on address bar http://127.0.0.1:5000/country-name
@app.route('/api/v1/countries')
def iso_country():
    dict={'UK':'GB', 'India':'IND','Ireland':'IE','France':'FR','China':'CHN','Indonesia':'IDN','Spain':'ES'}
    country_name = request.args.get('name')
    return dict[country_name]

if __name__ == '__main__':
    app.run()
