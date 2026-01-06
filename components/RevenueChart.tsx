'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const data = [
  { date: 'Jan 1', revenue: 4000 },
  { date: 'Jan 5', revenue: 3000 },
  { date: 'Jan 10', revenue: 5000 },
  { date: 'Jan 15', revenue: 7000 },
  { date: 'Jan 20', revenue: 6000 },
  { date: 'Jan 25', revenue: 8000 },
  { date: 'Jan 30', revenue: 9500 },
]

export default function RevenueChart() {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Revenue Overview</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" stroke="#0ea5e9" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
