import boto3
import json

class BedrockClient:
    def __init__(self, region="us-east-1"):
        self.bedrock = boto3.client("bedrock-runtime", region_name=region)

    def call_model(self, context: str, question: str):
        prompt = (
            "Você é um assistente técnico experiente, amigável e simpático. Responda de forma natural e conversacional, "
            "evite respostas longas e vá direto ao ponto.\n\n"
            "Se a pergunta for um cumprimento, como 'oi' ou 'olá', responda de forma curta e amigável.\n\n"
            "Se a pergunta for técnica, forneça uma resposta objetiva e evite explicações longas.\n\n"
            "Se solicitado, gere código claro e direto na linguagem solicitada.\n\n"
            f"\nContexto:\n{context}\n\n"
            f"Pergunta: {question}"
        )

        body = {
            "prompt": prompt,
            "max_gen_len": 1024,
            "temperature": 0.2,
            "top_p": 0.9
        }

        model_response = self.bedrock.invoke_model(
            modelId="meta.llama3-8b-instruct-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )

        response_body = model_response['body'].read()
        response_json = json.loads(response_body.decode('utf-8'))

        generation = response_json.get('generation')

        if not generation or not isinstance(generation, str) or not generation.strip():
            raise ValueError("A resposta do modelo está vazia ou mal formatada.")

        return generation.strip()