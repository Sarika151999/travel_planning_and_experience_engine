/**
 * Itinerary planning form component
 */

import React, { useState } from 'react'
import { EnergyLevel, ItineraryRequest } from '@/types'
import { useItinerary } from '@/hooks/useItinerary'

export function PlanningForm() {
  const { generate, isGenerating, error } = useItinerary()
  const [formData, setFormData] = useState<ItineraryRequest>({
    destination: '',
    budget: 2000,
    energy_level: EnergyLevel.BALANCED,
    days: 3,
    interests: [],
    travelers: 1,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.destination.trim()) {
      alert('Please enter a destination')
      return
    }

    await generate(formData)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'budget' || name === 'days' || name === 'travelers' 
        ? parseInt(value) 
        : value,
    }))
  }

  return (
    <div className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6 md:p-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-900">Plan Your Trip</h2>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Destination */}
        <div className="mb-5">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Destination *
          </label>
          <input
            type="text"
            name="destination"
            value={formData.destination}
            onChange={handleInputChange}
            placeholder="e.g., Paris, Tokyo, New York"
            disabled={isGenerating}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-100"
          />
        </div>

        {/* Budget */}
        <div className="mb-5">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Budget (USD): ${formData.budget}
          </label>
          <input
            type="range"
            name="budget"
            min="100"
            max="100000"
            value={formData.budget}
            onChange={handleInputChange}
            disabled={isGenerating}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer disabled:opacity-50"
          />
          <div className="text-xs text-gray-500 mt-1 flex justify-between">
            <span>$100</span>
            <span>$100,000</span>
          </div>
        </div>

        {/* Energy Level */}
        <div className="mb-5">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Vibe / Energy Level *
          </label>
          <div className="grid grid-cols-3 gap-3">
            {[EnergyLevel.CHILL, EnergyLevel.BALANCED, EnergyLevel.ADVENTUROUS].map((level) => (
              <button
                key={level}
                type="button"
                onClick={() => setFormData((prev) => ({ ...prev, energy_level: level }))}
                disabled={isGenerating}
                className={`py-2 px-3 rounded-lg font-medium text-sm transition-colors ${
                  formData.energy_level === level
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {level.charAt(0).toUpperCase() + level.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Days */}
        <div className="mb-5">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Number of Days: {formData.days}
          </label>
          <input
            type="range"
            name="days"
            min="1"
            max="30"
            value={formData.days}
            onChange={handleInputChange}
            disabled={isGenerating}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer disabled:opacity-50"
          />
        </div>

        {/* Travelers */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Number of Travelers
          </label>
          <input
            type="number"
            name="travelers"
            min="1"
            max="20"
            value={formData.travelers}
            onChange={handleInputChange}
            disabled={isGenerating}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:bg-gray-100"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isGenerating}
          className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:cursor-not-allowed"
        >
          {isGenerating ? (
            <span className="flex items-center justify-center">
              <span className="animate-spin mr-2">⏳</span>
              Generating...
            </span>
          ) : (
            'Generate Itinerary ✨'
          )}
        </button>
      </form>
    </div>
  )
}
