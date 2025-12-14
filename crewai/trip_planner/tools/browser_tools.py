import json
import os
import requests

from crewai.tools import BaseTool
from unstructured.partition.html import partition_html


class BrowserScrapeTool(BaseTool):
    name: str = "Scrape website content"
    description: str = (
        "Scrape and return raw text content from a given website URL. "
        "Use this when you need to read or analyze the contents of a web page."
    )

    def _run(self, website: str) -> str:
        """
        Synchronously scrape website content.
        """
        if "BROWSERLESS_API_KEY" not in os.environ:
            return "Error: BROWSERLESS_API_KEY environment variable not set."

        api_url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        payload = json.dumps({"url": website})
        headers = {
            "cache-control": "no-cache",
            "content-type": "application/json",
        }

        try:
            response = requests.post(api_url, headers=headers, data=payload)
            response.raise_for_status()

            elements = partition_html(text=response.text)
            content = "\n\n".join(str(el) for el in elements)

            max_len = 32000
            if len(content) > max_len:
                return content[:max_len]

            return content

        except requests.exceptions.RequestException as e:
            return f"Error scraping website: {e}"
        except Exception as e:
            return f"Error parsing content: {e}"
