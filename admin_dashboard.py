#!/usr/bin/env python3
"""
📊 PROFESSIONAL ADMIN DASHBOARD
Real-time monitoring and analytics dashboard

Features:
- FastAPI web server with REST API
- Real-time metrics and analytics
- Chart.js visualizations
- Revenue tracking
- Marketing channel performance
- System health monitoring
- Responsive Tailwind CSS design
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from datetime import datetime, timedelta
import random

app = FastAPI(title="Dropship Dashboard", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
async def admin_dashboard():
    """Professional admin dashboard with real-time metrics"""
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dropship Pro Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 1rem;
            padding: 1.5rem;
            color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .chart-container {
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-top: 1.5rem;
        }
        .status-dot {
            height: 12px;
            width: 12px;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .metric-label {
            font-size: 0.875rem;
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1;
        }
        .metric-change {
            font-size: 0.875rem;
            margin-top: 0.5rem;
        }
    </style>
</head>
<body class="bg-gray-100">
    <!-- Header -->
    <header class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg">
        <div class="container mx-auto px-6 py-4">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold">🚀 Dropship Pro Dashboard</h1>
                    <p class="text-purple-200">Real-time analytics & monitoring</p>
                </div>
                <div class="text-right">
                    <p class="text-sm">Status: <span class="status-dot bg-green-400"></span> Active</p>
                    <p class="text-sm" id="current-time"></p>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-6 py-8">
        
        <!-- Key Metrics Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Revenue -->
            <div class="stat-card">
                <div class="metric-label">💰 Total Revenue</div>
                <div class="metric-value" id="total-revenue">$0</div>
                <div class="metric-change">
                    <span class="text-green-300">▲ 24.5%</span> vs last month
                </div>
            </div>
            
            <!-- Orders -->
            <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">📦 Total Orders</div>
                <div class="metric-value" id="total-orders">0</div>
                <div class="metric-change">
                    <span class="text-green-300">▲ 12.3%</span> vs last month
                </div>
            </div>
            
            <!-- Conversion Rate -->
            <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">📊 Conversion Rate</div>
                <div class="metric-value" id="conversion-rate">0%</div>
                <div class="metric-change">
                    <span class="text-green-300">▲ 3.2%</span> vs last month
                </div>
            </div>
            
            <!-- Active Campaigns -->
            <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-label">🎯 Active Campaigns</div>
                <div class="metric-value" id="active-campaigns">0</div>
                <div class="metric-change">
                    <span class="text-white">12 channels active</span>
                </div>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Revenue Chart -->
            <div class="chart-container">
                <h3 class="text-xl font-bold text-gray-800 mb-4">📈 Revenue Trend (Last 7 Days)</h3>
                <canvas id="revenueChart"></canvas>
            </div>
            
            <!-- Marketing Channels Chart -->
            <div class="chart-container">
                <h3 class="text-xl font-bold text-gray-800 mb-4">🎯 Marketing Channels Performance</h3>
                <canvas id="channelsChart"></canvas>
            </div>
        </div>

        <!-- System Health -->
        <div class="chart-container mt-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">🔧 System Health</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-gray-50 p-4 rounded-lg">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-gray-600">CPU Usage</span>
                        <span class="text-green-600 font-bold" id="cpu-usage">0%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-green-600 h-2 rounded-full" id="cpu-bar" style="width: 0%"></div>
                    </div>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-gray-600">Memory Usage</span>
                        <span class="text-blue-600 font-bold" id="memory-usage">0%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-blue-600 h-2 rounded-full" id="memory-bar" style="width: 0%"></div>
                    </div>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-gray-600">Disk Usage</span>
                        <span class="text-purple-600 font-bold" id="disk-usage">0%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-purple-600 h-2 rounded-full" id="disk-bar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Activity -->
        <div class="chart-container mt-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">📋 Recent Activity</h3>
            <div id="activity-feed" class="space-y-3">
                <!-- Activity items will be inserted here -->
            </div>
        </div>

    </main>

    <script>
        // Update current time
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleTimeString();
        }
        setInterval(updateTime, 1000);
        updateTime();

        // Revenue Chart
        const revenueCtx = document.getElementById('revenueChart').getContext('2d');
        const revenueChart = new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Revenue ($)',
                    data: [1200, 1900, 1500, 2200, 2800, 3100, 3680],
                    borderColor: 'rgb(102, 126, 234)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });

        // Marketing Channels Chart
        const channelsCtx = document.getElementById('channelsChart').getContext('2d');
        const channelsChart = new Chart(channelsCtx, {
            type: 'doughnut',
            data: {
                labels: ['Facebook', 'Instagram', 'TikTok', 'Google', 'Email', 'Other'],
                datasets: [{
                    data: [25, 20, 18, 15, 12, 10],
                    backgroundColor: [
                        '#667eea',
                        '#f093fb',
                        '#4facfe',
                        '#43e97b',
                        '#fa709a',
                        '#feca57'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Fetch and update metrics
        async function updateMetrics() {
            try {
                const response = await fetch('/api/dashboard/metrics');
                const data = await response.json();
                
                // Update key metrics
                document.getElementById('total-revenue').textContent = '$' + data.revenue.toLocaleString();
                document.getElementById('total-orders').textContent = data.orders.toLocaleString();
                document.getElementById('conversion-rate').textContent = data.conversion_rate.toFixed(1) + '%';
                document.getElementById('active-campaigns').textContent = data.active_campaigns;
                
                // Update system health
                document.getElementById('cpu-usage').textContent = data.system.cpu + '%';
                document.getElementById('cpu-bar').style.width = data.system.cpu + '%';
                
                document.getElementById('memory-usage').textContent = data.system.memory + '%';
                document.getElementById('memory-bar').style.width = data.system.memory + '%';
                
                document.getElementById('disk-usage').textContent = data.system.disk + '%';
                document.getElementById('disk-bar').style.width = data.system.disk + '%';
                
                // Update activity feed
                const feed = document.getElementById('activity-feed');
                feed.innerHTML = data.recent_activity.map(activity => `
                    <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                        <span class="text-2xl mr-3">${activity.icon}</span>
                        <div class="flex-1">
                            <p class="text-gray-800 font-medium">${activity.message}</p>
                            <p class="text-gray-500 text-sm">${activity.time}</p>
                        </div>
                    </div>
                `).join('');
                
            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        }

        // Update metrics every 5 seconds
        updateMetrics();
        setInterval(updateMetrics, 5000);
    </script>
</body>
</html>
    """
    
    return html_content


