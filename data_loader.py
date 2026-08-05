import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Embedding model (served via HF Inference API — no local download needed)
EMBED_MODEL = "BAAI/bge-m3"
EMBED_DIM = 1024

# Text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Lazily loaded HF Inference Client
_hf_client = None


def _get_hf_client():
    global _hf_client
    if _hf_client is None:
        from huggingface_hub import InferenceClient
        hf_token = os.getenv("HF_TOKEN")
        _hf_client = InferenceClient(
            provider="hf-inference",
            api_key=hf_token,
        )
    return _hf_client


def load_and_chunk_pdf(path: str) -> list[str]:
    """
    Load a PDF and split it into chunks.
    """
    from langchain_community.document_loaders import PyPDFLoader
    loader = PyPDFLoader(path)
    documents = loader.load()

    chunks = splitter.split_documents(documents)

    return [chunk.page_content for chunk in chunks]


def load_and_chunk_docx(path: str) -> list[str]:
    """
    Load a DOCX file and split it into chunks.
    """
    from langchain_community.document_loaders import Docx2txtLoader
    loader = Docx2txtLoader(path)
    documents = loader.load()

    chunks = splitter.split_documents(documents)

    return [chunk.page_content for chunk in chunks]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings via the HF Inference API (cloud-based, no local model).
    """
    client = _get_hf_client()
    all_embeddings = []
    for text in texts:
        embedding = client.feature_extraction(
            text,
            model=EMBED_MODEL,
        )
        all_embeddings.append(embedding)
    return all_embeddings