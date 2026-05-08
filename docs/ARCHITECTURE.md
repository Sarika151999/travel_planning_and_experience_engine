# Architecture Overview - Vibe-Check Travel Agent

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Tailwind)              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  App Component                                       │   │
│  │  ├─ Header (Hero Section)                           │   │
│  │  ├─ PlanningForm (User Input)                        │   │
│  │  └─ ItineraryDisplay (Results)                       │   │
│  └──────────────────────────────────────────────────────┘   │
│          ▼ (API Calls)                                      │
└─────────────────────────────────────────────────────────────┘
                          │
                    HTTP/JSON
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
┌───────▼──────────────────────────────────▼──────┐
│         Backend (Python FastAPI)                 │
│  ┌──────────────────────────────────────────┐   │
│  │ API Routes Layer                         │   │
│  │ ├─ POST /itineraries/generate            │   │
│  │ ├─ GET /itineraries/{id}                 │   │
│  │ └─ GET /itineraries                      │   │
│  └──────────────────────────────────────────┘   │
│          ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │ Services Layer                           │   │
│  │ ├─ ItineraryService (Orchestration)      │   │
│  │ ├─ GeminiService (AI Generation)         │   │
│  │ ├─ MapsService (Location Intelligence)   │   │
│  │ └─ StorageService (GCS Integration)      │   │
│  └──────────────────────────────────────────┘   │
│          ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │ Utils & Middleware                       │   │
│  │ ├─ Validators (Input validation)         │   │
│  │ ├─ Security (Key management)             │   │
│  │ ├─ Logger (Structured logging)           │   │
│  │ ├─ CORS & Error Handlers                 │   │
│  └──────────────────────────────────────────┘   │
└────┬──────────┬──────────┬──────────┬────────────┘
     │          │          │          │
     ▼          ▼          ▼          ▼
  Google    Google Maps  Google    Google
  Gemini    Places API   Cloud     Cloud
  API                    Storage   Logging
```

---

## Component Breakdown

### Frontend Components

**PlanningForm Component**
- Collects user input: destination, budget, energy level, days, interests
- Form validation
- Integrates with Zustand store for state management
- Real-time form updates with sliders and inputs

**ItineraryDisplay Component**
- Renders generated itinerary data
- Shows day-by-day activities with times and costs
- Displays packing tips, transport tips, budget breakdown
- Provides shareable URL

**Header Component**
- Hero section with branding
- Value proposition messaging

### Frontend Services

**api.ts**
- Axios-based HTTP client
- Handles all backend communication
- Error interception and formatting
- Base URL configuration

**store.ts (Zustand)**
- Global state management
- Itinerary state (current, loading, error)
- Generated itineraries history
- Async action handlers

**useItinerary Hook**
- Custom React hook
- Simplifies component integration
- Manages generation lifecycle

---

### Backend API Layer

**Routes** (`app/api/routes.py`)
- `POST /itineraries/generate` - Generate new itinerary
- `GET /itineraries/{id}` - Retrieve saved itinerary
- `GET /itineraries` - List recent itineraries
- `GET /health` - Health check

---

### Backend Services Layer

**ItineraryService** (`app/services/itinerary_service.py`)
- Orchestrates all other services
- Validates requests
- Generates unique IDs
- Enriches with geographic data

**GeminiService** (`app/services/gemini_service.py`)
- Constructs detailed prompts based on user preferences
- Calls Google Gemini API
- Parses JSON responses
- Handles API errors gracefully

**MapsService** (`app/services/maps_service.py`)
- Geocodes destinations and locations
- Searches for places
- Calculates distances
- Implements geographic clustering (Haversine formula)
- Retrieves place details

**StorageService** (`app/services/storage_service.py`)
- Saves itineraries to Google Cloud Storage
- Generates public shareable URLs
- Retrieves saved itineraries
- Deletes old itineraries
- Lists recent itineraries

---

### Backend Utils Layer

**Validators** (`app/utils/validators.py`)
- Validates destination names
- Validates budget amounts
- Validates interests list
- Sanitizes string inputs

**Security** (`app/utils/security.py`)
- Generates unique itinerary IDs
- Hashes sensitive data
- Validates GCS bucket names
- Sanitizes file paths (prevents traversal attacks)

**Logger** (`app/utils/logger.py`)
- Structured logging setup
- Consistent log format
- Multiple log levels

---

### Middleware

**CORS** (`app/middleware/cors.py`)
- Configures cross-origin requests
- Whitelists allowed origins
- Handles preflight requests

**Error Handler** (`app/middleware/error_handler.py`)
- Global exception handling
- Consistent error responses
- Error logging

---

## Data Flow

### 1. User Generates Itinerary

```
Frontend Form Input
    ▼
