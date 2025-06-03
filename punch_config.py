__config_version__ = 1

GLOBALS = {"serializer": "{{major}}.{{minor}}.{{patch}}"}

FILES = [
    {
        "path": "pyproject.toml",
        "search": r'^version\s*=\s*".*"$',
        "replace": 'version = "{{major}}.{{minor}}.{{patch}}"',
    },
    {
        "path": "food_co2_estimator/__init__.py",
        "search": r'^__version__\s*=\s*".*"$',
        "replace": '__version__ = "{{major}}.{{minor}}.{{patch}}"',
    },
]

VERSION = ["major", "minor", "patch"]
