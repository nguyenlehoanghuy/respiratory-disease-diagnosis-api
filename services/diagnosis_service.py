import logging


class DiagnosisService:
    def __init__(self, ontology_loader):
        self.graph = ontology_loader.get_graph()
        self.EX = ontology_loader.get_namespace()

    def get_initial_symptoms(self):
        try:
            # Truy vấn các đối tượng thuộc lớp Symptom và lấy nhãn của chúng
            query = """
            PREFIX ctu: <http://www.ctu.edu.vn/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?symptom ?symptomName WHERE {
                ?symptom a ctu:Symptom .
                ?symptom ctu:hasSymptomName ?symptomName .
            }
            """

            results = self.graph.query(query)

            # Chuyển đổi kết quả thành danh sách các triệu chứng với nhãn của chúng
            symptoms = [
                {
                    "id": str(symptom).replace('http://www.ctu.edu.vn/', ''),
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
            PREFIX ctu: <http://www.ctu.edu.vn/>
            SELECT ?disease ?diseaseName WHERE {{
                ?disease a ctu:Disease .
                ?disease ctu:hasDiseaseName ?diseaseName .
                {" ".join(
                    [f'?disease ctu:hasSymptom ctu:{symptom} .' for symptom in symptoms])}
            }}
            """

            diseases = self.graph.query(query)
            result = [
                {
                    "id": str(disease).replace('http://www.ctu.edu.vn/', ''),
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

    def get_related_symptoms(self, symptom_id):
        try:
            # Truy vấn các triệu chứng liên quan đến symptom_id
            query = f"""
            PREFIX ctu: <http://www.ctu.edu.vn/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?relatedSymptom ?relatedSymptomName 
            WHERE {{
                ctu:{symptom_id} ctu:relatedTo ?relatedSymptom .
                ?relatedSymptom ctu:hasSymptomName ?relatedSymptomName .
            }}
            """

            results = self.graph.query(query)

            # Chuyển đổi kết quả thành danh sách các triệu chứng liên quan
            related_symptoms = [
                {
                    "id": str(relatedSymptom).replace('http://www.ctu.edu.vn/', ''),
                    "label": str(relatedSymptomName)
                }
                for relatedSymptom, relatedSymptomName in results
            ]

            return related_symptoms
        except Exception as e:
            logging.error(
                f"Error getting related symptoms for {symptom_id}: {e}")
            return []
