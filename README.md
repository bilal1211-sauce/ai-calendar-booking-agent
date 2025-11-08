# AI Calendar Booking Agent 🤖📅

An intelligent AI-powered agent that books appointments in Google Calendar using natural language. Just describe your appointment in plain English, and the AI handles the rest!

## ✨ Features

- 🧠 **Natural Language Processing** - No structured forms needed
- 📅 **Google Calendar Integration** - Direct integration via Pipedream
- 👥 **Automatic Invitations** - Sends calendar invites to attendees
- ⏰ **Smart Defaults** - Assumes reasonable values (1-hour duration, 9am if no time)
- 🔄 **Real-time Booking** - Creates events instantly with confirmation

## 🚀 Quick Start

### Option 1: Deploy on CodeWords (Recommended)

1. **Visit CodeWords**: [https://codewords.agemo.ai](https://codewords.agemo.ai)

2. **Connect Google Calendar**:
   - Visit [CodeWords Integrations](https://codewords.agemo.ai/account/integrations)
   - Search for "Google Calendar"
   - Click "Connect" and authorize access

3. **Deploy the service**:
   - Create a new service
   - Upload `ai_calendar_booking_agent.py`
   - Deploy!

4. **Start booking appointments**!

### Option 2: Run Locally (Development)

#### Prerequisites
- Python 3.11
- OpenAI API key
- Google Calendar API credentials
- CodeWords account (for Pipedream integration)

#### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bilal1211-sauce/ai-calendar-booking-agent.git
   cd ai-calendar-booking-agent
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run the service**:
   ```bash
   python ai_calendar_booking_agent.py
   ```

6. **Test the API**:
   ```bash
   curl -X POST http://localhost:8000/ \
     -H "Content-Type: application/json" \
     -d '{"booking_request": "Schedule a dentist appointment on Friday at 3pm"}'
   ```

## 📖 Usage Examples

### Simple Appointment
```
"Book a dentist appointment on Friday at 3pm"
```

### Meeting with Attendees
```
"Schedule a meeting with sarah@company.com and john@company.com tomorrow at 2pm to discuss Q1 budget"
```

### Call with Duration
```
"Book a 30-minute call with the CEO next Tuesday at 10am"
```

### All-day Event
```
"Create an all-day event called 'Conference' on November 15th"
```

## 🔧 API Documentation

### Endpoint: `POST /`

**Request Body:**
```json
{
  "booking_request": "Schedule a meeting with sarah@company.com tomorrow at 3pm"
}
```

**Response:**
```json
{
  "success": true,
  "message": "✅ Appointment booked successfully! 'Meeting with Sarah' scheduled for 2025-11-09T15:00:00",
  "event_details": {
    "id": "event_id_123",
    "htmlLink": "https://www.google.com/calendar/event?eid=...",
    "summary": "Meeting with Sarah",
    "start": {"dateTime": "2025-11-09T15:00:00Z"},
    "end": {"dateTime": "2025-11-09T16:00:00Z"}
  },
  "extracted_info": {
    "title": "Meeting with Sarah",
    "start_datetime": "2025-11-09T15:00:00",
    "end_datetime": "2025-11-09T16:00:00",
    "attendee_emails": ["sarah@company.com"],
    "description": null
  }
}
```

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Server port (default: 8000) | No |
| `LOGLEVEL` | Logging level (INFO, DEBUG) | No |
| `CODEWORDS_API_KEY` | CodeWords API key for service-to-service calls | Yes* |
| `CODEWORDS_RUNTIME_URI` | CodeWords runtime endpoint | Yes* |
| `PIPEDREAM_GOOGLE_CALENDAR_ACCESS` | Google Calendar OAuth token via Pipedream | Yes |
| `OPENAI_API_KEY` | OpenAI API key (auto-provided by CodeWords) | Yes* |

*Automatically provided when deployed on CodeWords

## 🏗️ Architecture

```
User Input (Natural Language)
    ↓
AI Extraction (GPT-4o-mini)
    ↓
Structured Appointment Data
    ↓
Google Calendar API (via Pipedream)
    ↓
Calendar Event Created ✅
```

## 🔄 Workflow Steps

1. **Extract Details** - AI parses natural language to extract:
   - Event title
   - Start date/time
   - End date/time
   - Attendee emails
   - Description

2. **Create Event** - Calls Google Calendar API with:
   - RFC3339 formatted timestamps
   - Attendee list for invitations
   - Event metadata

3. **Confirm** - Returns structured response with event details

## 🛠️ Technologies

- **FastAPI** - Modern async web framework
- **OpenAI GPT-4o-mini** - Natural language understanding
- **Google Calendar API** - Calendar event management (via Pipedream)
- **CodeWords Platform** - Serverless deployment & orchestration
- **Python 3.11** - Core runtime

## 📝 Development

### Running Tests
```bash
# Test the API endpoint
python test_booking_agent.py
```

### Project Structure
```
ai-calendar-booking-agent/
├── ai_calendar_booking_agent.py   # Main service file
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── LICENSE                         # MIT License
└── test_booking_agent.py          # Test script (optional)
```

## 🚢 Deployment on CodeWords

Your deployed service is available at:
```
https://codewords.agemo.ai/run/ai_calendar_booking_agent_c74191e6
```

## 🎯 Future Enhancements

- [ ] Add webhook support for automatic triggering
- [ ] Integrate with Slack/WhatsApp for messaging-based booking
- [ ] Support recurring events (daily, weekly, monthly)
- [ ] Add timezone detection and conversion
- [ ] Calendar conflict detection
- [ ] Multi-calendar support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **CodeWords Documentation**: [https://codewords.agemo.ai](https://codewords.agemo.ai)
- **Issues**: Open an issue on GitHub
- **Questions**: Contact via CodeWords platform

---

**Built with ❤️ using [CodeWords](https://codewords.agemo.ai)**
