from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from pydantic import BaseModel, Field

router = APIRouter()

class DocumentUploadRequest(BaseModel):
    filename: str = Field(..., example="token_mtls.md", description="Nome do arquivo Markdown salvo na pasta 'docs'")
    topic: str = Field(..., example="token", description="Título ou identificador do conteúdo para busca futura")

class AskRequest(BaseModel):
    question: str = Field(..., example="Como autenticar via mTLS?", description="Pergunta a ser respondida pela IA")

@router.post("/upload-documents", summary="Upload de novo documento de referência")
def upload_document(
    request: Request,
    file: UploadFile = File(..., description="Arquivo de documentação (.md)"),
    topic: str = Form(..., description="Título ou tópico associado ao documento")
):
    try:
        content = file.file.read().decode("utf-8")
        loader = request.app.state.dynamo  # Usa DynamoRepository com o embedding injetado
        loader.save_document(topic=topic, content=content)

        return {"message": f"Documento '{topic}' inserido com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask", summary="Faça uma pergunta")
def ask_question(request: Request, body: AskRequest):
    try:
        ask = request.app.state.ask
        resposta = ask.ask_question_to_model(body.question)
        return resposta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))