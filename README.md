# sheet2alias
Auto-sync a Google Sheet cell to a Bash alias using Python (OAuth2 + gspread).

⚙️ **“From Sheet cell to Shell command — instantly.”**
>
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-API-brightgreen)](https://developers.google.com/sheets/api)
[![Bash Alias](https://img.shields.io/badge/Bash-Alias-orange)](https://www.gnu.org/software/bash/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)]()


# 🔐 Google Sheet → Bash Alias Sync

This Python utility automatically **reads a specific cell** from a **Google Sheet** and updates your **Bash alias** with that value in your local environment.

Keep your bash aliases **automatically updated** from a Google Sheet cell.  
No manual edits, no stale values — just one command to pull the latest data from Google Sheets straight into your terminal 🚀  

---

## 💡 Why This Project?

In many teams or environments, certain credentials, access keys, or environment-specific values frequently change — for example, temporary passwords, access tokens, or API keys.  
  
Instead of copying them manually every time they change, this script:

1. Connects securely to your Google Sheet using OAuth  
2. Reads a specific cell value
3. Updates your `.bashrc` with a bash alias (like `alias ppwd='echo check@2025fresh'`)  
4. Keeps your local terminal in sync with your sheet
5. Keeps sensitive data **out of version control** while still being securely and dynamically accessible locally.

In short — this project provides a **bridge between a shared Google Sheet** and your **local shell environment**, keeping your configuration **in sync, secure, and effortless.**

So next time you type `ppwd` in your terminal —  💥 boom, it prints the latest value straight from your Google Sheet.

---

## 🧠 Why Use It?

- Centralize frequently changing values (tokens, passwords, URLs)  
- Sync shared data across teams securely  
- Avoid editing `.bashrc` manually  
- Lightweight — no cron, no cloud dependencies  
- Caches access token to avoid re-authentication
- Supports client credentials via environment variables
- Works seamlessly with read-only sheets

---


## 🧩 Configuration — `config.ini`

Your config file tells the script **what to fetch** and **how to name it**:  

```ini
[google]
sheet_id = <SHEET_ID>
cell = <CELL_NUMBER>
token_file = token.json
client_secret_file = client_secret.json

[bash]
alias_name = ppwd

| Key                  | Description                               |
| -------------------- | ----------------------------------------- |
| `sheet_id`           | Google Sheet ID (from your sheet’s URL)   |
| `cell`               | The cell to read (e.g. `E10`)             |
| `token_file`         | OAuth token cache (auto-created)          |
| `client_secret_file` | Temporary credentials file (auto-deleted) |
| `alias_name`         | Bash alias name (e.g., `ppwd`)            |

--- 
⚙️ Setup & Usage

1️⃣ Clone the Repo
git clone https://github.com/<your-username>/sheet2alias.git
cd sheet2alias

2️⃣ Install Dependencies
pip install gspread google-auth google-auth-oauthlib

3️⃣ Set Environment Variables

Before running the script, set your Google API credentials:

export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"


💡 You only need to do this once — consider adding it to your ~/.bashrc or ~/.zshrc.

4️⃣ Configure Your Sheet

Edit config.ini with:

Your Google Sheet ID

The target cell (like E10)

The alias name (like ppwd)

5️⃣ Run the Script
python3 simple.py


✅ The script will:

- Authenticate (only once — then reuse token.json)
- Read the Google Sheet cell
- Update .bashrc with your alias
- Reload your bash configuration

Example Output:

Fetched value from E10: check@202fresh1234
Updated alias `ppwd` in ~/.bashrc

6️⃣ Test It
source ~/.bashrc
ppwd


🎉 It should echo the value fetched from your Google Sheet!

--- 
| Use Case                | Example                                         |
| ----------------------- | ----------------------------------------------- |
| Shared test credentials | `alias testpwd='echo shared@123'`               |
| Dynamic tokens          | Automatically rotate tokens from a shared sheet |
| Environment versioning  | Keep app versions synced across teams           |
| Fun reminders           | `alias break='echo ☕ Time for a coffee!'`       |

---
🔒 Security Notes

- OAuth tokens are cached locally in token.json
- Temporary client_secret.json is auto-deleted after every run
- Your credentials never leave your machine

| Component        | Purpose                            |
| ---------------- | ---------------------------------- |
| **gspread**      | Read Google Sheets                 |
| **google-auth**  | Secure OAuth 2.0 authentication    |
| **configparser** | Lightweight configuration handling |
| **.bashrc**      | Alias persistence                  |


---
