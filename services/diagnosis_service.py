import logging


class DiagnosisService:
    def __init__(self, ontology_loader):
        self.graph = ontology_loader.get_graph()
        self.EX = ontology_loader.get_namespace()

    def get_initial_symptoms(self):
        try:
            # Truy vấn các đối tượng thuộc lớp Symptom và lấy nhãn của chúng
            query = """
            PREFIX ex: <http://example.com/schema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?symptom ?label WHERE {
                ?symptom a ex:Symptom .
                ?symptom rdfs:label ?label
            }
            """

            results = self.graph.query(query)

            # Chuyển đổi kết quả thành danh sách các triệu chứng với nhãn của chúng
            symptoms = [
                {
                    "id": str(symptom).split("#")[-1],
                    "label": str(label)
                }
                for symptom, label in results
            ]

            return symptoms
        except Exception as e:
            logging.error(f"Error getting symptoms: {e}")
            return []

    def diagnose_diseases(self, symptoms):
        try:
            # Loại bỏ 'hasSymptom' khỏi mảng triệu chứng
            print(symptoms)
            symptoms = [s for s in symptoms if s != 'hasSymptom']

            query = f"""
            PREFIX ex: <http://example.com/schema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?disease ?label WHERE {{
                ?disease a ex:Disease .
                ?disease rdfs:label ?label .
                {" ".join([f'?disease ex:hasSymptom ex:{symptom} .' for symptom in symptoms])}
            }}
            """

            diseases = self.graph.query(query)
            result = [
                {
                    "id": str(disease).split("#")[-1],
                    "label": str(label)
                }
                for disease, label in diseases
            ]

            logging.info(
                f"Diagnosed diseases for symptoms {symptoms}: {result}")
            return result
        except Exception as e:
            logging.error(f"Error diagnosing diseases: {e}")
            return []
