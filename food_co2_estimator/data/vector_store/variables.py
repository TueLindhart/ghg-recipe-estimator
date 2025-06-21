import os

EMBEDDING_MODEL = "text-embedding-3-large"
VECTOR_DB_COLLECTION_NAME_EN = "vector_co2_db_en"
VECTOR_DB_COLLECTION_NAME_DA = "vector_co2_db_da"
VECTOR_DB_PERSIST_DIR_EN = f"{os.getcwd()}/food_co2_estimator/data/vector_store/store"
VECTOR_DB_PERSIST_DIR_DA = f"{os.getcwd()}/food_co2_estimator/data/vector_store/store"
EMBEDDING_CACHE_DIR = (
    f"{os.getcwd()}/food_co2_estimator/data/vector_store/embedding_cache"
)
