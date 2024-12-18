import logging


class TreatmentService:
    def __init__(self, ontology_loader):
        self.graph = ontology_loader.get_graph()
        self.EX = ontology_loader.get_namespace()

    def get_treatments_for_disease(self, disease_name):
        try:
            query = f"""
            PREFIX ex: <http://example.com/schema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?treatment ?label WHERE {{
                ex:{disease_name} ex:hasTreatment ?treatment .
                ?treatment rdfs:label ?label .
            }}
            """
            treatments = self.graph.query(query)
            result = [
                {
                    "id": str(treatment).split("#")[-1],
                    "label": str(label)
                }
                for treatment, label in treatments
            ]

            logging.info(f"Treatments for {disease_name}: {result}")
            return result
        except Exception as e:
            logging.error(f"Error getting treatments: {e}")
            return []
