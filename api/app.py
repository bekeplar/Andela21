from flask import Flask, jsonify
from api.views.user_view import users_bp
from api.views.office_view import office_bp
from instance.config import app_config


def create_app(config_name):
    """Set up Flask application in function"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route("/")
    def _home():
        return (
            jsonify({"message": "Welcome to iReporter Api V1", "status": 200}),
            200,
        )

    @app.errorhandler(400)
    def _page_not_found(e):
        return (jsonify({"error": "Bad JSON format data", "status": 400}), 400)

    @app.errorhandler(401)
    def _not_authorized(e):
        return (
            jsonify(
                {
                    "error": "Access Denied",
                    "status": 401,
                }
            ),
            401,
        )

    @app.errorhandler(404)
    def _page_not_found(e):
        return (
            jsonify({"error": "Endpoint for specified URL does not exist"}),
            404,
        )

    @app.errorhandler(405)
    def _method_not_allowed(e):
        return (jsonify({"error": "Method not allowed"}), 405)

    app.register_blueprint(users_bp)
    app.register_blueprint(office_bp)
    return app
