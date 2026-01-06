#!/usr/bin/env python3
"""
Complete Automation Setup Script
Sets up your full dropshipping automation system
"""

import os
import sys
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()

class DropshippingSetup:
    def __init__(self):
        self.config = {}
        self.setup_complete = False
        
    def welcome(self):
        """Display welcome message"""
        console.print(Panel.fit(
            "[bold cyan]🚀 DROPSHIPPING AUTOMATION SETUP[/bold cyan]\n\n"
            "[white]This will configure your fully automated dropshipping system:[/white]\n\n"
            "✅ AI Product Finder (24/7)\n"
            "✅ Auto-Sourcing from Suppliers\n"
            "✅ Auto-Listing on Amazon\n"
            "✅ Auto-Order Fulfillment\n"
            "✅ Profit Tracking\n\n"
            "[yellow]The system finds products, lists them at markup,\n"
            "and when customers buy, auto-purchases from supplier[/yellow]",
            title="Welcome",
            border_style="cyan"
        ))
        console.print()
        
    def check_dependencies(self):
        """Check if required packages are installed"""
        console.print("[cyan]Checking dependencies...[/cyan]")
        
        required = ['requests', 'fastapi', 'uvicorn', 'sqlalchemy', 'stripe', 
                   'beautifulsoup4', 'httpx', 'python-dotenv']
        
        missing = []
        for package in required:
            try:
                __import__(package.replace('-', '_'))
                console.print(f"  ✅ {package}")
            except ImportError:
                console.print(f"  ❌ {package} [red](missing)[/red]")
                missing.append(package)
        
        if missing:
            console.print(f"\n[yellow]Installing missing packages...[/yellow]")
            os.system(f"pip install {' '.join(missing)}")
        
        console.print()
        
    def setup_database(self):
        """Initialize database"""
        console.print("[cyan]Setting up database...[/cyan]")
        
        from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        
        Base = declarative_base()
        
        class Product(Base):
            __tablename__ = 'products'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            source_asin = Column(String)
            cost = Column(Float)
            sell_price = Column(Float)
            profit_margin = Column(Float)
            supplier = Column(String)
            status = Column(String)  # active, sold_out, disabled
            created_at = Column(DateTime, default=datetime.now)
            
        class Order(Base):
            __tablename__ = 'orders'
            id = Column(Integer, primary_key=True)
            order_id = Column(String, unique=True)
            customer_email = Column(String)
            customer_name = Column(String)
            shipping_address = Column(JSON)
            products = Column(JSON)
            total_paid = Column(Float)
            total_cost = Column(Float)
            profit = Column(Float)
            status = Column(String)  # pending, processing, fulfilled, completed
            stripe_payment_id = Column(String)
            supplier_order_id = Column(String)
            tracking_number = Column(String)
            created_at = Column(DateTime, default=datetime.now)
            updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
        
        engine = create_engine('sqlite:///dropship.db')
        Base.metadata.create_all(engine)
        
        console.print("  ✅ Database initialized\n")
        
    def configure_services(self):
        """Configure API keys and services"""
        console.print(Panel.fit(
            "[bold yellow]SERVICE CONFIGURATION[/bold yellow]\n\n"
            "[white]You'll need accounts with these services (all have FREE plans):[/white]\n\n"
            "1. CJ Dropshipping - Product sourcing (FREE)\n"
            "2. Stripe - Payment processing (FREE, pay-per-transaction)\n"
            "3. Amazon Seller - Your selling platform (pending verification)\n\n"
            "[dim]You can skip any and configure later[/dim]",
            border_style="yellow"
        ))
        console.print()
        
        # CJ Dropshipping
        if Confirm.ask("Configure CJ Dropshipping API? (recommended)", default=True):
            console.print("\n[cyan]CJ Dropshipping Setup:[/cyan]")
            console.print("1. Go to: https://www.cjdropshipping.com")
            console.print("2. Sign up for FREE account")
            console.print("3. Go to Settings → API → Get your credentials\n")
            
            cj_email = Prompt.ask("CJ Email", default="skip")
            cj_key = Prompt.ask("CJ API Key", default="skip")
            
            if cj_email != "skip" and cj_key != "skip":
                self.config['cj_email'] = cj_email
                self.config['cj_api_key'] = cj_key
        
        # Stripe
        if Confirm.ask("\nConfigure Stripe payments? (recommended)", default=True):
            console.print("\n[cyan]Stripe Setup:[/cyan]")
            console.print("1. Go to: https://dashboard.stripe.com/register")
            console.print("2. Sign up for FREE account")
            console.print("3. Get your test API keys from Dashboard\n")
            
            stripe_key = Prompt.ask("Stripe Secret Key", default="skip")
            
            if stripe_key != "skip":
                self.config['stripe_secret_key'] = stripe_key
        
        console.print()
        
    def save_config(self):
        """Save configuration to .env file"""
        console.print("[cyan]Saving configuration...[/cyan]")
        
        # Read existing .env
        env_content = []
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_content = f.readlines()
        
        # Update with new values
        updated_lines = []
        keys_updated = set()
        
        for line in env_content:
            if '=' in line and not line.strip().startswith('#'):
                key = line.split('=')[0].strip()
                if key == 'CJ_EMAIL' and 'cj_email' in self.config:
                    updated_lines.append(f"CJ_EMAIL={self.config['cj_email']}\n")
                    keys_updated.add('CJ_EMAIL')
                elif key == 'CJ_API_KEY' and 'cj_api_key' in self.config:
                    updated_lines.append(f"CJ_API_KEY={self.config['cj_api_key']}\n")
                    keys_updated.add('CJ_API_KEY')
                elif key == 'STRIPE_SECRET_KEY' and 'stripe_secret_key' in self.config:
                    updated_lines.append(f"STRIPE_SECRET_KEY={self.config['stripe_secret_key']}\n")
                    keys_updated.add('STRIPE_SECRET_KEY')
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # Add any new keys
        if 'cj_email' in self.config and 'CJ_EMAIL' not in keys_updated:
            updated_lines.append(f"\nCJ_EMAIL={self.config['cj_email']}\n")
        if 'cj_api_key' in self.config and 'CJ_API_KEY' not in keys_updated:
            updated_lines.append(f"CJ_API_KEY={self.config['cj_api_key']}\n")
        if 'stripe_secret_key' in self.config and 'STRIPE_SECRET_KEY' not in keys_updated:
            updated_lines.append(f"STRIPE_SECRET_KEY={self.config['stripe_secret_key']}\n")
        
        with open('.env', 'w') as f:
            f.writelines(updated_lines)
        
        console.print("  ✅ Configuration saved\n")
        
    def create_startup_scripts(self):
        """Create automation startup scripts"""
        console.print("[cyan]Creating automation scripts...[/cyan]")
        
        # Create master automation script
        automation_script = """#!/usr/bin/env python3
\"\"\"
MASTER AUTOMATION CONTROLLER
Runs all automation systems 24/7
\"\"\"

import subprocess
import time
import os
from datetime import datetime

class AutomationController:
    def __init__(self):
        self.processes = {}
        
    def start_backend(self):
        \"\"\"Start FastAPI backend\"\"\"
        print("🚀 Starting backend API...")
        proc = subprocess.Popen(['python3', 'server.py'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        self.processes['backend'] = proc
        time.sleep(3)
        
    def start_product_finder(self):
        \"\"\"Start 24/7 product finder\"\"\"
        print("🔍 Starting AI Product Finder (24/7)...")
        proc = subprocess.Popen(['python3', 'auto_finder_24_7.py'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        self.processes['finder'] = proc
        
    def start_order_processor(self):
        \"\"\"Start order fulfillment processor\"\"\"
        print("📦 Starting Order Processor...")
        proc = subprocess.Popen(['python3', 'order_fulfillment.py'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        self.processes['orders'] = proc
        
    def monitor(self):
        \"\"\"Monitor all processes\"\"\"
        print("\\n" + "="*50)
        print("✅ AUTOMATION RUNNING 24/7")
        print("="*50)
        print("\\n📊 Active Services:")
        print("  • Backend API: http://localhost:8000")
        print("  • Product Finder: Finding trending products")
        print("  • Order Processor: Auto-fulfilling orders")
        print("\\n💰 The system will:")
        print("  1. Find profitable products every hour")
        print("  2. List them on Amazon (when verified)")
        print("  3. Auto-fulfill orders when customers buy")
        print("  4. Track profits automatically")
        print("\\n🛑 To stop: Press Ctrl+C")
        print("="*50 + "\\n")
        
        try:
            while True:
                # Check if processes are still running
                for name, proc in self.processes.items():
                    if proc.poll() is not None:
                        print(f"⚠️  {name} stopped, restarting...")
                        if name == 'backend':
                            self.start_backend()
                        elif name == 'finder':
                            self.start_product_finder()
                        elif name == 'orders':
                            self.start_order_processor()
                
                time.sleep(10)  # Check every 10 seconds
                
        except KeyboardInterrupt:
            print("\\n🛑 Stopping automation...")
            for proc in self.processes.values():
                proc.terminate()
            print("✅ Stopped")

if __name__ == '__main__':
    controller = AutomationController()
    controller.start_backend()
    time.sleep(2)
    controller.start_product_finder()
    time.sleep(2)
    controller.start_order_processor()
    time.sleep(2)
    controller.monitor()
"""
        
        with open('run_automation.py', 'w') as f:
            f.write(automation_script)
        os.chmod('run_automation.py', 0o755)
        
        console.print("  ✅ Automation scripts created\n")
        
    def display_next_steps(self):
        """Show user what to do next"""
        
        table = Table(title="🎯 Your Automation System is Ready!", 
                     title_style="bold green",
                     show_header=True)
        table.add_column("Step", style="cyan", width=6)
        table.add_column("Action", style="white", width=60)
        table.add_column("Status", width=12)
        
        table.add_row("1", "Wait for Amazon Seller approval (1-3 days)", "[yellow]PENDING[/yellow]")
        table.add_row("2", "Sign up for CJ Dropshipping (FREE)", 
                     "[green]READY[/green]" if 'cj_email' in self.config else "[yellow]TODO[/yellow]")
        table.add_row("3", "Sign up for Stripe payments (FREE)",
                     "[green]READY[/green]" if 'stripe_secret_key' in self.config else "[yellow]TODO[/yellow]")
        table.add_row("4", "Start automation: ./run_automation.py", "[green]READY[/green]")
        table.add_row("5", "System finds & lists products automatically", "[cyan]AUTO[/cyan]")
        table.add_row("6", "Make money while you sleep! 💰", "[green]24/7[/green]")
        
        console.print()
        console.print(table)
        console.print()
        
        console.print(Panel.fit(
            "[bold green]QUICK START COMMANDS:[/bold green]\n\n"
            "[cyan]# Start full automation (24/7)[/cyan]\n"
            "python3 run_automation.py\n\n"
            "[cyan]# Or start components individually:[/cyan]\n"
            "python3 server.py              # Backend API\n"
            "python3 auto_finder_24_7.py    # Product finder\n"
            "python3 order_fulfillment.py   # Order processor\n\n"
            "[bold yellow]HOW IT WORKS:[/bold yellow]\n"
            "1. AI finds trending products from suppliers\n"
            "2. Lists them on Amazon at 2-3x markup\n"
            "3. Customer buys from you\n"
            "4. System auto-orders from supplier\n"
            "5. Supplier ships to customer\n"
            "6. You keep the profit! 💰",
            title="Next Steps",
            border_style="green"
        ))
        console.print()
        
    def run(self):
        """Run the setup"""
        self.welcome()
        input("Press Enter to begin setup...")
        console.print()
        
        self.check_dependencies()
        self.setup_database()
        self.configure_services()
        self.save_config()
        self.create_startup_scripts()
        
        console.print("[bold green]✅ SETUP COMPLETE![/bold green]\n")
        self.display_next_steps()

if __name__ == '__main__':
    setup = DropshippingSetup()
    setup.run()