@app.get("/api/dashboard/metrics")
async def get_metrics():
    """API endpoint for dashboard metrics"""
    
    # Simulate real-time metrics (replace with actual data from database)
    metrics = {
        "revenue": random.randint(25000, 50000),
        "orders": random.randint(500, 1000),
        "conversion_rate": round(random.uniform(3.5, 6.5), 2),
        "active_campaigns": 12,
        "system": {
            "cpu": random.randint(15, 45),
            "memory": random.randint(40, 70),
            "disk": random.randint(35, 60)
        },
        "recent_activity": [
            {
                "icon": "🛒",
                "message": "New order #" + str(random.randint(1000, 9999)) + " - $127.99",
                "time": "2 minutes ago"
            },
            {
                "icon": "📧",
                "message": "Email campaign sent to 5,432 subscribers",
                "time": "15 minutes ago"
            },
            {
                "icon": "🎯",
                "message": "Facebook ad reached 52,341 people",
                "time": "32 minutes ago"
            },
            {
                "icon": "💳",
                "message": "Payment received: $89.99",
                "time": "1 hour ago"
            },
            {
                "icon": "📦",
                "message": "3 orders shipped via CJ Dropshipping",
                "time": "2 hours ago"
            }
        ]
    }
    
    return metrics


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "dropship-pro"
    }


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Admin Dashboard...")
    print("📊 Dashboard: http://localhost:8000")
    print("🔧 API Docs: http://localhost:8000/docs")
    print("\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
