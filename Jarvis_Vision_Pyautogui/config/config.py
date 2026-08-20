import os
import json

CONFIG_FILE = "config.json"


# =====================================
# SETUP
# =====================================

def setup_config():

    print("\n" + "=" * 40)
    print("          JARVIS SETUP")
    print("=" * 40)

    # -----------------------------
    # Providers
    # -----------------------------

    providers = {
        "1": {
            "name": "ollama",
            "models": [
                "qwen2.5:3b"
            ]
        },

        "2": {
            "name": "gemini",
            "models": [
                "models/gemini-3.6-flash",
                "models/gemini-3.5-flash",
                "models/gemini-3.5-flash-lite"
            ]
        }
    }

    vision_models = [
        "models/gemini-3.5-flash-lite",
        "models/gemini-2.5-flash-lite",
        "models/gemini-3.6-flash"
    ]

    print("\nProviders")
    print("1. Ollama (Local)")
    print("2. Gemini (Cloud)")

    choice = input("\nSelect Provider [1]: ").strip()

    if choice not in providers:
        choice = "1"

    provider = providers[choice]

    # -----------------------------
    # Thinking Model
    # -----------------------------

    print("\nAvailable Models")

    for i, model in enumerate(provider["models"], start=1):
        print(f"{i}. {model}")

    model_choice = input("\nSelect Model [1]: ").strip()

    try:
        model = provider["models"][int(model_choice) - 1]
    except:
        model = provider["models"][0]

    # -----------------------------
    # Vision Model
    # -----------------------------

    print("\nAvailable Vision Models")

    for i, model_name in enumerate(vision_models, start=1):
        print(f"{i}. {model_name}")

    vision_choice = input("\nSelect Vision Model [1]: ").strip()

    try:
        vision_model = vision_models[int(vision_choice) - 1]
    except:
        vision_model = vision_models[0]

    # -----------------------------
    # API Keys
    # -----------------------------

    api_key = ""
    vision_api_key = ""

    if provider["name"] == "gemini":

        api_key = input(
            "\nGemini API Key: "
        ).strip()

    vision_api_key = input(
        "\nGemini Vision API Key: "
    ).strip()

    if provider["name"] == "gemini" and not vision_api_key:
        vision_api_key = api_key

    # -----------------------------
    # User
    # -----------------------------

    username = input("\nYour Name: ").strip()

    assistant = input(
        "\nAssistant Name [Jarvis]: "
    ).strip()

    if not assistant:
        assistant = "Jarvis"

    config = {

        "provider": provider["name"],

        "model": model,

        "vision_model": vision_model,

        "api_key": api_key,

        "vision_api_key": vision_api_key,

        "username": username,

        "assistant_name": assistant

    }

    save_config(config)

    print("\n✅ Configuration saved.\n")

    return config


# =====================================
# SAVE
# =====================================

def save_config(config):

    with open(CONFIG_FILE, "w") as f:
        json.dump(
            config,
            f,
            indent=4
        )


# =====================================
# LOAD
# =====================================

def load_config():

    if not os.path.exists(CONFIG_FILE):
        return setup_config()

    try:

        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        required = [
            "provider",
            "model",
            "vision_model",
            "api_key",
            "vision_api_key",
            "username",
            "assistant_name"
        ]

        for key in required:

            if key not in config:
                raise ValueError()

        return config

    except Exception:

        print("\n⚠️ Invalid configuration.")
        print("Running setup again...\n")

        return setup_config()