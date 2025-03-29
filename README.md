
# 🤖 DocBot API

Uma API inteligente com **RAG (Retrieval-Augmented Generation)** para responder perguntas com base em documentos Markdown salvos no DynamoDB. Utiliza **embeddings com Sentence Transformers** e **integração com Amazon Bedrock (LLaMA 3)** para gerar respostas contextuais e relevantes.

---

## 🚀 Funcionalidades

- 📥 Upload de documentos `.md` com geração de embeddings
- 🔎 Busca vetorial por similaridade (cosine similarity)
- 🧠 Geração de respostas com Amazon Bedrock (LLaMA3)
- 🔐 Modular e escalável com FastAPI
- ☁️ Integração com AWS: DynamoDB + Bedrock

---

## ⚙️ Tecnologias utilizadas

- Python 3.11+
- FastAPI
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Amazon Bedrock (LLaMA3)
- Amazon DynamoDB
- NumPy + Decimal
- Docker e Docker Compose

---

## 📦 Estrutura de pastas

```text
src/
├── api/
│   └── routes.py               # Rotas da API
├── services/
│   ├── ask_question.py         # Orquestração RAG
│   ├── bedrock_client.py       # Chamada à API do Bedrock
│   ├── document_loader.py      # Leitura e armazenamento de documentos
│   ├── dynamo_repository.py    # Interface com DynamoDB
│   └── embedding.py            # Geração e conversão de embeddings
├── docs/                       # Documentos de entrada (.md)
├── app.py                      # Inicialização do FastAPI
├── requirements.txt
├── Dockerfile
└── docker-compose.yaml
```

---

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/sua-org/docbot-api.git
cd docbot-api
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure variáveis de ambiente

Você pode usar um `.env`, ou configurar variáveis direto no sistema:

```bash
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

---

## ▶️ Executando localmente

```bash
uvicorn src.app:app --reload
```

Acesse a documentação interativa:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐳 Executando com Docker

```bash
docker build -t docbot-api .
docker run -p 8000:8000 docbot-api
```

Ou com Docker Compose:

```bash
docker-compose up --build
```

---

## 🧪 Exemplos de uso

### 1. Upload de documento

```http
POST /upload-documents
Content-Type: multipart/form-data

Campos:
- file: documento .md
- topic: nome do tópico associado
```

### 2. Perguntar à IA

```http
POST /ask
Content-Type: application/json

{
  "question": "Como autenticar via mTLS?"
}
```

---

## ✅ TODOs

- [ ] Adicionar autenticação (JWT ou API Key)
- [ ] Salvar histórico de perguntas e respostas
- [ ] Adicionar testes automatizados (`pytest`)
- [ ] Limiar de similaridade para considerar documentos
- [ ] Suporte a outros formatos (PDF, DOCX, etc.)

---

## 📬 Contato

Desenvolvido por Ana Caroline.  
🔗 [linkedin.com/in/theanaoliveira](https://linkedin.com/in/theanaoliveira)

---

## 📝 Licença

MIT License