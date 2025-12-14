from crewai import Task
from textwrap import dedent


class TripTasks:
    def identify_city(self, agent, origin, cities, interests, trip_range):
        return Task(
            description=dedent(
                f"""
                Analyze and select the best city for the trip based on weather patterns,
                seasonal events, and travel costs.

                You must compare the city options by:
                - Current and forecasted weather
                - Seasonal or cultural events around the travel dates
                - Approximate travel and lodging costs

                Your final answer must be a detailed report on the chosen city
                and everything you found out about it, including actual example
                flight costs, weather forecast, and top attractions.

                {self.__tip_section()}

                Traveling from: {origin}
                City options: {cities}
                Trip Date: {trip_range}
                Traveler Interests: {interests}
                """
            ),
            agent=agent,
            expected_output=(
                "Detailed report on the chosen city including flight costs, "
                "weather forecast, and attractions."
            ),
        )

    def gather_city(self, agent, origin, interests, trip_range):
        return Task(
            description=dedent(
                f"""
                As a local expert on this city, compile an in-depth guide
                for someone traveling there and wanting to have THE BEST trip ever!

                You must:
                - Gather information about key attractions, local customs, and special events
                - Highlight hidden gems and non-touristy spots
                - Include must-visit landmarks and neighborhoods
                - Provide a general idea of daily costs and logistics

                The final answer must be a comprehensive city guide full of
                cultural insights and practical tips.

                {self.__tip_section()}

                Trip Date: {trip_range}
                Traveling from: {origin}
                Traveler Interests: {interests}
                """
            ),
            agent=agent,
            expected_output=(
                "Comprehensive city guide including hidden gems, cultural hotspots, "
                "and practical travel tips."
            ),
        )

    def plan_trip(self, agent, origin, interests, trip_range):
        return Task(
            description=dedent(
                f"""
                Expand the city guide into a full 7-day travel itinerary with
                detailed per-day plans, including:

                - Daily schedule with morning, afternoon, and evening activities
                - Actual places to visit (attractions, neighborhoods)
                - Actual hotel or lodging suggestions
                - Actual restaurants and food spots
                - Approximate daily budget and trip total
                - Packing suggestions aligned with weather and activities

                Your final answer MUST be:
                - A complete expanded travel plan
                - Formatted as markdown
                - Including daily schedule, expected weather, recommended clothing,
                  and a detailed budget breakdown.

                Be specific and explain why you picked each place and what makes it special.

                {self.__tip_section()}

                Trip Date: {trip_range}
                Traveling from: {origin}
                Traveler Interests: {interests}
                """
            ),
            agent=agent,
            expected_output=(
                "Complete expanded travel plan with daily schedule, weather conditions, "
                "packing suggestions, and budget breakdown."
            ),
        )

    def __tip_section(self) -> str:
        return "If you do your BEST WORK, I'll tip you $100!"
