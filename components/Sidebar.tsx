'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  LayoutDashboard, 
  TrendingUp, 
  Package, 
  Megaphone, 
  BarChart3, 
  Settings,
  Zap
} from 'lucide-react'

const menuItems = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Product Research', href: '/research', icon: TrendingUp },
  { name: 'Products', href: '/products', icon: Package },
  { name: 'Marketing', href: '/marketing', icon: Megaphone },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Automation', href: '/automation', icon: Zap },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="w-64 bg-gradient-to-b from-blue-600 to-purple-700 text-white">
      <div className="p-6">
        <h1 className="text-2xl font-bold">DropShip AI</h1>
        <p className="text-sm text-blue-100">Intelligent Automation</p>
      </div>

      <nav className="mt-6">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center px-6 py-3 text-sm transition-colors ${
                isActive
                  ? 'bg-white/20 border-r-4 border-white'
                  : 'hover:bg-white/10'
              }`}
            >
              <Icon className="w-5 h-5 mr-3" />
              {item.name}
            </Link>
          )
        })}
      </nav>
    </div>
  )
}
