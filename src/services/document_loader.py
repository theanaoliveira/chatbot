import os

from services.dynamo import Dynamo
from services.embedding import Embedding

class DocumentLoader:    
    def store_doc_from_file(self, filename: str, topic: str, dynamo: Dynamo):
        base_path = os.path.join(os.path.dirname(__file__), "..", "docs")
        file_path = os.path.abspath(os.path.join(base_path, filename))

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo '{filename}' não encontrado na pasta 'docs'.")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        dynamo.save_document(topic, content)

        return {"message": f"Documento '{topic}' inserido com sucesso."}
