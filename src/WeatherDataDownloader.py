from os import makedirs
import pandas as pd
import requests
import time
from datetime import datetime
from ast import literal_eval
from Config import Config
from DatabaseManager import DatabaseManager
from sqlalchemy.exc import SQLAlchemyError


class WeatherDataDownloader:
    """
    This class downloads weather data using the OpenWeatherMap API,
    transforms and saves it as CSV and to a database.


    ###
    Esta clase descarga datos meteorológicos mediante la API de OpenWeatherMap,
    lo guarda como CSV, los trandforma guarda y en una base de datos.
    """

    def __init__(self):
        """
        Initialize the WeatherDataDownloader instance with necessary configurations.


        ###
        Inicialice la instancia de WeatherDataDownloader con las configuraciones necesarias.
        """
        self.instance = Config.get_instance()
        self.db_manager = DatabaseManager()
        self.api_key = self.instance.API_KEY
        self.api_url = self.instance.BASE_URL
        self.time_unix_now = int(time.time())

    def download_weather_data(self, cityList, coordList):
        """
        Download weather data, transform it, and save it to CSV and a database.

         Args:
             cityList (list): List of city names.
             coordList (list): List of coordinates.

         Returns:
             True or None


        ###
        Descargua datos meteorológicos, los trandforma y guarda en CSV y en una base de datos.

         Argumentos:
             cityList (lista): Lista de nombres de ciudades.
             coordList (lista): Lista de coordenadas.

         Devoluciones:
             True or None
        """

        file_path = self._save_weather_data_as_csv(coordList)

        df = self._transform_weather_data(file_path)

        return self._save_weather_data_as_database(df, cityList)

    def _fetch_weather_data(self, url):
        """
        Fetch weather data from the OpenWeatherMap API.

        Args:
            url (str): API URL for weather data.

        Returns:
            dict: Weather data in JSON format.


        ###
        Obtiene datos meteorológicos de la API de OpenWeatherMap.

         Argumentos:
             url (str): URL de API para datos meteorológicos.

         Devoluciones:
             dict: datos meteorológicos en formato JSON.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.exceptions.HTTPError as e:
            # Manejo de excepciones relacionadas con errores HTTP, por ejemplo, 404, 503, etc.
            print(f'Http error: {e}')
        except requests.exceptions.ConnectionError as e:
            # Manejo de excepciones relacionadas con problemas de conexión
            print(f'Connection error: {e}')
        except requests.exceptions.TooManyRedirects as e:
            # Manejo de excepciones relacionadas con demasiadas redirecciones
            print(f'Too many redirects: {e}')
        except requests.exceptions.RequestException as e:
            # Manejo de excepciones relacionadas con problemas de conexión o errores de solicitud
            print(f'Failed to make the request: {e}')
        except Exception as e:
            # Manejo de cualquier otra excepción no especificada anteriormente
            print(f'unknown error: {e}')

    def _save_weather_data_as_csv(self, coordList):
        """
        Save weather data to a CSV file.

        Args:
            coordList (list): List of coordinates.

        Returns:
            str: File path of the saved CSV.


        ###
        Guarde los datos meteorológicos en un archivo CSV.

         Argumentos:
             coordList (lista): Lista de coordenadas.

         Devoluciones:
             str: Ruta del archivo del CSV guardado.
        """
        time_now = self.time_unix_now
        all_data_df = pd.DataFrame()
        for coords in coordList:
            for i in range(5):
                url = f'{self.api_url}{coords}&dt={time_now}&appid={self.api_key}&units=metric'
                data = self._fetch_weather_data(url)
                if data:
                    df = pd.json_normalize(data)
                    all_data_df = pd.concat(
                        [all_data_df, df], ignore_index=True)
                time_now += 86400
            time_now = self.time_unix_now
        date_time = datetime.now().strftime('%Y%m%d')
        output_dir = 'data_analytics/openweather/'
        makedirs(output_dir, exist_ok=True)
        file_path = f'{output_dir}tiempodiario_{date_time}.csv'

        try:
            all_data_df.to_csv(file_path, index=False)
            print(f"Data saved to: {file_path}")
            return file_path
        except IOError as io_err:
            print(f"IOError occurred while saving data: {io_err}")
        except Exception as ex:
            print(f"An error occurred while saving data: {ex}")

    def _transform_weather_data(self, path):
        """
        Transform weather data from a CSV file.

        Args:
            path (str): File path of the CSV containing weather data.

        Returns:
            pandas.DataFrame: Transformed weather data DataFrame.


        ###
        Transforma los datos meteorológicos de un archivo CSV.

         Argumentos:
             ruta (str): ruta del archivo del CSV que contiene datos meteorológicos.

         Devoluciones:
             pandas.DataFrame: DataFrame de datos meteorológicos transformados.
        """
        df_db = pd.DataFrame()

        try:
            df = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            print("The CSV file is empty.")
        except pd.errors.ParserError as parser_err:
            print(f"ParserError occurred while reading CSV: {parser_err}")
        except Exception as ex:
            print(f"An error occurred while reading CSV: {ex}")

        df['hourly'] = df['hourly'].apply(literal_eval)

        def get_values(items_list):
            if len(items_list) > 0:
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

    def _save_weather_data_as_database(self, df, cityList):
        """
        Save weather data to the database.

        Args:
            df (pandas.DataFrame): DataFrame containing weather data.
            cityList (list): List of city names.

        Returns:
            bool: True if the data is successfully saved, False otherwise.


        ###
        Guarda los datos meteorológicos en la base de datos.

         Argumentos:
             df (pandas.DataFrame): DataFrame que contiene datos meteorológicos.
             cityList (lista): Lista de nombres de ciudades.

         Devoluciones:
             bool: True si los datos se guardaron correctamente, False en caso contrario.
        """
        with self.db_manager.session as session:
            self.db_manager.create_weather_data_table()
            all_data = []
            for index, row in df.iterrows():
                for i in range(len(row['temperature'])):
                    data = {
                        'city': cityList[index],
                        'temperature': row['temperature'][i],
                        'humidity': row['humidity'][i],
                        'wind_speed': row['wind_speed'][i],
                        'date': row['date'][i]
                    }
                    all_data.append(data)
            all_data_df = pd.DataFrame(all_data)
            try:
                all_data_df.to_sql(
                    name="weather_data", con=self.db_manager.engine, if_exists="append", index=False)
                return True
            except SQLAlchemyError as error:
                print(
                    f"Error inserting data into database: {error}")
