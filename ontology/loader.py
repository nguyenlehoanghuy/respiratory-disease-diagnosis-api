import logging
from rdflib import Graph, Namespace


class OntologyLoader:
    def __init__(self, ontology_path):
        self.graph = Graph()
        self.EX = Namespace("http://example.com/schema#")

        try:
            self.graph.parse(ontology_path, format="turtle")
            logging.info(f"Ontology loaded successfully from {ontology_path}")
        except Exception as e:
            logging.error(f"Error loading ontology: {e}")
            raise

    def get_graph(self):
        return self.graph

    def get_namespace(self):
        return self.EX
