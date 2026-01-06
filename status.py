#!/usr/bin/env python3
"""
Quick Status Dashboard - See What Your Automation is Doing
"""

import os
import json
import glob
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def show_status():
    console.clear()
    
    # Header
    console.print(Panel.fit(
        "[bold cyan]💰 DROPSHIPPING AUTOMATION STATUS[/bold cyan]\n"
        f"[dim]{datetime.now().strftime('%B %d, %Y - %I:%M %p')}[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    # Check running processes
    console.print("[bold yellow]🔄 Running Services:[/bold yellow]")
    services = {
        'Backend API': 'server.py',
        'Product Finder': 'auto_finder_24_7.py',
        'Order Processor': 'order_fulfillment.py'
    }
    
    for name, script in services.items():
        status = os.popen(f'pgrep -f "{script}" 2>/dev/null').read().strip()
        if status:
            console.print(f"  ✅ {name} - [green]RUNNING[/green] (PID: {status})")
        else:
            console.print(f"  ❌ {name} - [red]STOPPED[/red]")
    console.print()
    
    # Products found
    console.print("[bold yellow]📦 Products Found:[/bold yellow]")
    campaigns = glob.glob('campaigns/*.json')
    
    if campaigns:
        console.print(f"  Total: {len(campaigns)} products discovered")
        
        # Show latest 5
        latest = sorted(campaigns, key=os.path.getmtime, reverse=True)[:5]
        
        table = Table(show_header=True)
        table.add_column("Product", style="cyan", width=40)
        table.add_column("Cost", style="green", width=10)
        table.add_column("Sell", style="yellow", width=10)
        table.add_column("Profit", style="bold green", width=10)
        
        for camp_file in latest:
            try:
                with open(camp_file, 'r') as f:
                    data = json.load(f)
                    product = data.get('product', {})
                    name = product.get('name', 'Unknown')[:35]
                    cost = product.get('cost', 0)
                    sell = product.get('suggested_resale_price', 0)
                    profit = sell - cost
                    
                    table.add_row(
                        name,
                        f"${cost:.2f}",
                        f"${sell:.2f}",
                        f"${profit:.2f}"
                    )
            except:
                pass
        
        console.print(table)
    else:
        console.print("  [dim]No products found yet - system just started[/dim]")
    
    console.print()
    
    # Potential earnings
    if campaigns:
        total_potential = 0
        for camp_file in campaigns:
            try:
                with open(camp_file, 'r') as f:
                    data = json.load(f)
                    product = data.get('product', {})
                    cost = product.get('cost', 0)
                    sell = product.get('suggested_resale_price', 0)
                    total_potential += (sell - cost)
            except:
                pass
        
        console.print(Panel.fit(
            f"[bold green]💵 Potential Earnings[/bold green]\n\n"
            f"If you sell just 1 of each product:\n"
            f"[bold yellow]${total_potential:.2f}[/bold yellow] profit\n\n"
            f"If you sell 10 of each:\n"
            f"[bold yellow]${total_potential * 10:.2f}[/bold yellow] profit",
            border_style="green"
        ))
        console.print()
    
    # Next steps
    console.print("[bold yellow]⏭️  Next Steps:[/bold yellow]")
    console.print("  1. ⏳ Wait for Amazon Seller approval")
    console.print("  2. 🚀 Products will auto-list when approved")
    console.print("  3. 💰 Start making sales automatically")
    console.print()
    console.print("[dim]Press Ctrl+C to exit | Refresh: python3 status.py[/dim]")

if __name__ == '__main__':
    show_status()
