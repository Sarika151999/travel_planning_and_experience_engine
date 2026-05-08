/**
 * Custom hook for managing itinerary generation
 */

import { useState, useCallback } from 'react'
import { ItineraryRequest, ItineraryResponse } from '@/types'
import { useItineraryStore } from '@/services/store'

export function useItinerary() {
  const [isGenerating, setIsGenerating] = useState(false)
  const { generateItinerary, currentItinerary, error } = useItineraryStore()

  const generate = useCallback(
    async (request: ItineraryRequest) => {
      setIsGenerating(true)
      try {
        await generateItinerary(request)
      } finally {
        setIsGenerating(false)
      }
    },
    [generateItinerary]
  )

  return {
    generate,
    isGenerating,
    itinerary: currentItinerary,
    error,
  }
}
