from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

from services.embedding import Embedding
from services.dynamo import DynamoRepository
from services.bedrock import BedrockClient
from services.ask_question import AskQuestion
from services.generate_document import GenerateDocument

# Inicialização da aplicação
app = FastAPI(
    title="DocBot API",
    description="API para gerenciar documentos técnicos com embeddings no DynamoDB e integração com LLM",
    version="1.0.0"
)

# Middleware de CORS (pode restringir em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas da API
app.include_router(router)

# Inicialização das dependências na startup
@app.on_event("startup")
def startup_event():
    embedding = Embedding()
    dynamo = DynamoRepository(embedding=embedding)
    bedrock = BedrockClient()
    ask = AskQuestion(dynamo=dynamo, embedding=embedding, bedrock=bedrock)
    generate_doc = GenerateDocument(bedrock=bedrock)

    app.state.embedding = embedding
    app.state.dynamo = dynamo
    app.state.bedrock = bedrock
    app.state.ask = ask
    app.state.generate_doc = generate_doc