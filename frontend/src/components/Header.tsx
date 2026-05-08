/**
 * Hero/Header component for the landing page
 */

import React from 'react'

export function Header() {
  return (
    <header className="bg-gradient-to-r from-primary-600 to-secondary-600 text-white py-16 md:py-24">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          🌍 Vibe-Check Travel Agent
        </h1>
        <p className="text-lg md:text-xl text-primary-50 mb-4">
          AI-powered travel planning tailored to your energy level
        </p>
        <p className="text-base md:text-lg text-primary-100">
          Generate personalized itineraries powered by Google Gemini and Maps
        </p>
      </div>
    </header>
  )
}
