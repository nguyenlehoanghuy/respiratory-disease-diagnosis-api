from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

diagnosis_bp = Blueprint('diagnosis', __name__)


class DiagnosisRoutes:
    def __init__(self, diagnosis_service):
        self.diagnosis_service = diagnosis_service

    def init_routes(self, diagnosis_bp):
        @diagnosis_bp.route('/api/diagnose', methods=['POST'])
        @cross_origin()
        def diagnose():
            data = request.json
            symptoms = data.get("symptoms", [])

            if not symptoms:
                return jsonify({"error": "No symptoms provided"}), 400

            result = self.diagnosis_service.diagnose_diseases(symptoms)

            if result:
                return jsonify({"diseases": result})
            else:
                return jsonify({"message": "No matching diseases found."})
