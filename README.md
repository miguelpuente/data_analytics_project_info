# Final Project Data Analytics - Informatorio

## Summary

The project consumes the [OpenWeathermap](https://openweathermap.org) api where it gets the current weather forecast plus the next four days and the name of the city given the latitude and longitude of the geographic location to query. The information obtained is stored in a postgres database.

## Prepare the environment

* 1 - Create the virtual environment.
    ```bash
        python -m venv venv
    ```
* 2 - Activate the virtual environment.
    * Windows.
        ```bash
            venv\Scripts\activate.bat
        ```
    * Linux.
        ```bash
            source venv/bin/activate
        ```
* 3 - Clone this repository.
    ```bash
        git clone https://github.com/miguelpuente/data_analytics_project_info.git
    ```
* 4 - Install the dependencies.
    ```bash
        cd data_analytics_project_info
        python -m pip install -r requirements.txt
    ```
* 5 - Rename the .env.example file and assign its values to environment variables.
    ```bash
        mv .env.example .env
        nano .env
    ```
    ```bash
        # API Key de OpenWeatherMap
        API_KEY = "TU_CLAVE_DE_API"
        # API url de OpenWeatherMap
        BASE_URL = https://api.openweathermap.org/data/2.5/onecall/timemachine?

        # Configuración de la base de datos PostgreSQL
        DB_LANG_DRIVER = postgresql+psycopg2
        DB_HOST = "nombre_del_host"
        DB_PORT = "numero_del_puerto"
        DB_NAME = "nombre_de_la_base_de_datos"
        DB_USER = "usuario_de_la_base_de_datos"
        DB_PASSWORD = "contraseña_de_la_base_de_datos"
    ```
* 6 - Start the Docker container.
    ```bash
        docker-compose up -d
    ```
* 7 - Run the src/main.py script
    ```bash
        python src/main.py
    ```
#
# Español

# Proyecto final Data Analytics - Informatorio

## Resumen

El proyecto consume la api [OpenWeathermap](https://openweathermap.org) donde obtiene la predicción climática del momento actual más los próximos cuatro días y el nombre de la ciudad dada la latitud y longitud de la ubicación geográfica a consultar. La información obtebida se guarda en una base de datos postgres.

## Crear el entorno

* 1 - Crear el entorno virtual.
    ```bash
        python -m venv venv
    ```
* 2 - Activar el entorno virtual.
    * Windows.
        ```bash
            venv\Scripts\activate.bat
        ```
    * Linux.
        ```bash
            source venv/bin/activate
        ```
* 3 - Clonar éste repositorio
    ```bash
        git clone https://github.com/miguelpuente/data_analytics_project_info.git
    ```
* 4 - Instalar las dependendencias.
    ```bash
        cd data_analytics_project_info
        python -m pip install -r requirements.txt
    ```
* 5 - Renombrar el archivo .env.example y asignar tus valores a las variables de entorno.
    ```bash
        mv .env.example .env
        nano .env
    ```
    ```bash
        # API Key de OpenWeatherMap
        API_KEY = "TU_CLAVE_DE_API"
        # API url de OpenWeatherMap
        BASE_URL = https://api.openweathermap.org/data/2.5/onecall/timemachine?

        # Configuración de la base de datos PostgreSQL
        DB_LANG_DRIVER = postgresql+psycopg2
        DB_HOST = "nombre_del_host"
        DB_PORT = "numero_del_puerto"
        DB_NAME = "nombre_de_la_base_de_datos"
        DB_USER = "usuario_de_la_base_de_datos"
        DB_PASSWORD = "contraseña_de_la_base_de_datos"
    ```
* 6 - Iniciar el contenedor Docker.
    ```bash
        docker-compose up -d
    ```
* 7 - Ejecutar el script src/main.py
    ```bash
        python src/main.py
    ```