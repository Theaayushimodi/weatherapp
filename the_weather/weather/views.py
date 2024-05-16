from django.shortcuts import render
import requests
from.models import City
from.forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&appid=5befb5c5c036ba7ddf7f3996e3af9065'
    cities = City.objects.all()
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            if not City.objects.filter(name=city_name).exists():
                form.save()
    form = CityForm()
    weather_data = []
    city_names = []
    for city in cities:
        if city.name not in city_names:
            city_names.append(city.name)
            city_weather = requests.get(url.format(city.name)).json()
            weather = {
                'city': city,
                'temperature_f':  city_weather['list'][0]['main']['temp'],
                'temperature_c': (city_weather['list'][0]['main']['temp'] - 32) * 5/9,
                'humidity': city_weather['list'][0]['main']['humidity'],
                'pressure': city_weather['list'][0]['main']['pressure'],
                'description': city_weather['list'][0]['weather'][0]['description'],
                'icon': city_weather['list'][0]['weather'][0]['icon'],
                'forecast': city_weather['list'][1:6],  # Get the forecast data for the next 5 days
                'wind_speed': city_weather['list'][0]['wind']['speed'],
            }
            weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)