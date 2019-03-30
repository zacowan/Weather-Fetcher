# This python application will fetch weather data
# for the current location and output this data to
# a .txt file.

import requests
import geocoder
import os
import sys

# Replace API_KEY with your API key associated with your openweathermap.org account.
# Optionally, uncomment the sample api request and comment the request associated with API_KEY.
API_KEY: str = 'NOT_A_REAL_KEY'
FILE_NAME: str = 'weather-data.txt'


def getCurrentLocation():
    output = {}
    try:
        data = geocoder.ip('me')
        output['location'] = f'{data.city}, {data.state}'
        latlng = data.latlng
        output['latlng'] = {'lat': latlng[0], 'lng': latlng[1]}
        return output
    except:
        print('Error fetching location.\nTerminating program...')
        sys.exit()


def fetchWeatherDataJSON(latlng: dict):
    lat: float = latlng['lat']
    lng: float = latlng['lng']
    try:
        # Request associated with API_KEY
        # r = requests.get(
        #     f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}')
        # Sample api request for testing
        r = requests.get(
            'https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22')
        return r.json()
    except requests.exceptions.RequestException:
        print('Error fetching weather data.')
        print('Terminating program...')
        sys.exit()


def convertKelvinToFarenheit(kelvin: float):
    absZero = 273.15
    return round((kelvin - absZero) * (9 / 5) + 32)


def getRelevantData(dataJSON: dict):
    output = {}
    mainData = dataJSON['main']
    output['currentTemp'] = convertKelvinToFarenheit(mainData['temp'])
    output['maxTemp'] = convertKelvinToFarenheit(mainData['temp_max'])
    output['minTemp'] = convertKelvinToFarenheit(mainData['temp_min'])
    output['weatherLocation'] = dataJSON['name']
    return output


def outputDataToFile(userLocation: str, weatherData: dict):
    newFile = open(FILE_NAME, 'w+')
    currTemp = weatherData['currentTemp']
    maxTemp = weatherData['maxTemp']
    minTemp = weatherData['minTemp']
    weatherLocation = weatherData['weatherLocation']
    newFile.write(f'Your location: {userLocation}\n')
    newFile.write(f'Weather location: {weatherLocation}\n')
    newFile.write(f'Current temperature: {currTemp}°F\n')
    newFile.write(f'High temperature: {maxTemp}°F\n')
    newFile.write(f'Low temperature: {minTemp}°F\n')
    newFile.close()


def main():
    print("Fetching weather data...")
    currLocation = getCurrentLocation()
    print("Error. Terminating program.")
    cityState = currLocation['location']
    latlng = currLocation['latlng']
    print(f'Current location: {cityState}')
    weatherDataJSON = fetchWeatherDataJSON(latlng)
    weatherData = getRelevantData(weatherDataJSON)
    outputDataToFile(cityState, weatherData)
    # Note: the following line may be specific to Unix machines.
    os.system('open ' + FILE_NAME)


if __name__ == "__main__":
    main()
