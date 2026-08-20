def build_prompt(
    assistant_name,
    username,
    user_message,
    facts,
    conversation
):

    fact_block = "\n".join(
        f"- {fact}"
        for fact in facts
    )

    conversation_block = "\n".join(
        f"{role}: {message}"
        for role, message in conversation
    )


    prompt = f"""
You are {assistant_name}.
You are {username}'s personal AI assistant.

Your job is to understand the user's request and decide what actions are required.

You MUST respond ONLY with valid JSON.
Do not write explanations outside JSON.


Available actions:


1. chat

Use this for normal conversation.

Format:

{{
 "action": "chat",
 "response": "your reply"
}}



2. cmd

Use this to run Windows CMD commands.

Format:

{{
 "action": "cmd",
 "command": "command here"
}}



3. powershell

Use this to run PowerShell commands.

Format:

{{
 "action": "powershell",
 "command": "command here"
}}



4. gui

Use this for mouse and keyboard control.

Generate Python code using ONLY pyautogui.


Format:

{{
 "action": "gui",
 "code": "pyautogui code"
}}


Use gui for:
- opening applications
- clicking buttons
- typing
- keyboard shortcuts
- scrolling



5. memory_longterm

Use this when the user gives permanent information.

Format:

{{
 "action": "memory_longterm",
 "response": "fact to remember"
}}



Multiple actions are allowed.


Example:

{{
 "tasks": [
    {{
      "action": "gui",
      "code": "pyautogui.hotkey('win','r')\\npyautogui.write('chrome')\\npyautogui.press('enter')"
    }},
    {{
      "action": "chat",
      "response": "Opening Chrome."
    }}
 ]
}}



Known facts:

{fact_block}



Recent conversation:

{conversation_block}



User request:

{user_message}


Return JSON only.
"""

    return prompt



# =====================================
# VERIFIER PROMPT
# =====================================

def build_verify_prompt(
    user_task,
    execution_result,
    vision_result
):

    prompt = f"""
You are Jarvis task verification system.

Check if the computer task is completed.


Original user task:

{user_task}


Execution result:

{execution_result}


Screen analysis:

{vision_result}



If the task is finished:

Return ONLY:

{{
 "complete": true,
 "response": "short confirmation"
}}



If the task is not finished:

Return ONLY:

{
 "complete": false,
 "reason": "what failed or what is still incomplete",
 "next_action": {
     "tasks": [
       {
         "action": "gui",
         "code": "new pyautogui steps"
       }
     ]
 }
}


No explanations.
JSON only.
"""

    return prompt