import json
import re
import os

# Mocking flight data
FLIGHT_DB = {
    "AI123": {"flight_number": "AI123", "departure_time": "08:00 AM", "destination": "Delhi", "status": "Delayed"},
    "AI456": {"flight_number": "AI456", "departure_time": "06:30 PM", "destination": "Mumbai", "status": "On Time"},
    "BA789": {"flight_number": "BA789", "departure_time": "10:15 AM", "destination": "London", "status": "On Time"},
    "QR101": {"flight_number": "QR101", "departure_time": "02:45 PM", "destination": "Doha", "status": "Delayed"},
    "EK202": {"flight_number": "EK202", "departure_time": "09:30 AM", "destination": "Dubai", "status": "Cancelled"},
    "LH303": {"flight_number": "LH303", "departure_time": "11:50 AM", "destination": "Frankfurt", "status": "On Time"},
    "CX404": {"flight_number": "CX404", "departure_time": "04:10 PM", "destination": "Hong Kong", "status": "Delayed"},
    "SQ505": {"flight_number": "SQ505", "departure_time": "07:25 AM", "destination": "Singapore", "status": "On Time"},
    "DL606": {"flight_number": "DL606", "departure_time": "05:40 PM", "destination": "New York", "status": "On Time"},
    "AA707": {"flight_number": "AA707", "departure_time": "03:30 AM", "destination": "Los Angeles", "status": "Cancelled"},
    "AF808": {"flight_number": "AF808", "departure_time": "01:55 PM", "destination": "Paris", "status": "Delayed"},
    "TK909": {"flight_number": "TK909", "departure_time": "06:20 AM", "destination": "Istanbul", "status": "On Time"},
    "QF010": {"flight_number": "QF010", "departure_time": "08:45 PM", "destination": "Sydney", "status": "On Time"},
    "AI111": {"flight_number": "AI111", "departure_time": "12:00 PM", "destination": "Chennai", "status": "Delayed"},
    "BA222": {"flight_number": "BA222", "departure_time": "09:10 AM", "destination": "Toronto", "status": "Cancelled"}
}


# API Key handling
from dotenv import load_dotenv
load_dotenv("api_keys.env")

def get_flight_info(flight_number: str) -> dict:
    """ Fetches flight info from the database. """
    return FLIGHT_DB.get(flight_number, None)

def info_agent_request(flight_number: str) -> str:
    """ Calls get_flight_info and returns the data in JSON format. """
    flight_data = get_flight_info(flight_number)
    if not flight_data:
        return json.dumps({"error": "Flight not found"})
    return json.dumps(flight_data)

def qa_agent_respond(user_query: str) -> str:
    """ Extracts flight number from user query and fetches flight data. """
    match = re.search(r'Flight (\w+)', user_query, re.IGNORECASE)
    if not match:
        return json.dumps({"error": "No valid flight number found in query"})

    flight_number = match.group(1)
    flight_info_json = info_agent_request(flight_number)
    flight_info = json.loads(flight_info_json)

    if "error" in flight_info:
        return json.dumps({"answer": f"Flight {flight_number} not found in database."})

    return json.dumps({
        "answer": f"Flight {flight_info['flight_number']} departs at {flight_info['departure_time']} "
                  f"to {flight_info['destination']}. Current status: {flight_info['status']}."
    })

if __name__ == "__main__":
    print(qa_agent_respond("When does Flight AI123 depart?"))
    print(qa_agent_respond("What is the status of Flight AI999?"))
    print(qa_agent_respond("Where does Flight BA222 go?"))