Zustand Store (setLoading=true)
    ▼
API POST /itineraries/generate
    ▼
Backend: FastAPI Route Handler
    ▼
Request Validation (Pydantic)
    ▼
ItineraryService.generate_and_save_itinerary()
    ▼
GeminiService.generate_itinerary()
    → Build prompt with user preferences
    → Call Google Gemini API
    → Parse JSON response
    ▼
MapsService.geocode_address()
    → Geocode destination
    → Geocode each activity location
    ▼
StorageService.save_itinerary()
    → Serialize itinerary to JSON
    → Upload to Google Cloud Storage
    → Generate public shareable URL
    ▼
Return ItineraryResponse
    ▼
Zustand Store (setItinerary, setLoading=false)
    ▼
Frontend Display Itinerary
```

---

## Data Models

### Request Flow
```
ItineraryRequest (Frontend Input)
  ├─ destination: str
  ├─ budget: int
  ├─ energy_level: EnergyLevel (enum)
  ├─ days: int
  ├─ interests: List[str]
  └─ travelers: int
```

### Response Flow
```
ItineraryResponse (API Response)
  ├─ itinerary_id: str
  ├─ itinerary: Itinerary
  │   ├─ destination: str
  │   ├─ duration_days: int
  │   ├─ energy_level: EnergyLevel
  │   ├─ total_budget: int
  │   ├─ estimated_cost: int
  │   ├─ highlights: List[str]
  │   ├─ packing_tips: List[str]
  │   ├─ transport_tips: List[str]
  │   ├─ budget_breakdown: Dict[str, int]
  │   └─ itinerary_days: List[ItineraryDay]
  │       ├─ day_number: int
  │       ├─ theme: str
  │       ├─ activities: List[Activity]
  │       │   ├─ name: str
  │       │   ├─ description: str
  │       │   ├─ location: str
  │       │   ├─ duration_hours: float
  │       │   ├─ cost_per_person: int
  │       │   ├─ energy_required: EnergyLevel
  │       │   ├─ time_of_day: str
  │       │   ├─ latitude: Optional[float]
  │       │   └─ longitude: Optional[float]
  │       ├─ estimated_cost: int
  │       └─ tips: List[str]
  ├─ shareable_url: Optional[str]
  └─ generated_at: str (ISO timestamp)
```

---

## Key Design Decisions

### 1. Separation of Concerns
- Frontend isolated from backend logic
- Services encapsulate external API calls
- Middleware handles cross-cutting concerns

### 2. Type Safety
- TypeScript for frontend
- Pydantic for backend validation
- Enum types for energy levels

### 3. Error Handling
- Try-catch blocks in all services
- Informative error messages
- Global error middleware

### 4. Security
- Input validation on all requests
- GCS path sanitization to prevent traversal
- Environment-based secrets
- CORS configuration

### 5. Scalability
- Async/await for I/O operations
- State management for frontend
- Microservice-friendly API design
- Easy to add authentication later

### 6. Mobile-First Design
- Responsive Tailwind CSS
- Mobile-optimized form layout
- Touch-friendly buttons and inputs
- Flexible container layouts

---

## Performance Considerations

### Caching Opportunities
- Cache geocoding results
- Cache place search results
- Browser caching for static assets

### API Optimization
- Batch multiple requests where possible
- Implement request pagination
- Add response compression
- Consider request queuing

### Frontend Optimization
- Lazy load components
- Virtualize long lists (if needed)
- Minimize bundle size with tree-shaking
- Use React.memo for component optimization

---

## Future Enhancements

1. **User Authentication**
   - User accounts and history
   - Saved itinerary collections
   - Sharing with other users

2. **Advanced Features**
   - Real-time travel alerts
   - Weather integration
   - Restaurant reservations
   - Flight/hotel booking integration

3. **AI Improvements**
   - Multi-turn conversation mode
   - Itinerary refinement based on feedback
   - Personalization from past trips

4. **Analytics**
   - Track popular destinations
   - Monitor Gemini API usage
   - User behavior analytics

5. **Infrastructure**
   - Add database (PostgreSQL)
   - Implement caching layer (Redis)
   - Set up CI/CD pipelines
   - Add monitoring and observability
