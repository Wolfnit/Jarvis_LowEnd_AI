from providers.gemini_provider import GeminiProvider
from providers.ollama_provider import OllamaProvider



def create_provider(
    provider,
    api_key=None,
    model=None
):

    if provider == "gemini":

        return GeminiProvider(
            api_key,
            model
        )


    elif provider == "ollama":

        return OllamaProvider(
            model
        )


    else:

        raise Exception(
            f"Unknown provider: {provider}"
        )