import logging
from flask import Flask
from flask_cors import CORS
from config import Config
from ontology.loader import OntologyLoader
from services.diagnosis_service import DiagnosisService
from services.treatment_service import TreatmentService
from routes.symptom_routes import SymptomRoutes, symptoms_bp
from routes.diagnosis_routes import DiagnosisRoutes, diagnosis_bp
from routes.treatment_routes import TreatmentRoutes, treatment_bp

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    # Load Ontology
    ontology_loader = OntologyLoader(app.config['ONTOLOGY_PATH'])

    # Initialize Services
    diagnosis_service = DiagnosisService(ontology_loader)
    treatment_service = TreatmentService(ontology_loader)

    # Initialize Routes
    symptom_routes = SymptomRoutes(diagnosis_service)
    diagnosis_routes = DiagnosisRoutes(diagnosis_service)
    treatment_routes = TreatmentRoutes(treatment_service)

    # Register Blueprints
    symptom_routes.init_routes(symptoms_bp)
    diagnosis_routes.init_routes(diagnosis_bp)
    treatment_routes.init_routes(treatment_bp)

    app.register_blueprint(symptoms_bp)
    app.register_blueprint(diagnosis_bp)
    app.register_blueprint(treatment_bp)

    return app


# run.py
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
