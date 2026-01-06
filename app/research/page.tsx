'use client'

import { useState } from 'react'
import { Search, TrendingUp, DollarSign } from 'lucide-react'

export default function ResearchPage() {
  const [keyword, setKeyword] = useState('')
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const analyzeTrend = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${process.env.API_URL}/api/trends/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keyword,
          platforms: ['google_trends', 'tiktok']
        })
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Product Research</h1>
        <p className="text-gray-600">Discover trending products and analyze market potential</p>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex space-x-4">
          <input
            type="text"
            placeholder="Enter product keyword (e.g., wireless earbuds)"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          <button
            onClick={analyzeTrend}
            disabled={loading}
            className="btn-primary px-8"
          >
            {loading ? 'Analyzing...' : 'Analyze Trend'}
          </button>
        </div>
      </div>

      {/* Results */}
      {results && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
              Trend Score
            </h3>
            <div className="text-4xl font-bold text-primary-600 mb-2">
              {results.combined_trend_score}/100
            </div>
            <p className="text-gray-600">
              {results.combined_trend_score > 75 ? 'Excellent' : 
               results.combined_trend_score > 60 ? 'Good' : 'Moderate'} opportunity
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Platform Data</h3>
            <div className="space-y-3">
              {results.platform_data.map((platform: any) => (
                <div key={platform.platform} className="p-3 bg-gray-50 rounded-lg">
                  <p className="font-medium capitalize">{platform.platform.replace('_', ' ')}</p>
                  <p className="text-2xl font-bold text-primary-600">{platform.trend_score}/100</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tools */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="font-semibold mb-2">Niche Validator</h3>
          <p className="text-sm text-gray-600 mb-4">Validate market viability</p>
          <button className="btn-secondary w-full">Validate Niche</button>
        </div>
        <div className="card">
          <h3 className="font-semibold mb-2">Competitor Analysis</h3>
          <p className="text-sm text-gray-600 mb-4">Analyze competition</p>
          <button className="btn-secondary w-full">Analyze Competitors</button>
        </div>
        <div className="card">
          <h3 className="font-semibold mb-2">Profit Calculator</h3>
          <p className="text-sm text-gray-600 mb-4">Calculate margins & ROI</p>
          <button className="btn-secondary w-full">Calculate Profit</button>
        </div>
      </div>
    </div>
  )
}
