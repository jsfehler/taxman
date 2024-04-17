from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger

from .views.income_tax import income_tax


def create_app():
    """Create and configure the app."""
    app = Flask(__name__)
    CORS(app)
    Swagger(app)

    app.register_blueprint(income_tax)

    @app.errorhandler(400)
    def bad_respect(e):
        return jsonify(error=str(e)), 400

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(422)
    def unprocessable_entity(e):
        return jsonify(error=str(e)), 422

    @app.errorhandler(503)
    def service_unavailable(e):
        return jsonify(error=str(e)), 503

    return app
