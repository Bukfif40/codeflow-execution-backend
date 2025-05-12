"""
Search provider classes for the backend.
"""

import requests
from typing import List, Dict


class SerpAPIProvider:
    import os
    API_KEY = os.getenv(
        "SERPAPI_KEY",
        "d52702c67892dcd126e274078e3c63bd719fc73a372f1ba903dbda07aa174969"
    )
    BASE_URL = "https://serpapi.com/search"

    @classmethod
    def search(cls, query: str, num_results: int = 10) -> List[Dict]:
        params = {
            "engine": "google",
            "q": query,
            "api_key": cls.API_KEY,
            "num": num_results,
            "hl": "en",
        }
        try:
            response = requests.get(
                cls.BASE_URL, params=params, timeout=10
            )
            response.raise_for_status()
            results = response.json().get("organic_results", [])
            return [
                {
                    "title": r.get("title"),
                    "link": r.get("link"),
                    "snippet": r.get("snippet", "")
                }
                for r in results
            ]
        except Exception as e:
            return [
                {"title": "Error", "link": "", "snippet": str(e)}
            ]


class BingProvider:
    @classmethod
    def search(cls, query: str, num_results: int = 10) -> List[Dict]:
        # Placeholder: implement Bing search logic here
        return [
            {
                "title": f"Bing result {i+1} for '{query}'",
                "link": f"https://bing.com/{i+1}",
                "snippet": f"Bing snippet {i+1}."
            }
            for i in range(num_results)
        ]


def get_provider(name: str):
    providers = {
        "serpapi": SerpAPIProvider,
        "bing": BingProvider,
    }
    return providers.get(name.lower(), SerpAPIProvider)
