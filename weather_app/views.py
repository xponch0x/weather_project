import requests
from django.shortcuts import render
from django.conf import settings

def index(request):
    api_key = settings.OPENWEATHERMAP_API_KEY
    api_endpoint = settings.OPENWEATHERMAP_API_ENDPOINT
    cities = [
        {'name': 'Fargo,US', 'title': 'Fargo, ND'},
        {'name': 'Moorhead,US', 'title': 'Moorhead, MN'}
    ]
    units = 'imperial'
    weather_data = []
    for city in cities:
        url = f"{api_endpoint}?q={city['name']}&units={units}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        weather_data.append({
            'city': city['title'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        })
    
    return render(request, 'index.html', {'weather_data': weather_data})
