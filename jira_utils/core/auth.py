import os
import json
import logging
from cryptography.fernet import Fernet
from jira_utils.config.paths import CONFIG_PATH, KEY_PATH

logger = logging.getLogger("jira_cli")

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    logger.info("Encryption key generated and saved.")
    return key

def load_key():
    if not os.path.exists(KEY_PATH):
        logger.warning("Key file not found. Generating new key.")
        return generate_key()
    with open(KEY_PATH, "rb") as f:
        logger.info("Encryption key loaded.")
        return f.read()

def save_config(server, username, token):
    key = load_key()
    fernet = Fernet(key)
    encrypted_token = fernet.encrypt(token.encode()).decode()
    config = {"server": server, "username": username, "token": encrypted_token}
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        logger.info("Config saved to %s", CONFIG_PATH)
    except Exception as e:
        logger.exception("Failed to save config: %s", str(e))

def load_config(args=None):
    if not os.path.exists(CONFIG_PATH):
        logger.error("Config file not found at %s", CONFIG_PATH)
        raise FileNotFoundError("❌ Config not found. Run `configure` first.")

    key = load_key()
    fernet = Fernet(key)

    try:
        with open(CONFIG_PATH, "r") as f:
            cfg = json.load(f)
        cfg["token"] = fernet.decrypt(cfg["token"].encode()).decode()
        logger.info("Config loaded and decrypted successfully.")

        if args:
            cfg["server"] = args.server or cfg["server"]
            cfg["username"] = args.username or cfg["username"]
            cfg["token"] = args.token or cfg["token"]
        return cfg

    except Exception as e:
        logger.exception("Failed to load or decrypt config: %s", str(e))
        raise
