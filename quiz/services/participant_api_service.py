import requests
from typing import Optional, Dict, List


class ParticipantAPIService:
    """
    Service to fetch participants from external NexusOfThings API.
    """
    
    BASE_URL = "https://nexusofthings.onrender.com/api/participants/"
    
    @staticmethod
    def fetch_participant_by_email(email: str) -> Optional[Dict]:
        """
        Fetch participant by email from API.
        Returns None if not found.
        """
        try:
            response = requests.get(
                ParticipantAPIService.BASE_URL,
                params={"email": email},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("count", 0) > 0:
                    participants = data.get("participants", [])
                    # Find exact email match (case-insensitive)
                    email_lower = email.lower()
                    for participant in participants:
                        if participant.get("email", "").lower() == email_lower:
                            return participant
            return None
        except Exception as e:
            print(f"Error fetching participant: {e}")
            return None
    
    @staticmethod
    def fetch_participants_by_event(event: str) -> List[Dict]:
        """
        Fetch all participants for a specific event.
        """
        try:
            response = requests.get(
                ParticipantAPIService.BASE_URL,
                params={"event": event},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("participants", [])
            return []
        except Exception as e:
            print(f"Error fetching participants by event: {e}")
            return []
    
    @staticmethod
    def get_available_events() -> List[str]:
        """
        Get list of available events from API.
        """
        events = ["InnovWEB", "SensorShowDown", "IdeaArena", "Error Erase"]
        return events

