from crewai import Agent
from langchain_openai import ChatOpenAI

from tools import BrowserScrapeTool, CalculatorTool, SearchInternetTool


class TripAgents:
    def __init__(self):
        # Shared LLM for all agents
        self.llm = ChatOpenAI(model="gpt-4o-mini")

        # Instantiate tools (BaseTool subclasses)
        self.search_tool = SearchInternetTool()
        self.browser_tool = BrowserScrapeTool()
        self.calculator_tool = CalculatorTool()

    def _search_tools(self):
        return [
            self.search_tool,
            self.browser_tool,
        ]

    def _calc_tools(self):
        return [
            self.search_tool,
            self.browser_tool,
            self.calculator_tool,
        ]

    def city_selection_agent(self) -> Agent:
        return Agent(
            role="City Selection Expert",
            goal="Select the best city based on weather, season, and prices",
            backstory=(
                "An expert in analyzing travel and pricing data to pick "
                "ideal destinations based on time of year, cost, and traveler profile."
            ),
            tools=self._search_tools(),
            llm=self.llm,
            verbose=True,
        )

    def local_expert(self) -> Agent:
        return Agent(
            role="Local Expert at this city",
            goal="Provide the BEST insights about the selected city",
            backstory=(
                "A knowledgeable local guide with extensive information about the city, "
                "its attractions, neighborhoods, and culture."
            ),
            tools=self._search_tools(),
            llm=self.llm,
            verbose=True,
        )

    def travel_concierge(self) -> Agent:
        return Agent(
            role="Amazing Travel Concierge",
            goal=(
                "Create the most amazing travel itineraries with budget and "
                "packing suggestions for the city."
            ),
            backstory=(
                "Specialist in travel planning and logistics with decades of experience "
                "designing unforgettable trips."
            ),
            tools=self._calc_tools(),
            llm=self.llm,
            verbose=True,
        )
