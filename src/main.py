from WeatherDataDownloader import WeatherDataDownloader

api_manager = WeatherDataDownloader()

cityList = ["Helmand Province", "Great River", "Colonia Caroya", "Pasni",
            "Ombues de Lavalle", "Tlalnepantla", "Tijnje", "Amasia", "Malé", "Shuzenji"]
coordList = ["lat=31&lon=64", "lat=40&lon=-73", "lat=-31&lon=-64", "lat=25&lon=64", "lat=-34&lon=-58",
             "lat=19&lon=-99", "lat=53&lon=6", "lat=41&lon=44", "lat=4&lon=74", "lat=35&lon=139"]


def main():
    """
    Main function to initiate the weather data download and processing.


    ###
    Función principal para iniciar la descarga y el procesamiento de datos meteorológicos.
    """
    print("Starting weather data download and processing...")

    if api_manager.download_weather_data(cityList, coordList):
        print("Weather data download and processing completed.")
    else:
        print("Weather data is empty or could not be processed.")


if __name__ == "__main__":
    main()
