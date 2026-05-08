/**
 * Main App component
 */

import React, { useEffect, useState } from 'react'
import { Header } from '@/components/Header'
import { PlanningForm } from '@/components/PlanningForm'
import { ItineraryDisplay } from '@/components/ItineraryDisplay'
import { useItineraryStore } from '@/services/store'
import { apiClient } from '@/services/api'
import '@/styles/index.css'

function App() {
  const { currentItinerary, loading } = useItineraryStore()
  const [apiHealthy, setApiHealthy] = useState(true)

  useEffect(() => {
    // Check API health on mount
    const checkHealth = async () => {
      try {
        await apiClient.healthCheck()
        setApiHealthy(true)
      } catch (error) {
        console.error('API health check failed:', error)
        setApiHealthy(false)
      }
    }

    checkHealth()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      {!apiHealthy && (
        <div className="bg-yellow-50 border-b border-yellow-200 px-4 py-4">
          <div className="max-w-6xl mx-auto">
            <p className="text-yellow-800">
              ⚠️ Backend service is unavailable. Make sure the Python backend is running on http://localhost:8000
            </p>
          </div>
        </div>
      )}

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="flex items-start">
            <PlanningForm />
          </div>

          {/* Results Section */}
          <div className="md:col-span-1">
            <ItineraryDisplay itinerary={currentItinerary} loading={loading} />
          </div>
        </div>

        {/* When on mobile, stack results below */}
        <div className="md:hidden mt-12">
          <ItineraryDisplay itinerary={currentItinerary} loading={loading} />
        </div>
      </main>

      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>🌍 Vibe-Check Travel Agent © 2024</p>
          <p className="text-gray-400 text-sm mt-2">Powered by Google Gemini AI & Google Cloud Services</p>
        </div>
      </footer>
    </div>
  )
}

export default App
