from flask import Blueprint, request
from api.controllers.office import OfficeController
from api.utilitiez.auth_token import (
    token_required,
    non_admin,
    admin_required,
)

office_bp = Blueprint("offices", __name__, url_prefix="/api/v1")

office = OfficeController()


@office_bp.route("/offices", methods=["POST"])
@token_required
@non_admin
def Add_office():
    data = request.get_json(force=True)
    return office.new_office(data)


@office_bp.route("/offices", methods=["GET"])
@token_required
@non_admin
def fetch_offices():
    return office.get_offices()


@office_bp.route("/offices/<office_id>", methods=["GET"])
@token_required
@non_admin
def fetch_Single_office(office_id):
    return office.get_an_office(office_id)


@office_bp.route("/offices/<office_id>", methods=["DELETE"])
@token_required
@admin_required
def Delete_single_office(office_id):
    return office.delete_record(office_id)


@office_bp.route("/offices/<office_id>", methods=["PUT"])
@token_required
@admin_required
def Update_Single_office(office_id):
    data = request.get_json(force=True)
    return office.edit_office(office_id, data)