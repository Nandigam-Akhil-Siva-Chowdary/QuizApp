import requests
from typing import List, Dict


class EventsAPIService:
    """
    Service to fetch events from external NexusOfThings API.
    """

    BASE_URL = "https://nexusofthings.onrender.com/api/events/"

    @staticmethod
    def fetch_events() -> List[Dict]:
        """
        Fetch all events.
        """
        try:
            response = requests.get(EventsAPIService.BASE_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("events", [])
        except Exception as e:
            print(f"Error fetching events: {e}")
        return []

    @staticmethod
    def get_event_name_choices() -> List[tuple]:
        """
        Return choices list suitable for Django ChoiceField:
        [(name, name), ...]
        """
        events = EventsAPIService.fetch_events()
        choices = []
        for ev in events:
            name = ev.get("name")
            if name:
                choices.append((name, name))
        return choices


