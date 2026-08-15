# Desafio MBA Engenharia de Software com IA - Full Cycle

## Ingestão e Busca Semântica com LangChain e Postgres

Sistema de RAG (Retrieval-Augmented Generation) em Python que ingere um PDF em
um banco PostgreSQL com pgvector, faz busca semântica sobre o conteúdo e responde
perguntas via CLI, **usando apenas o contexto recuperado do PDF**.

## Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Uma API Key da OpenAI

## Ordem de execução

```bash
# 1. Subir o banco (Postgres + pgvector). O serviço bootstrap cria a extensão "vector".
docker compose up -d

# 2. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows PowerShell
# source venv/bin/activate     # Linux / macOS

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Configurar o ambiente
copy .env.example .env         # Windows  (cp .env.example .env no Linux/macOS)
# edite o .env e preencha os valores (ver seção abaixo)

# 5. Ingerir o PDF no banco vetorial (rodar uma vez)
python src/ingest.py

# 6. Iniciar o chat interativo
python src/chat.py
```

## Variáveis de ambiente (`.env`)

Copie `.env.example` para `.env` e preencha os valores.

| Variável | Descrição |
| --- | --- |
| `OPENAI_API_KEY` | Chave da API da OpenAI (obrigatória). |
| `OPENAI_EMBEDDING_MODEL` | Modelo de embeddings da OpenAI. Padrão: `text-embedding-3-small`. |
| `OPENAI_LLM_MODEL` | Modelo de LLM da OpenAI para responder. Padrão: `gpt-5-nano`. |
| `DATABASE_URL` | String de conexão do Postgres. Com o compose fornecido: `postgresql+psycopg://postgres:postgres@localhost:5432/rag`. |
| `PG_VECTOR_COLLECTION_NAME` | Nome da collection/tabela usada pelo `PGVector`. |
| `PDF_PATH` | Caminho do PDF de origem (ex.: `document.pdf` na raiz do projeto). |

**Importante:** trocar o modelo de embeddings depois da ingestão exige refazer a
ingestão, pois as dimensões dos vetores gravados precisam bater com as da consulta.
