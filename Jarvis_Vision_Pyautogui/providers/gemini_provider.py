from google import genai


class GeminiProvider:

    def __init__(self, api_key, model):

        self.client = genai.Client(
            api_key=api_key
        )

        self.models = []

        self.models.append(model)

        fallbacks = [
            "models/gemini-3.6-flash",
            "models/gemini-3.5-flash",
            "models/gemini-3.5-flash-lite",
            "models/gemini-2.5-flash-lite"
        ]

        for m in fallbacks:

            if m not in self.models:
                self.models.append(m)

        self.current_model_index = 0


    # TEXT GENERATION

    def generate(self, prompt):

        last_error = None

        for _ in range(len(self.models)):

            model = self.models[
                self.current_model_index
            ]

            try:

                response = (
                    self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )
                )

                print(
                    f"\n✓ Using {model}"
                )

                return response.text


            except Exception as e:

                print(
                    f"\n {model} failed"
                )

                last_error = e

                self.current_model_index += 1

                if (
                    self.current_model_index
                    >= len(self.models)
                ):
                    self.current_model_index = 0


        return (
            f"All Gemini models failed.\n\n"
            f"{last_error}"
        )


    # SCREEN ANALYSIS

    def analyze_image(self, image, prompt):

        last_error = None


        for _ in range(len(self.models)):

            model = self.models[
                self.current_model_index
            ]

            try:

                response = (
                    self.client.models.generate_content(
                        model=model,
                        contents=[
                            prompt,
                            image
                        ]
                    )
                )

                print(
                    f"\n Vision using {model}"
                )

                return response.text


            except Exception as e:

                print(
                    f"\n Vision {model} failed"
                )

                last_error = e

                self.current_model_index += 1

                if (
                    self.current_model_index
                    >= len(self.models)
                ):
                    self.current_model_index = 0


        return (
            f"All Gemini vision models failed.\n\n"
            f"{last_error}"
        )