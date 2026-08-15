import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def ingest_pdf():
    documents = PyPDFLoader(PDF_PATH).load()
    print(f"PDF carregado: {PDF_PATH} ({len(documents)} paginas)")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    print(f"Chunks gerados: {len(chunks)}")

    store = PGVector(
        embeddings=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )
    store.add_documents(chunks)

    print(f"Ingestao concluida na collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    ingest_pdf()
