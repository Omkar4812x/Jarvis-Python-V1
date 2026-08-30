



import os
import subprocess
import webbrowser
import pyautogui 
import time

# Try to import Google API Client (Handle if not installed)
try:
    from googleapiclient.discovery import build
    GOOGLE_API_INSTALLED = True
except ImportError:
    GOOGLE_API_INSTALLED = False
    print("⚠️ Warning: 'google-api-python-client' is not installed. YouTube Autoplay won't work.")

# --- DATABASE ---
APP_MAP = {
    # APPS (Type: "app")
    "notepad": ["notepad.exe", "start notepad", "app"],
    "calculator": ["CalculatorApp.exe", "start calc", "app"],
    "vs code": ["Code.exe", "code", "app"],
    "visual studio": ["Code.exe", "code", "app"],
    "visual studio code": ["Code.exe", "code", "app"],
    "file explorer": ["explorer.exe", "start explorer", "app"],
    "word": ["WINWORD.EXE", "start winword", "app"],
    "powerpoint": ["POWERPNT.EXE", "start powerpnt", "app"],
    "excel": ["EXCEL.EXE", "start excel", "app"],
    "cmd": ["cmd.exe", "start cmd", "app"],
    "terminal": ["cmd.exe", "start cmd", "app"],
    
    # WEBSITES (Type: "web")
    "google": ["web", "https://google.com"],
    "youtube": ["web", "https://youtube.com"],
    "instagram": ["web", "https://instagram.com"],
    "facebook": ["web", "https://facebook.com"],
    "twitter": ["web", "https://twitter.com"],
    "whatsapp": ["web", "https://web.whatsapp.com"],
    "chatgpt": ["web", "https://chatgpt.com"],
    "github": ["web", "https://github.com"],
    "gmail": ["web", "https://mail.google.com"]
}

def get_yt_video_url(query, api_key):
    """
    Searches YouTube API for the first video and returns its direct watch URL.
    """
    if not GOOGLE_API_INSTALLED:
        return None

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=1,
            type='video'
        )
        response = request.execute()
        
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"❌ YouTube API Error: {e}")
    
    return None

def execute(command, youtube_key=None):
    cmd = command.lower()

    # 1. SEARCH GOOGLE
    if "search google for" in cmd:
        query = cmd.replace("search google for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for {query}."

    # 2. SEARCH/PLAY YOUTUBE (UPDATED FOR AUTOPLAY)
    if "play" in cmd or "search youtube for" in cmd:
        query = cmd.replace("play", "").replace("search youtube for", "").replace("on youtube", "").strip()
        
        # Method A: API Autoplay (If Key exists and user said "Play")
        if "play" in cmd and youtube_key:
            print(f"🔎 Searching YouTube API for: {query}...")
            video_url = get_yt_video_url(query, youtube_key)
            
            if video_url:
                webbrowser.open(video_url)
                return f"Playing {query} on YouTube."
            else:
                print("⚠️ API search failed or no results. Falling back to standard search.")

        # Method B: Standard Search (Fallback)
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Opening YouTube results for {query}."

    # 3. SMART CLOSE (Tab vs App)
    if "close" in cmd or "exit" in cmd:
        for app_name, details in APP_MAP.items():
            if app_name in cmd:
                app_type = details[2] if len(details) > 2 else "web"
                
                if app_type == "web":
                    # Close Browser Tab (Ctrl + W)
                    pyautogui.hotkey('ctrl', 'w')
                    return f"Closing {app_name} tab."
                else:
                    # Kill App Process
                    process_name = details[0]
                    os.system(f"taskkill /f /im {process_name}")
                    return f"Closing {app_name}."

    # 4. SMART OPEN
    if "open" in cmd or "start" in cmd:
        for app_name, details in APP_MAP.items():
            if app_name in cmd:
                launch_cmd = details[1]
                
                # VS Code Special Handling
                if "code" in launch_cmd:
                    try: subprocess.Popen("code", shell=True)
                    except: os.system(launch_cmd)
                # Website
                elif launch_cmd.startswith("http"):
                    webbrowser.open(launch_cmd)
                # Standard App
                else:
                    os.system(launch_cmd)
                return f"Opening {app_name}."

    return None

def type_and_save(text, app="notepad"):
    """Types text into Notepad/Word and saves it."""
    filename = f"Genius_Note_{int(time.time())}"
    
    if app == "word":
        os.system("start winword")
        time.sleep(4) 
        pyautogui.press('enter') 
    else:
        os.system("start notepad")
        time.sleep(1)
        
    time.sleep(1)
    pyautogui.write(text, interval=0.001) 
    
    time.sleep(1)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.write(filename)
    pyautogui.press('enter')
    
    return f"I have written and saved the content in {app}."

def create_coding_project(code_content, lang="html"):
    """Creates a code file and opens it in VS Code."""
    filename = "index.html"
    if lang == "python": filename = "script.py"
    
    base_folder = os.getcwd() 
    project_folder = os.path.join(base_folder, "My_AI_Projects")
    
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
        
    file_path = os.path.join(project_folder, filename)
    
    # Write File
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_content)
    except Exception as e:
        print(f"File Write Error: {e}")
        return "I couldn't save the file due to a permission error."

    # Open VS Code
    try:
        subprocess.Popen(f'code "{project_folder}"', shell=True)
        time.sleep(2)
        subprocess.Popen(f'code "{file_path}"', shell=True)
    except:
        return "Created the file, but VS Code didn't open."

    # Run in Browser (if HTML)
    if lang == "html":
        time.sleep(1)
        webbrowser.open('file://' + file_path)
    
    return f"I built the {lang} project and opened it."


