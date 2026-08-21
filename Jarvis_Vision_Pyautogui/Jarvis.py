import time
from config import load_config
from providers.router import create_provider
from voice.voice import listen_once
from tts.router import TTSRouter
from memory.memory import Memory
from agent.prompt import build_prompt
from agent.planner import Planner
from agent.executor import execute
from vision.controller import VisionController
from agent.verifier import Verifier
from vision.vision_prompt import build_verify_prompt

# STARTUP
config = load_config()


print("\nLoading Jarvis...\n")



# AI PROVIDER

provider = create_provider(
    config["provider"],
    config["api_key"],
    config["model"]
)



# VISION

vision_provider = create_provider(
    "gemini",
    config["vision_api_key"],
    config["vision_model"]
)


vision = VisionController(
    vision_provider
)



# MEMORY + TTS


memory = Memory()


tts = TTSRouter(
    mode="auto"
)



# AGENTS


planner = Planner(
    provider,
    build_prompt
)


verifier = Verifier(
    provider,
    build_verify_prompt
)



assistant_name = config["assistant_name"]

username = config["username"]



print("\n" + "=" * 40)
print(f" {assistant_name} Online")
print("=" * 40)

print(f"\nHello {username}!")
print("Speak naturally...\n")



# HELPERS


def speak(text):

    if text:

        print(
            f"\n{assistant_name}: {text}"
        )

        tts.speak(text)

        # allow audio system to settle

        time.sleep(2)



# MAIN LOOP


while True:


    try:


        # LISTEN


        print(
            "\n Waiting..."
        )


        time.sleep(1)


        start = time.perf_counter()


        user_message = listen_once()


        print(
            f" Listen: {time.perf_counter()-start:.2f}s"
        )


        if not user_message:

            continue



        print(
            f"\nYOU: {user_message}"
        )

        # EXIT


        if user_message.lower() in [

            "exit",
            "quit",
            "shutdown"

        ]:


            speak(
                "Goodbye!"
            )

            break





        # PLANNER


        print(
            "\n🧠 Planning..."
        )


        plan = planner.plan(

            assistant_name,

            username,

            user_message,

            memory.get_facts(),

            memory.get_recent()

        )


        print(
            "\nPLAN:"
        )

        print(plan)





        # CHAT


        if "tasks" not in plan:


            response = plan.get(
                "response",
                ""
            )


            speak(
                response
            )


            memory.save_message(
                "user",
                user_message
            )


            memory.save_message(
                "assistant",
                response
            )


            continue





        # TASK LOOP


        current_plan = plan

        complete = False


        while not complete:



            # EXECUTE


            print(
                "\n Executing..."
            )


            execution_result, task_reply, memories = execute(
                current_plan
            )



            print(
                execution_result
            )



            if task_reply:

                speak(
                    task_reply
                )




            # VISION


            print(
                "\n Checking screen..."
            )


            screen = vision.observe()


            print(
                screen
            )





            # ---------------------
            # VERIFY
            # ---------------------


            print(
                "\n Verifying..."
            )


            verification = verifier.verify(

                user_message,

                execution_result,

                screen

            )


            print(
                verification
            )



            complete = verification.get(
                "complete",
                False
            )



            if not complete:


                print(
                    "\n Task incomplete"
                )


                current_plan = verification.get(
                    "next_action"
                )


                if not current_plan:

                    print(
                        "No recovery action."
                    )

                    break





        # MEMORY SAVE


        for fact in memories:

            memory.save_fact(
                fact
            )


        memory.save_message(
            "user",
            user_message
        )


        print(
            "\n Task finished"
        )



    except KeyboardInterrupt:


        print(
            "\nJarvis shutting down..."
        )

        break



    except Exception as e:


        print(
            f"\n Error: {e}"
        )