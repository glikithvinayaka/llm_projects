import streamlit as st
import openai
import pandas as pd

# OpenAI API key
openai.api_key = '*********************************************'

# Title with HTML styling
st.markdown('<h1 style="text-align: center;">' +
            '<span style="color: #006bb8;">SAP</span> ' +
            'Travel Assistant</h1>', 
            unsafe_allow_html=True)

chat_bubble_css = """
<style>

.chat-wrapper {
    display: flex;
    flex-direction: column;
    height: 50vh;
    justify-content: flex-end;
}

.chat-container {
    display: flex;
    flex-direction: column-reverse;
    flex-grow: 1;
    padding-bottom: 30px;
    overflow-y: auto;
}

.chat-bubble {
    padding: 10px;
    border-radius: 15px;
    margin: 5px;
    max-width: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-bubble {
    background-color: #8d8f8e;
    color: white;
    align-self: flex-end;
    text-align: auto;
    max-width: 40%;
    margin-left: auto;
}

.agent-bubble {
    background-color: #2196F3;
    color: white;
    align-self: flex-start;
    text-align: left;
    max-width: 50%;
    margin-right: auto;
}

</style>
"""

# CSS Styling
st.write(chat_bubble_css, unsafe_allow_html=True)

# Mock employee data
employees = [
    {
        "name": "Alice",
        "home_office": "Dallas",
        "eligible_airports": ["DFW", "DAL"]
    },
    {
        "name": "Bob",
        "home_office": "San Francisco",
        "eligible_airports": ["SFO", "OAK"]
    },
    {
        "name": "Charlie",
        "home_office": "New York",
        "eligible_airports": ["JFK", "LGA"]
    },
    {
        "name": "Dave",
        "home_office": "Chicago",
        "eligible_airports": ["ORD", "MDW"]
    },
    {
        "name": "Eve",
        "home_office": "Seattle",
        "eligible_airports": ["SEA"]
    }
]

# Mock event data
events = [
    {
        "name": "Sapphire",
        "location": "Orlando",
        "start_date": "2024-06-03 09:00:00",
        "end_date": "2024-06-05 17:00:00"
    },
    {
        "name": "TechEd",
        "location": "Las Vegas",
        "start_date": "2024-09-20 09:00:00",
        "end_date": "2024-09-22 17:00:00"
    },
    {
        "name": "SuccessConnect",
        "location": "Berlin",
        "start_date": "2024-11-10 09:00:00",
        "end_date": "2024-11-12 17:00:00"
    }
]

