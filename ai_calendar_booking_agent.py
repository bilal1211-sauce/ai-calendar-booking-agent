# /// script
# requires-python = "==3.11.*"
# dependencies = [
#   "codewords-client==0.4.0",
#   "fastapi==0.116.1",
#   "openai==1.59.5",
#   "python-dateutil==2.9.0"
# ]
# [tool.env-checker]
# env_vars = [
#   "PORT=8000",
#   "LOGLEVEL=INFO",
#   "CODEWORDS_API_KEY",
#   "CODEWORDS_RUNTIME_URI",
#   "PIPEDREAM_GOOGLE_CALENDAR_ACCESS"
# ]
# ///

from typing import Optional
from datetime import datetime, timedelta
import json

from codewords_client import logger, run_service, AsyncCodewordsClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
from dateutil import parser as date_parser

class ExtractedAppointment(BaseModel):
    """Structured appointment details extracted by AI."""
    title: str = Field(..., description="Meeting/appointment title")
    start_datetime: str = Field(..., description="Start date and time in ISO format")
    end_datetime: str = Field(..., description="End date and time in ISO format")
    attendee_emails: list[str] = Field(default_factory=list, description="List of attendee email addresses")
    description: Optional[str] = Field(None, description="Additional meeting description")

async def extract_appointment_details(booking_request: str) -> ExtractedAppointment:
    """Use AI to extract structured appointment details from natural language."""
    logger.info("STEPLOG START extract_details")
    logger.info("Extracting appointment details from request", request=booking_request)
    
    # Initialize OpenAI client
    openai_client = AsyncOpenAI()
    
    current_time = datetime.now().isoformat()
    
    system_prompt = f"""You are an AI assistant that extracts appointment details from natural language requests.
    
Current date and time: {current_time}
    
Extract the following information:
- title: The meeting/appointment title
- start_datetime: Start date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- end_datetime: End date and time in ISO 8601 format (default to 1 hour after start if not specified)
- attendee_emails: List of email addresses (extract from text if provided, otherwise empty list)
- description: Any additional context or description

Rules:
- Use the current date/time as reference for relative dates ("tomorrow", "next week", etc.)
- If no time is specified, default to 9:00 AM
- If no duration is specified, default to 1 hour
- If no attendees are mentioned, return empty list
- Infer reasonable defaults when information is missing"""
    
    response = await openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": booking_request}
        ],
        response_format=ExtractedAppointment
    )
    
    extracted = response.choices[0].message.parsed
    logger.info("Successfully extracted appointment details", extracted=extracted.model_dump())
    return extracted

async def create_calendar_event(appointment: ExtractedAppointment) -> dict:
    """Create a Google Calendar event using the Pipedream integration."""
    logger.info("STEPLOG START create_event")
    logger.info("Creating calendar event", appointment=appointment.model_dump())
    
    # Format datetimes with timezone indicator for RFC3339 compliance
    start_dt = appointment.start_datetime if appointment.start_datetime.endswith('Z') else f"{appointment.start_datetime}Z"
    end_dt = appointment.end_datetime if appointment.end_datetime.endswith('Z') else f"{appointment.end_datetime}Z"
    
    # Build props for Google Calendar create-event action (detailed mode)
    props = {
        "calendarId": "primary",
        "addType": "detailed",
        "summary": appointment.title,
        "eventStartDate": start_dt,  # RFC3339 format with timezone
        "eventEndDate": end_dt,      # RFC3339 format with timezone
    }
    
    # Add optional properties if present
    if appointment.attendee_emails:
        props["attendees"] = appointment.attendee_emails  # Array of email strings
        props["sendUpdates"] = "all"  # Send invites to attendees
    else:
        props["sendUpdates"] = "none"
    
    if appointment.description:
        props["description"] = appointment.description
    
    async with AsyncCodewordsClient() as client:
        response = await client.run(
            service_id="pipedream",
            inputs={
                "app": "google_calendar",
                "action": "create-event",
                "props": props,
                "dynamic_props_id": "dyp_d6UEwoy"  # From reload-props
            }
        )
        
        result = response.json()
        logger.info("Calendar event created successfully", result=result)
        return result.get("ret", {})

# -------------------------
# FastAPI Application
# -------------------------
app = FastAPI(
    title="AI Calendar Booking Agent",
    description="An AI-powered agent that books appointments in Google Calendar from natural language requests.",
    version="1.0.0",
)

class BookingRequest(BaseModel):
    """Request to book an appointment using natural language."""
    booking_request: str = Field(
        ...,
        description="Natural language description of the appointment to book",
        example="Schedule a meeting with john@example.com tomorrow at 2pm to discuss the Q1 budget"
    )

class BookingResponse(BaseModel):
    """Response after successfully booking an appointment."""
    success: bool = Field(..., description="Whether the booking was successful")
    message: str = Field(..., description="Confirmation message")
    event_details: dict = Field(..., description="Details of the created calendar event")
    extracted_info: dict = Field(..., description="Information extracted by AI from the request")

@app.post("/", response_model=BookingResponse)
async def book_appointment(request: BookingRequest):
    """
    Book an appointment in Google Calendar using natural language.
    
    Provide a natural language description of the appointment you want to book.
    The AI will extract the title, date/time, attendees, and other details,
    then create the event in your Google Calendar.
    
    **Examples:**
    - "Schedule a meeting with sarah@company.com tomorrow at 3pm"
    - "Book a call with John next Tuesday at 10am for 30 minutes"
    - "Set up a team standup every Monday at 9am"
    - "Create an event called 'Dentist appointment' on Friday at 2pm"
    """
    logger.info("Processing appointment booking request", request=request.booking_request)
    
    # Step 1: Extract appointment details using AI
    extracted = await extract_appointment_details(request.booking_request)
    
    # Step 2: Create the calendar event
    event_result = await create_calendar_event(extracted)
    
    # Step 3: Build response
    message = f"✅ Appointment booked successfully! '{extracted.title}' scheduled for {extracted.start_datetime}"
    if extracted.attendee_emails:
        message += f" with {len(extracted.attendee_emails)} attendee(s)"
    
    return BookingResponse(
        success=True,
        message=message,
        event_details=event_result,
        extracted_info=extracted.model_dump()
    )

if __name__ == "__main__":
    run_service(app)
