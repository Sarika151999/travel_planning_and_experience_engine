/**
 * API service for communicating with the backend
 */

import axios, { AxiosInstance } from 'axios'
import { ItineraryRequest, ItineraryResponse, ApiError } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add error interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error)
        throw error
      }
    )
  }

  /**
   * Generate a new travel itinerary
   */
  async generateItinerary(request: ItineraryRequest): Promise<ItineraryResponse> {
    try {
      const response = await this.client.post('/itineraries/generate', request)
      return response.data
    } catch (error: any) {
      const apiError: ApiError = error.response?.data || {
        error: 'Failed to generate itinerary',
        status_code: error.response?.status || 500,
      }
      throw apiError
    }
  }

  /**
   * Retrieve a saved itinerary by ID
   */
  async getItinerary(itineraryId: string): Promise<ItineraryResponse> {
    try {
      const response = await this.client.get(`/itineraries/${itineraryId}`)
      return response.data
    } catch (error: any) {
      const apiError: ApiError = error.response?.data || {
        error: 'Failed to retrieve itinerary',
        status_code: error.response?.status || 500,
      }
      throw apiError
    }
  }

  /**
   * List recent itineraries
   */
  async listItineraries(limit: number = 10): Promise<any[]> {
    try {
      const response = await this.client.get('/itineraries', {
        params: { limit },
      })
      return response.data
    } catch (error: any) {
      const apiError: ApiError = error.response?.data || {
        error: 'Failed to list itineraries',
        status_code: error.response?.status || 500,
      }
      throw apiError
    }
  }

  /**
   * Health check
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/health')
      return response.data
    } catch (error: any) {
      throw error.response?.data || { error: 'Health check failed' }
    }
  }
}

export const apiClient = new ApiClient()
