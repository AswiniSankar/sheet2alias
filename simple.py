import os
import json
import configparser
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# ===============================
# LOAD CONFIG
# ===============================
config = configparser.ConfigParser()
config.read("config.ini")

SHEET_ID = config.get("google", "sheet_id")
CELL = config.get("google", "cell")
ALIAS_NAME = config.get("bash", "alias_name")
TOKEN_FILE = config.get("google", "token_file", fallback="token.json")
CLIENT_SECRET_FILE = config.get("google", "client_secret_file", fallback="client_secret.json")

# ===============================
# GOOGLE API CONFIG
# ===============================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

if not google_client_id or not google_client_secret:
    raise EnvironmentError("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET environment variables.")

client_secret_content = {
    "installed": {
        "client_id": google_client_id,
        "project_id": "sheet2alias-auto",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": google_client_secret,
        "redirect_uris": ["http://localhost"]
    }
}

# Write a temporary client secret file (required by Google SDK)
with open(CLIENT_SECRET_FILE, "w") as f:
    json.dump(client_secret_content, f)

# ===============================
# AUTHENTICATION
# ===============================
creds = None
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

client = gspread.authorize(creds)

# ===============================
# FETCH VALUE FROM SHEET
# ===============================
sheet = client.open_by_key(SHEET_ID).sheet1
value = sheet.acell(CELL).value
print(f"Fetched value from {CELL}: {value}")

# ===============================
# UPDATE BASH ALIAS
# ===============================
alias_line = f"alias {ALIAS_NAME}='echo {value}'\n"
bashrc_path = os.path.expanduser("~/.bashrc")

# Read .bashrc
with open(bashrc_path, "r") as f:
    lines = f.readlines()

# Overwrite alias if already exists
with open(bashrc_path, "w") as f:
    for line in lines:
        if not line.strip().startswith(f"alias {ALIAS_NAME}="):
            f.write(line)
    f.write(alias_line)

print(f"Updated alias `{ALIAS_NAME}` in {bashrc_path}")

# Reload bashrc (applies alias in next shell)
os.system(f"bash -c 'source {bashrc_path}'")

# Clean up
os.remove(CLIENT_SECRET_FILE)
