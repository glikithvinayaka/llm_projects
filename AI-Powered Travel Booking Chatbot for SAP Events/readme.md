# SAP Travel Assistant - Offline Coding Challenge

## Project Overview
This project is an offline coding challenge that tasks with creating a chat interface using an agent framework, such as Autogen, along with mocked data and APIs. The primary objective is to facilitate SAP employees in booking round-trip flights for any SAP event through a chat interface. The project showcases the ability to handle complex queries, manage state, and provide a user-friendly interaction experience.

## Key Features
1. Natural language interaction
2. Chat-based Travel Booking: Users can book flights and accommodations for SAP events via a conversational interface.
3. Multi-Agent System:
   - Travel Agent: Manages travel-related tasks.
   - Search Agent: Retrieves SAP internal information.
4. Employee Authentication: Verifies user identity against a predefined list.
5. Event-specific Queries: Handles queries for various SAP events like Sapphire, TechEd, and SuccessConnect.
6. Multi-event support
7. Dynamic Flight Options: Offers multiple flight options based on the user's home office.
8. Round-Trip Booking: Supports both one-way and round-trip flight bookings.
9. Accommodation Suggestions: Provides hotel options near event venues and airports.
10. Real-time Chat History: Displays a scrollable, visually appealing chat history.
11. Session Management: Tracks and manages user sessions.
12. Error Handling: Gracefully handles unauthorized access.
13. Logging: Records chat interactions for audit purposes.

## Technical Stack
- **Framework**: Streamlit for the frontend
- **Language**: Python
- **AI Model**: GPT-4-turbo from OpenAI
- **Data Storage**: Python lists and dictionaries (mocked data)
- **Styling**: CSS for chat bubble styling

## Project Structure
  - `SAP_Chatbot.py`: Main application file containing all the code.
  - Imports and global variables
  - Mocked data (employees, events, flights, accommodations)
  - Agent classes (`TravelAgent`, `SearchAgent`)
  - Helper functions for data generation and response handling
  - OpenAI API integration
  - Streamlit UI components and logic
  - Main function and application flow

## Setup and Installation
1. Install dependencies:
   ```
   pip install streamlit openai pandas
   ```
2. Set up the OpenAI API key:
   - openai.api_key = `'sk-proj-sH2dYuFUic0wA7uLUH91T3BlbkFJUemP5XpWqOPGGRxqpf0d'`

## Running the Application
1. Navigate to the project directory.
2. Run the Streamlit app:
   ```
   streamlit run SAP_Chatbot.py
   ```
3. Access the app in your browser. (You'll be greeted by the SAP Travel Assistant interface.)


## Usage Guide: Navigating the SAP Travel Assistant

1. Employee Authentication: Enter the SAP Employee Name in the sidebar.

2. In the sidebar, you'll see a prompt: "Please enter your SAP Employee Name:"
    Enter your name exactly as it appears in our system. 
    # Our database recognizes:

    Alice (Dallas office)
    Bob (San Francisco office)
    Charlie (New York office)
    Dave (Chicago office)
    Eve (Seattle office)

    If authorized, you'll be greeted by the SAP Travel Agent.

3. Understanding Your Travel Privileges

    Each employee is assigned a home office and eligible departure airports:

    Alice: Dallas (DFW, DAL)
    Bob: San Francisco (SFO, OAK)
    Charlie: New York (JFK, LGA)
    Dave: Chicago (ORD, MDW)
    Eve: Seattle (SEA)
    
    You can only book flights departing from your assigned airports.

4. Type your query, e.g., "Book me a flight to Sapphire."

    Type your request in natural language, e.g., "Book me a flight to Sapphire."
    The assistant understands SAP event names:

    Sapphire (Orlando, June 3-5, 2024)
    TechEd (Las Vegas, Sept 20-22, 2024)
    SuccessConnect (Berlin, Nov 10-12, 2024)

    ## Sample Interactions

    # Successful Query:

    User: "Book me a flight to Sapphire."
    Assistant: [Lists flights from the eligible airports]

    # Booking a Return Flight:

    User: "I'd like the round-trip option to Sapphire."
    Assistant: [Confirms booking with flight details]

    # Accommodation Query:

    User: "Any hotel suggestions for SuccessConnect?"
    Assistant: [Lists policy-compliant hotels]

    # Complex Query:

    User: "I'm attending both Sapphire and TechEd. Any flights?"
    Assistant: [Provides options for both events]

5. What to Expect: View flight options and accommodations.

    **Flight Options**: The system will display both one-way and round-trip options.

    **Accommodations**: Details of hotels near the event venue or airport.

6. Provide additional preferences or choose from the options.
7. Continue the conversation to refine your booking.
8. Type "exit" to end the chat session.

## Code Highlights

### Agent Classes
- `TravelAgent`: Books flights and accommodations.
- `SearchAgent`: Retrieves employee and event information.

### OpenAI Integration
```python
def generate_response(prompt):
    response = OpenAI(api_key=openai.api_key).chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful SAP travel guide."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
```

### Dynamic Query Handling
```python
def handle_chat_tmp2(query, employee_name, last_query):
    # ...
    tokens = last_query.lower().split()
    requested_events = []
    for token in tokens:
        event = search_agent.search_event(token)
        if event:
            requested_events.append(event)
    # ...
```

### Session Management
```python
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
        # ...
```

### Logging
```python
def setup_logging(log_file_name):
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    root_logger.addHandler(file_handler)
```

## Future Enhancements
1. Integrate with actual SAP APIs and databases.
2. Add more agents (e.g., Booking Agent, Payment Agent).
3. Add multi-language support.
4. Integrate with calendar APIs for scheduling.
5. Implement voice-based interactions.
6. Add personalized recommendations based on user preferences.
7. Integrate with external services (e.g., weather, local events).
8. Implement end-to-end encryption for security.
9. Add unit tests and integration tests.

## Known Issues
- The application uses mocked data, which may not reflect real-world complexities.
- No persistent storage; session data is lost on restart.
- Limited error handling for complex edge cases.
- No multi-user support; designed for one user at a time.

## Contributors
- Likith Vinayaka Giridhar - Developer

## License
This project is part of an offline coding challenge and is not publicly licensed. All rights are reserved.

## Acknowledgments
- Microsoft Autogen for inspiration on agent frameworks.
- OpenAI for providing the GPT-4-turbo model.
- Streamlit for the user-friendly web app framework.
