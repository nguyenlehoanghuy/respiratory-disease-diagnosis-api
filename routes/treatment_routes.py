from flask import Blueprint, jsonify
from flask_cors import cross_origin

treatment_bp = Blueprint('treatment', __name__)


class TreatmentRoutes:
    def __init__(self, treatment_service):
        self.treatment_service = treatment_service

    def init_routes(self, treatment_bp):
        @treatment_bp.route('/api/treatment/<disease_name>', methods=['GET'])
        @cross_origin()
        def get_treatment(disease_name):
            if not disease_name:
                return jsonify({"error": "No disease name provided"}), 400

            treatments = self.treatment_service.get_treatments_for_disease(
                disease_name)

            if treatments:
                return jsonify({"disease": disease_name, "treatments": treatments})
            else:
                return jsonify({"message": f"No treatments found for disease {disease_name}."})
