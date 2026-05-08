# API Documentation - Vibe-Check Travel Agent

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check
```
GET /health
```

**Description**: Check if the API is running and healthy

**Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### Generate Itinerary
```
POST /itineraries/generate
```

**Description**: Generate a personalized travel itinerary

**Request Body**:
```json
{
  "destination": "Paris",
  "budget": 3000,
  "energy_level": "balanced",
  "days": 5,
  "interests": ["museums", "food", "art"],
  "travelers": 2
}
```

**Parameters**:
| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| destination | string | Yes | - | 2-100 chars |
| budget | integer | Yes | - | 100-100,000 USD |
| energy_level | enum | Yes | - | "chill", "balanced", "adventurous" |
| days | integer | No | 3 | 1-30 |
| interests | array | No | [] | Max 10 items, 2-50 chars each |
| travelers | integer | No | 1 | 1-20 |

**Response** (201 Created):
```json
{
  "itinerary_id": "a1b2c3d4e5f6g7h8",
  "itinerary": {
    "destination": "Paris",
    "duration_days": 5,
    "energy_level": "balanced",
    "total_budget": 3000,
    "estimated_cost": 2850,
    "highlights": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise"],
    "packing_tips": ["Comfortable walking shoes", "Light jacket"],
    "transport_tips": ["Use Metro for efficient travel", "Buy a 5-day pass"],
    "budget_breakdown": {
      "accommodation": 1000,
      "food": 750,
      "activities": 850,
      "transport": 250
    },
    "itinerary_days": [
      {
        "day_number": 1,
        "theme": "Arrival & Exploration",
        "estimated_cost": 150,
        "tips": ["Check into hotel", "Rest after travel"],
        "activities": [
          {
            "name": "Explore Marais District",
            "description": "Historical neighborhood with charming streets",
            "location": "Marais, Paris",
            "duration_hours": 3,
            "cost_per_person": 50,
            "energy_required": "balanced",
            "time_of_day": "afternoon",
            "latitude": 48.8597,
            "longitude": 2.3623
          }
        ]
      }
    ]
  },
  "shareable_url": "https://storage.googleapis.com/...",
  "generated_at": "2024-01-01T12:00:00"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Validation Error",
  "detail": "Budget must be between 100 and 100000",
  "status_code": 400
}
```

---

### Retrieve Itinerary
```
GET /itineraries/{itinerary_id}
```

**Description**: Retrieve a previously generated itinerary by ID

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| itinerary_id | string | ID of the itinerary to retrieve |

**Response** (200 OK): Same as generate itinerary response

**Error Response** (404 Not Found):
```json
{
  "error": "Not Found",
  "detail": "Itinerary a1b2c3d4e5f6g7h8 not found",
  "status_code": 404
}
```

---

### List Recent Itineraries
```
GET /itineraries?limit=10
```

**Description**: List recently generated itineraries

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 10 | Maximum number of itineraries to return |

**Response** (200 OK):
```json
[
  {
    "id": "a1b2c3d4e5f6g7h8",
    "created": "2024-01-01T12:00:00",
    "size": 2048
  }
]
```

---

## Error Handling

### Common Error Codes

| Status | Error | Description |
|--------|-------|-------------|
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error during processing |

### Error Response Format
```json
{
  "error": "Error Type",
  "detail": "Detailed error message",
  "status_code": 400
}
```

---

## Rate Limiting

- Maximum 30 itinerary generation requests per hour per client
- Burst limit: 5 requests per minute

---

## CORS

Allowed origins (configurable):
- `http://localhost:3000`
- `http://localhost:5173`
- Your production domain

---

## Authentication

Currently, the API is open without authentication. For production, implement:
- API Key authentication
- JWT token-based auth
- User-specific rate limiting
