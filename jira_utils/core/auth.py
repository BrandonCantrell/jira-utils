import os
import json
from cryptography.fernet import Fernet
from jira_utils.config.paths import CONFIG_PATH, KEY_PATH

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_PATH):
        return generate_key()
    with open(KEY_PATH, "rb") as f:
        return f.read()

def save_config(server, username, token):
    key = load_key()
    fernet = Fernet(key)
    encrypted_token = fernet.encrypt(token.encode()).decode()
    config = {"server": server, "username": username, "token": encrypted_token}
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def load_config(args=None):
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("❌ Config not found. Run `configure` first.")
    key = load_key()
    fernet = Fernet(key)
    with open(CONFIG_PATH, "r") as f:
        cfg = json.load(f)
    cfg["token"] = fernet.decrypt(cfg["token"].encode()).decode()
    if args:
        cfg["server"] = args.server or cfg["server"]
        cfg["username"] = args.username or cfg["username"]
        cfg["token"] = args.token or cfg["token"]
    return cfg
