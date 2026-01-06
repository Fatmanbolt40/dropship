#!/usr/bin/env python3
"""
Live Demo Client - Watch your AI work in real-time
"""

import requests
import json
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

console = Console()

BASE_URL = "http://localhost:8000"

def print_header():
    console.print("\n[bold magenta]🚀 DROPSHIP AI - LIVE DEMONSTRATION[/bold magenta]")
    console.print("[cyan]Watch your AI analyze products and generate content in real-time[/cyan]\n")

def analyze_product(product_name):
    """Analyze product with live AI"""
    console.print(f"\n[yellow]🔍 Analyzing: {product_name}[/yellow]")
    console.print("[dim]Calling AI market analysis...[/dim]")
    
    response = requests.post(
        f"{BASE_URL}/api/analyze-product",
        json={"product_name": product_name}
    )
    
    data = response.json()
    
    # Display results
    console.print(Panel(
        f"[bold green]Trend Score: {data['trend_score']}/100[/bold green]\n"
        f"[bold cyan]✅ {data['recommendation']}[/bold cyan]\n\n"
        f"👥 Target: {data['target_audience']}\n"
        f"💰 Profit Potential: {data['profit_potential']}/10\n"
        f"📈 Market: {data['market_saturation']}",
        title=f"📊 {data['product_name']}",
        border_style="green"
    ))
    
    return data

def generate_content(product_name):
    """Generate AI content"""
    console.print(f"\n[yellow]✨ Generating AI content for: {product_name}[/yellow]")
    console.print("[dim]AI is writing product description and ads...[/dim]")
    
    response = requests.post(
        f"{BASE_URL}/api/generate-content",
        json={"product_name": product_name, "product_type": "consumer_electronics"}
    )
    
    data = response.json()
    
    # Display description
    console.print(Panel(
        data['description'],
        title="📝 AI-Generated Product Description",
        border_style="blue"
    ))
    
    # Display ad headlines
    console.print("\n[bold]🎯 AI-Generated Ad Headlines:[/bold]")
    for i, headline in enumerate(data['ad_headlines'], 1):
        console.print(f"  {i}. [cyan]{headline}[/cyan]")
    
    # Display target audiences
    console.print("\n[bold]👥 Target Audiences:[/bold]")
    for audience in data['target_audiences']:
        console.print(f"  • [green]{audience['name']}[/green] - {audience['platforms']}")
    
    return data

def generate_video_script(product_name):
    """Generate video script"""
    console.print(f"\n[yellow]🎬 Creating TikTok/Instagram script for: {product_name}[/yellow]")
    console.print("[dim]AI is writing your viral video script...[/dim]")
    
    response = requests.post(
        f"{BASE_URL}/api/generate-video-script",
        json={"product_name": product_name, "product_type": "consumer_electronics"}
    )
    
    data = response.json()
    
    console.print(Panel(
        f"⏱️  Duration: {data['duration']}\n\n" +
        "\n\n".join([
            f"[bold cyan]{section['time']}[/bold cyan]\n"
            f"🎤 {section['voiceover']}\n"
            f"📹 {section['visual']}\n"
            f"📝 {section['overlay']}"
            for section in data['script_sections']
        ]) +
        f"\n\n[bold]🔗 CTA:[/bold] {data['cta']}\n"
        f"[bold]#️⃣  Hashtags:[/bold] {' '.join(data['hashtags'])}",
        title="🎬 TikTok/Instagram Video Script",
        border_style="magenta"
    ))
    
    return data

def main():
    print_header()
    
    # Test products
    products = [
        "Wireless Earbuds",
        "Smart Water Bottle",
        "LED Strip Lights"
    ]
    
    for product in products:
        console.print(f"\n{'='*70}")
        console.print(f"[bold white]Testing Product: {product}[/bold white]")
        console.print(f"{'='*70}")
        
        # Run analysis
        analysis = analyze_product(product)
        time.sleep(1)
        
        # Generate content
        content = generate_content(product)
        time.sleep(1)
        
        # Generate video script
        video = generate_video_script(product)
        
        console.print("\n[bold green]✅ Complete![/bold green]")
        time.sleep(2)
    
    console.print("\n\n[bold magenta]🔥 LIVE DEMO COMPLETE![/bold magenta]")
    console.print("[cyan]Your AI is working perfectly and ready for your client![/cyan]")
    console.print(f"\n[dim]API Server: {BASE_URL}[/dim]")
    console.print(f"[dim]Dashboard: file://{__file__.replace('test_live.py', 'dashboard.html')}[/dim]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo stopped by user[/yellow]")
    except requests.exceptions.ConnectionError:
        console.print("\n[bold red]❌ Error: Backend server not running![/bold red]")
        console.print("[yellow]Start the server with: python server.py[/yellow]\n")
