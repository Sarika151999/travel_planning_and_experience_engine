/**
 * Zustand store for managing itinerary state
 */

import { create } from 'zustand'
import { ItineraryResponse, ItineraryRequest } from '@/types'
import { apiClient } from './api'

interface ItineraryStore {
  currentItinerary: ItineraryResponse | null
  loading: boolean
  error: string | null
  generatedItineraries: ItineraryResponse[]
  
  generateItinerary: (request: ItineraryRequest) => Promise<void>
  getItinerary: (id: string) => Promise<void>
  clearError: () => void
  setItinerary: (itinerary: ItineraryResponse) => void
}

export const useItineraryStore = create<ItineraryStore>((set) => ({
  currentItinerary: null,
  loading: false,
  error: null,
  generatedItineraries: [],

  generateItinerary: async (request: ItineraryRequest) => {
    set({ loading: true, error: null })
    try {
      const response = await apiClient.generateItinerary(request)
      set({
        currentItinerary: response,
        loading: false,
        generatedItineraries: (state) => [...state.generatedItineraries, response],
      })
    } catch (error: any) {
      set({
        error: error.detail || 'Failed to generate itinerary',
        loading: false,
      })
    }
  },

  getItinerary: async (id: string) => {
    set({ loading: true, error: null })
    try {
      const response = await apiClient.getItinerary(id)
      set({ currentItinerary: response, loading: false })
    } catch (error: any) {
      set({
        error: error.detail || 'Failed to retrieve itinerary',
        loading: false,
      })
    }
  },

  clearError: () => set({ error: null }),
  setItinerary: (itinerary: ItineraryResponse) => set({ currentItinerary: itinerary }),
}))
