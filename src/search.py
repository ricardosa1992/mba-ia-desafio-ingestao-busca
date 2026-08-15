import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    try:
        store = PGVector(
            embeddings=OpenAIEmbeddings(model=EMBEDDING_MODEL),
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            use_jsonb=True,
        )

        def retrieve_context(pergunta):
            results = store.similarity_search_with_score(pergunta, k=10)
            return "\n\n".join(doc.page_content for doc, _score in results)

        chain = (
            {
                "contexto": RunnableLambda(retrieve_context),
                "pergunta": RunnablePassthrough(),
            }
            | ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            | ChatOpenAI(model=LLM_MODEL)
            | StrOutputParser()
        )
    except Exception as erro:
        print(f"Erro ao inicializar a busca: {erro}")
        return None

    if question:
        return chain.invoke(question)

    return chain