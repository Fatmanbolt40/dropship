'use client'

import { useState } from 'react'
import { Sparkles, Copy } from 'lucide-react'

export default function MarketingPage() {
  const [productTitle, setProductTitle] = useState('')
  const [description, setDescription] = useState('')
  const [adCopy, setAdCopy] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const generateAdCopy = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${process.env.API_URL}/api/marketing/generate-ad-copy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_title: productTitle,
          product_description: description,
          platform: 'facebook'
        })
      })
      const data = await response.json()
      setAdCopy(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Marketing Intelligence</h1>
        <p className="text-gray-600">AI-powered marketing content generation</p>
      </div>

      {/* Input */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Generate Ad Copy</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Title
            </label>
            <input
              type="text"
              value={productTitle}
              onChange={(e) => setProductTitle(e.target.value)}
              placeholder="Wireless Earbuds Pro"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Premium wireless earbuds with noise cancellation..."
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <button
            onClick={generateAdCopy}
            disabled={loading}
            className="btn-primary flex items-center"
          >
            <Sparkles className="w-4 h-4 mr-2" />
            {loading ? 'Generating...' : 'Generate AI Ad Copy'}
          </button>
        </div>
      </div>

      {/* Results */}
      {adCopy && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Headlines</h3>
            <div className="space-y-2">
              {adCopy.headlines.map((headline: string, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm">{headline}</p>
                  <button className="text-primary-600 hover:text-primary-700">
                    <Copy className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Body Copy</h3>
            <div className="space-y-2">
              {adCopy.body_copy.map((copy: string, index: number) => (
                <div key={index} className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm">{copy}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Call-to-Actions</h3>
            <div className="flex flex-wrap gap-2">
              {adCopy.call_to_actions.map((cta: string, index: number) => (
                <span key={index} className="px-4 py-2 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
                  {cta}
                </span>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold mb-4">Target Audiences</h3>
            <div className="space-y-3">
              {adCopy.target_audiences.map((audience: any, index: number) => (
                <div key={index} className="p-3 bg-gray-50 rounded-lg">
                  <p className="font-medium">{audience.name}</p>
                  <p className="text-sm text-gray-600">Age: {audience.age}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tools */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="font-semibold mb-2">Video Script</h3>
          <p className="text-sm text-gray-600 mb-4">TikTok/Instagram Reels</p>
          <button className="btn-secondary w-full">Generate Script</button>
        </div>
        <div className="card">
          <h3 className="font-semibold mb-2">Email Sequence</h3>
          <p className="text-sm text-gray-600 mb-4">Automated email campaign</p>
          <button className="btn-secondary w-full">Create Sequence</button>
        </div>
        <div className="card">
          <h3 className="font-semibold mb-2">Product Description</h3>
          <p className="text-sm text-gray-600 mb-4">SEO-optimized content</p>
          <button className="btn-secondary w-full">Generate Description</button>
        </div>
      </div>
    </div>
  )
}
