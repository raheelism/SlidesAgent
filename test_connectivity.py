import requests

def test_url(url):
    print(f"Testing {url}...")
    try:
        response = requests.get(url, timeout=5)
        print(f"Success: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_url("https://www.google.com")
    test_url("https://en.wikipedia.org")
    test_url("https://commons.wikimedia.org")
