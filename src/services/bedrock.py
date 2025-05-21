import boto3
import re

class BedrockClient:
    def __init__(self, region="us-east-1"):
        self.bedrock = boto3.client("bedrock-runtime", region_name=region)

    def _clean_response(self, response):
        cleaned_response = re.sub(r'```[\s]*```', '', response)
        cleaned_response = re.sub(r'\n+', '\n', cleaned_response)
        cleaned_response = re.sub(r'(\n)(\*\*|__|\*|_|\n)', r'\1', cleaned_response)

        return cleaned_response

    def _call_model(self, conversation: list[dict[str, any]], max_tokens: int):
        inference_config = {
            "maxTokens": max_tokens,
            "temperature": 0.3,
            "topP": 0.9
        }

        response = self.bedrock.converse(
            modelId="meta.llama3-8b-instruct-v1:0",
            messages=conversation,
            inferenceConfig=inference_config
        )

        return response["output"]["message"]["content"][0]["text"]

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

        response_text = self._call_model(conversation, 1024)

        return self._clean_response(response_text)
    
    def generate_document(self, content: str):
        conversation = [
            {
                "role": "user",
                "content": [{"text": f"""
                Gere um arquivo `.md` (Markdown) completo com base no contrato Swagger a seguir. A documentação deve incluir:

                - Nome da API como título
                - Explicação completa do propósito de cada endpoint
                - Método HTTP e path
                - Parâmetros com tipo e obrigatoriedade
                - Corpo da requisição, se houver
                - Exemplo de curl de cada requisição
                - Respostas possíveis com status e descrição
                - Estilo organizado, limpo e de fácil leitura
                - Em português do brasil

                Swagger:
                {content}
                """}]
            }
        ]

        return self._call_model(conversation, 2048)