# Mock flight data
flights = [
    # Flights to Sapphire (Orlando)
    {"origin": "DFW", "destination": "Orlando", "flight_number": "AA123", "departure_time": "2024-05-31 10:00:00", "arrival_time": "2024-05-31 14:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "DFW", "destination": "Orlando", "flight_number": "AA124", "departure_time": "2024-06-01 12:00:00", "arrival_time": "2024-06-01 16:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "DAL", "destination": "Orlando", "flight_number": "WN789", "departure_time": "2024-06-02 09:00:00", "arrival_time": "2024-06-02 13:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "SFO", "destination": "Orlando", "flight_number": "UA456", "departure_time": "2024-05-31 11:00:00", "arrival_time": "2024-05-31 19:00:00", "airline": "United Airlines", "aircraft_model": "Airbus A320", "seats_left": 160},
    {"origin": "SFO", "destination": "Orlando", "flight_number": "UA457", "departure_time": "2024-06-02 13:00:00", "arrival_time": "2024-06-02 21:00:00", "airline": "United Airlines", "aircraft_model": "Airbus A320", "seats_left": 160},
    {"origin": "JFK", "destination": "Orlando", "flight_number": "DL789", "departure_time": "2024-05-31 09:00:00", "arrival_time": "2024-05-31 13:00:00", "airline": "Delta Air Lines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "JFK", "destination": "Orlando", "flight_number": "DL790", "departure_time": "2024-06-01 11:00:00", "arrival_time": "2024-06-01 15:00:00", "airline": "Delta Air Lines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "LGA", "destination": "Orlando", "flight_number": "AA234", "departure_time": "2024-06-02 10:00:00", "arrival_time": "2024-06-02 14:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "ORD", "destination": "Orlando", "flight_number": "AA101", "departure_time": "2024-05-31 12:00:00", "arrival_time": "2024-05-31 16:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "ORD", "destination": "Orlando", "flight_number": "AA102", "departure_time": "2024-06-01 14:00:00", "arrival_time": "2024-06-01 18:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "MDW", "destination": "Orlando", "flight_number": "WN123", "departure_time": "2024-06-02 08:00:00", "arrival_time": "2024-06-02 12:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "SEA", "destination": "Orlando", "flight_number": "AS202", "departure_time": "2024-06-01 08:00:00", "arrival_time": "2024-06-01 16:00:00", "airline": "Alaska Airlines", "aircraft_model": "Airbus A320", "seats_left": 160},
    {"origin": "SEA", "destination": "Orlando", "flight_number": "AS203", "departure_time": "2024-06-02 10:00:00", "arrival_time": "2024-06-02 18:00:00", "airline": "Alaska Airlines", "aircraft_model": "Airbus A320", "seats_left": 160},
    # Flights from Sapphire (Orlando)
    {"origin": "Orlando", "destination": "DFW", "flight_number": "AA125", "departure_time": "2024-06-05 20:00:00", "arrival_time": "2024-06-05 22:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 120},
    {"origin": "Orlando", "destination": "DAL", "flight_number": "WN790", "departure_time": "2024-06-06 10:00:00", "arrival_time": "2024-06-06 12:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 130},
    {"origin": "Orlando", "destination": "SFO", "flight_number": "UA458", "departure_time": "2024-06-06 09:00:00", "arrival_time": "2024-06-06 18:00:00", "airline": "United Airlines", "aircraft_model": "Airbus A320", "seats_left": 150},
    {"origin": "Orlando", "destination": "JFK", "flight_number": "DL791", "departure_time": "2024-06-06 14:00:00", "arrival_time": "2024-06-06 18:00:00", "airline": "Delta Air Lines", "aircraft_model": "Boeing 757", "seats_left": 140},
    {"origin": "Orlando", "destination": "LGA", "flight_number": "AA235", "departure_time": "2024-06-06 16:00:00", "arrival_time": "2024-06-06 20:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 120},
    {"origin": "Orlando", "destination": "ORD", "flight_number": "AA103", "departure_time": "2024-06-06 18:00:00", "arrival_time": "2024-06-06 22:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 130},
    {"origin": "Orlando", "destination": "MDW", "flight_number": "WN124", "departure_time": "2024-06-06 13:00:00", "arrival_time": "2024-06-06 17:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "Orlando", "destination": "SEA", "flight_number": "AS204", "departure_time": "2024-06-06 12:00:00", "arrival_time": "2024-06-06 20:00:00", "airline": "Alaska Airlines", "aircraft_model": "Airbus A320", "seats_left": 150},



    # Flights to TechEd (Las Vegas)
    {"origin": "DFW", "destination": "Las Vegas", "flight_number": "BC561", "departure_time": "2024-09-18 10:00:00", "arrival_time": "2024-09-18 14:00:00", "airline": "Blue Airlines", "aircraft_model": "Airbus A320", "seats_left": 180},
    {"origin": "DFW", "destination": "Las Vegas", "flight_number": "BC562", "departure_time": "2024-09-19 12:00:00", "arrival_time": "2024-09-19 16:00:00", "airline": "Blue Airlines", "aircraft_model": "Airbus A320", "seats_left": 180},
    {"origin": "DAL", "destination": "Las Vegas", "flight_number": "WN654", "departure_time": "2024-09-19 11:00:00", "arrival_time": "2024-09-19 15:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "SFO", "destination": "Las Vegas", "flight_number": "GH367", "departure_time": "2024-09-18 11:00:00", "arrival_time": "2024-09-18 15:00:00", "airline": "Golden Horizon Airlines", "aircraft_model": "Boeing 737", "seats_left": 160},
    {"origin": "SFO", "destination": "Las Vegas", "flight_number": "GH368", "departure_time": "2024-09-19 13:00:00", "arrival_time": "2024-09-19 17:00:00", "airline": "Golden Horizon Airlines", "aircraft_model": "Boeing 737", "seats_left": 160},
    {"origin": "OAK", "destination": "Las Vegas", "flight_number": "WN567", "departure_time": "2024-09-19 09:00:00", "arrival_time": "2024-09-19 13:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "JFK", "destination": "Las Vegas", "flight_number": "DV722", "departure_time": "2024-09-18 09:00:00", "arrival_time": "2024-09-18 13:00:00", "airline": "Delta Airlines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "JFK", "destination": "Las Vegas", "flight_number": "DV723", "departure_time": "2024-09-19 11:00:00", "arrival_time": "2024-09-19 15:00:00", "airline": "Delta Airlines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "LGA", "destination": "Las Vegas", "flight_number": "AA567", "departure_time": "2024-09-19 12:00:00", "arrival_time": "2024-09-19 16:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "ORD", "destination": "Las Vegas", "flight_number": "HS671", "departure_time": "2024-09-18 12:00:00", "arrival_time": "2024-09-18 16:00:00", "airline": "High Skies Airlines", "aircraft_model": "Boeing 737", "seats_left": 160},
    {"origin": "ORD", "destination": "Las Vegas", "flight_number": "HS672", "departure_time": "2024-09-19 14:00:00", "arrival_time": "2024-09-19 18:00:00", "airline": "High Skies Airlines", "aircraft_model": "Boeing 737", "seats_left": 160},
    {"origin": "MDW", "destination": "Las Vegas", "flight_number": "WN321", "departure_time": "2024-09-18 08:00:00", "arrival_time": "2024-09-18 12:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "SEA", "destination": "Las Vegas", "flight_number": "HH666", "departure_time": "2024-09-18 08:00:00", "arrival_time": "2024-09-18 12:00:00", "airline": "Highland Airlines", "aircraft_model": "Airbus A320", "seats_left": 170},
    {"origin": "SEA", "destination": "Las Vegas", "flight_number": "HH667", "departure_time": "2024-09-19 10:00:00", "arrival_time": "2024-09-19 14:00:00", "airline": "Highland Airlines", "aircraft_model": "Airbus A320", "seats_left": 170},
    # Flights from TechEd (Las Vegas)
    {"origin": "Las Vegas", "destination": "DFW", "flight_number": "BC563", "departure_time": "2024-09-22 19:30:00", "arrival_time": "2024-09-22 23:30:00", "airline": "Blue Airlines", "aircraft_model": "Airbus A320", "seats_left": 130},
    {"origin": "Las Vegas", "destination": "DAL", "flight_number": "WN655", "departure_time": "2024-09-23 15:00:00", "arrival_time": "2024-09-23 19:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "Las Vegas", "destination": "SFO", "flight_number": "GH369", "departure_time": "2024-09-23 10:00:00", "arrival_time": "2024-09-23 14:00:00", "airline": "Golden Horizon Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "Las Vegas", "destination": "OAK", "flight_number": "WN568", "departure_time": "2024-09-23 14:00:00", "arrival_time": "2024-09-23 18:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "Las Vegas", "destination": "JFK", "flight_number": "DV724", "departure_time": "2024-09-23 14:00:00", "arrival_time": "2024-09-23 18:00:00", "airline": "Delta Airlines", "aircraft_model": "Airbus A321", "seats_left": 160},
    {"origin": "Las Vegas", "destination": "LGA", "flight_number": "AA568", "departure_time": "2024-09-23 10:00:00", "arrival_time": "2024-09-23 14:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 737", "seats_left": 130},
    {"origin": "Las Vegas", "destination": "ORD", "flight_number": "HS673", "departure_time": "2024-09-23 16:00:00", "arrival_time": "2024-09-23 20:00:00", "airline": "High Skies Airlines", "aircraft_model": "Boeing 737", "seats_left": 140},
    {"origin": "Las Vegas", "destination": "MDW", "flight_number": "WN322", "departure_time": "2024-09-23 13:00:00", "arrival_time": "2024-09-23 17:00:00", "airline": "Southwest Airlines", "aircraft_model": "Boeing 737", "seats_left": 150},
    {"origin": "Las Vegas", "destination": "SEA", "flight_number": "HH668", "departure_time": "2024-09-23 12:00:00", "arrival_time": "2024-09-23 16:00:00", "airline": "Highland Airlines", "aircraft_model": "Airbus A320", "seats_left": 160},



    # Flights to SuccessConnect (Berlin)
    {"origin": "DFW", "destination": "Berlin", "flight_number": "AA900", "departure_time": "2024-11-08 10:00:00", "arrival_time": "2024-11-08 22:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 787", "seats_left": 220},
    {"origin": "DFW", "destination": "Berlin", "flight_number": "AA901", "departure_time": "2024-11-09 12:00:00", "arrival_time": "2024-11-09 23:59:00", "airline": "American Airlines", "aircraft_model": "Boeing 787", "seats_left": 220},
    {"origin": "DAL", "destination": "Berlin", "flight_number": "LH123", "departure_time": "2024-11-08 09:00:00", "arrival_time": "2024-11-08 21:00:00", "airline": "Lufthansa", "aircraft_model": "Airbus A330", "seats_left": 200},
    {"origin": "SFO", "destination": "Berlin", "flight_number": "UA700", "departure_time": "2024-11-08 11:00:00", "arrival_time": "2024-11-09 07:00:00", "airline": "United Airlines", "aircraft_model": "Boeing 777", "seats_left": 250},
    {"origin": "SFO", "destination": "Berlin", "flight_number": "UA701", "departure_time": "2024-11-09 13:00:00", "arrival_time": "2024-11-10 09:00:00", "airline": "United Airlines", "aircraft_model": "Boeing 777", "seats_left": 250},
    {"origin": "OAK", "destination": "Berlin", "flight_number": "BA256", "departure_time": "2024-11-08 10:00:00", "arrival_time": "2024-11-09 06:00:00", "airline": "British Airways", "aircraft_model": "Airbus A350", "seats_left": 300},
    {"origin": "JFK", "destination": "Berlin", "flight_number": "DL300", "departure_time": "2024-11-08 10:00:00", "arrival_time": "2024-11-09 04:00:00", "airline": "Delta Airlines", "aircraft_model": "Boeing 787", "seats_left": 220},
    {"origin": "JFK", "destination": "Berlin", "flight_number": "DL301", "departure_time": "2024-11-09 12:00:00", "arrival_time": "2024-11-10 06:00:00", "airline": "Delta Airlines", "aircraft_model": "Boeing 787", "seats_left": 220},
    {"origin": "LGA", "destination": "Berlin", "flight_number": "AA654", "departure_time": "2024-11-08 14:00:00", "arrival_time": "2024-11-09 08:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 787", "seats_left": 220},
    {"origin": "ORD", "destination": "Berlin", "flight_number": "AA400", "departure_time": "2024-11-08 12:00:00", "arrival_time": "2024-11-09 02:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 787", "seats_left": 220},
    {"origin": "ORD", "destination": "Berlin", "flight_number": "AA401", "departure_time": "2024-11-09 14:00:00", "arrival_time": "2024-11-10 04:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 787", "seats_left": 220},
    {"origin": "MDW", "destination": "Berlin", "flight_number": "UA123", "departure_time": "2024-11-08 09:00:00", "arrival_time": "2024-11-08 23:00:00", "airline": "United Airlines", "aircraft_model": "Boeing 777", "seats_left": 250},
    {"origin": "SEA", "destination": "Berlin", "flight_number": "LH789", "departure_time": "2024-11-08 08:00:00", "arrival_time": "2024-11-09 06:00:00", "airline": "Lufthansa", "aircraft_model": "Airbus A330", "seats_left": 200},
    {"origin": "SEA", "destination": "Berlin", "flight_number": "LH790", "departure_time": "2024-11-09 10:00:00", "arrival_time": "2024-11-10 08:00:00", "airline": "Lufthansa", "aircraft_model": "Airbus A330", "seats_left": 200},
    # Flights from SuccessConnect (Berlin)
    {"origin": "Berlin", "destination": "DFW", "flight_number": "AA902", "departure_time": "2024-11-13 10:00:00", "arrival_time": "2024-11-13 22:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 777", "seats_left": 200},
    {"origin": "Berlin", "destination": "DAL", "flight_number": "LH124", "departure_time": "2024-11-13 09:00:00", "arrival_time": "2024-11-13 21:00:00", "airline": "Lufthansa", "aircraft_model": "Airbus A350", "seats_left": 220},
    {"origin": "Berlin", "destination": "SFO", "flight_number": "UA702", "departure_time": "2024-11-13 11:00:00", "arrival_time": "2024-11-14 07:00:00", "airline": "United Airlines", "aircraft_model": "Boeing 787", "seats_left": 180},
    {"origin": "Berlin", "destination": "OAK", "flight_number": "BA257", "departure_time": "2024-11-13 10:00:00", "arrival_time": "2024-11-14 06:00:00", "airline": "British Airways", "aircraft_model": "Airbus A330", "seats_left": 190},
    {"origin": "Berlin", "destination": "JFK", "flight_number": "DL302", "departure_time": "2024-11-13 10:00:00", "arrival_time": "2024-11-14 04:00:00", "airline": "Delta Air Lines", "aircraft_model": "Boeing 767", "seats_left": 170},
    {"origin": "Berlin", "destination": "LGA", "flight_number": "AA655", "departure_time": "2024-11-13 14:00:00", "arrival_time": "2024-11-14 08:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 777", "seats_left": 200},
    {"origin": "Berlin", "destination": "ORD", "flight_number": "AA402", "departure_time": "2024-11-13 12:00:00", "arrival_time": "2024-11-14 02:00:00", "airline": "American Airlines", "aircraft_model": "Boeing 777", "seats_left": 190},
    {"origin": "Berlin", "destination": "MDW", "flight_number": "UA124", "departure_time": "2024-11-13 09:00:00", "arrival_time": "2024-11-13 23:00:00", "airline": "United Airlines", "aircraft_model": "Boeing 787", "seats_left": 180},
    {"origin": "Berlin", "destination": "SEA", "flight_number": "LH791", "departure_time": "2024-11-13 08:00:00", "arrival_time": "2024-11-14 06:00:00", "airline": "Lufthansa", "aircraft_model": "Airbus A350", "seats_left": 220}
    ]

# Mock accommodation data
accommodations = [
    {
        "event": "Sapphire",
        "location": "Orlando",
        "hotels": [
            {
                "name": "Hyatt Regency Orlando International Airport",
                "address": "9300 Jeff Fuqua Blvd, Orlando, FL",
                "distance_from_airport": "0.1 miles",
                "distance_from_venue": "15 miles",
                "proximity": "Airport",
                "Average Price/night": "$100",
                "contact": {
                    "number": "+1 407-825-1234",
                    "email": "info@hyattorlando.com"
                }
            },
            {
                "name": "Rosen Centre Hotel",
                "address": "9840 International Dr, Orlando, FL",
                "distance_from_airport": "13 miles",
                "distance_from_venue": "0.3 miles",
                "proximity": "Venue",
                "Average Price/night": "$150",
                "contact": {
                    "number": "+1 407-996-9840",
                    "email": "reservations@rosencentre.com"
                }
            }
        ]
    },
    {
        "event": "TechEd",
        "location": "Las Vegas",
        "hotels": [
            {
                "name": "Best Western McCarran Inn",
                "address": "4970 Paradise Rd, Las Vegas, NV",
                "distance_from_airport": "1.2 miles",
                "distance_from_venue": "2.5 miles",
                "proximity": "Airport",
                "Average Price/night": "$80",
                "contact": {
                    "number": "+1 702-798-5530",
                    "email": "info@mccarraninn.com"
                }
            },
            {
                "name": "MGM Grand",
                "address": "3799 S Las Vegas Blvd, Las Vegas, NV",
                "distance_from_airport": "2.5 miles",
                "distance_from_venue": "0.5 miles",
                "proximity": "Venue",
                "Average Price/night": "$120",
                "contact": {
                    "number": "+1 877-880-0880",
                    "email": "reservations@mgmgrand.com"
                }
            }
        ]
    },
    {
        "event": "SuccessConnect",
        "location": "Berlin",
        "hotels": [
            {
                "name": "Motel One Berlin-Airport",
                "address": "Kurt-Schumacher-Damm 202, 13405 Berlin, Germany",
                "distance_from_airport": "1 km",
                "distance_from_venue": "9 km",
                "proximity": "Airport",
                "Average Price/night": "$120",
                "contact": {
                    "number": "+49 30 417240",
                    "email": "info@berlin-airport.motel-one.com"
                }
            },
            {
                "name": "Hotel Adlon Kempinski",
                "address": "Unter den Linden 77, 10117 Berlin, Germany",
                "distance_from_airport": "8 km",
                "distance_from_venue": "0.5 km",
                "proximity": "Venue",
                "Average Price/night": "$140",
                "contact": {
                    "number": "+49 30 22610",
                    "email": "reservations.adlon@kempinski.com"
                }
            }
        ]
    }
]

# Defining Travel Agent:
class TravelAgent:
    def book_flight(self, employee, events, return_trip=False):
        flights_info = {}
        for event in events:
            logging.info(f"Booking flights for event: {event['name']}")
            available_flights = []
            for i in employee['eligible_airports']:
                eligible_airport = i
                for f in flights:
                    if f['origin'] == eligible_airport and f['destination'] == event['location']:
                        available_flights.append(f)
                        logging.info(f"Found flight: {f['flight_number']} from {eligible_airport} to {event['location']}")
            if return_trip:
                for f in flights:
                    if f['origin'] == event['location'] and f['destination'] == eligible_airport:
                        available_flights.append(f)
                        logging.info(f"Found return flight: {f['flight_number']} from {event['location']} to {eligible_airport}")
            flights_info[event['name']] = available_flights
        return flights_info

    def book_accommodation(self, event_name):
        for accommodation in accommodations:
            if accommodation['event'].lower() == event_name.lower():
                return accommodation['hotels']
        return None

class SearchAgent:
    def search_employee(self, employee_name):
        logging.info(f"Searching for employee: {employee_name}")
        for employee in employees:
            if employee['name'].lower() == employee_name.lower():
                logging.info(f"Employee found: {employee_name}")
                return employee
        logging.info(f"Employee not found: {employee_name}")
        return None

    def search_event(self, event_name):
        for event in events:
            if event['name'].lower() == event_name.lower():
                logging.info(f"Event found: {event_name}")
                return event
        return None

# Pulling all the flight detials
def generate_flight_details(available_flights):
    flight_details = ""
    for event_name, flights in available_flights.items():
        if flights:
            flight_details += f"\nFor the {event_name} event:\n"
            for flight in flights:
                flight_details += f"Flight {flight['flight_number']} departing from {flight['origin']} at {flight['departure_time']} and arriving at {flight['arrival_time']}. This is a {flight['aircraft_model']} operated by {flight['airline']} with {flight['seats_left']} seats left\n"
    return flight_details

# Pulling all the  accomodation details
def generate_accommodation_details(accommodation_details):
    accommodation_str = ""
    for event_name, hotels in accommodation_details.items():
        if hotels:
            accommodation_str += f"\nFor the {event_name} event:\n"
            for hotel in hotels:
                accommodation_str += f"Hotel {hotel['name']} located at {hotel['address']}, {hotel['distance_from_airport']} from the airport and {hotel['distance_from_venue']} from the venue. Proximity: {hotel['proximity']}. Contact: {hotel['contact']['number']}, Email: {hotel['contact']['email']}, Price: {hotel['Average Price/night']}\n"
    return accommodation_str

# Instantiating agents
travel_agent = TravelAgent()
search_agent = SearchAgent()

import os
from openai import OpenAI

# OpenAI integration to generate a response using GPT-4-turbo
def generate_response(prompt):
    response = OpenAI(api_key=openai.api_key).chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful SAP travel guide."},
            {"role": "user", "content": prompt}
        ],
        #max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].message.content

def handle_chat_tmp2(query, employee_name, last_query):
    search_agent = SearchAgent()
    travel_agent = TravelAgent()

    # We look for the employee
    employee = search_agent.search_employee(employee_name)
    if not employee:
        prompt = f"User: {query}\nAgent: Sorry, I couldn't find an employee named {employee_name}. Please check the name and try again."
        return generate_response(prompt)

    # Extract event names from the query
    tokens = last_query.lower().split()
    requested_events = []
    for token in tokens:
        event = search_agent.search_event(token)
        if event:
            requested_events.append(event)

    if not requested_events:
        prompt = f"""User Details: [Name:{employee['name']},Home office: {employee['home_office']},Eligible Airports: {employee['eligible_airports']}] 
        User: {query}\nAgent: I am your SAP travel guide. How can I assist you today?\n
        The latest query always has the maximum weightage and all the previous queries and responses are for context"""
        general_response = generate_response(prompt)
        if "assist" in general_response or "help" in general_response:
            prompt += "\nAgent: I can help you book flights and accommodations to SAP events. Which of the following SAP events are you planning to visit 'Sapphire', 'TechEd', or 'SuccessConnect'?"
            return generate_response(prompt)
        return general_response

    # Book the flights for both one-way and return trip
    available_flights_one_way = travel_agent.book_flight(employee, requested_events)
    available_flights_round_trip = travel_agent.book_flight(employee, requested_events, return_trip=True)
    
    # Get accommodation details
    accommodation_details = {}
    for event in requested_events:
        hotels = travel_agent.book_accommodation(event['name'])
        if hotels:
            accommodation_details[event['name']] = hotels

    # Generate a response using GPT-4 Turbo with the available flights and accommodations
    flight_details_one_way = generate_flight_details(available_flights_one_way)
    flight_details_round_trip = generate_flight_details(available_flights_round_trip)

    # Generate accommodation details
    accommodation_details_str = generate_accommodation_details(accommodation_details)

    prompt = f"""
    User: {query}
    Agent: Sure, I can help with that. Let's see what flights and accommodations are available for one-way and round-trip.
    If the user asks to fly from a different location/airport than their city of home office, tell them that you are only allowed to select from the city your home office.
    For One-Way Flights:
    {flight_details_one_way}

    For Round-Trip Flights:
    {flight_details_round_trip}

    For Accommodations:
    {accommodation_details_str}

    Provide a response based on the following statements:
    Please choose one of the flights and/or accommodations or provide additional preferences.
    For every prompt, parse through the below information and answer user about their location/flights/accommodations and employee details.
    
    Also, if a users asks you to book a flight, tell them that you will book it and email the details.
    """

    return generate_response(prompt)
##########################################################################
import logging
from datetime import datetime

# Set up logging function
def setup_logging(log_file_name):
    
    # Set up logging to write messages to the specified log file
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    # Exclude API call logs
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    root_logger.addHandler(file_handler)

# Set up logging configuration
log_format = '%(asctime)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
def submit():
    if st.session_state.first_run:
        logging.info(f"New chat session initiated for employee: {st.session_state.employee_name}")
    query = st.session_state.query_input
    if query:
        if query.lower() == "exit":
            st.session_state.chat_history = []  # Clear chat history
            st.session_state.chat_active = False  # End chat session
            # Log chat session end
            logging.info(f"Chat session ended for employee: {st.session_state.employee_name}")
            st.session_state.employee_input=''
            st.session_state.pop('employee_name') 
            st.session_state.pop('current_employee')
            st.session_state.full_query=''
            st.session_state.first_run=False
        else:
            if 'full_query' not in st.session_state:
                st.session_state.full_query = f"User's Query 1: {query}\n"
            else:
                st.session_state.full_query += f"User's Query {len(st.session_state.chat_history) + 1}: {query}\n"
            
            response = handle_chat_tmp2(st.session_state.full_query, st.session_state.employee_name, query)
            
            st.session_state.chat_history.append((query, response))
            
            st.session_state.full_query += f"Agent: {response}\n"
            
            # Log chat messages
            logging.info(f"{st.session_state.employee_name.capitalize()}'s Query: {query}")
            logging.info(f"SAP Agent's Response: {response}")
            st.session_state.query_input = ''

def main():
    st.sidebar.title("Chat Login")
    with st.sidebar:
        st.write("Hey there! I am here to help you setup your travel itinerary for SAP events!")
        employee_name = st.text_input("Please enter your SAP Employee Name:", key = 'employee_input')
        
    # Initialize session state variables
    if 'chat_active' not in st.session_state:
        st.session_state.chat_active = False
    if 'unauthorized' not in st.session_state:
        st.session_state.unauthorized = False
    if 'first_run' not in st.session_state:
        st.session_state.first_run = True

    if not st.session_state.chat_active and employee_name:
        employee_exists = False
        for employee in employees:
            if employee['name'].lower() == employee_name.lower():
                employee_exists = True
                break

        if employee_exists:
            st.session_state.employee_name = employee_name
            st.session_state.chat_active = True
            st.session_state.unauthorized = False
            # Generate unique log file name based on employee name and timestamp
            log_file_name = f"chat_log_{employee_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            # Set up logging for this session
            setup_logging(log_file_name)
            #logging.info(f"New chat session initiated for employee: {employee_name}")
        else:
            st.session_state.unauthorized = True
    if st.session_state.unauthorized:
        st.session_state.first_run = True
        st.write("Unauthorized User")

    if st.session_state.chat_active:
        # Clear chat history when a new valid employee starts chatting
        if 'current_employee' not in st.session_state or st.session_state.current_employee != st.session_state.employee_name:
            st.session_state.chat_history = []
            st.session_state.current_employee = st.session_state.employee_name

        # Capture the query input from the query bar
        query = st.text_input("Hi " + st.session_state.employee_name.capitalize() + "! How may I assist you?", key='query_input', on_change=submit)
        st.markdown("""
        <style>
            .small-text {
                font-size: 12px;
            }
        </style>
        """, unsafe_allow_html=True)

        st.write("<span class='small-text'>Enter 'exit' to end chat session.</span>", unsafe_allow_html=True, key='chat_instruction')
        st.button("Submit", on_click=submit)
    if not st.session_state.chat_active and not st.session_state.first_run:
        st.write("Chat session ended.")
    elif 'chat_history' in st.session_state:
        # Display the chat history
        for user_msg, bot_msg in reversed(st.session_state.chat_history):
            st.markdown(f'<div class="chat-bubble user-bubble"><p><b>{st.session_state.employee_name.capitalize()}:</b></p>{user_msg}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble agent-bubble"><p><b>SAP Travel Agent:</b></p>{bot_msg}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
