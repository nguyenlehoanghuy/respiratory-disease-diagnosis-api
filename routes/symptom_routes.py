from flask import Blueprint, jsonify
from flask_cors import cross_origin

symptoms_bp = Blueprint('symptoms', __name__)


class SymptomRoutes:
    def __init__(self, diagnosis_service):
        self.diagnosis_service = diagnosis_service

    def init_routes(self, symptoms_bp):
        @symptoms_bp.route('/api/symptoms', methods=['GET'])
        @cross_origin()
        def get_initial_symptoms():
            symptoms = self.diagnosis_service.get_initial_symptoms()
            if not symptoms:
                return jsonify({"error": "No symptoms found in the ontology."}), 404
            return jsonify({"symptoms": symptoms})
