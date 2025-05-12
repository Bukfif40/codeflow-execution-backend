import requests

# Replace this with your actual SerpAPI key
API_KEY ='d52702c67892dcd126e274078e3c63bd719fc73a372f1ba903dbda07aa174969'

def search_serpapi(query, num_results=10):
    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY,
        "num": num_results,
        "hl": "en",
    }

    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json().get("organic_results", [])

    if not results:
        print("No results found.")
        return

    for result in results:
        title = result.get("title")
        link = result.get("link")
        snippet = result.get("snippet", "")
        print(f"📘 {title}\n🔗 {link}\n📝 {snippet}\n")

if __name__ == "__main__":
    print("""
Welcome to the SerpAPI Google Search Tool!
You can search Google and see results right here.

Example queries:
 - Python list comprehension
 - Deep learning site:arxiv.org
 - Data science cheat sheet filetype:pdf
 - Large language models site:stanford.edu

Type 'exit' at any prompt to quit.
""")
    while True:
        query = input("\nEnter your search query (or type 'exit' to quit): ").strip()
        if query.lower() == 'exit':
            print("Goodbye!")
            break
        if not query:
            print("Please enter a search query.")
            continue
        try:
            num_results_input = input("How many results do you want? (default 10): ").strip()
            if num_results_input.lower() == 'exit':
                print("Goodbye!")
                break
            num_results = int(num_results_input) if num_results_input else 10
        except ValueError:
            print("Invalid number, using default of 10.")
            num_results = 10
        try:
            search_serpapi(query, num_results=num_results)
        except Exception as e:
            print(f"An error occurred: {e}\nPlease check your internet connection and API key.")
        again = input("\nWould you like to search again? (y/n): ").strip().lower()
        if again not in ('y', 'yes', ''):
            print("Goodbye!")
            break
