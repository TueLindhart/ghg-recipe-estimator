import os

from food_co2_estimator.url.url2markdown import get_markdown_from_url
from tests.data_paths import TEXT_INPUT_DIR
from tests.urls import TEST_URLS

# Directory to store the results
os.makedirs(TEXT_INPUT_DIR, exist_ok=True)

# Fetch and store the results
for file_name, url in TEST_URLS.items():
    markdown_content = get_markdown_from_url(url)
    if markdown_content:
        # Create a valid filename from the URL
        filename = file_name + ".md"
        filepath = os.path.join(TEXT_INPUT_DIR, filename)

        # Write the content to a file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(markdown_content)
        print(f"Stored content from {url} in {filepath}")
    else:
        print(f"Failed to fetch content from {url}")
