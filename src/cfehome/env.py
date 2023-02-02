import io
import os
import pathlib
from functools import lru_cache

import google.auth
from decouple import Config, RepositoryEmpty, RepositoryEnv
from google.cloud import secretmanager

BASE_DIR = pathlib.Path(__file__).parent.parent

ENV_PATH = BASE_DIR / ".env"
DB_ENV_PATH = BASE_DIR / "db.env"

class RepositoryString(RepositoryEmpty):
    """
    Retrieves option keys from an ENV string
    """

    def __init__(self, source):
        source = io.StringIO(source)
        if not isinstance(source, io.StringIO):
            raise ValueError("source must be an instance of io.StringIO")
        self.data = {}
        file_ = source.read().split("\n")
        for line in file_:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if len(v) >= 2 and (
                (v[0] == "'" and v[-1] == "'") or (v[0] == '"' and v[-1] == '"')
            ):
                v = v[1:-1]
            self.data[k] = v

    def __contains__(self, key):
        return key in os.environ or key in self.data

    def __getitem__(self, key):
        return self.data[key]


def get_google_secret_payload():
    try:
        _, project_id = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError:
        project_id = None
    if project_id:
        client = secretmanager.SecretManagerServiceClient()
        settings_name = os.environ.get("GCLOUD_SETTINGS_NAME", "cfe_django_settings")
        name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
        payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
        return payload
    return None


@lru_cache()
def get_config(use_gcloud=True):
    if ENV_PATH.exists():
        return Config(RepositoryEnv(ENV_PATH))
    if use_gcloud:
        payload = get_google_secret_payload()
        if payload is not None:
            return Config(RepositoryString(payload))
    from decouple import config

    return config


config = get_config()


@lru_cache()
def get_db_config():
    if DB_ENV_PATH.exists():
        return Config(RepositoryEnv(DB_ENV_PATH))
    return get_config()

db_config = get_db_config()