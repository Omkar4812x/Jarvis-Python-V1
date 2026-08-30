import os
import time
import re
import threading
import webbrowser
import speech_recognition as sr
from openai import OpenAI
import pyttsx3
from flask import Flask, render_template, jsonify, request
import logging
from queue import Queue

# CUSTOM MODULES
import memory
import automation
import youtube_helper

# ==========================================
#        SETTINGS
# ==========================================

GROQ_API_KEY = "YOUR_GROQ_API_KEY"
ROBOT_SPEED = 140

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
app = Flask(__name__)

shared_data = {
    "status": "idle",
    "last_text": "",
    "running": True
}

speech_queue = Queue()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# ==========================================
#        BACKGROUND TTS (FIXED & STABLE)
# ==========================================

def tts_worker():
    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", ROBOT_SPEED)
    engine.setProperty("volume", 1.0)

    while True:
        text = speech_queue.get()
        if text is None:
            break
        try:
            print(f"Genius (VOICE): {text}")
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("TTS ERROR:", e)
        speech_queue.task_done()

threading.Thread(target=tts_worker, daemon=True).start()

def speak(text):
    shared_data["status"] = "speaking"
    shared_data["last_text"] = text
    print(f"Genius: {text}")
    speech_queue.put(text)
    shared_data["status"] = "listening"

# ==========================================
#        ASSISTANT LOGIC
# ==========================================

def assistant_logic():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    # init memory with simple system prompt
    memory.init_memory([
        {
            "role": "system",
            "content": "You are Jarvis, an intelligent assistant. Always reply in clear English."
        }
    ])

    speak("System online. I am ready.")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while shared_data["running"]:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, phrase_time_limit=10)

            shared_data["status"] = "processing"

            try:
                text = recognizer.recognize_google(audio, language="en-IN")
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print("Speech service error:", e)
                continue

            print(f"User: {text}")
            cmd = text.lower()

            if "stop" in cmd or "exit" in cmd:
                speak("Goodbye.")
                os._exit(0)

            # ======================================
            # CODING MODE (INLINE PROMPT – NO MISSING PART)
            # ======================================
            if "build" in cmd or "code" in cmd or "create a website" in cmd:
                speak("I am building the project now.")

                coding_prompt = (
                    "You are a world class frontend developer. "
                    "Generate a complete single HTML file starting with <!DOCTYPE html>. "
                    "Use inline CSS and JavaScript only. "
                    "No markdown, no explanations, only pure code."
                )

                completion = client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3-0324",
                    messages=[
                        {"role": "system", "content": coding_prompt},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.1
                )

                code = completion.choices[0].message.content
                match = re.search(r"(<!DOCTYPE html>[\s\S]*</html>)", code, re.I)
                if match:
                    code = match.group(1)

                speak(automation.create_coding_project(code, "html"))
                continue

            # ======================================
            # AUTOMATION
            # ======================================
            auto = automation.execute(text, None)
            if auto:
                speak(auto)
                continue

            # ======================================
            # NORMAL CHAT
            # ======================================
            memory.add_user_message(text)

            # -------- CHAT (OpenRouter-safe) --------

            raw_messages = memory.get_messages()

            safe_messages = []
            for msg in raw_messages[-6:]:  # keep last 6 for speed
                if isinstance(msg.get("content"), str):
                    safe_messages.append(msg)
                else:
                    # force content to string (FIX)
                    safe_messages.append({
                        "role": msg.get("role", "user"),
                        "content": str(msg.get("content"))
                    })

            completion = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324",
                messages=safe_messages,
                max_tokens=80,
                temperature=0.6,
                timeout=15
            )

            reply = completion.choices[0].message.content
            memory.add_ai_message(reply)
            speak(reply)

            reply = completion.choices[0].message.content
            memory.add_ai_message(reply)
            speak(reply)

        except Exception as e:
            print("Main loop error:", e)
            time.sleep(0.3)

# ==========================================
#        ROUTES
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify(shared_data)

@app.route("/shutdown")
def shutdown():
    shared_data["running"] = False
    speech_queue.put(None)
    return "Bye"

# ==========================================
#        START
# ==========================================

if __name__ == "__main__":
    threading.Thread(target=assistant_logic, daemon=True).start()
    webbrowser.open("http://127.0.0.1:5000")
    app.run(port=5000)
