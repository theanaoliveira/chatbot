import boto3

from services.embedding import Embedding

class DynamoRepository:
    def __init__(self, embedding: Embedding, table_name="docbot-texts", region="us-east-1"):
        self.embedding = embedding
        self.dynamodb = boto3.resource("dynamodb", region_name=region)
        self.table = self.dynamodb.Table(table_name)

    def get_all_documents(self):
        response = self.table.scan()
        documents = response.get("Items", [])

        return documents
    
    def save_document(self, topic: str, content: any):
        embedding_str = self.embedding.encode_content(content)

        item = {
            "topic": topic,
            "content": content,
            "embedding": embedding_str
        }

        self.table.put_item(Item=item)