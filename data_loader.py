from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embedding model
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DIM = 384  # Correct embedding dimension

# Text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Lazily loaded — model is only initialized on first use, NOT at import time.
# We also lazy-import sentence_transformers because it pulls in PyTorch (~200MB),
# which takes 2-3 minutes to import on Render's free tier CPU and causes port timeout.
_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


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
    Generate embeddings for a list of text chunks.
    """
    embeddings = _get_model().encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings.tolist()