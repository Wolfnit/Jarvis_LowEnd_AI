import json
import subprocess
import sys
import importlib

from speech.speak import speak

from brain.brain import think, set_model

import memory.memory as memory



def get_ollama_models():

    try:

        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=True
        )

        models = []

        for line in result.stdout.strip().splitlines()[1:]:

            parts = line.split()

            if parts:
                models.append(parts[0])

        return models

    except Exception as e:

        print(f"[Ollama Error] {e}")
        return []


def select_model():

    models = get_ollama_models()

    if not models:

        print("No Ollama models found.")
        print("Make sure Ollama is installed and running.")
        sys.exit(1)

    print("\nAvailable Ollama models:\n")

    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")

    print()

    while True:

        try:

            choice = int(
                input(
                    f"Select model [1-{len(models)}]: "
                )
            )

            if 1 <= choice <= len(models):

                selected = models[choice - 1]

                print(
                    f"\n[Jarvis] Model: {selected}"
                )

                return selected

        except ValueError:
            pass

        print("Invalid selection.\n")




def select_speech_engine():

    print("\nSpeech engine:\n")
    print("1. CPU")
    print("2. GPU")
    print()

    while True:

        choice = input("Select [1-2]: ").strip()

        if choice == "1":

            module = importlib.import_module(
                "speech.listen_cpu"
            )

            print("\n[Jarvis] Speech: CPU")

            return module

        elif choice == "2":

            module = importlib.import_module(
                "speech.listen_gpu"
            )

            print("\n[Jarvis] Speech: GPU")

            return module

        print("Invalid selection.\n")




print("================================")
print("       JARVIS V0.1")
print("================================")


selected_model = select_model()

set_model(selected_model)


listen_module = select_speech_engine()


listen_once = listen_module.listen_once
start_stream = listen_module.start_stream
stop_stream = listen_module.stop_stream


print("\nReady.\n")




while True:

    try:

      

        user_text = listen_once()

        if not user_text:
            continue

        print(f"You: {user_text}")


  

        short_term = memory.get_short_term()
        long_term = memory.get_long_term()


 

        raw_result = think(
            user_text,
            short_term,
            long_term
        )


  

        result = json.loads(raw_result)

        response = result.get(
            "response",
            ""
        )

        facts = result.get(
            "memory",
            []
        )


        # SAVE MEMORY

        memory.add_conversation(
            user_text,
            response
        )

        memory.add_facts(
            facts
        )


        # SPEAK

        print(f"Jarvis: {response}\n")

        # Stop microphone
        stop_stream()

        # Speak
        speak(response)

        # Restart microphone
        start_stream()

    except KeyboardInterrupt:

        print("\nJarvis shutting down...")

        stop_stream()

        break




    except Exception as e:

        print(f"[Jarvis Error] {e}\n")

        try:
            start_stream()
        except:
            pass