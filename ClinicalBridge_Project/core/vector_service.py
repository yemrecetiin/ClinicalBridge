import json
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import VECTOR_STORE_PATH, EMBEDDING_MODEL_NAME

class VectorService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
            google_api_key=api_key
        )
        self.vector_store_path = VECTOR_STORE_PATH

    def init_vector_store(self, data_path: str):
        """
        Reads patient_cohort.json, chunks the data, and builds a local FAISS index.
        """
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        texts = []
        metadatas = []
        for patient in data.get("patients", []):
            patient_id = patient.get("patient_id")
            content = f"Patient ID: {patient_id}\n"
            content += f"Demographics: {json.dumps(patient.get('demographics', {}))}\n"
            content += f"Diagnoses: {json.dumps(patient.get('diagnoses', []))}\n"
            content += f"Medications: {json.dumps(patient.get('active_medications', []))}\n"
            content += f"Labs: {json.dumps(patient.get('recent_labs', []))}\n"
            content += f"Clinical Notes: {patient.get('clinical_notes', '')}"
            
            texts.append(content)
            metadatas.append({"patient_id": patient_id})
            
        vectorstore = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        
        os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
        vectorstore.save_local(self.vector_store_path)
        print(f"Vector store initialized at {self.vector_store_path}")

    def retrieve_context(self, patient_id: str, query: str = "medical history") -> str:
        """
        Retrieves context specific to a patient ID.
        """
        if not os.path.exists(self.vector_store_path):
            raise FileNotFoundError("Vector store not initialized.")
            
        # allow_dangerous_deserialization is required for local trusted FAISS files
        vectorstore = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
        
        docs = vectorstore.similarity_search(query, k=2, filter={"patient_id": patient_id})
        if not docs:
            return "UNKNOWN"
        return "\n\n".join([doc.page_content for doc in docs])
