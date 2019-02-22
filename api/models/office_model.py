from database.db_conn import DatabaseConnection
from api.utilitiez.responses import duplicate_office


class Office:
    """Class that will contain Office objects """
    def __init__(self):
        self.db = DatabaseConnection()

    def create_office(self, **kwargs):
        """Method for inserting a new office in the database"""
        office_type = kwargs.get("type")
        office_name = kwargs.get("officeName")

        # Querry for inserting a new office record to db 
        sql = (
            "INSERT INTO offices ("
            "office_type, office_name) VALUES ("
            f"'{office_type}', '{office_name}') returning "
            "_id,office_type as office_type,"
            "office_name as office_name;"
        )
        self.db.cursor_database.execute(sql)
        new_office = self.db.cursor_database.fetchone()
        return new_office

    def get_all_offices(self):
        sql = f"SELECT * FROM offices;"
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchall()

    def get_an_office_by_id(self, off_id):
        """Function for getting an office by its id"""
        sql = f"SELECT * FROM offices" f"WHERE _id='{off_id}';"
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def update_office(self, off_id, office_name):
        """Method for updating details of an office."""
        office_name = office_name.strip()
        sql = (
            f"UPDATE offices SET office_name='{office_name}' "
            f"WHERE _id='{off_id}' returning _id, office_name;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def delete_office_record(self, off_id):
        """Function to delete an office record."""
        sql = (
            f"DELETE FROM incidents "
            f"WHERE _id='{off_id}' returning *;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def check_office_exists(self, office_name):
        """Making sure new office is unique"""
        exists_query = (
            "SELECT office_name from offices where "
            f"office_name ='{office_name}';"
        )
        self.db.cursor_database.execute(exists_query)
        office_exists = self.db.cursor_database.fetchone()
        error = {}
        if office_exists and office_exists.get("office_name") == office_name:
            error["office_name"] = duplicate_office
        return error

