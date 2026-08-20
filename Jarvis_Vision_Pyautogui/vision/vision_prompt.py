def build_verify_prompt(
    user_task,
    execution_result,
    screen_state
):

    return f"""
You are Jarvis task verification AI.

Your job:
Check if the user's requested task has been completed.

USER REQUEST:
{user_task}


EXECUTION RESULT:
{execution_result}


CURRENT SCREEN STATE:
{screen_state}


Decide:

If the task is completed:

Return ONLY:

{{
    "complete": true,
    "response": "short confirmation"
}}


If the task is NOT completed:

Return ONLY:

{{
    "complete": false,
    "reason": "what is missing",
    "next_action": {{
        "tasks": [
            {{
                "action": "gui",
                "code": "pyautogui code"
            }}
        ]
    }}
}}


Do not explain anything.
Return JSON only.
"""