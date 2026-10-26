from google.cloud import secretmanager
from gcp.paths    import PROJECT_ID
import json


client = secretmanager.SecretManagerServiceClient()


def get_secret(secret_id, as_json=False):

    secret_name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"

    response = client.access_secret_version(
        request={"name": secret_name}
    )

    secret_value = response.payload.data.decode("utf-8")

    return json.loads(secret_value) if as_json else secret_value


def get_nextbike_creds():
    return tuple(get_secret("pmedina-nextbike-creds").splitlines())


def get_gmail_creds():
    return tuple(get_secret("pmedina-gmail-creds").splitlines())


def get_moxsi_gs_links():
    return get_secret("moxsi-gs-links", as_json=True)


def get_gs_service_account_creds():
    return get_secret("gs-service-account-creds", as_json=True)
