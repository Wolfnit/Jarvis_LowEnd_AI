import json
import subprocess
import pyautogui


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1



def execute(ai_response):
    """
    Executes AI generated tasks.

    Returns:
        execution_result
        chat_response
        memories
    """


    try:

        if isinstance(ai_response, str):

            data = json.loads(
                ai_response
            )

        else:

            data = ai_response


    except Exception as e:


        return (
            f"Invalid JSON: {e}",
            "",
            []
        )



    if "tasks" in data:

        tasks = data["tasks"]

    else:

        tasks = [data]



    execution_logs = []

    chat_response = ""

    memories = []



    for task in tasks:


        action = task.get(
            "action",
            ""
        ).lower()



        # CHAT MESSAGE

        if action == "chat":

            chat_response = task.get(
                "response",
                ""
            )


        # CMD

        elif action == "cmd":


            command = task.get(
                "command",
                ""
            )


            print(
                f"⚡ CMD: {command}"
            )


            try:

                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )


                execution_logs.append(
                    result.stdout or result.stderr
                )


            except Exception as e:

                execution_logs.append(
                    f"CMD error: {e}"
                )



        # POWERSHELL

        elif action == "powershell":


            command = task.get(
                "command",
                ""
            )


            print(
                f"⚡ PowerShell: {command}"
            )


            try:

                result = subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        command
                    ],
                    capture_output=True,
                    text=True
                )


                execution_logs.append(
                    result.stdout or result.stderr
                )


            except Exception as e:

                execution_logs.append(
                    f"Powershell error: {e}"
                )

        # GUI

        elif action == "gui":


            code = task.get(
                "code",
                ""
            )


            print(
                "\n GUI:"
            )

            print(code)


            try:


                exec(
                    code,
                    {
                        "pyautogui": pyautogui
                    }
                )


                execution_logs.append(
                    "GUI executed successfully"
                )


            except Exception as e:


                execution_logs.append(
                    f"GUI error: {e}"
                )



        # MEMORY
        elif action == "memory_longterm":


            fact = task.get(
                "response",
                ""
            )


            if fact:

                memories.append(
                    fact
                )



        else:

            execution_logs.append(
                f"Unknown action: {action}"
            )



    execution_result = "\n".join(
        execution_logs
    )


    return (
        execution_result,
        chat_response,
        memories
    )