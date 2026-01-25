#!/usr/bin/env python3
"""
🔧 ADVANCED DEBUGGING & MONITORING SYSTEM
Professional-grade system health monitoring and diagnostics

Features:
- Real-time CPU, RAM, disk monitoring with psutil
- API performance tracking
- Error tracking and logging
- System health dashboard
- Automated issue detection
- Performance metrics
"""

import psutil
import logging
import json
import time
from datetime import datetime
from collections import defaultdict, deque
import traceback
import os

class AdvancedDebugger:
    """Enterprise-grade debugging and monitoring system"""
    
    def __init__(self, log_level=logging.INFO):
        # Setup logging
        self.logger = self._setup_logging(log_level)
        
        # Metrics storage
        self.metrics = {
            'cpu': deque(maxlen=100),
            'memory': deque(maxlen=100),
            'disk': deque(maxlen=100),
            'network': deque(maxlen=100),
            'api_calls': defaultdict(list),
            'errors': []
        }
        
        # Performance thresholds
        self.thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'disk_percent': 90,
            'api_response_time': 5.0  # seconds
        }
        
        self.start_time = datetime.now()
        
    def _setup_logging(self, log_level):
        """Setup advanced logging configuration"""
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Configure logger
        logger = logging.getLogger('DropshipDebugger')
        logger.setLevel(log_level)
        
        # File handler with rotation
        log_file = f"logs/debug_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def monitor_system_health(self):
        """Monitor CPU, RAM, disk, network in real-time"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            
            # Network metrics
            network = psutil.net_io_counters()
            
            # Store metrics
            timestamp = datetime.now()
            
            self.metrics['cpu'].append({
                'timestamp': timestamp,
                'percent': cpu_percent,
                'count': cpu_count,
                'freq': cpu_freq.current if cpu_freq else 0
            })
            
            self.metrics['memory'].append({
                'timestamp': timestamp,
                'percent': memory.percent,
                'used': memory.used,
                'available': memory.available,
                'total': memory.total
            })
            
            self.metrics['disk'].append({
                'timestamp': timestamp,
                'percent': disk.percent,
                'used': disk.used,
                'free': disk.free,
                'total': disk.total
            })
            
            self.metrics['network'].append({
                'timestamp': timestamp,
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            })
            
            # Check thresholds
            alerts = []
            if cpu_percent > self.thresholds['cpu_percent']:
                alerts.append(f"⚠️  HIGH CPU: {cpu_percent}%")
                
            if memory.percent > self.thresholds['memory_percent']:
                alerts.append(f"⚠️  HIGH MEMORY: {memory.percent}%")
                
            if disk.percent > self.thresholds['disk_percent']:
                alerts.append(f"⚠️  HIGH DISK: {disk.percent}%")
            
            # Log results
            health_status = {
                'timestamp': timestamp.isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'cores': cpu_count,
                    'status': '✅ Good' if cpu_percent < 80 else '⚠️  High'
                },
                'memory': {
                    'percent': memory.percent,
                    'used_gb': round(memory.used / (1024**3), 2),
                    'total_gb': round(memory.total / (1024**3), 2),
                    'status': '✅ Good' if memory.percent < 85 else '⚠️  High'
                },
                'disk': {
                    'percent': disk.percent,
                    'used_gb': round(disk.used / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2),
                    'status': '✅ Good' if disk.percent < 90 else '⚠️  High'
                },
                'network': {
                    'sent_mb': round(network.bytes_sent / (1024**2), 2),
                    'recv_mb': round(network.bytes_recv / (1024**2), 2)
                },
                'alerts': alerts
            }
            
            if alerts:
                for alert in alerts:
                    self.logger.warning(alert)
            else:
                self.logger.info("System health: ✅ All systems normal")
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Error monitoring system health: {str(e)}")
            self.track_error(e, "system_monitoring")
            return None
    
    def track_api_performance(self, api_name, response_time, status_code, error=None):
        """Track API call performance"""
        try:
            call_data = {
                'timestamp': datetime.now().isoformat(),
                'api': api_name,
                'response_time': response_time,
                'status_code': status_code,
                'error': str(error) if error else None
            }
            
            self.metrics['api_calls'][api_name].append(call_data)
            
            # Check response time threshold
            if response_time > self.thresholds['api_response_time']:
                self.logger.warning(
                    f"⚠️  Slow API: {api_name} took {response_time:.2f}s"
                )
            
            # Log successful calls
            if status_code == 200 or status_code == 201:
                self.logger.info(
                    f"✅ API Success: {api_name} ({response_time:.2f}s)"
                )
            else:
                self.logger.error(
                    f"❌ API Error: {api_name} - Status {status_code}"
                )
            
            return call_data
            
        except Exception as e:
            self.logger.error(f"Error tracking API performance: {str(e)}")
            return None
    
    def track_error(self, error, context=""):
        """Track and log errors with full context"""
        try:
            error_data = {
                'timestamp': datetime.now().isoformat(),
                'error_type': type(error).__name__,
                'error_message': str(error),
                'context': context,
                'traceback': traceback.format_exc()
            }
            
            self.metrics['errors'].append(error_data)
            
            # Log error with full traceback
            self.logger.error(
                f"❌ ERROR in {context}: {type(error).__name__}: {str(error)}\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
            
            # Save error to file for analysis
            error_file = f"logs/errors_{datetime.now().strftime('%Y%m%d')}.json"
            
            try:
                with open(error_file, 'a') as f:
                    f.write(json.dumps(error_data) + '\n')
            except:
                pass  # Don't fail if we can't write error file
            
            return error_data
            
        except Exception as e:
            print(f"Critical: Error in error tracking: {str(e)}")
            return None
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            info = {
                'system': {
                    'boot_time': boot_time.isoformat(),
                    'uptime_hours': round(uptime.total_seconds() / 3600, 2),
                    'python_version': os.sys.version.split()[0]
                },
                'cpu': {
                    'physical_cores': psutil.cpu_count(logical=False),
                    'logical_cores': psutil.cpu_count(logical=True),
                    'current_freq_mhz': psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'
                },
                'memory': {
                    'total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                    'available_gb': round(psutil.virtual_memory().available / (1024**3), 2)
                },
                'disk': {
                    'total_gb': round(psutil.disk_usage('/').total / (1024**3), 2),
                    'free_gb': round(psutil.disk_usage('/').free / (1024**3), 2)
                }
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting system info: {str(e)}")
            return None
    
    def diagnose_issues(self):
        """AI-powered issue diagnosis"""
        issues = []
        recommendations = []
        
        try:
            # Check CPU
            if self.metrics['cpu']:
                recent_cpu = list(self.metrics['cpu'])[-10:]
                avg_cpu = sum(m['percent'] for m in recent_cpu) / len(recent_cpu)
                
                if avg_cpu > 80:
                    issues.append(f"High CPU usage: {avg_cpu:.1f}%")
                    recommendations.append("Consider scaling to more instances or optimizing code")
            
            # Check Memory
            if self.metrics['memory']:
                recent_mem = list(self.metrics['memory'])[-10:]
                avg_mem = sum(m['percent'] for m in recent_mem) / len(recent_mem)
                
                if avg_mem > 85:
                    issues.append(f"High memory usage: {avg_mem:.1f}%")
                    recommendations.append("Check for memory leaks or increase RAM allocation")
            
            # Check API performance
            for api_name, calls in self.metrics['api_calls'].items():
                if calls:
                    recent_calls = calls[-10:]
                    avg_response = sum(c['response_time'] for c in recent_calls) / len(recent_calls)
                    
                    if avg_response > 3:
                        issues.append(f"Slow API: {api_name} avg {avg_response:.2f}s")
                        recommendations.append(f"Optimize {api_name} calls or add caching")
            
            # Check error rate
            if len(self.metrics['errors']) > 10:
                issues.append(f"High error rate: {len(self.metrics['errors'])} errors")
                recommendations.append("Review error logs and fix root causes")
            
            diagnosis = {
                'timestamp': datetime.now().isoformat(),
                'overall_health': 'Good' if not issues else 'Needs Attention',
                'issues': issues,
                'recommendations': recommendations
            }
            
            if issues:
                self.logger.warning(f"⚠️  Diagnosed {len(issues)} issues")
                for issue in issues:
                    self.logger.warning(f"   - {issue}")
            else:
                self.logger.info("✅ No issues detected - system healthy")
            
            return diagnosis
            
        except Exception as e:
            self.logger.error(f"Error in diagnosis: {str(e)}")
            return None
    
    def print_dashboard(self):
        """Print real-time terminal dashboard"""
        try:
            health = self.monitor_system_health()
            
            if not health:
                return
            
            print("\n" + "="*70)
            print("🔧 SYSTEM HEALTH DASHBOARD")
            print("="*70)
            print(f"Timestamp: {health['timestamp']}")
            print(f"\n📊 CPU:")
            print(f"   Usage: {health['cpu']['percent']}% | Cores: {health['cpu']['cores']} | {health['cpu']['status']}")
            print(f"\n💾 Memory:")
            print(f"   Usage: {health['memory']['percent']}% | Used: {health['memory']['used_gb']}GB / {health['memory']['total_gb']}GB | {health['memory']['status']}")
            print(f"\n💿 Disk:")
            print(f"   Usage: {health['disk']['percent']}% | Free: {health['disk']['free_gb']}GB | {health['disk']['status']}")
            print(f"\n🌐 Network:")
            print(f"   Sent: {health['network']['sent_mb']}MB | Received: {health['network']['recv_mb']}MB")
            
            if health['alerts']:
                print(f"\n⚠️  ALERTS:")
                for alert in health['alerts']:
                    print(f"   {alert}")
            
            # API Stats
            if self.metrics['api_calls']:
                print(f"\n📡 API Calls:")
                for api_name, calls in list(self.metrics['api_calls'].items())[:5]:
                    if calls:
                        avg_time = sum(c['response_time'] for c in calls) / len(calls)
                        print(f"   {api_name}: {len(calls)} calls, avg {avg_time:.2f}s")
            
            # Error Count
            if self.metrics['errors']:
                print(f"\n❌ Errors: {len(self.metrics['errors'])} total")
            
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"Error printing dashboard: {str(e)}")
    
    def export_metrics(self, filename=None):
        """Export all metrics to JSON file"""
        try:
            if not filename:
                filename = f"metrics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {
                'export_time': datetime.now().isoformat(),
                'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
                'metrics': {
                    'cpu': [dict(m, timestamp=m['timestamp'].isoformat()) for m in self.metrics['cpu']],
                    'memory': [dict(m, timestamp=m['timestamp'].isoformat()) for m in self.metrics['memory']],
                    'disk': [dict(m, timestamp=m['timestamp'].isoformat()) for m in self.metrics['disk']],
                    'network': [dict(m, timestamp=m['timestamp'].isoformat()) for m in self.metrics['network']],
                    'api_calls': {k: v for k, v in self.metrics['api_calls'].items()},
                    'errors': self.metrics['errors']
                }
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            self.logger.info(f"✅ Metrics exported to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {str(e)}")
            return None


def main():
    """Test the advanced debugging system"""
    print("\n🔧 Testing Advanced Debugging System...\n")
    
    # Initialize debugger
    debugger = AdvancedDebugger()
    
    # Test 1: System health monitoring
    print("Test 1: System Health Monitoring")
    debugger.print_dashboard()
    time.sleep(1)
    
    # Test 2: API performance tracking
    print("\nTest 2: API Performance Tracking")
    debugger.track_api_performance("Claude API", 0.5, 200)
    debugger.track_api_performance("Stripe API", 1.2, 200)
    debugger.track_api_performance("CJ API", 6.5, 200)  # Slow
    time.sleep(1)
    
    # Test 3: Error tracking
    print("\nTest 3: Error Tracking")
    try:
        raise ValueError("Test error for debugging")
    except Exception as e:
        debugger.track_error(e, "test_function")
    
    # Test 4: System info
    print("\nTest 4: System Information")
    info = debugger.get_system_info()
    print(json.dumps(info, indent=2))
    
    # Test 5: Issue diagnosis
    print("\nTest 5: Issue Diagnosis")
    diagnosis = debugger.diagnose_issues()
    print(json.dumps(diagnosis, indent=2))
    
    # Test 6: Export metrics
    print("\nTest 6: Export Metrics")
    export_file = debugger.export_metrics()
    print(f"✅ Metrics exported to: {export_file}")
    
    print("\n✅ All debugging tests completed!\n")


if __name__ == "__main__":
    main()
