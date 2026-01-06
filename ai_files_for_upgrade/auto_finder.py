#!/usr/bin/env python3
"""
Auto Product Finder & Marketer
Continuously finds trending products and auto-generates marketing campaigns
"""

import requests
import json
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
import random

console = Console()

class AutoProductFinder:
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.found_products = []
        self.marketed_products = []
        
    def search_trending_products(self):
        """Scrape and find trending products from multiple sources"""
        # Simulate finding products from different niches
        niches = [
            "Electronics", "Fashion", "Home & Garden", "Beauty", 
            "Sports & Outdoors", "Pet Supplies", "Baby Products"
        ]
        
        products = [
            # Electronics
            ("Wireless Earbuds", "Electronics", 15, 49.99),
            ("Smart Watch", "Electronics", 25, 89.99),
            ("LED Strip Lights", "Electronics", 8, 29.99),
            ("Phone Ring Light", "Electronics", 6, 19.99),
            ("Portable Charger", "Electronics", 12, 34.99),
            
            # Fashion
            ("Crossbody Bag", "Fashion", 18, 39.99),
            ("Oversized Sunglasses", "Fashion", 5, 24.99),
            ("Minimalist Watch", "Fashion", 20, 59.99),
            
            # Home & Garden
            ("Aroma Diffuser", "Home & Garden", 10, 29.99),
            ("Plant Grow Lights", "Home & Garden", 15, 44.99),
            ("Silicone Baking Mat", "Home & Garden", 7, 19.99),
            
            # Beauty
            ("Jade Roller", "Beauty", 6, 19.99),
            ("Hair Straightening Brush", "Beauty", 16, 39.99),
            ("Makeup Organizer", "Beauty", 9, 24.99),
            
            # Sports
            ("Resistance Bands Set", "Sports & Outdoors", 11, 29.99),
            ("Yoga Mat", "Sports & Outdoors", 14, 34.99),
            ("Water Bottle with Time Marker", "Sports & Outdoors", 8, 24.99),
            
            # Pets
            ("Automatic Pet Feeder", "Pet Supplies", 22, 59.99),
            ("Pet Hair Remover", "Pet Supplies", 7, 19.99),
            ("Interactive Cat Toy", "Pet Supplies", 9, 24.99),
            
            # Baby
            ("Baby Sleep Soother", "Baby Products", 18, 44.99),
            ("Silicone Feeding Set", "Baby Products", 10, 29.99),
        ]
        
        # Randomly select products to "find"
        found = random.sample(products, k=random.randint(3, 6))
        
        results = []
        for name, niche, cost, price in found:
            margin = ((price - cost) / price) * 100
            results.append({
                "name": name,
                "niche": niche,
                "cost": cost,
                "retail_price": price,
                "margin": round(margin, 1),
                "source": random.choice(["AliExpress", "Amazon", "DHGate", "Alibaba"]),
                "found_at": datetime.now().isoformat()
            })
        
        return results
    
    def analyze_product(self, product_name):
        """Analyze product market opportunity"""
        try:
            response = requests.post(
                f"{self.api_base}/api/analyze-product",
                json={"product_name": product_name},
                timeout=10
            )
            return response.json()
        except Exception as e:
            console.print(f"[red]Error analyzing {product_name}: {e}[/red]")
            return None
    
    def generate_marketing_campaign(self, product):
        """Auto-generate complete marketing campaign"""
        try:
            # Generate content
            content_response = requests.post(
                f"{self.api_base}/api/generate-content",
                json={
                    "product_name": product["name"],
                    "product_type": product["niche"].lower()
                },
                timeout=15
            )
            content = content_response.json()
            
            # Generate video script
            video_response = requests.post(
                f"{self.api_base}/api/generate-video-script",
                json={
                    "product_name": product["name"],
                    "product_type": product["niche"].lower()
                },
                timeout=15
            )
            video = video_response.json()
            
            campaign = {
                "product": product,
                "content": content,
                "video": video,
                "created_at": datetime.now().isoformat(),
                "platforms": ["Facebook", "Instagram", "TikTok", "Pinterest"],
                "status": "ready_to_launch"
            }
            
            return campaign
            
        except Exception as e:
            console.print(f"[red]Error generating campaign for {product['name']}: {e}[/red]")
            return None
    
    def save_campaign(self, campaign):
        """Save campaign to file"""
        filename = f"campaigns/{campaign['product']['name'].replace(' ', '_').lower()}_{int(time.time())}.json"
        
        import os
        os.makedirs("campaigns", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(campaign, f, indent=2)
        
        return filename
    
    def run_auto_discovery(self, cycles=3, delay=5):
        """Run automated product discovery and marketing"""
        console.print(Panel(
            "[bold cyan]🤖 AUTO PRODUCT FINDER & MARKETER[/bold cyan]\n"
            "[yellow]Continuously finding trending products and auto-generating marketing campaigns[/yellow]",
            border_style="cyan"
        ))
        
        for cycle in range(1, cycles + 1):
            console.print(f"\n{'='*80}")
            console.print(f"[bold magenta]🔄 CYCLE {cycle}/{cycles}[/bold magenta]")
            console.print(f"{'='*80}\n")
            
            # Step 1: Find products
            console.print("[yellow]🔍 Searching for trending products...[/yellow]")
            products = self.search_trending_products()
            
            # Display found products
            table = Table(title=f"✨ Found {len(products)} Trending Products")
            table.add_column("Product", style="cyan")
            table.add_column("Niche", style="green")
            table.add_column("Cost", style="yellow")
            table.add_column("Retail", style="magenta")
            table.add_column("Margin", style="green")
            table.add_column("Source", style="blue")
            
            for p in products:
                table.add_row(
                    p["name"],
                    p["niche"],
                    f"${p['cost']}",
                    f"${p['retail_price']}",
                    f"{p['margin']}%",
                    p["source"]
                )
            
            console.print(table)
            
            # Step 2: Analyze and market each product
            for i, product in enumerate(products, 1):
                console.print(f"\n[bold cyan]📊 Processing Product {i}/{len(products)}: {product['name']}[/bold cyan]")
                
                # Analyze
                console.print("[dim]→ Analyzing market opportunity...[/dim]")
                analysis = self.analyze_product(product['name'])
                
                if analysis:
                    console.print(f"  [green]✓[/green] Trend Score: {analysis['trend_score']}/100")
                    console.print(f"  [green]✓[/green] Profit Potential: {analysis['profit_potential']}/10")
                    
                    # Only market if good opportunity
                    if analysis['trend_score'] >= 70:
                        console.print("[dim]→ Generating marketing campaign...[/dim]")
                        campaign = self.generate_marketing_campaign(product)
                        
                        if campaign:
                            # Save campaign
                            filename = self.save_campaign(campaign)
                            
                            console.print(f"  [green]✓[/green] Generated ad headlines: {len(campaign['content']['ad_headlines'])}")
                            console.print(f"  [green]✓[/green] Generated video script: {campaign['video']['duration']}")
                            console.print(f"  [green]✓[/green] Target platforms: {', '.join(campaign['platforms'])}")
                            console.print(f"  [bold green]✓ Campaign saved: {filename}[/bold green]")
                            
                            self.marketed_products.append(campaign)
                    else:
                        console.print(f"  [yellow]⊘ Skipped (low trend score)[/yellow]")
                
                time.sleep(1)  # Rate limiting
            
            # Summary
            console.print(f"\n[bold green]✅ Cycle {cycle} Complete![/bold green]")
            console.print(f"  • Products found: {len(products)}")
            console.print(f"  • Campaigns created: {len([p for p in products if self.analyze_product(p['name']) and self.analyze_product(p['name'])['trend_score'] >= 70])}")
            
            if cycle < cycles:
                console.print(f"\n[dim]Waiting {delay} seconds before next cycle...[/dim]")
                time.sleep(delay)
        
        # Final summary
        console.print(f"\n{'='*80}")
        console.print("[bold magenta]📈 FINAL SUMMARY[/bold magenta]")
        console.print(f"{'='*80}\n")
        console.print(f"[green]Total campaigns created: {len(self.marketed_products)}[/green]")
        console.print(f"[cyan]All campaigns saved in: ./campaigns/[/cyan]")
        console.print("\n[bold green]🚀 Ready to launch marketing campaigns![/bold green]")

def main():
    finder = AutoProductFinder()
    
    # Run auto discovery
    finder.run_auto_discovery(cycles=3, delay=5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⏸️  Auto-discovery stopped by user[/yellow]")
    except requests.exceptions.ConnectionError:
        console.print("\n[bold red]❌ Error: Backend server not running![/bold red]")
        console.print("[yellow]Start the server with: python server.py[/yellow]\n")
