from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class WebSearcher(BaseTool):
    """
    A tool to search the web for AI trends using Tavily API.
    """
    query: str = Field(
        ..., description="The search query for finding AI trends."
    )
    search_depth: str = Field(
        "basic", description="The depth of search: 'basic' or 'deep'."
    )

    def run(self):
        """Search the web using Tavily API."""
        try:
            response = client.search(
                query=self.query,
                search_depth=self.search_depth,
                include_answer=True,
                include_domains=["techcrunch.com", "wired.com", "venturebeat.com", "ai.gov"]
            )
            return response
        except Exception as e:
            return f"Error searching web: {str(e)}"

if __name__ == "__main__":
    tool = WebSearcher(query="latest developments in AI technology")
    print(tool.run()) 