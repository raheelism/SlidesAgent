import requests

def test_wikimedia(query):
    print(f"Testing Wikimedia for: {query}")
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": 6,  # File namespace
        "gsrsearch": query,
        "gsrlimit": 1,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    headers = {
        "User-Agent": "SlidesAgent/1.0 (https://github.com/yourusername/slides-agent; your@email.com)"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            print("No results found.")
            return

        for page_id, page_data in pages.items():
            image_info = page_data.get("imageinfo", [])
            if image_info:
                image_url = image_info[0]["url"]
                print(f"Found image URL: {image_url}")
                return image_url
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_wikimedia("Artificial Intelligence")
    test_wikimedia("Neural Network")
