'use client'

import { TrendingUp } from 'lucide-react'

const topProducts = [
  { name: 'Wireless Earbuds Pro', sales: 1250, revenue: '$24,975', roi: '245%' },
  { name: 'Smart Watch Ultra', sales: 890, revenue: '$35,600', roi: '198%' },
  { name: 'Portable Charger Max', sales: 756, revenue: '$15,120', roi: '176%' },
  { name: 'Bluetooth Speaker Mini', sales: 654, revenue: '$13,080', roi: '165%' },
  { name: 'Phone Stand Pro', sales: 543, revenue: '$8,145', roi: '142%' },
]

export default function TopProducts() {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Top Performing Products</h2>
        <TrendingUp className="w-5 h-5 text-green-600" />
      </div>
      
      <div className="space-y-4">
        {topProducts.map((product, index) => (
          <div key={product.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center font-semibold">
                {index + 1}
              </div>
              <div>
                <p className="font-medium text-gray-900">{product.name}</p>
                <p className="text-sm text-gray-500">{product.sales} sales</p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-semibold text-gray-900">{product.revenue}</p>
              <p className="text-sm text-green-600">{product.roi} ROI</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
