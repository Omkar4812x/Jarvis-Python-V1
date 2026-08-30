import os

# --- THE HTML CODE FOR THE UI ---
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genius AI | Premium</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Lato:wght@300;400&display=swap');
        :root { --gold: #D4AF37; --glass: rgba(255, 255, 255, 0.8); }
        body { margin: 0; background: linear-gradient(135deg, #fdfbf7 0%, #e8e6e1 100%); height: 100vh; display: flex; justify-content: center; align-items: center; font-family: 'Lato', sans-serif; overflow: hidden; }
        .container { background: var(--glass); backdrop-filter: blur(20px); width: 90%; max-width: 500px; padding: 40px; border-radius: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.05); text-align: center; }
        h1 { font-family: 'Playfair Display', serif; color: #2C2C2C; margin-bottom: 5px; font-size: 2rem; }
        .orb-container { height: 150px; display: flex; justify-content: center; align-items: center; margin: 30px 0; }
        .orb { width: 80px; height: 80px; background: linear-gradient(45deg, var(--gold), #F6E27A); border-radius: 50%; box-shadow: 0 0 30px rgba(212, 175, 55, 0.4); transition: all 0.3s ease; }
        .listening .orb { animation: pulse 1.5s infinite; transform: scale(1.2); }
        .speaking .orb { animation: vibrate 0.2s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.7); } 70% { box-shadow: 0 0 0 30px rgba(212, 175, 55, 0); } 100% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); } }
        @keyframes vibrate { 0% { transform: translate(0); } 20% { transform: translate(-2px, 2px); } 40% { transform: translate(-2px, -2px); } 60% { transform: translate(2px, 2px); } 80% { transform: translate(2px, -2px); } 100% { transform: translate(0); } }
        .btn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .btn { background: white; border: 1px solid #ddd; padding: 15px; border-radius: 12px; cursor: pointer; font-family: 'Lato', sans-serif; font-weight: 600; transition: all 0.3s; }
        .btn:hover { border-color: var(--gold); transform: translateY(-2px); }
        .btn-stop { grid-column: span 2; background: #fff0f0; color: #d9534f; border-color: #ffcccc; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Genius AI</h1>
        <p style="color:#888; font-size:0.9rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:30px;">Premium Voice Assistant</p>
        
        <div id="selection-screen">
            <p>Select Mode:</p>
            <div class="btn-grid">
                <button class="btn" onclick="startMode('1')">English</button>
                <button class="btn" onclick="startMode('2')">Kanglish</button>
                <button class="btn" onclick="startMode('3')">Kannada</button>
                <button class="btn" onclick="startMode('4')">Hindi</button>
                <button class="btn" onclick="startMode('5')">Hinglish</button>
            </div>
        </div>

        <div id="active-screen" class="hidden">
            <div class="orb-container" id="orb-container"><div class="orb"></div></div>
            <div id="status-text" style="font-weight:bold; color:#D4AF37; margin-bottom:10px;">Connecting...</div>
            <div id="conversation" style="min-height:40px; font-style:italic; color:#555; margin-bottom:30px;">...</div>
            <div class="btn-grid"><button class="btn btn-stop" onclick="shutdown()">End Session</button></div>
        </div>
    </div>
    <script>
        let poller;
        function startMode(mode) {
            document.getElementById('selection-screen').classList.add('hidden');
            document.getElementById('active-screen').classList.remove('hidden');
            fetch(`/start_mode/${mode}`);
            poller = setInterval(checkStatus, 500);
        }
        function checkStatus() {
            fetch('/status').then(r => r.json()).then(data => {
                document.getElementById('status-text').innerText = data.status.toUpperCase();
                if(data.last_text) document.getElementById('conversation').innerText = `"${data.last_text}"`;
                const orb = document.getElementById('orb-container');
                orb.className = 'orb-container';
                if (data.status === 'listening') orb.classList.add('listening');
                if (data.status === 'speaking') orb.classList.add('speaking');
                if (data.status === 'stopped') { clearInterval(poller); window.close(); }
            });
        }
        function shutdown() { fetch('/shutdown'); setTimeout(() => window.close(), 2000); }
    </script>
</body>
</html>
"""

# --- AUTO-FIX LOGIC ---
current_dir = os.getcwd()
templates_dir = os.path.join(current_dir, "templates")
html_path = os.path.join(templates_dir, "index.html")

print(f"🔧 Fixing folders in: {current_dir}")

# 1. Create 'templates' folder
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
    print("✅ Created 'templates' folder.")
else:
    print("✅ 'templates' folder exists.")

# 2. Write the HTML file
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Created 'index.html' inside 'templates'.")
print("\n🎉 REPAIR COMPLETE!")
print("👉 You can now run 'python main.py'")