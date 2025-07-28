import logging
import os
from typing import Any, Dict, List
from uuid import uuid4

import pandas as pd  # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document

from food_co2_estimator.data.vector_store.vector_store import get_vector_store
from food_co2_estimator.language.detector import Languages

EXCEL_FILE_DIR = f"{os.getcwd()}/food_co2_estimator/data/fooddatabase.xlsx"

# Read Excel files

document_rephrasing = {
    "Eggs, chicken, free-range hens (indoor), raw": "eggs",
    "Æg, skrabeæg": "Æg",
    "Milk, partly skimmed, 1.5 % fat": "milk",
    "Sunflower oil": "oil for frying",
    "Sosikkeolie": "olie til stegning",
}

READY_MEALS = "Færdigretter"


# Loop over the records with a progress bar
rephrasings = []


def add_documents(
    documents: list[Document], emission_record_dk: dict[str, str], name: str
):
    documents.append(
        Document(
            page_content=name.lower(),
            metadata=emission_record_dk,
            id=str(uuid4()),
        )
    )
    rephrased_name = document_rephrasing.get(name)
    if rephrased_name:
        documents.append(
            Document(
                page_content=rephrased_name,
                metadata=emission_record_dk,
                id=str(uuid4()),
            )
        )


# Add documents to the vector store
def add_documents_to_vector_store(documents: list[Document], language: Languages):
    vector_store = get_vector_store(language)
    vector_store.reset_collection()
    vector_store.add_documents(documents)


def create_vector_stores():
    """Create vector stores for Danish and English food emissions data.

    Both stores are populated with danish environmental data from an Excel file
    because the application is for danish users, but the English store is
    used to get good translations of the danish food items to english.
    """
    df_dk = pd.read_excel(EXCEL_FILE_DIR, sheet_name="DK")
    df_gb = pd.read_excel(EXCEL_FILE_DIR, sheet_name="GB")

    # Convert DataFrame to a list of dictionaries
    emission_records_dk: List[Dict[Any, Any]] = df_dk.to_dict(orient="records")
    emission_records_gb: List[Dict[Any, Any]] = df_gb.to_dict(orient="records")

    en_documents = []
    dk_documents = []
    for emission_record_dk, emission_record_gb in zip(
        emission_records_dk, emission_records_gb
    ):
        category = emission_record_dk.get("Kategori", "")
        if category == READY_MEALS:
            continue
        dk_name: str | None = emission_record_dk.get("Produkt", None)
        if dk_name is not None:
            logging.warning(f"Object {emission_record_dk} is not added to danish DB")
            add_documents(dk_documents, emission_record_dk, dk_name)

        en_name: str | None = emission_record_gb.get("Name", None)
        if en_name is not None:
            logging.warning(f"Object {emission_record_dk} is not added to English DB")
            add_documents(en_documents, emission_record_dk, en_name)

    add_documents_to_vector_store(en_documents, Languages.English)
    add_documents_to_vector_store(dk_documents, Languages.Danish)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Creating vector stores...")
    create_vector_stores()
    logging.info("Vector stores created successfully.")
