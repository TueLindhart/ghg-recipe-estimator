from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from food_co2_estimator.data.vector_store.variables import (
    EMBEDDING_MODEL,
    VECTOR_DB_COLLECTION_NAME,
    VECTOR_DB_PERSIST_DIR,
)


def get_vector_store() -> Chroma:
    # underlying_embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    # embedding_store = LocalFileStore(EMBEDDING_CACHE_DIR)
    # cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    #     underlying_embeddings, embedding_store, namespace=underlying_embeddings.model
    # )
    embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        collection_name=VECTOR_DB_COLLECTION_NAME,
        embedding_function=embedder,
        persist_directory=VECTOR_DB_PERSIST_DIR,
        collection_metadata={"hnsw:search_ef": 1000},
    )
