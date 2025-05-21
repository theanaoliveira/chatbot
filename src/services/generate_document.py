import json

from tempfile import NamedTemporaryFile

from services.bedrock import BedrockClient

class GenerateDocument:
    def __init__(self, bedrock: BedrockClient):
        self.bedrock = bedrock

    def generate_markdown_doc(self, content: any):

        swagger_dict = json.loads(content)

        GenerateDocument._validar_swagger(swagger_dict)

        swagger_str = json.dumps(swagger_dict, indent=2)
        markdown_str = self.bedrock.generate_document(swagger_str)

        return GenerateDocument._salvar_markdown_em_arquivo(markdown_str)

    @staticmethod
    def _validar_swagger(json_dict: dict):
        if not isinstance(json_dict, dict):
            raise ValueError("O conteúdo não é um JSON válido.")

        if "swagger" not in json_dict and "openapi" not in json_dict:
            raise ValueError("O arquivo não parece ser um Swagger ou OpenAPI.")

        if "paths" not in json_dict:
            raise ValueError("O Swagger precisa conter a definição de 'paths'.")
        
    @staticmethod        
    def _salvar_markdown_em_arquivo(markdown_str: str) -> str:
        with NamedTemporaryFile(delete=False, suffix=".md", mode="w", encoding="utf-8") as tmp:
            tmp.write(markdown_str)
            return tmp.name
