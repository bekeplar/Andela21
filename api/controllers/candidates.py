from flask import jsonify, request
from api.models.candidates_model import Candidate
from api.utilitiez.validation import validate_a_candidate, validate_name
from api.utilitiez.responses import wrong_name

candid_obj = Candidate()


class CandidateController:
    """
    Class containing all logic connecting candidate views and models.
    """

    def new_candidate(self, data):
        if not request.data:
            return (
                jsonify({"error": "Please provide some  data", "status": 400}),
                400,
            )
        data = request.get_json()

        candidate_data = {
            "candidate_name": data.get("candidate_name"),
            "office_id": data.get("OfficeId"),
            "party_id": data.get("partyId"),
        }

        not_valid = validate_a_candidate(**candidate_data)
        response = None
        if not_valid:
            response = not_valid
        exists = candid_obj.check_candidate_exists(
            candidate_data["candidate_name"])
        response = None
        if exists:
            response = jsonify({"error": exists, "status": 409}), 409
        else:
            new_nominee = candid_obj.create_candidate(**candidate_data)
            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "Office": new_nominee,
                                "success": "candidate created successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        return response

    def get_candidates(self):
        results = candid_obj.get_candidates()
        return jsonify({"status": 200,
                        "data": results,
                        "message": "The following are the nominees"}), 200

    def get_one_candidate(self, candidate_id):
        results = candid_obj.get_one(candidate_id)
        response = None
        if results and "error" in results:
            response = (
                jsonify({"status": 401, "error": results["error"]}), 401)
        elif results:
            response = jsonify({"status": 200, "data": [results]}), 200
        else:

            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "Candidate with such id not found"
                    }
                ),
                404,
            )
        return response

    def delete(self, candidate_id):
        response = None

        results = candid_obj.delete_candidate(candidate_id)
        details = candid_obj.get_one(candidate_id)
        if not results:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "such candidate does not exist",
                    }
                ),
                404,
            )
        elif results:

            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "office": details,
                                "success": "Nominee has been deleted successfully"
                            }
                        ],
                    }
                ),
                200,
            )
        else:
            response = (
                jsonify(
                    {
                        "status": 403,
                        "error": (
                            "Access Denied"
                        ),
                    }
                ),
                403,
            )
        return response

    def change_candidate_details(self, candidate_id, data):
        candidate_name = request.get_json(force=True).get("candidate_name")
        results = candid_obj.get_one(candidate_id)
        response = None
        if not results:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "candidate with specified id does not exist",
                    }
                ),
                404,
            )
        elif not validate_name(candidate_name):
            response = jsonify({"status": 400, "error": wrong_name}), 400

        else:
            update = candid_obj.get_one(candidate_id)
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "id": update["candidate_id"],
                                "success": "Candidate name updated successfully",
                            }
                        ],
                    }
                ),
                200,
            )
        return response
