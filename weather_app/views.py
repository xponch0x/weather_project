import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime, timedelta

def home(request):
    api_key = settings.OPENWEATHERMAP_API_KEY
    api_endpoint = settings.OPENWEATHERMAP_API_ENDPOINT
    air_pollution_endpoint = settings.OPENWEATHERMAP_API_AQI_ENDPOINT
    air_pollution_history_endpoint = settings.OPENWEATHERMAP_API_HISTORY
    forecast_endpoint = settings.OPENWEATHERMAP_FORECAST_API_ENDPOINT

    cities = [
        {'name': 'Fargo,US', 'title': 'Fargo, ND'},
        {'name': 'Moorhead,US', 'title': 'Moorhead, MN'}
    ]
    units = 'imperial'
    weather_data = []
    air_pollution_data = []
    forecast_data = []
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
        forecast_url = f"{forecast_endpoint}?lat={weather_json['coord']['lat']}&lon={weather_json['coord']['lon']}&appid={api_key}"
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
        
        city_forecast = {
            'city': city['title'],
            'forecasts': []
        }
        
        #Get today's date
        today = datetime.now().date()
        #Define the start date for the forecast (May 1st)
        start_date = datetime(today.year, 5, 1).date()
        #Calculate the end date (5 days from start date)
        end_date = start_date + timedelta(days=4)


        for forecast in forecast_json['list']:
            #Extract date from timestamp
            forecast_date = datetime.fromtimestamp(forecast['dt']).date()
            #Check if the forecast date is within the desired range
            if start_date <= forecast_date <= end_date:
                #Add forecast data to city_forecast
                city_forecast['forecasts'].append({
                    'date': forecast_date.strftime('%Y-%m-%d'),
                    'temperature': forecast['main']['temp'],
                    'description': forecast['weather'][0]['description']
                })
                
        #Append city_forecast to forecast_data
        forecast_data.append(city_forecast)

    return render(request, 'weather/home.html', {'weather_data': weather_data, 'air_pollution_data': air_pollution_data, 'forecast_data': forecast_data})
