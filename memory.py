# memory.py

# This list stores the conversation
conversation_history = []

def init_memory(system_prompt):
    """
    Clears memory and sets the initial personality (System Prompt).
    """
    global conversation_history
    conversation_history = [
        {"role": "system", "content": system_prompt}
    ]

def add_user_message(text):
    """Adds what the User said to memory."""
    conversation_history.append({"role": "user", "content": text})
    _trim_memory()

def add_ai_message(text):
    """Adds what the AI answered to memory."""
    conversation_history.append({"role": "assistant", "content": text})
    _trim_memory()

def get_messages():
    """Returns the full list of messages for the AI to read."""
    return conversation_history

def _trim_memory():
    """
    Keeps only the last 10 messages to prevent the AI from getting slow.
    Always keeps the System Prompt [0].
    """
    global conversation_history
    if len(conversation_history) > 11:
        # Keep index 0 (System), remove index 1 (Oldest message)
        conversation_history.pop(1)