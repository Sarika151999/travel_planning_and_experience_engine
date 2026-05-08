/**
 * Itinerary display component
 */

import React from 'react'
import { ItineraryResponse } from '@/types'

interface ItineraryDisplayProps {
  itinerary: ItineraryResponse | null
  loading: boolean
}

export function ItineraryDisplay({ itinerary, loading }: ItineraryDisplayProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin text-4xl mb-4">🌍</div>
          <p className="text-gray-600">Crafting your perfect itinerary...</p>
        </div>
      </div>
    )
  }

  if (!itinerary) {
    return null
  }

  const { itinerary: plan, shareable_url } = itinerary

  return (
    <div className="w-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6 md:p-8">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          🎉 Your {plan.duration_days}-Day {plan.destination} Adventure
        </h2>
        <p className="text-gray-600 mb-4">
          Vibe: <span className="font-semibold capitalize text-primary-600">{plan.energy_level}</span> | 
          Budget: <span className="font-semibold">${plan.total_budget}</span> | 
          Estimated Cost: <span className="font-semibold">${plan.estimated_cost}</span>
        </p>

        {shareable_url && (
          <div className="mb-4 p-4 bg-primary-50 rounded-lg">
            <p className="text-sm text-gray-700 mb-2">Share your itinerary:</p>
            <a 
              href={shareable_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 break-all text-sm font-mono"
            >
              {shareable_url.substring(0, 50)}...
            </a>
          </div>
        )}
      </div>

      {/* Highlights */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">✨ Highlights</h3>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {plan.highlights.map((highlight, idx) => (
            <li key={idx} className="flex items-start">
              <span className="mr-2">⭐</span>
              <span className="text-gray-700">{highlight}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Daily Itinerary */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">📅 Day-by-Day Itinerary</h3>
        <div className="space-y-6">
          {plan.itinerary_days.map((day) => (
            <div key={day.day_number} className="border-l-4 border-primary-600 pl-4 pb-6">
              <h4 className="text-lg font-bold text-gray-900 mb-2">
                Day {day.day_number}: {day.theme}
              </h4>
              <p className="text-sm text-gray-600 mb-3">💰 Est. Cost: ${day.estimated_cost}</p>

              {/* Activities */}
              <div className="space-y-3">
                {day.activities.map((activity, idx) => (
                  <div key={idx} className="bg-gray-50 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h5 className="font-semibold text-gray-900">{activity.name}</h5>
                      <span className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded">
                        {activity.time_of_day}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 mb-2">{activity.description}</p>
                    <div className="flex flex-wrap gap-4 text-xs text-gray-600">
                      <span>📍 {activity.location}</span>
                      <span>⏱️ {activity.duration_hours}h</span>
                      <span>💵 ${activity.cost_per_person}/person</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Day Tips */}
              {day.tips.length > 0 && (
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-xs font-semibold text-blue-900 mb-2">💡 Tips:</p>
                  <ul className="text-sm text-blue-800 space-y-1">
                    {day.tips.map((tip, idx) => (
                      <li key={idx}>• {tip}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Packing Tips */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">🎒 Packing Tips</h3>
        <ul className="space-y-2">
          {plan.packing_tips.map((tip, idx) => (
            <li key={idx} className="text-gray-700">✓ {tip}</li>
          ))}
        </ul>
      </div>

      {/* Transport Tips */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">🚗 Transport Tips</h3>
        <ul className="space-y-2">
          {plan.transport_tips.map((tip, idx) => (
            <li key={idx} className="text-gray-700">✓ {tip}</li>
          ))}
        </ul>
      </div>

      {/* Budget Breakdown */}
      <div>
        <h3 className="text-xl font-bold text-gray-900 mb-4">💰 Budget Breakdown</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(plan.budget_breakdown).map(([category, amount]) => (
            <div key={category} className="bg-gray-50 rounded-lg p-4 text-center">
              <p className="text-xs text-gray-600 capitalize mb-1">{category}</p>
              <p className="text-lg font-bold text-primary-600">${amount}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
