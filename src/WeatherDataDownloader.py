from os import makedirs
import pandas as pd
import requests
import time
from datetime import datetime
from ast import literal_eval
from Config import Config
from DatabaseManager import DatabaseManager

instance = Config.get_instance()


class WeatherDataDownloader:

    def __init__(self):
        self.api_key = instance.API_KEY
        self.api_url = instance.BASE_URL
        self.time_unix_now = int(time.time())
        self.db_manager = DatabaseManager()

    def download_weather_data(self, cityList, coordList):
        # Extract
        # file_path = self._save_weather_data_as_csv(coordList)

        df = self._transform_weather_data(
            'data_analytics/openweather/tiempodiario_20230809.csv')

        self.db_manager.create_weather_data_table()
        session = self.db_manager.create_db_session()
        for index, row in df.iterrows():
            for i in range(len(row['temperature'])):
                data = {
                    'city': cityList[index],
                    'temperature': row['temperature'][i],
                    'humidity': row['humidity'][i],
                    'wind_speed': row['wind_speed'][i],
                    'date': row['date'][i]
                }
                # Agregar el registro directamente a la base de datos usando to_sql
                pd.DataFrame(data, index=[0]).to_sql(
                    name="weather_data", con=self.db_manager.engine, if_exists="append", index=False)

        print("Datos agregados a la base de datos")

        session.close()

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
            for i in range(5):
                url = f'{self.api_url}{coords}&dt={time_now}&appid={self.api_key}&units=metric'
                print(url)
                data = self._fetch_weather_data(url)
                if data:
                    df = pd.json_normalize(data)
                    print(df)
                    all_data_df = pd.concat(
                        [all_data_df, df], ignore_index=True)
                time_now += 86400
            time_now = self.time_unix_now
        date_time = datetime.now().strftime('%Y%m%d')
        output_dir = 'data_analytics/openweather/'
        makedirs(output_dir, exist_ok=True)
        file_path = f'{output_dir}tiempodiario_{date_time}.csv'
        all_data_df.to_csv(file_path, index=False)
        return file_path

    def _transform_weather_data(self, path):
        df_db = pd.DataFrame()
        df = pd.read_csv(path)

        # Convertir las cadenas en listas de diccionarios
        df['hourly'] = df['hourly'].apply(literal_eval)

        # Definir la función para obtener los valores
        def get_values(items_list):
            if len(items_list) > 0:
                # Obtener los primeros 5 elementos de la lista de diccionarios
                items = items_list
                temps = [item['temp'] for item in items]
                humidities = [item['humidity'] for item in items]
                wind_speeds = [item['wind_speed'] for item in items]
                dates = [datetime.fromtimestamp(item['dt']).strftime(
                    '%Y-%m-%d %H:%M:%S') for item in items]
                return temps, humidities, wind_speeds, dates
            else:
                return None, None, None, None

        df_db[['temperature', 'humidity', 'wind_speed', 'date']
              ] = df['hourly'].apply(get_values).apply(pd.Series)
        return df_db
