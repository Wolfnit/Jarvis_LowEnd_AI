from providers.gemini_provider import GeminiProvider


def create_provider(
    provider,
    api_key,
    model
):

    if provider == "gemini":

        return GeminiProvider(
            api_key,
            model
        )

    raise ValueError(
        f"Unsupported provider: {provider}"
    )