import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import runtime_mode
import os


class DatabaseConnection:
    def __init__(self):
        """class initializing method"""
        try:
            self.database_name = ""
            self.database_connect = None

            if runtime_mode == "Development":
                self.database_connect = self.database_connection("postgres")

            if runtime_mode == "Testing":
                self.database_connect = self.database_connection("testing_db")

            if runtime_mode == "Production":
                DATABASE_URL = os.environ['DATABASE_URL']
                self.database_connect = psycopg2.connect(
                    DATABASE_URL, sslmode='require')

            self.database_connect.autocommit = True
            self.cursor_database = self.database_connect.cursor(
                cursor_factory=RealDictCursor)
            print('Connected to the database successfully.')

            create_user_table = """CREATE TABLE IF NOT EXISTS users
            (
                user_id SERIAL NOT NULL PRIMARY KEY,
                first_name VARCHAR(25) NOT NULL,
                last_name VARCHAR(25) NOT NULL,
                other_names VARCHAR(25) NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone_number VARCHAR(10) NOT NULL UNIQUE,
                user_name VARCHAR(50) NOT NULL UNIQUE,
                registered_on DATE DEFAULT CURRENT_TIMESTAMP,
                passport_url VARCHAR(25) NULL,
                user_password VARCHAR(255) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE
            );"""

            create_office = """CREATE TABLE IF NOT EXISTS offices(
                        office_id          SERIAL  PRIMARY KEY NOT NULL,
                        office_type   VARCHAR(100) NOT NULL,
                        office_name   VARCHAR(100) UNIQUE NOT NULL);"""

            create_petition = """CREATE TABLE IF NOT EXISTS petitions(
                            office_id          SERIAL  PRIMARY KEY NOT NULL,
                            created_on   DATE NOT NULL DEFAULT CURRENT_DATE,
                            created_by   INTEGER NOT NULL REFERENCES users(user_id),
                            office       INTEGER NOT NULL REFERENCES offices(office_id),
                            body         VARCHAR(500) NOT NULL );"""

            create_parties = """CREATE TABLE IF NOT EXISTS parties(
                            party_id         SERIAL  PRIMARY KEY NOT NULL,
                            party_name  VARCHAR(50)   UNIQUE NOT NULL,
                            hq_address  VARCHAR(100)  NOT NULL,
                            logo_url    VARCHAR(200)  NOT NULL);"""

            create_votes = """CREATE TABLE IF NOT EXISTS votes(
                        party_id          SERIAL  PRIMARY KEY NOT NULL,
                        created_on    DATE NOT NULL DEFAULT CURRENT_DATE,
                        created_by    INTEGER NOT NULL REFERENCES users(user_id),
                        office        INTEGER NOT NULL REFERENCES offices(office_id),
                        candidate     INTEGER NOT NULL REFERENCES  candidates(candidate_id));"""

            create_candidates = """CREATE TABLE IF NOT EXISTS candidates(
                                candidate_id  SERIAL  PRIMARY KEY NOT NULL,
                                office        INTEGER NOT NULL REFERENCES offices(office_id),
                                party         INTEGER NOT NULL REFERENCES parties(party_id),
                                candidate_name     VARCHAR NOT NULL);"""
            # Store queries in a list and loop over each

            self.cursor_database.execute(create_user_table)
            self.cursor_database.execute(create_office)
            self.cursor_database.execute(create_parties)
            self.cursor_database.execute(create_candidates)
            self.cursor_database.execute(create_votes)
            self.cursor_database.execute(create_petition)

            # self.cursor_database.execute(create_petition)

        except (Exception, psycopg2.Error) as e:
            print(e)

    def database_connection(self, database_name):
        """Function for connecting to appropriate database"""
        return psycopg2.connect(dbname='postgres', user='postgres',
                                host='localhost', port=5432, password='bekeplar')

    def drop_table(self, table_name):
        """
        Drop tables after tests
        """
        drop = f"DROP TABLE {table_name};"
        self.cursor_database.execute(drop)


if __name__ == '__main__':
    database_name = DatabaseConnection()
