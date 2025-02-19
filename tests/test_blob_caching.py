import datetime
import json

import pytest

from food_co2_estimator.blob_caching import (
    cache_results,
    create_cache_key,
    create_cache_key_path,
    get_cache,
    get_epoch_ts,
    get_now_isoformat,
    sort_blobs,
    store_json_in_blob_storage,
    url_to_key,
)


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
            "example.com/path_this_is_a_test_arg_query_string/1.0",
        ),
        (
            "https://www.example.com",
            "1.0",
            "example.com/path_no_path_arg__no_query/1.0",
        ),
        (
            "https://www.example.com/this/is/a/test",
            "1.0",
            "example.com/path_this_is_a_test_arg__no_query/1.0",
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
            "example.com/path_this_is_a_test_arg_query_string/1.0/",
        ),
        (
            "https://www.example.com",
            "1.0",
            "example.com/path_no_path_arg__no_query/1.0/",
        ),
        (
            "https://www.example.com/this/is/a/test",
            "1.0",
            "example.com/path_this_is_a_test_arg__no_query/1.0/",
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
    sorted_blobs = sort_blobs(blobs)
    assert sorted_blobs == list(reversed(blobs))


def test_get_epoch_ts():
    blob = MockBlob("blob/1234567890")
    assert get_epoch_ts(blob) == 1234567890


def test_get_now_isoformat():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    assert get_now_isoformat()[:19] == now[:19]


@pytest.mark.asyncio
async def test_cache_results(mock_bucket):
    @cache_results
    async def dummy_func(url, negligeble_threshold):
        return {"result": "data"}

    url = "https://www.example.com"
    negligeble_threshold = 0.1
    result = await dummy_func(url=url, negligeble_threshold=negligeble_threshold)
    assert result == {"result": "data"}
    prefix = create_cache_key_path(url, "1.0")
    cache = get_cache(prefix)
    assert cache["result"] == "data"


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
