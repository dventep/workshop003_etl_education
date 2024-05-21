""" This module is to establish connection with PostgreSQL's database """

# Import libraries
import sys
import os
import importlib.util
import logging
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
sys.path.append(os.path.abspath("/opt/airflow/shared_functions/database_models/"))
sys.path.append(os.path.abspath("../shared_functions/database_models/"))
import sql_classes

# spec = importlib.util.spec_from_file_location("sql_classes", "../code/database_models/sql_classes.py")
# sql_classes = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(sql_classes)

# ? Logger basic settings
# logging.basicConfig(
#     level=logging.DEBUG,
#     filename="../code/log/workshop001.log",
#     encoding="utf-8",
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

class ConnectionPostgres:
    """Create connection with PostgreSQL"""

    PARSER = ConfigParser()
    # Connection data for PostgreSQL
    DATABASE_SECTION = "postgresql"

    def __init__(self, credentials_filename_url = "", specified_host = False, specified_port = False, specified_user = False, specified_password = False) -> None:
        """Constructor"""
        self.specified_host = False
        self.specified_port = False
        self.specified_user = False
        self.specified_password = False
        self.CREDENTIALS_FILENAME = credentials_filename_url
        if specified_host:
            self.specified_host = specified_host
        if specified_port:
            self.specified_port = specified_port
        if specified_user:
            self.specified_user = specified_user
        if specified_password:
            self.specified_password = specified_password
        self.connection_config = False
        self.engine = False
        self.session = False
        self.data_to_connection()
        self.modules = {}

        if self.connection_config:
            self.create_engine_database()
            self.create_connection()

    def make_tables(self) -> None:
        """Method to create tables in database
            
            Returns: None
        """

        sql_classes.BASE.metadata.drop_all(self.engine)
        sql_classes.BASE.metadata.create_all(self.engine)

    def get_module_records(self, table_name):
        """Method to get records of a table in the database
        
            Parameters:
                table_name: str
                    Name of the table in the database
            Returns: List
                List of dictionaries with records of the specified table.        
        """

        raw_table = self.get_modules()[table_name]
        records = self.session.query(raw_table).all()
        return [record.__dict__ for record in records]

    # def get_modules(self) -> dict:
    #     """Method to get classes structure of every table in the database

    #         Returns: dict
    #             Dictionary with classes structure of every table in the database
    #     """

    #     self.modules = {"RawSpotify": sql_classes.RawSpotify, "RawGrammyAwards": sql_classes.RawGrammyAwards}
    #     return self.modules

    def data_to_connection(self) -> None:
        """Method to get credentials data to connect with database
        
            Returns: None
        """

        self.PARSER.read(self.CREDENTIALS_FILENAME)
        connection_config = {}

        if not self.PARSER.has_section(self.DATABASE_SECTION):
            raise Exception(f"Section {self.DATABASE_SECTION} not found in {self.CREDENTIALS_FILENAME} file.")

        params = self.PARSER.items(self.DATABASE_SECTION)
        for param in params:
            connection_config[param[0]] = param[1]
        if self.specified_host:
            connection_config["host"] = self.specified_host
        if self.specified_port:
            connection_config["port"] = self.specified_port
        if self.specified_user:
            connection_config["user"] = self.specified_user
        if self.specified_password:
            connection_config["password"] = self.specified_password
        self.connection_config = connection_config

    def create_connection(self) -> None:
        """Method to create a connection with database
        
            Returns: None
        """

        Session = sessionmaker(self.engine)
        self.session = Session()
        logging.info(f"Connected with {self.connection_config['database']} - user: {self.connection_config['user']}")

    def close_connection(self) -> None:
        """Method to close connection with database
        
            Returns: None
        """

        if self.session:
            self.session.close()
            logging.info(
                f"Connection with {self.connection_config['database']} - user: {self.connection_config['user']} closed."
            )

    def log(self, text) -> None:
        """Method to create log records
        
            Parameters:
                text: str
                    Text to be logged.
            
            Returns: None
        """

        logging.info(text)

    def create_engine_database(self) -> None:
        """Method to create a connection with database
        
            Returns: None
        """

        engine_url = f"{self.DATABASE_SECTION}+psycopg2://{self.connection_config['user']}:{self.connection_config['password']}@{self.connection_config['host']}:{self.connection_config['port']}/{self.connection_config['database']}"

        self.engine = create_engine(engine_url)

        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            logging.info(f"Database {self.connection_config['database']} created.")
