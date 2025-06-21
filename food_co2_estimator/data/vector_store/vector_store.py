from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from food_co2_estimator.data.vector_store.variables import (
    EMBEDDING_MODEL,
    VECTOR_DB_COLLECTION_NAME_DA,
    VECTOR_DB_COLLECTION_NAME_EN,
    VECTOR_DB_PERSIST_DIR_DA,
    VECTOR_DB_PERSIST_DIR_EN,
)
from food_co2_estimator.language.detector import Languages


def get_vector_store(language: Languages = Languages.English) -> Chroma:
    # underlying_embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    # embedding_store = LocalFileStore(EMBEDDING_CACHE_DIR)
    # cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    #     underlying_embeddings, embedding_store, namespace=underlying_embeddings.model
    # )
    embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    collection_name = (
        VECTOR_DB_COLLECTION_NAME_EN
        if language == Languages.English
        else VECTOR_DB_COLLECTION_NAME_DA
    )
    persist_dir = (
        VECTOR_DB_PERSIST_DIR_EN
        if language == Languages.English
        else VECTOR_DB_PERSIST_DIR_DA
    )
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedder,
        persist_directory=persist_dir,
        collection_metadata={"hnsw:search_ef": 1000},
    )
