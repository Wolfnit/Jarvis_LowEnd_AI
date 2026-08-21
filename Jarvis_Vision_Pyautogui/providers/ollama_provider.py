import time
import requests


class OllamaProvider:

    def __init__(self, model):

        self.model = model

        self.url = (
            "http://localhost:11434/api/generate"
        )

    def generate(
        self,
        prompt,
        temperature=0.7,
        num_predict=256
    ):

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": temperature,

                "num_predict": num_predict

            }

        }

        try:

            start = time.perf_counter()

            response = requests.post(
                self.url,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            elapsed = (
                time.perf_counter() - start
            )

            data = response.json()

            print(
                f"\n✓ Ollama ({self.model}) "
                f"{elapsed:.2f}s"
            )

            return data.get(
                "response",
                "No response from model."
            ).strip()

        except requests.exceptions.Timeout:

            return (
                "Ollama request timed out."
            )

        except requests.exceptions.ConnectionError:

            return (
                "Couldn't connect to Ollama.\n"
                "Make sure Ollama is running."
            )

        except requests.exceptions.HTTPError as e:

            return (
                f"Ollama HTTP error:\n{e}"
            )

        except Exception as e:

            return (
                f"Ollama error:\n{e}"
            )