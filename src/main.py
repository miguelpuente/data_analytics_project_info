from WeatherDataDownloader import WeatherDataDownloader
from DatabaseManager import DatabaseManager

# Coordenadas de las ciudades
cityList = ["London", "New York", "Cordoba", "Taipei",
            "Buenos Aires", "Mexico DF", "Dublin", "Tilfis", "Bogota", "Tokio"]
coordList = ["lat=31&lon=64", "lat=40&lon=-73", "lat=-31&lon=-64", "lat=25&lon=64", "lat=-34&lon=-58",
             "lat=19&lon=-99", "lat=53&lon=6", "lat=41&lon=44", "lat=4&lon=74", "lat=35&lon=139"]

db_manager = DatabaseManager()
api_manager = WeatherDataDownloader()


def main():
    '''
    Main function that performs the following tasks:
     1. Create the 'weather_data' table in the database using the db_manager object.
     2. Create a database session using the db_manager object.
     3. Download weather data for specific cities using the api_manager object.
     4. Print the downloaded data for each city.
     5. If the data is not null, it saves it in the 'weather_data' table of the database.

     This function takes no arguments.

     Usage example:
     main()


    ###
    Función principal que realiza las siguientes tareas:
     1. Crea la tabla 'weather_data' en la base de datos utilizando el objeto db_manager.
     2. Crea una sesión de base de datos utilizando el objeto db_manager.
     3. Descarga datos meteorológicos para ciudades específicas utilizando el objeto api_manager.
     4. Si los datos no son nulos, los guarda en la tabla 'weather_data' de la base de datos.

     Esta función no recibe argumentos.

     Ejemplo de uso:
     main()
    '''
    db_manager.create_weather_data_table()
    session = db_manager.create_db_session()

    for city, coords in zip(cityList, coordList):
        df = api_manager.download_weather_data(city, coords)
        if df is not None:
            df.to_sql(name="weather_data", con=db_manager.engine,
                      if_exists="append", index=False)

    session.close()


if __name__ == "__main__":
    main()
