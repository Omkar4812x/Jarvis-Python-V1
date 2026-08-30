# # prompts.py

# # --- THE STRICT RULE (Applies to all languages) ---
# # This ensures the AI never gives long, boring definitions.
# STRICT_RULES = (
#     " IMPORTANT: Answer in 1 short sentence only. "
#     "Do not give definitions. Do not use bullet points. "
#     "Do not say 'I am an AI'. Act like a human friend."
# )

# # --- LANGUAGE MODES ---
# MODES = {
#     '1': "Reply in English only.",
    
#     '2': (
#         "Reply in Kanglish (Kannada grammar with English words). "
#         "Example: 'Oota aita?'. Do not use Kannada script."
#     ),
    
#     '3': "Reply in Kannada script (ಕನ್ನಡ) only.",
    
#     '4': "Reply in Hindi script (हिंदी) only.",
    
#     '5': (
#         "Reply in Hinglish (Hindi grammar with English words). "
#         "Example: 'Kya haal hai?'. Do not use Devanagari script."
#     )
# }

# def get_prompt(choice):
#     """
#     Combines the language mode with the strict rules.
#     """
#     # Get the specific language instruction (Default to English '1' if error)
#     base_instruction = MODES.get(choice, MODES['1'])
    
#     # Combine them
#     return f"{base_instruction} {STRICT_RULES}"



# prompts.py

# --- THE STRICT RULE (Applies to all languages) ---
STRICT_RULES = (
    " IMPORTANT: Answer in 1 short, intelligent sentence. "
    "If the user's input is incomplete, guess their intent and answer helpfuly. "
    "Do not simply repeat the user's words. Give a meaningful fact or answer."
)

# --- LANGUAGE MODES ---
MODES = {
    # 1. English
    '1': "Reply in English. Be precise and factual.",
    
    # 2. Hindi (Mapped to Option 2 now)
    '2': "Reply in pure Hindi script (हिंदी). Give factual, meaningful answers using natural conversational Hindi."
}

def get_prompt(choice):
    """
    Combines the language mode with the strict rules.
    """
    # Default to English '1' if error
    base_instruction = MODES.get(choice, MODES['1'])
    return f"{base_instruction} {STRICT_RULES}"