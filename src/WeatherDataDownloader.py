from os import makedirs
import pandas as pd
import requests
import time
import json
from datetime import datetime
from Config import Config

instance = Config.get_instance()


class WeatherDataDownloader:

    def __init__(self):
        self.api_key = instance.API_KEY
        self.api_url = instance.BASE_URL
        self.time_unix_now = int(time.time())

    def download_weather_data(self, cityList, coordList):
        # Extract
        # file_path = self._save_weather_data_as_csv(coordList)
        self._transform_weather_data(
            'data_analytics/openweather/tiempodiario_20230808.csv')

    def _fetch_weather_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
            else:
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

    def _save_weather_data_as_csv(self, coordList):
        time_now = self.time_unix_now
        all_data_df = pd.DataFrame()
        for coords in (coordList):
            print
            url = f'{self.api_url}{coords}&dt={self.time_unix_now}&appid={self.api_key}&units=metric'
            data = self._fetch_weather_data(url)
            if data:
                df = pd.json_normalize(data)
                all_data_df = pd.concat([all_data_df, df], ignore_index=True)
            time_now += 86400
        date_time = datetime.now().strftime('%Y%m%d')
        output_dir = 'data_analytics/openweather/'
        makedirs(output_dir, exist_ok=True)
        file_path = f'{output_dir}tiempodiario_{date_time}.csv'
        all_data_df.to_csv(file_path, index=False)
        return file_path

    def _transform_weather_data(self, path):
        df = pd.read_csv(path)
        for item in df['hourly']:
            print(item)
