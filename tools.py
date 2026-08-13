import requests
import re

def get_weather(query):
    try:
        # Extract city name — assumes "in <city>" or "of <city>" pattern
        match = re.search(r"(?:in|of|for)\s+([A-Za-z\s]+)\??$", query)
        city = match.group(1).strip() if match else query.strip()
        
        url = f"https://wttr.in/{city}?format=3"
        return requests.get(url).text
    except:
        return "Weather service unavailable."