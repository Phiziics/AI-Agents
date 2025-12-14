from crewai import Crew
from textwrap import dedent
from dotenv import load_dotenv

from trip_agents import TripAgents
from trip_tasks import TripTasks

# Load environment variables from .env (OPENAI_API_KEY, SERPER_API_KEY, BROWSERLESS_API_KEY)
load_dotenv()


class TripCrew:
    def __init__(self, origin: str, cities: str, date_range: str, interests: str):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        # Create agents
        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        # Create tasks
        identify_task = tasks.identify_city(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range,
        )
        gather_task = tasks.gather_city(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range,
        )
        plan_task = tasks.plan_trip(
            travel_concierge_agent,
            self.origin,
            self.interests,
            self.date_range,
        )

        # Wire everything into a Crew
        crew = Crew(
            agents=[city_selector_agent, local_expert_agent, travel_concierge_agent],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True,
        )

        return crew.kickoff()


if __name__ == "__main__":
    print("## Welcome to Trip Planner Crew")
    print("-------------------------------")

    origin = input(
        dedent(
            """
        From where will you be traveling?
    """
        )
    )
    cities = input(
        dedent(
            """
        What city options are you considering?
        (Example: New York, Miami, Los Angeles)
    """
        )
    )
    date_range = input(
        dedent(
            """
        What is the date range you are interested in traveling?
        (Example: March 15–22, 2026)
    """
        )
    )
    interests = input(
        dedent(
            """
        What are some of your high-level interests and hobbies?
        (Example: museums, nightlife, food, hiking)
    """
        )
    )

    trip_crew = TripCrew(origin, cities, date_range, interests)
    result = trip_crew.run()

    print("\n\n########################")
    print("## Here is your Trip Plan")
    print("########################\n")
    print(result)