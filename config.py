import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv('FLASK_DEBUG', True)
    ONTOLOGY_PATH = os.path.join(os.path.dirname(
        __file__), 'ontology', 'respiratory_disease_ontology.owl')
