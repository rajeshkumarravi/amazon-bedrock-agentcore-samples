import os
import json
from pathlib import Path

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

if not trace.get_tracer_provider().__class__.__name__ == "TracerProvider":
    pass
else:
    tracer_provider = TracerProvider()
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if otlp_endpoint:
        tracer_provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces"))
        )
    trace.set_tracer_provider(tracer_provider)

from openinference.instrumentation.google_adk import GoogleADKInstrumentor
GoogleADKInstrumentor().instrument()

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model.load import load_model

app = BedrockAgentCoreApp()
log = app.logger

APP_NAME = "googleOInfTravelContainer"
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
MODEL_ID = f"openai/{BEDROCK_MODEL_ID}"

_data_path = Path(__file__).parent / "travel_data.json"
with open(_data_path) as f:
    TRAVEL_DATA = json.load(f)


# --- Travel Tools ---

def search_flights(origin: str, destination: str, date: str) -> dict:
    """Search for available flights between cities.

    Args:
        origin: Origin airport code (e.g., SEA, NYC, LAX, MIA).
        destination: Destination airport code.
        date: Travel date (e.g., 2025-03-15).

    Returns:
        dict: Flight search results.
    """
    route = f"{origin.upper()}-{destination.upper()}"
    flights = TRAVEL_DATA["flights"].get(route, [])
    return {"origin": origin, "destination": destination, "date": date, "flights": flights}


def book_flight(flight_id: str) -> dict:
    """Book a specific flight by ID.

    Args:
        flight_id: The flight ID to book (e.g., AA101).

    Returns:
        dict: Booking confirmation.
    """
    return {"booking_id": f"FB{flight_id}", "flight_id": flight_id, "status": "confirmed"}


def search_hotels(city: str, checkin: str, checkout: str) -> dict:
    """Search for available hotels in a city.

    Args:
        city: City airport code (e.g., NYC, LAX, SEA, MIA).
        checkin: Check-in date.
        checkout: Check-out date.

    Returns:
        dict: Hotel search results.
    """
    hotels = TRAVEL_DATA["hotels"].get(city.upper(), [])
    return {"city": city, "checkin": checkin, "checkout": checkout, "hotels": hotels}


def book_hotel(hotel_id: str, checkin: str, checkout: str) -> dict:
    """Book a specific hotel by ID.

    Args:
        hotel_id: The hotel ID to book.
        checkin: Check-in date.
        checkout: Check-out date.

    Returns:
        dict: Booking confirmation.
    """
    return {"booking_id": f"HB{hotel_id}", "hotel_id": hotel_id, "checkin": checkin, "checkout": checkout, "status": "confirmed"}


def search_activities(city: str) -> dict:
    """Search for activities in a city.

    Args:
        city: City airport code (e.g., NYC, LAX, SEA, MIA).

    Returns:
        dict: Available activities.
    """
    activities = TRAVEL_DATA["activities"].get(city.upper(), [])
    return {"city": city, "activities": activities}


def book_activity(activity_id: str, date: str) -> dict:
    """Book a specific activity by ID.

    Args:
        activity_id: The activity ID to book.
        date: Date for the activity.

    Returns:
        dict: Booking confirmation.
    """
    return {"booking_id": f"AB{activity_id}", "activity_id": activity_id, "date": date, "status": "confirmed"}


tools = [search_flights, book_flight, search_hotels, book_hotel, search_activities, book_activity]

AGENT_INSTRUCTION = """You are a travel planning assistant. Help users plan trips by:
- Searching and booking flights
- Finding and booking hotels
- Suggesting and booking activities

IMPORTANT: All data is indexed by airport/city codes (e.g., NYC, LAX, SEA, MIA).
Always use the airport code when calling tools, not the full city name.

Remember context from the conversation - destinations, dates, preferences, and previous bookings.
When user refers to previous choices (e.g., "book the cheapest one", "the second hotel"), use conversation history.
"""

_credentials_loaded = False


def ensure_credentials_loaded():
    global _credentials_loaded
    if not _credentials_loaded:
        load_model()
        _credentials_loaded = True


agent = Agent(
    model=MODEL_ID,
    name="googleOInfTravelContainer",
    description="Travel planning assistant that searches and books flights, hotels, and activities",
    instruction=AGENT_INSTRUCTION,
    tools=tools,
)


async def setup_session_and_runner(user_id, session_id):
    ensure_credentials_loaded()
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
    return session, runner


async def call_agent_async(query, user_id, session_id):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner(user_id, session_id)
    events = runner.run_async(
        user_id=user_id, session_id=session.id, new_message=content
    )

    final_response = None
    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text

    return final_response


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking travel agent...")

    prompt = payload.get("prompt", "What can you help me with?")
    session_id = getattr(context, "session_id", "default_session")
    user_id = payload.get("user_id", "default_user")

    result = await call_agent_async(prompt, user_id, session_id)
    return {"result": result}


if __name__ == "__main__":
    app.run()
