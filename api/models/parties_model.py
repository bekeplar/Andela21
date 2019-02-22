from database.db_conn import DatabaseConnection
from api.utilitiez.responses import duplicate_logo, duplicate_party_name


class Party:
    """Class that will contain Party objects """
    def __init__(self):
        self.db = DatabaseConnection()

    def create_Parties(self, **kwargs):
        """Method for inserting a new party in the database"""
        party_name = kwargs.get("party_name")
        hq_address = kwargs.get("HqAddress")
        logo_url = kwargs.get("logourl")
       
        sql = (
            "INSERT INTO parties ("
            "party_name, hq_address, logo_url) VALUES ("
            f"'{party_name}', '{hq_address}', '{logo_url}') returning "
            "_id,party_name as partyName,"
            "hq_address as HqAddress, "
            "logo_url as logourl ;"
        )
        self.db.cursor_database.execute(sql)
        new_office = self.db.cursor_database.fetchone()
        return new_office

    def get_parties(self):
        sql = f"SELECT * FROM parties;"
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchall()

    def get_party_by_id(self, party_id):
        """Function for getting a party by its id"""
        sql = f"SELECT * FROM parties" f"WHERE _id='{party_id}';"
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def update_party_name(self, party_id, party_name):
        """Method for updating details."""
        party_name = party_name.strip()
        sql = (
            f"UPDATE parties SET party_name='{party_name}' "
            f"WHERE _id='{party_id}' returning _id, party_name;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def delete_record(self, party_id):
        """Function to delete a party record."""
        sql = (
            f"DELETE FROM parties "
            f"WHERE _id='{party_id}' returning *;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def check_party_exists(self, party_name, party_logo):
        """Making sure that a party is unique"""
        party_exists_sql = (
            "SELECT party_name, logo_url from parties where "
            f"party_name ='{party_name}' OR"
            f" logo_url='{party_logo}';"
        )
        self.db.cursor_database.execute(party_exists_sql)
        party_exists = self.db.cursor_database.fetchone()
        error = {}
        if party_exists and party_exists.get("party_name") == party_name:
            error["party_name"] = duplicate_party_name
        if party_exists and party_exists.get("logo_url") == party_logo:
            error["party_name"] = duplicate_logo
        return error


