import logging


class TreatmentService:
    def __init__(self, ontology_loader):
        self.graph = ontology_loader.get_graph()
        self.EX = ontology_loader.get_namespace()

    def get_treatments_for_disease(self, disease_name):
        try:
            query = f"""
            PREFIX ctu: <http://www.ctu.edu.vn/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?treatment ?treatmentName WHERE {{
                ctu:{disease_name} ctu:hasTreatment ?treatment .
                ?treatment ctu:hasTreatmentName ?treatmentName .
            }}
            """
            treatments = self.graph.query(query)
            result = [
                {
                    "id": str(treatment).replace('http://www.ctu.edu.vn/', ''),
                    "label": str(label)
                }
                for treatment, label in treatments
            ]

            logging.info(f"Treatments for {disease_name}: {result}")
            return result
        except Exception as e:
            logging.error(f"Error getting treatments: {e}")
            return []
