import boto3
import json
import re

class BedrockClient:
    def __init__(self, region="us-east-1"):
        self.bedrock = boto3.client("bedrock-runtime", region_name=region)

    def call_model(self, context: str, question: str):
        conversation = [
            {
                "role": "user",
                "content": [{"text": f"Contexto: {context} "}],
            },
            {
                "role": "assistant",
                "content": [{"text": "Aqui está o contexto que você deve utilizar como base para responder a pergunta do usuário"}],
            },
            {
                "role": "user",
                "content": [{"text": f"{question}"}],
            }
        ]

        inference_config = {
            "maxTokens": 512,
            "temperature": 0.3,
            "topP": 0.9
        }

        response = self.bedrock.converse(
            modelId="meta.llama3-8b-instruct-v1:0",
            messages=conversation,
            inferenceConfig=inference_config
        )

        response_text = response["output"]["message"]["content"][0]["text"]

        return self._clean_response(response_text)

    def _clean_response(self, response):
        cleaned_response = re.sub(r'```[\s]*```', '', response)
        cleaned_response = re.sub(r'\n+', '\n', cleaned_response)
        cleaned_response = re.sub(r'(\n)(\*\*|__|\*|_|\n)', r'\1', cleaned_response)

        return cleaned_response