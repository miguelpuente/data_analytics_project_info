from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from Config import Config

Base = declarative_base()
instance = Config.get_instance()


class DatabaseManager:
    '''
    Class that is in charge of managing the database and its sessions.

     Attributes:
     engine (sqlalchemy.engine.Engine): Database engine.
     session (sqlalchemy.orm.Session): Database session.

     Methods:
     __init__(): Constructor of the class that initializes the engine and the database session.
     create_db_engine(): Creates and returns a SQLAlchemy database engine.
     create_db_session(): Creates and returns a session of the SQLAlchemy database.

     Subclass:
     WeatherData: Subclass that represents the 'weather_data' table in the database.

     Methods:
     create_weather_data_table(): Creates the 'weather_data' table in the database.


    ###
    Clase que se encarga de gestionar la base de datos y sus sesiones.

     Atributos:
     engine (sqlalchemy.engine.Engine): Motor de la base de datos.
     session (sqlalchemy.orm.Session): Sesión de la base de datos.

     Métodos:
     __init__(): Constructor de la clase que inicializa el motor y la sesión de la base de datos.
     create_db_engine(): Crea y retorna un motor de base de datos SQLAlchemy.
     create_db_session(): Crea y retorna una sesión de la base de datos SQLAlchemy.

     Subclase:
     WeatherData: Subclase que representa la tabla 'weather_data' en la base de datos.

     Métodos:
     create_weather_data_table(): Crea la tabla 'weather_data' en la base de datos.
    '''

    def __init__(self):
        '''
        Constructor of the class that initializes the engine and the database session.


        ###
        Constructor de la clase que inicializa el motor y la sesión de la base de datos.
        '''
        self.engine = self._create_db_engine()
        self.session = self._create_db_session()

    def _create_db_engine(self):
        '''
        Creates and returns a SQLAlchemy database engine.

         Returns:
         sqlalchemy.engine.Engine: Database engine.


        ###
        Crea y retorna un motor de base de datos SQLAlchemy.

         Retorna:
         sqlalchemy.engine.Engine: Motor de la base de datos.
        '''
        try:
            engine = create_engine(instance.SQLALCHEMY_DATABASE_URI, echo=True)
            return engine
        except SQLAlchemyError as sql_err:
            print(
                f"An SQLAlchemy error occurred while creating the engine: {sql_err}")
            return None
        except Exception as ex:
            print(f"An error occurred in _create_db_engine: {ex}")
            return None

    def _create_db_session(self):
        '''
        Creates and returns a session of the SQLAlchemy database.

         Returns:
         sqlalchemy.orm.Session: Database session.


        ###
        Crea y retorna una sesión de la base de datos SQLAlchemy.

         Retorna:
         sqlalchemy.orm.Session: Sesión de la base de datos.
        '''
        try:
            session = sessionmaker(bind=self.engine)
            return session()

        except SQLAlchemyError as sql_err:
            print(
                f"An SQLAlchemy error occurred while creating the session: {sql_err}")
            return None
        except Exception as ex:
            print(f"An error occurred in _create_db_session: {ex}")
            return None

    class WeatherData(Base):
        '''
        Subclass that represents the 'weather_data' table in the database.

         Attributes:
         id (sqlalchemy.Column): Column for the primary key.
         city (sqlalchemy.Column): Column for the name of the city.
         temperature (sqlalchemy.Column): Column for temperature.
         humidity (sqlalchemy.Column): Column for humidity.
         wind_speed (sqlalchemy.Column): Column for wind speed.
         date (sqlalchemy.Column): Column for the date.


        ###
        Subclase que representa la tabla 'weather_data' en la base de datos.

         Atributos:
         id (sqlalchemy.Column): Columna para la clave primaria.
         city (sqlalchemy.Column): Columna para el nombre de la ciudad.
         temperature (sqlalchemy.Column): Columna para la temperatura.
         humidity (sqlalchemy.Column): Columna para la humedad.
         wind_speed (sqlalchemy.Column): Columna para la velocidad del viento.
         date (sqlalchemy.Column): Columna para la fecha.

        '''
        __tablename__ = 'weather_data'
        id = Column(Integer, primary_key=True)
        city = Column(String)
        temperature = Column(Float)
        humidity = Column(Float)
        wind_speed = Column(Float)
        date = Column(DateTime)

    def create_weather_data_table(self):
        '''
        Create the 'weather_data' table in the database.


        ###
        Crea la tabla 'weather_data' en la base de datos.
        '''
        try:
            Base.metadata.create_all(self.engine)
        except SQLAlchemyError as sql_err:
            print(
                f"An SQLAlchemy error occurred while creating the weather data table: {sql_err}")
        except Exception as ex:
            print(f"An error occurred in create_weather_data_table: {ex}")
