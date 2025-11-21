from duckduckgo_search import DDGS

def test_search():
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(keywords="neural network diagram", max_results=1))
            if results:
                print(f"Found image: {results[0]['image']}")
            else:
                print("No results found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
