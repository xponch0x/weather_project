import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime, timedelta

def index(request):
    api_key = settings.OPENWEATHERMAP_API_KEY
    api_endpoint = settings.OPENWEATHERMAP_API_ENDPOINT
    air_pollution_endpoint = settings.OPENWEATHERMAP_API_AQI_ENDPOINT
    air_pollution_history_endpoint = settings.OPENWEATHERMAP_API_HISTORY
    forecast_endpoint = settings.OPENWEATHERMAP_FORECAST_API_ENDPOINT
    cities = [
        {'name': 'Fargo,US', 'title': 'Fargo, ND'},
    ]
    units = 'imperial'
    weather_data = []
    air_pollution_data = []
    forecast_data = []
    #Calculate timestamps for start and end dates
    start_date = datetime.now()
    end_date = start_date + timedelta(days=16)
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    for city in cities:
        #Retrieve weather data
        weather_url = f"{api_endpoint}?q={city['name']}&units={units}&appid={api_key}"
        weather_response = requests.get(weather_url)
        weather_json = weather_response.json()
        #Retrieve air pollution data
        air_pollution_url = f"{air_pollution_endpoint}?lat={weather_json['coord']['lat']}&lon={weather_json['coord']['lon']}&appid={api_key}"
        air_pollution_response = requests.get(air_pollution_url)
        air_pollution_json = air_pollution_response.json()
        #Retrieve historical air pollution data
        historical_air_pollution_url = f"{air_pollution_history_endpoint}?lat={weather_json['coord']['lat']}&lon={weather_json['coord']['lon']}&start={start_timestamp}&end={end_timestamp}&appid={api_key}"
        historical_air_pollution_response = requests.get(historical_air_pollution_url)
        historical_air_pollution_json = historical_air_pollution_response.json()
        
        #Retrieve forecast data
        forecast_url = f"{forecast_endpoint}?q={city}&appid={api_key}"
        forecast_response = requests.get(forecast_url)
        forecast_json = forecast_response.json()
        
        weather_data.append({
            'city': city['title'],
            'temperature' : round(weather_json['main']['temp']),
            'description': weather_json['weather'][0]['description']
        })
        air_pollution_data.append({
            'city': city['title'],
            'aqi': air_pollution_json['list'][0]['main']['aqi'],
            'historical_data': historical_air_pollution_json,
        })
        forecast_data.append({
            'city': city['title'],
            'weather': forecast_json["list"][0]
            
        })
    
    return render(request, 'index.html', {'weather_data': weather_data, 'air_pollution_data': air_pollution_data, 'forecast_data': forecast_data,})



    