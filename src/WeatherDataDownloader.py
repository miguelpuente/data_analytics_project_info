import pandas as pd
import requests
import time
from datetime import datetime
from Config import Config

instance = Config.get_instance()


class WeatherDataDownloader:
    '''
    Class that is responsible for managing communication with the OpenWeathermap API.

     Attributes:
     api_key (str): API key to access OpenWeathermap.
     api_url (str): OpenWeathermap API base URL.
     time_unix_now (int): Current UNIX timestamp in seconds since the epoch.

     Methods:
     __init__(): Constructor of the class that initializes the api_key, api_url and time_unix_now attributes.

     download_weather_data(city, coords): Gets weather data from different days for the given coordinates.

     Parameters:
     city (str): Name of the city.
     coords (str): Geographic coordinates in 'latitude,longitude' format.

     Returns:
     pd.DataFrame: A DataFrame containing weather information for different days,
                    including the city, temperature, humidity, wind speed and date.


    ###
    Clase que se encarga de gestionar la comunicación con la API de OpenWeathermap.

     Atributos:
     api_key (str): Clave de API para acceder a OpenWeathermap.
     api_url (str): URL base de la API de OpenWeathermap.
     time_unix_now (int): Marca de tiempo UNIX actual en segundos desde el epoch.

     Métodos:
     __init__(): Constructor de la clase que inicializa los atributos api_key, api_url y time_unix_now.

     download_weather_data(city, coords): Obtiene datos climáticos de diferentes días para las coordenadas dadas.

     Parámetros:
     city (str): Nombre de la ciudad.
     coords (str): Coordenadas geográficas en formato 'latitud,longitud'.

     Retorna:
     pd.DataFrame: Un DataFrame que contiene información climática para diferentes días,
                    incluyendo la ciudad, temperatura, humedad, velocidad del viento y fecha.
    '''

    def __init__(self):
        '''
        Constructor of the class that initializes the api_key, api_url, and time_unix_now attributes.


        ###
        Constructor de la clase que inicializa los atributos api_key, api_url y time_unix_now.
        '''
        self.api_key = instance.API_KEY
        self.api_url = instance.BASE_URL
        self.time_unix_now = int(time.time())

    def download_weather_data(self, city, coords):
        '''
        Gets weather data from different days for the given coordinates.

         Parameters:
         city (str): Name of the city.
         coords (str): Geographic coordinates in 'latitude,longitude' format.

         Returns:
         pd.DataFrame: A DataFrame containing weather information for different days,
                        including the city, temperature, humidity, wind speed and date.


        ###
        Obtiene datos climáticos de diferentes días para las coordenadas dadas.

         Parámetros:
         city (str): Nombre de la ciudad.
         coords (str): Coordenadas geográficas en formato 'latitud,longitud'.

         Retorna:
         pd.DataFrame: Un DataFrame que contiene información climática para diferentes días,
                        incluyendo la ciudad, temperatura, humedad, velocidad del viento y fecha.
        '''
        time_now = self.time_unix_now
        all_data_df = pd.DataFrame()
        for i in range(5):
            url = f'{self.api_url}{coords}&dt={self.time_unix_now}&appid={self.api_key}&units=metric'
            try:
                response = requests.get(url)
                response.raise_for_status()
                if response.status_code == 200:
                    data = response.json()
                    data = {
                        'city': data['name'],
                        'temperature': float(data['main']['temp']),
                        'humidity': float(data['main']['humidity']),
                        'wind_speed': float(data['wind']['speed']),
                        'date': datetime.fromtimestamp(time_now)
                    }
                    df = pd.json_normalize(data)
                    time_now += 86400
                    all_data_df = pd.concat(
                        [all_data_df, df], ignore_index=True)
                else:
                    print(
                        f"Error al obtener datos para {city}. Status code: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                # Manejo de excepciones relacionadas con problemas de conexión o errores de solicitud
                print(f"Error al realizar la solicitud: {e}")
            except requests.exceptions.HTTPError as e:
                # Manejo de excepciones relacionadas con errores HTTP, por ejemplo, 404, 503, etc.
                print(f"Error HTTP: {e}")
            except requests.exceptions.ConnectionError as e:
                # Manejo de excepciones relacionadas con problemas de conexión
                print(f"Error de conexión: {e}")
            except requests.exceptions.TooManyRedirects as e:
                # Manejo de excepciones relacionadas con demasiadas redirecciones
                print(f"Demasiadas redirecciones: {e}")
            except Exception as e:
                # Manejo de cualquier otra excepción no especificada anteriormente
                print(f"Error desconocido: {e}")

        return all_data_df
