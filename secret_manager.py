from google.cloud import secretmanager
import json


PROJECT_ID = 'bigdata-fase2'
CLIENT     = secretmanager.SecretManagerServiceClient()


def get_secret(secret_id, as_json=False):

    secret_name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"

    response = CLIENT.access_secret_version(
        request={"name": secret_name}
    )

    secret_value = response.payload.data.decode("utf-8")

    return json.loads(secret_value) if as_json else secret_value


def get_nextbike_creds():
    return tuple(get_secret("pmedina-nextbike-creds").splitlines())


def get_gmail_creds():
    return tuple(get_secret("pmedina-gmail-creds").splitlines())
