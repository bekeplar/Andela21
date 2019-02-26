from flask import jsonify, request
from api.models.parties_model import Party
from api.utilitiez.validation import validate_parties, validate_name
from api.utilitiez.responses import wrong_name

party_obj = Party()


class PartiesController:
    """
    Class containing all logic connecting Parties views and models.
    """

    def create_new_party(self, data):
        if not request.data:
            return (
                jsonify({"error": "Please provide some  data", "status": 400}),
                400,
            )
        data = request.get_json()

        new_party_data = {
            "party_name": data.get("partyName"),
            "hq_address": data.get("HqAddress"),
            "logo_url": data.get("logourl"),
        }

        not_valid = validate_parties(**new_party_data)
        response = None
        if not_valid:
            response = not_valid
        exists = party_obj.check_party_exists(
            new_party_data["part_name"], new_party_data["logo_url"])
        response = None
        if exists:
            response = jsonify({"error": exists, "status": 409}), 409
        else:
            new_party = party_obj.create_Parties(**new_party_data)
            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "Office": new_party,
                                "success": "Created new party successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        return response

    def get_all_parties(self):
        results = party_obj.get_parties()
        return jsonify({"status": 200,
                        "data": results,
                        "message": "Office records found"}), 200

    def get_one_party(self, party_id):
            results = party_obj.get_party_by_id(party_id)
            response = None
            if results and "error" in results:
                response = (jsonify({"status": 401, "error": results["error"]}), 401)
            elif results:
                response = jsonify({"status": 200, "data": [results]}), 200
            else:

                response = (
                    jsonify(
                        {
                            "status": 404,
                            "error": "Party with such id not found"
                        }
                    ),
                    404,
                )
            return response

    def delete_party(self, party_id):
        response = None

        outcome = party_obj.delete_record(party_id)
        party_details = party_obj.get_party_by_id(party_id)
        if not outcome:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "such party does not exist",
                    }
                ),
                404,
            )
        elif outcome:

            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "office": party_details,
                                "success": "Party record has been deleted"
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

    def change_details(self, party_id, data):
        new_name = request.get_json(force=True).get("party_name")
        outcome = party_obj.get_party_by_id(party_id)
        response = None
        if not outcome:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "Party with specified id does not exist",
                    }
                ),
                404,
            )
        elif not validate_name(new_name):
            response = jsonify({"status": 400, "error": wrong_name}), 400

        else:
            update = party_obj.update_party_name(party_id, new_name)
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "id": update["party_id"],
                                "success": "Party name updated successfully",
                            }
                        ],
                    }
                ),
                200,
            )
        return response
