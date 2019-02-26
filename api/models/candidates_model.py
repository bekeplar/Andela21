from database.db_conn import DatabaseConnection
from api.utilitiez.responses import duplicate_candidate


class Candidate:
    def __init__(self):
        self.db = DatabaseConnection()

    def create_candidate(self, **kwargs):
        """Method for inserting a new party in the database"""
        candidate_name = kwargs.get("candidate_name")
        office_id = kwargs.get("OfficeId")
        party_id = kwargs.get("PartyId")
       
        sql = (
            "INSERT INTO candidates ("
            "candidate_name, office_id, party_id) VALUES ("
            f"'{candidate_name}', '{office_id}', '{party_id}') returning "
            "_id,candidate_name as CandidateName,"
            "party_id as PartyId, "
            "office_id as OfficeId ;"
        )
        self.db.cursor_database.execute(sql)
        new_candidate = self.db.cursor_database.fetchone()
        return new_candidate

    def get_candidates(self):
        sql = f"SELECT * FROM candidates;"
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchall()

    def get_one(self, cand_id):
        sql = f"SELECT * FROM candidates" f"WHERE _id='{cand_id}';"
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def update_candidate_name(self, cand_id, candidate_name):
        """Method for updating details."""
        candidate_name = candidate_name.strip()
        sql = (
            f"UPDATE candidates SET candidate_name='{candidate_name}' "
            f"WHERE _id='{cand_id}' returning _id, candidate_name;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def delete_candidate(self, cand_id):
        """Function to delete a candidate record."""
        sql = (
            f"DELETE FROM candidates "
            f"WHERE _id='{cand_id}' returning *;"
        )
        self.db.cursor_database.execute(sql)
        return self.db.cursor_database.fetchone()

    def check_candidate_exists(self, cand_name):
        """Function to check for duplication"""
        exists_sql = (
            "SELECT candidate_name where "
            f"candidate_name ='{cand_name}' ;"
        )
        self.db.cursor_database.execute(exists_sql)
        cand_exists = self.db.cursor_database.fetchone()
        error = {}
        if cand_exists and cand_exists.get("candidate_name") == cand_name:
            error["candidate_name"] = duplicate_candidate
        return error
