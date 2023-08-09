from decouple import config


class Config:
    '''
    Class that represents the configuration of the application.

     Attributes:
     API_KEY (str): OpenWeatherMap API key.
     BASE_URL (str): OpenWeatherMap API base URL.
     SQLALCHEMY_DATABASE_URI (str): Connection string for the PostgreSQL database.

     Methods:
     __new__(cls): Special method to create a single instance of the class (Singleton).
     _initialize_config(self): Private method to initialize the configuration.
     get_instance(): Static method to get a single instance of the class.

     Usage example:
     config_instance = Config.get_instance()
     print(config_instance.API_KEY) # Prints the OpenWeatherMap API key.


    ###
    Clase que representa la configuración de la aplicación.

     Atributos:
     API_KEY (str): Clave de API de OpenWeatherMap.
     BASE_URL (str): URL base de la API de OpenWeatherMap.
     SQLALCHEMY_DATABASE_URI (str): Cadena de conexión para la base de datos PostgreSQL.

     Métodos:
     __new__(cls): Método especial para crear una única instancia de la clase (Singleton).
     _initialize_config(self): Método privado para inicializar la configuración.
     get_instance(): Método estático para obtener una instancia única de la clase.

     Ejemplo de uso:
     config_instance = Config.get_instance()
     print(config_instance.API_KEY)  # Imprime la clave de la API de OpenWeatherMap.
    '''
    _instance = None

    def __new__(cls):
        '''
        Special method to create a single instance of the class (Singleton).


        ###
        Método especial para crear una única instancia de la clase (Singleton).
        '''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_config()
        return cls._instance

    def _initialize_config(self):
        '''
        Private method to initialize the configuration.

         Set the following attributes:
         - API_KEY: OpenWeatherMap API key.
         - BASE_URL: OpenWeatherMap API base URL.
         - SQLALCHEMY_DATABASE_URI: Connection string for the PostgreSQL database.


        ###
        Método privado para inicializar la configuración.

         Establece los siguientes atributos:
         - API_KEY: Clave de API de OpenWeatherMap.
         - BASE_URL: URL base de la API de OpenWeatherMap.
         - SQLALCHEMY_DATABASE_URI: Cadena de conexión para la base de datos PostgreSQL.
        '''
        self.API_KEY = config('API_KEY')
        self.BASE_URL = config('BASE_URL')
        # self.SQLALCHEMY_DATABASE_URI = f'{config("DB_LANG_DRIVER")}://{config("DB_USER")}:{config("DB_PASSWORD")}@{config("DB_HOST")}:{config("DB_PORT")}/{config("DB_NAME")}'
        self.SQLALCHEMY_DATABASE_URI = f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@{config("DB_HOST")}:{config("DB_PORT")}/{config("DB_NAME")}'

    @staticmethod
    def get_instance():
        '''
        Static method to get a single instance of the class.

         Returns:
         Config: Single instance of the Config class.


        ###
        Método estático para obtener una instancia única de la clase.

         Retorna:
         Config: Instancia única de la clase Config.
        '''
        return Config()
