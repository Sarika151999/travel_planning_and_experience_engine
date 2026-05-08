/**
 * TypeScript type definitions for Vibe-Check Travel Agent frontend
 */

export enum EnergyLevel {
  CHILL = 'chill',
  BALANCED = 'balanced',
  ADVENTUROUS = 'adventurous',
}

export interface Activity {
  name: string
  description: string
  location: string
  duration_hours: number
  cost_per_person: number
  energy_required: EnergyLevel
  time_of_day: string
  google_place_id?: string
  latitude?: number
  longitude?: number
}

export interface ItineraryDay {
  day_number: number
  theme: string
  activities: Activity[]
  estimated_cost: number
  tips: string[]
}

export interface Itinerary {
  destination: string
  duration_days: number
  energy_level: EnergyLevel
  total_budget: number
  estimated_cost: number
  itinerary_days: ItineraryDay[]
  highlights: string[]
  packing_tips: string[]
  transport_tips: string[]
  budget_breakdown: Record<string, number>
}

export interface ItineraryResponse {
  itinerary_id: string
  itinerary: Itinerary
  shareable_url?: string
  generated_at: string
}

export interface ItineraryRequest {
  destination: string
  budget: number
  energy_level: EnergyLevel
  days?: number
  interests?: string[]
  travelers?: number
}

export interface ApiError {
  error: string
  detail?: string
  status_code: number
}
