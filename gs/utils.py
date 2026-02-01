from   google.oauth2.service_account import Credentials
import pandas as pd, gspread, json, os, io


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

# 1) Aquí GS_SERVICE_ACCOUNT_CREDS es un STRING con el JSON (no una ruta)
json_str = os.environ["GS_SERVICE_ACCOUNT_CREDS"]

# 2) Lo convertimos a dict de Python
service_account_info = json.loads(json_str)  # <-- ESTO NO ES UNA RUTA

# service_account_info = "{\"type\": \"service_account\", \"project_id\": \"bigdata-fase2\", \"private_key_id\": \"84a88ec0c1cbdeb29d9121fd038e852b4ca9bc91\", \"private_key\": \"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMVYMs2N0PTVgb\nFR1lOJ/e5BA9UwU90Nooo1h2nUU80ZtlLddVos5qPVL1cEQLKc39DdtCpHjRZ+wN\noOsMFECz0JLCOUv/RXj0ajHkWcLjqQGIxuRbVxFWWdwPIqHz52AkwJThqPcOuVSx\nOZkmPpPuec+63dMwXhdiWmzv1hIWsj7A18y11F6ctsHm3sc7swACMJWWsSVKYl3K\nTUHX9LfourWVOymJ6rAHL2i+BVROD5CsBdtYvsRuz0dJ9gLb84BoayqfqoIUEiE2\n2owbOW2VCToY8gZoH0YwbpMak5QmO75GG6YVhe0qjLkm1DCMT0EPmjET5S/WcarB\n9a0C8PQbAgMBAAECggEAGzzK34+I6CFHPVTzNir2JKACCiqm6DaO3hvoDuen8xN9\nw1749VFecor6I/1zFIneC31tXNTPxho0PRzWOCX6+f0zkvBQURbRqML/I5FTiUVe\nDv10MzjH9trDmsDjFcAh8MQ7FFmRlUTfJUCoSZDN51wVdLNdE3V3aITlQJMolh2v\nfAsqBhtYBhQh6COCaKt1CpNIyFTkXFKZ+tDAueCHQp83NCPCBqGhQPmKKXWoll4d\ncs5F7cMY+EmQnHRgt+8yljcQRm1TChR+DSI1pN8BWKeeHFuNBkaf7nMmE0A1AV1K\ndweVJsXFOIbWNfhBybhyVUfLiLPQk7bxZEgjwOojAQKBgQDtFR9cTB3mFcX9Y01o\nfkvVcZMwzOoDeam40vpjxQOwyN+/rN9kmBzksjwvVjYdUfVO73YkNeR9ylYSv/Ns\nBwuKMJenqmge13hafeUwuOco1F2mbAKL5++a2X3UuVTJoiqvL+O7H0dqqCfV7DTe\nXMjCd0m7H2ycL8C0zWCs0KhVlQKBgQDco3AOYg28AH0xZlbr+uMDeO14m+W0iMfu\np01fK0kkGgoHKEWNUGhJ2VKL1nd6JhqdI146iMzzUeEIShktcfpodl8LAJUZaHQH\nYM3kFcKdJL6aH4Ytja0koHY8ySYrDlB6VIR0YytnXXgl5r2R5K0Omlygm2flA05Z\nfp4kgKVW7wKBgQDYLxqZnw7kb5ZKp/I+BmxABYCiTzhUUuxgjIGl2FC1M3ZT4d8S\na2JtZ9lZkNNniQSXJeQkwL/JtGcoUcA2EXaEXCrtyIWJGhG08ne7JeAjawK6bmMk\nECp8mTYUc6rM8gLaHGEckDkfGJa6itjqqtCmAwBIkS8IfMLMGzq8WsgkwQKBgHUk\nRPst7hLRw6Y1qpKRWnPegV4WjyeBs3yu0LJlfeiv9oEETaEQfr4uptfdnwN4NYsW\nWxICzaWl5C8NgD6TlBpgNmfWAFNEFM5SBB5Du1bJSnTzpb6LyNB4bS4qsZwMdofs\nVYKhoEq54m9lCWLrIUJujB0tRUTes3tqcTX6I057AoGAWf62yxiGkJvyz6YEutTw\nTKWjdg2vEcYpQnxYz6Sa6ffEliPhl0as+ZU5KAtolZeIkZ51X/rlp0nWIAt563+d\nMHl1WTkkxhF9YEM2ut4lvdyTOP4/08q+44akryFCD/LerZCTOmco0qmuNsX80FRS\nATW39Q9JNdJBr3YDxfWd/Xc=\n-----END PRIVATE KEY-----\n\", \"client_email\": \"moxsi-stats-pipeline@bigdata-fase2.iam.gserviceaccount.com\", \"client_id\": \"110860911350013102505\", \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\", \"token_uri\": \"https://oauth2.googleapis.com/token\", \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\", \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/moxsi-stats-pipeline%40bigdata-fase2.iam.gserviceaccount.com\", \"universe_domain\": \"googleapis.com\"}"
# service_account_info = json.loads(service_account_info.replace('\n', '\\n'))

# 3) Creamos las credenciales a partir de ese dict
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

# Autenticarse con gspread
CLIENT = gspread.authorize(creds)


def download_from_gs_excel(sheet_url):
    """(igual que antes) descarga TODAS las hojas a un Excel en memoria."""
    sh = CLIENT.open_by_url(sheet_url)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for ws in sh.worksheets():
            values = ws.get_all_values()
            header = values[0]
            rows = values[1:]
            df = pd.DataFrame(rows, columns=header)

            sheet_name = (ws.title or "Sheet")[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return output.getvalue()


def download_from_gs_single_sheet(sheet_url, sheet_name=None):
    """
    Descarga SOLO una hoja de un Google Sheet y la devuelve como DataFrame.
    Luego `upload_to_gcp` la subirá como CSV.
    """
    sh = CLIENT.open_by_url(sheet_url)
    ws = sh.worksheet(sheet_name) if sheet_name else sh.sheet1

    values = ws.get_all_values()
    if not values: return pd.DataFrame()

    header = values[0]
    rows = values[1:]

    return pd.DataFrame(rows, columns=header)
