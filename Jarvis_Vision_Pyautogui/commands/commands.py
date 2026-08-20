def handle(user_message, memory):

    command = user_message.lower().strip()

    if command == "/exit":
        return True, True

    if command == "/clear":

        memory.clear()

        print("🗑 Memory cleared.")

        return True, False

    if command == "/facts":

        print("\n===== FACTS =====\n")

        facts = memory.get_facts()

        if not facts:
            print("No facts stored.")

        else:
            for fact in facts:
                print("-", fact)

        print()

        return True, False

    return False, False