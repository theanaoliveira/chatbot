from decimal import Decimal, ROUND_HALF_UP

import numpy as np

from sentence_transformers import SentenceTransformer


class Embedding:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
    def encode_content(self, content: any):
        embedding_np = self.embedding_model.encode(content)
        embedding_dec = [
            Decimal(f"{x:.10f}").quantize(Decimal("1.0000000000"), rounding=ROUND_HALF_UP)
            for x in embedding_np
        ]
        return embedding_dec
    
    @staticmethod
    def decode_content(embedding_dec):
        return [float(x) for x in embedding_dec]

    @staticmethod
    def to_numpy(vector):
        return np.array(vector)
    
    @staticmethod
    def cosine_similarity(question_vector, document_vector):
        question_vector = Embedding.to_numpy(question_vector)
        document_vector = Embedding.to_numpy(document_vector)
        
        return np.dot(question_vector, document_vector) / (
            np.linalg.norm(question_vector) * np.linalg.norm(document_vector)
        )