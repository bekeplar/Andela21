from flask import jsonify, request
from api.models.office_model import Office
from api.utilitiez.validation import validate_new_office, validate_name
from api.utilitiez.responses import wrong_name


office_obj = Office()


class OfficeController:
    """
    Class containing all logic connecting Office views and models.
    """

    def new_office(self, data):
        if not request.data:
            return (
                jsonify({"error": "Please provide some  data", "status": 400}),
                400,
            )
        data = request.get_json()

        new_office_inputs = {
            "office_type": data.get("type"),
            "office_name": data.get("officeName")
        }

        not_valid = validate_new_office(**new_office_inputs)
        response = None
        if not_valid:
            response = not_valid
        office_exists = office_obj.check_office_exists(
            new_office_inputs["office_name"])
            
        response = None
        if office_exists:
            response = jsonify({"error": office_exists, "status": 409}), 409

        else:
            new_office = office_obj.create_office(**new_office_inputs)
            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                "Office": new_office,
                                "success": "Created new office successfully",
                            }
                        ],
                    }
                ),
                201,
            )
        return response

    def get_offices(self):
        results = office_obj.get_all_offices()

        return jsonify({"status": 200,
                        "data": results,
                        "message": "Office records found"}), 200

    def get_an_office(self, office_id):
            results = office_obj.get_an_office_by_id(office_id)
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
                            "error": "Office with such id not found"
                        }
                    ),
                    404,
                )
            return response

    def delete_record(self, office_id):
        response = None

        results = office_obj.delete_office_record(office_id)
        office_details = office_obj.get_an_office_by_id(office_id)
        if not results:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "Office record does not exist",
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
                                "office": office_details,
                                "success": "Office has been deleted"
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

    def edit_office(self, office_id, data):
        update_name = request.get_json(force=True).get("office_name")
        results = office_obj.get_an_office_by_id(office_id)
        response = None
        if not results:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": "Office with specified id does not exist",
                    }
                ),
                404,
            )
        elif not validate_name(office_name):
            response = jsonify({"status": 400, "error": wrong_name}), 400

        else:

            update = office_obj.update_office(office_id, update_name)
            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "id": update["office_id"],
                                "success": "Office name updated successfully",
                            }
                        ],
                    }
                ),
                200,
            )

        return response
