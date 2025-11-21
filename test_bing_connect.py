import requests

def test_bing_connect():
    url = "https://www.bing.com/images/search?q=cat"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    print(f"Testing {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(f"Success: {response.status_code}")
        if "iusc" in response.text:
            print("Found 'iusc' class (scraper likely to work).")
        else:
            print("Did not find 'iusc' class.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_bing_connect()
