from services.bedrock import BedrockClient
from services.dynamo import DynamoRepository
from services.embedding import Embedding

class AskQuestion:
    def __init__(self, dynamo: DynamoRepository, embedding: Embedding, bedrock: BedrockClient):
        self.embedding = embedding
        self.dynamo = dynamo
        self.bedrock = bedrock

    def ask_question_to_model(self, question: str):
        documents = self.dynamo.get_all_documents()

        if not documents:
            return {
                "resposta": "Nenhum documento foi encontrado na base de conhecimento.",
                "confianca": 0,
                "documentos_utilizados": []
            }
        
        relevant_documents = self._relevant_documents(documents, question)

        if not relevant_documents:
            return {
                "resposta": "Nenhum documento relevante foi encontrado para essa pergunta.",
                "confianca": 0,
                "documentos_utilizados": []
            }

        context = "\n\n".join([doc["content"] for doc in relevant_documents])

        try:
            response = self.bedrock.call_model(context, question)
        except Exception as e:
            response = f"Erro ao chamar o modelo Bedrock: {str(e)}"

        return {
            "resposta": response.strip(),
            "confianca": round(relevant_documents[0]["score"], 4),
            "documentos_utilizados": [
                {"topic": d["topic"], "score": round(d["score"], 4)}
                for d in relevant_documents
            ]
        }

    def _relevant_documents(self, documents: any, question: str):
        similar_documents = []
        question_embedding = self.embedding.decode_content(self.embedding.encode_content(question))

        for doc in documents:
            if "embedding" in doc:
                doc_embedding = self.embedding.decode_content(doc["embedding"])

                score = self.embedding.cosine_similarity(question_embedding, doc_embedding)
                
                similar_documents.append({
                    "topic": doc["topic"],
                    "content": doc["content"],
                    "score": score
                })

        return sorted(similar_documents, key=lambda d: d["score"], reverse=True)[:3]



