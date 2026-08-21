from json import loads


class Verifier:

    def __init__(
        self,
        provider,
        prompt_builder
    ):

        self.provider = provider
        self.prompt_builder = prompt_builder

    def _parse_response(self, response):

        response = response.strip()

        # Try normal JSON first
        try:
            return loads(response)
        except Exception:
            pass

        # Handle ```json ... ``` responses
        if response.startswith("```"):

            lines = response.splitlines()

            # Remove opening ``` or ```json
            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            # Remove closing ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            response = "\n".join(lines).strip()

            try:
                return loads(response)
            except Exception:
                pass

        return None

    def verify(
        self,
        user_task,
        execution_result,
        screen_state
    ):

        prompt = self.prompt_builder(
            user_task,
            execution_result,
            screen_state
        )

        response = self.provider.generate(
            prompt
        )

        result = self._parse_response(response)

        if result is None:

            print("Invalid verifier JSON")
            print("Verifier response:")
            print(repr(response))

            return {
                "complete": False,
                "reason": "Verifier returned invalid JSON",
                "next_action": None
            }

        if "complete" not in result:

            print(" Verifier JSON missing 'complete'")

            return {
                "complete": False,
                "reason": "Verifier response missing 'complete'",
                "next_action": None
            }

        return result