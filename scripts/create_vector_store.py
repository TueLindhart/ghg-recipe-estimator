import logging
import os
from typing import Any, Dict, List
from uuid import uuid4

import pandas as pd
from langchain_core.documents import Document

from food_co2_estimator.data.vector_store.vector_store import get_vector_store

EXCEL_FILE_DIR = f"{os.getcwd()}/data/DBv2.xlsx"

# Read Excel files
df_dk = pd.read_excel(EXCEL_FILE_DIR, sheet_name="DK")
df_gb = pd.read_excel(EXCEL_FILE_DIR, sheet_name="GB")

# Convert DataFrame to a list of dictionaries
emission_records_dk: List[Dict[Any, Any]] = df_dk.to_dict(orient="records")
emission_records_gb: List[Dict[Any, Any]] = df_gb.to_dict(orient="records")

documents = []
uuids = []

document_rephrasing = {
    "Eggs, chicken, free-range hens (indoor), raw": "eggs",
    "Milk, partly skimmed, 1.5 % fat": "milk",
    "Sunflower oil": "oil for frying",
    # "Avocado, raw": "avocado",
}

READY_MEALS = "ready meals"

# Loop over the records with a progress bar
rephrasings = []
for emission_record_dk, emission_record_gb in zip(
    emission_records_dk, emission_records_gb
):
    en_name: str | None = emission_record_gb.get("Name", None)
    if en_name is None:
        logging.warning(f"Object {emission_record_gb} is not added to DB")
        continue

    if en_name.endswith(READY_MEALS):
        continue

    documents.append(
        Document(
            page_content=en_name.lower(),
            metadata=emission_record_dk,
            id=str(uuid4()),
        )
    )
    rephrased_name = document_rephrasing.get(en_name)
    if rephrased_name:
        documents.append(
            Document(
                page_content=rephrased_name,
                metadata=emission_record_dk,
                id=str(uuid4()),
            )
        )


# Add documents to the vector store
vector_store = get_vector_store()
vector_store.reset_collection()
vector_store.delete_collection()
vector_store.add_documents(documents)
