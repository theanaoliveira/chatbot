import boto3
import json

class BedrockClient:
    def __init__(self, region="us-east-1"):
        self.bedrock = boto3.client("bedrock-runtime", region_name=region)

    def call_model(self, context: str, question: str):
        prompt = (
            f"Você é um assistente técnico experiente. Responda de forma clara, objetiva e direta, sem divagações ou informações desnecessárias.\n\n"
            f"\nContexto:\n{context}\n\n"
            f"Pergunta: {question}"
        )

        body = {
            "prompt": prompt,
            "max_gen_len": 512,  # Número máximo de tokens de saída
            "temperature": 0.1,  # Controla a aleatoriedade (quanto mais baixo, mais determinístico)
            "top_p": 1,  # Controle de diversidade (Top-p sampling)
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