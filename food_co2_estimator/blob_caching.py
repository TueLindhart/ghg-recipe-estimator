import datetime
import functools
import json
import logging
import os
import urllib.parse
import warnings
from typing import Any

from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage

from food_co2_estimator import __version__ as version
from food_co2_estimator.logger_utils import logger
from food_co2_estimator.pydantic_models.estimator import RunParams

CACHE_EXPIRATION_DAYS = 30


# Ignore the specific RuntimeWarning from google_crc32c
warnings.filterwarnings(
    "ignore",
    message="As the c extension couldn't be imported, `google-crc32c` is using a pure python implementation that is significantly slower",
    category=RuntimeWarning,
    module="google_crc32c",
)

bucket_cache: dict[str, storage.Bucket | None] = {"bucket": None}


def get_bucket() -> storage.Bucket:
    BUCKET_NAME = os.environ.get("CACHE_BUCKET")
    bucket = bucket_cache["bucket"]
    if bucket is None:
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(BUCKET_NAME)
            bucket_cache["bucket"] = bucket
        except DefaultCredentialsError as e:
            logging.info(f"Error: {e}")
            raise e
    return bucket


def url_to_key(url: str) -> str:
    """Convert a URL to a key that can be used in a blob storage bucket"""
    return url.replace("/", "_").replace(":", "_").replace("?", "_").replace("=", "_")


def create_cache_key_path(url: str, version: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    base_url = parsed_url.netloc.lstrip("www.")
    path = parsed_url.path if parsed_url.path else "_no_path"
    query = parsed_url.query if parsed_url.query else "_no_query"
    path_and_args = f"path{path}_arg_{query}"
    cache_key_path = f"{version}/{url_to_key(base_url)}/{url_to_key(path_and_args)}"
    return cache_key_path


def create_cache_key(url: str, version: str) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    epoch_ts = int(now.timestamp())
    cache_key_path = create_cache_key_path(url, version)
    blob_key = f"{cache_key_path}/{epoch_ts}"
    return blob_key


def store_json_in_blob_storage(blob_key: str, data: dict[str, Any]) -> None:
    if "timestamp" not in data:
        raise ValueError("Data must contain a 'timestamp' key")

    bucket = get_bucket()
    blob = bucket.blob(blob_key)
    blob.upload_from_string(data=json.dumps(data), content_type="application/json")  # type: ignore


def get_cache(prefix: str) -> dict[str, Any] | None:
    bucket = get_bucket()
    blobs = list(bucket.list_blobs(prefix=prefix))  # type: ignore

    if not blobs:
        return

    sorted_blobs = sort_blobs(blobs)
    for blob in sorted_blobs:
        try:
            data_str = blob.download_as_string().decode("utf-8")  # type: ignore
            data: dict[str, Any] = json.loads(data_str)
        except Exception as e:
            logging.error(f"Error reading blob {blob.name}: {e}")
            continue

        timestamp_str = data.get("timestamp")
        if not timestamp_str:
            continue

        try:
            cached_time = datetime.datetime.fromisoformat(timestamp_str)
        except ValueError:
            continue

        age = datetime.datetime.now(datetime.timezone.utc) - cached_time
        if age > datetime.timedelta(days=CACHE_EXPIRATION_DAYS):
            logging.info(f"Latest blob {blob.name} is expired (age: {age.days} days)")
            continue

        logging.info(f"Cache hit using blob {blob.name} (age: {age.days} days)")
        return data


def sort_blobs(blobs: list[storage.Blob]) -> list[storage.Blob]:
    sorted_blobs = sorted(blobs, key=get_epoch_ts, reverse=True)
    return sorted_blobs


# Sort blobs by the timestamp in the blob name (newest first)
def get_epoch_ts(blob: storage.Blob) -> int:
    try:
        return int(blob.name.split("/")[-1])  # type: ignore
    except ValueError:
        return 0


def get_now_isoformat() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def cache_results(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Get the function's argument names
        arg_names = func.__code__.co_varnames[: func.__code__.co_argcount]

        # Convert positional arguments to keyword arguments
        kwargs.update(dict(zip(arg_names, args)))

        runparams: RunParams | None = kwargs.get("runparams")
        if runparams is None:
            raise ValueError("runparams argument is required")

        # Check if cache exists
        if runparams.use_cache:
            cache = fetch_matching_cache(runparams)
            if cache is not None:
                return cache

        # Call the original function and store the result in cache
        success, result = await func(**kwargs)
        if success and runparams.use_cache:
            cache_estimator_result(runparams, result)
        return success, result

    return wrapper


def cache_estimator_result(runparams: RunParams, result: str):
    parsed_result = json.loads(result)
    data = {
        "runparams": runparams.model_dump(),
        "result": parsed_result,
        "timestamp": get_now_isoformat(),
    }
    blob_key = create_cache_key(runparams.url, version)
    store_json_in_blob_storage(blob_key, data)
    logger.info(f"URL={runparams.url}: Stored result in blob storage")


def fetch_matching_cache(runparams: RunParams) -> tuple[bool, Any] | None:
    prefix = create_cache_key_path(runparams.url, version)
    cache = get_cache(prefix)
    cache_runparams = cache.get("runparams") if cache else None
    result = cache.get("result") if cache else None
    if cache_runparams:
        cache_runparams = RunParams(**cache_runparams)
    if runparams == cache_runparams and result is not None:
        logger.info(f"URL={runparams.url}: Using cache")
        return True, json.dumps(result)


if __name__ == "__main__":
    # run create_cache_key with a URL to see the output
    url = "https://www.example.com/this/is/a/test?query=string"
    blob_key = create_cache_key(url, version)
    # run store_json_in_blob_storage with a blob_key and some data to see the output
    data = {
        "example": "data",
        "timestamp": get_now_isoformat(),
    }
    store_json_in_blob_storage(blob_key, data)

    # run get_cache with a prefix to see the output
    prefix = create_cache_key_path(url, version)
    cache = get_cache(prefix)
    if cache:
        print(cache)
    else:
        print("No cache found")
