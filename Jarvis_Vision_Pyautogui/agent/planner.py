import json


class Planner:

    def __init__(self, provider, prompt_builder):

        self.provider = provider
        self.prompt_builder = prompt_builder



    def plan(
        self,
        assistant_name,
        username,
        user_message,
        facts=None,
        conversation=None
    ):


        prompt = self.prompt_builder(

            assistant_name,

            username,

            user_message,

            facts or [],

            conversation or []

        )


        response = self.provider.generate(
            prompt
        )


        try:

            return json.loads(
                response
            )


        except Exception:


            print(
                "\n❌ Planner returned invalid JSON:"
            )

            print(response)



            # fallback to chat

            return {

                "action": "chat",

                "response": response

            }