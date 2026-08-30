# voice_manager.py
import pyttsx3

def get_system_voices():
    """
    Initializes a temporary engine to fetch available system voices.
    Returns a list of dictionaries: [{'id': '...', 'name': '...'}]
    """
    try:
        # We initialize a temp engine just to read the list
        temp_engine = pyttsx3.init()
        voices = temp_engine.getProperty('voices')
        
        voice_list = []
        for v in voices:
            # Clean up the name for the UI
            name = v.name.replace("Microsoft", "").replace("Desktop", "").strip()
            voice_list.append({
                "id": v.id,
                "name": name
            })
            
        return voice_list
    except Exception as e:
        print(f"Error fetching voices: {e}")
        return []

def set_engine_voice(engine, voice_id):
    """
    Safely sets the voice on the running engine.
    """
    try:
        engine.setProperty('voice', voice_id)
        return True
    except:
        return 

