# 🤖 Jarvis Python V1 Assistant

> **Modular Python virtual assistant v1 featuring multi-threaded speech-to-text, DeepSeek / Groq API LLM integration, desktop web UI, and code generation automation.**

---

## ✨ Features

- 🔊 **Multi-Threaded Speech Queue (TTS)**
  - Asynchronous background text-to-speech worker thread using `pyttsx3` and thread-safe queues.
- 🧠 **Groq & DeepSeek API Brain**
  - High-speed conversational AI response using DeepSeek (`deepseek-chat-v3`) and Groq API gateways.
- 💻 **Autonomous Code Generator Mode**
  - Generates standalone single-file HTML/CSS/JS frontend projects on voice command.
- 🌐 **Flask Control Interface**
  - Real-time web status endpoint (`http://127.0.0.1:5000`) and live voice status dashboard.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Voice**: `SpeechRecognition`, `pyttsx3`, `SAPI5`, `Queue`
- **Web & API**: Flask, OpenAI SDK (Groq/OpenRouter endpoint), Requests

---

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Omkar4812x/Jarvis-Python-V1.git
   cd Jarvis-Python-V1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run Jarvis V1**:
   ```bash
   python main.py
   ```

---

## 📄 License

Distributed under the MIT License.
