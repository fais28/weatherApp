from flask import Flask, render_template, request
import requests

app = Flask(__name__)
def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Change to "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["cod"] == 200:
            weather = {
                'main':data['weather'][0]['main'],
                "description": data["weather"][0]["description"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "visibility" : data['visibility']
            }
            weather['wind_speed'] = round(weather['wind_speed']*3.6,2)
            return weather
        else:
            print("Error: Unable to fetch weather data.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)


@app.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city_name = request.form['city']
        f = open('static\\api_files\\api.txt','r')
        api_key = f.read()
        f.close()
        

        weather_data = get_weather(api_key, city_name)
        if weather_data:
            print(weather_data['main'])
            return render_template('index.html', city=city_name.lower().capitalize(), weather=weather_data,atmos = weather_data['main'])
        
        else:
            return render_template('index.html', error="Error: Unable to fetch weather data.")
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
