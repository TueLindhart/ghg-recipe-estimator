import datetime
import json
from unittest.mock import patch

import pytest

from food_co2_estimator.blob_caching import (
    cache_estimator_result,
    cache_results,
    create_cache_key,
    create_cache_key_path,
    fetch_matching_cache,
    get_cache,
    get_epoch_ts,
    get_now_isoformat,
    sort_blobs,
    store_json_in_blob_storage,
    url_to_key,
)
from food_co2_estimator.pydantic_models.estimator import RunParams


class MockData:
    def __init__(self, data: str):
        self.data = data

    def decode(self, *args, **kwargs):
        return json.loads(self.data)


# Mock bucket and blob
class MockBlob:
    def __init__(self, name):
        self.name = name
        self.data: str | None = None

    def upload_from_string(self, data: str, content_type=None):
        self.data = data

    def download_as_string(self):
        return MockData(json.dumps(self.data))


class MockBucket:
    def __init__(self):
        self.blobs = {}

    def blob(self, name):
        if name not in self.blobs:
            self.blobs[name] = MockBlob(name)
        return self.blobs[name]

    def list_blobs(self, prefix=None):
        return [blob for name, blob in self.blobs.items() if name.startswith(prefix)]


@pytest.fixture
def mock_bucket(monkeypatch: pytest.MonkeyPatch):
    bucket = MockBucket()
    monkeypatch.setattr("food_co2_estimator.blob_caching.get_bucket", lambda: bucket)
    return bucket


@pytest.mark.parametrize(
    "url, version, expected",
    [
        (
            "https://www.example.com/this/is/a/test?query=string",
            "1.0",
            "dev/1.0/example.com/path_this_is_a_test_arg_query_string",
        ),
        (
            "https://www.example.com",
            "1.0",
            "dev/1.0/example.com/path_no_path_arg__no_query",
        ),
        (
            "https://www.example.com/this/is/a/test",
            "1.0",
            "dev/1.0/example.com/path_this_is_a_test_arg__no_query",
        ),
    ],
)
def test_create_cache_key_path(url, version, expected):
    assert create_cache_key_path(url, version) == expected


@pytest.mark.parametrize(
    "url, version, expected_prefix",
    [
        (
            "https://www.example.com/this/is/a/test?query=string",
            "1.0",
            "dev/1.0/example.com/path_this_is_a_test_arg_query_string/",
        ),
        (
            "https://www.example.com",
            "1.0",
            "dev/1.0/example.com/path_no_path_arg__no_query/",
        ),
        (
            "https://www.example.com/this/is/a/test",
            "1.0",
            "dev/1.0/example.com/path_this_is_a_test_arg__no_query/",
        ),
    ],
)
def test_create_cache_key(url, version, expected_prefix):
    result = create_cache_key(url, version)
    assert result.startswith(expected_prefix)


def test_store_json_in_blob_storage(mock_bucket):
    blob_key = "test_blob"
    data = {"example": "data", "timestamp": get_now_isoformat()}
    store_json_in_blob_storage(blob_key, data)
    assert mock_bucket.blob(blob_key).data == json.dumps(data)


def test_get_cache(mock_bucket):
    prefix = "test_prefix"
    data = {"example": "data", "timestamp": get_now_isoformat()}
    mock_bucket.blob(f"{prefix}/1").upload_from_string(json.dumps(data))
    cache = get_cache(prefix)
    assert cache == data


def test_sort_blobs(mock_bucket: MockBucket):
    blobs = [MockBlob(f"blob_{i}") for i in range(5)]
    for i, blob in enumerate(blobs):
        blob.name = f"blob_{i}/{i}"
    sorted_blobs = sort_blobs(blobs)  # type: ignore
    assert sorted_blobs == list(reversed(blobs))


def test_get_epoch_ts():
    blob = MockBlob("blob/1234567890")
    assert get_epoch_ts(blob) == 1234567890  # type: ignore


def test_get_now_isoformat():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    assert get_now_isoformat()[:19] == now[:19]


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://www.example.com/this/is/a/test?query=string",
            "https___www.example.com_this_is_a_test_query_string",
        ),
        ("https://www.example.com", "https___www.example.com"),
        (
            "https://www.example.com/this/is/a/test",
            "https___www.example.com_this_is_a_test",
        ),
    ],
)
def test_url_to_key(url, expected):
    assert url_to_key(url) == expected


@pytest.mark.asyncio
async def test_cache_results(monkeypatch: pytest.MonkeyPatch):
    async def mock_func(runparams):
        return True, "result"

    runparams = RunParams(
        url="https://www.example.com", use_cache=True, store_in_cache=True
    )
    mock_cache_results = cache_results(mock_func)

    monkeypatch.setattr(
        "food_co2_estimator.blob_caching.fetch_matching_cache", lambda x: None
    )
    monkeypatch.setattr(
        "food_co2_estimator.blob_caching.cache_estimator_result", lambda x, y: None
    )
    success, result = await mock_cache_results(runparams=runparams)
    assert success
    assert result == "result"


def test_cache_estimator_result(monkeypatch: pytest.MonkeyPatch):
    runparams = RunParams(
        url="https://www.example.com", use_cache=True, store_in_cache=True
    )
    result = '{"key": "value"}'

    mock_store_json_in_blob_storage = patch(
        "food_co2_estimator.blob_caching.store_json_in_blob_storage"
    )
    with mock_store_json_in_blob_storage as mock_store:
        cache_estimator_result(runparams, result)
        mock_store.assert_called_once()


def test_fetch_matching_cache(monkeypatch: pytest.MonkeyPatch):
    runparams = RunParams(
        url="https://www.example.com", use_cache=True, store_in_cache=True
    )
    cache_data = {
        "runparams": runparams.model_dump(),
        "result": {"key": "value"},
        "timestamp": get_now_isoformat(),
    }

    monkeypatch.setattr(
        "food_co2_estimator.blob_caching.get_cache", lambda x: cache_data
    )

    result = fetch_matching_cache(runparams)
    assert result == (True, json.dumps({"key": "value"}))
