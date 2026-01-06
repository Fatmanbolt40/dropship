'use client'

import { useEffect, useState } from 'react'
import { BarChart3, TrendingUp, DollarSign, Package, ArrowUp, ArrowDown } from 'lucide-react'
import StatsCard from '@/components/StatsCard'
import RevenueChart from '@/components/RevenueChart'
import TopProducts from '@/components/TopProducts'

export default function Dashboard() {
  const [metrics, setMetrics] = useState({
    total_revenue: 0,
    total_sales: 0,
    active_products: 0,
    roi: 0,
    average_order_value: 0,
  })

  useEffect(() => {
    fetchDashboardMetrics()
  }, [])

  const fetchDashboardMetrics = async () => {
    try {
      const response = await fetch(`${process.env.API_URL}/api/analytics/dashboard`)
      const data = await response.json()
      setMetrics(data)
    } catch (error) {
      console.error('Failed to fetch metrics:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to your DropShip AI command center</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Revenue"
          value={`$${metrics.total_revenue.toLocaleString()}`}
          icon={<DollarSign className="w-6 h-6" />}
          trend={{ value: 12.5, isPositive: true }}
          color="blue"
        />
        <StatsCard
          title="Total Sales"
          value={metrics.total_sales.toLocaleString()}
          icon={<TrendingUp className="w-6 h-6" />}
          trend={{ value: 8.2, isPositive: true }}
          color="green"
        />
        <StatsCard
          title="Active Products"
          value={metrics.active_products}
          icon={<Package className="w-6 h-6" />}
          trend={{ value: 3, isPositive: true }}
          color="purple"
        />
        <StatsCard
          title="ROI"
          value={`${metrics.roi}%`}
          icon={<BarChart3 className="w-6 h-6" />}
          trend={{ value: 15.3, isPositive: true }}
          color="orange"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RevenueChart />
        <TopProducts />
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="btn-primary">
            Find Trending Products
          </button>
          <button className="btn-primary">
            Generate Ad Copy
          </button>
          <button className="btn-primary">
            Import to Shopify
          </button>
        </div>
      </div>
    </div>
  )
}
