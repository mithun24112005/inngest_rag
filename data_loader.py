from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Embedding model
EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"
EMBED_DIM = 768  # Correct embedding dimension

# Text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Load embedding model
model = SentenceTransformer(EMBED_MODEL)


def load_and_chunk_pdf(path: str) -> list[str]:
    """
    Load a PDF and split it into chunks.
    """
    loader = PyPDFLoader(path)
    documents = loader.load()

    chunks = splitter.split_documents(documents)

    return [chunk.page_content for chunk in chunks]


def load_and_chunk_docx(path: str) -> list[str]:
    """
    Load a DOCX file and split it into chunks.
    """
    loader = Docx2txtLoader(path)
    documents = loader.load()

    chunks = splitter.split_documents(documents)

    return [chunk.page_content for chunk in chunks]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks.
    """
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings.tolist()