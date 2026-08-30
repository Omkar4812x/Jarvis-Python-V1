import webbrowser

def search_video(command):
    """
    Parses the command, cleans it, and opens the YouTube search results.
    """
    # 1. Remove trigger words to get the actual query
    query = command.lower()
    trigger_words = ["play", "youtube", "search for", "watch", "open", "on"]
    
    for word in trigger_words:
        query = query.replace(word, "")
    
    query = query.strip()

    if not query:
        return "I didn't hear a video name."

    # 2. Construct the URL
    # This URL format forces YouTube to search for the query
    url = f"https://www.youtube.com/results?search_query={query}"

    # 3. Open in default browser
    webbrowser.open(url)

    return f"Opening YouTube results for {query}"