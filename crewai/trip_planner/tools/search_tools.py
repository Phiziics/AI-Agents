import json
import os
import requests

from crewai.tools import BaseTool


class SearchInternetTool(BaseTool):
    name: str = "Search the internet"
    description: str = (
        "Search the internet about a given topic and return relevant results. "
        "Uses the Serper.dev Google Search API."
    )

    def _run(self, query: str) -> str:
        """
        Synchronously search the web for the given query.
        """
        if "SERPER_API_KEY" not in os.environ:
            return "Error: SERPER_API_KEY environment variable not set."

        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            "X-API-KEY": os.environ["SERPER_API_KEY"],
            "content-type": "application/json",
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()

            if "organic" not in data:
                return (
                    "Sorry, I couldn't find anything about that. "
                    "There may be an issue with your Serper API key or query."
                )

            results = data["organic"]
            lines = []

            for result in results[:top_result_to_return]:
                try:
                    lines.append(
                        "\n".join(
                            [
                                f"Title: {result['title']}",
                                f"Link: {result['link']}",
                                f"Snippet: {result['snippet']}",
                                "-----------------",
                            ]
                        )
                    )
                except KeyError:
                    continue

            if not lines:
                return "No usable search results were returned."

            return "\n\n".join(lines)

        except requests.exceptions.RequestException as e:
            return f"Error searching the internet: {e}"
        except Exception as e:
            return f"Unexpected error while searching the internet: {e}"
