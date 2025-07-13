#!/usr/bin/env python3
"""
🌀 REM Dashboard Demo - Quick Showcase ✨
Demonstrates all enhanced features in a short demo
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("❌ Rich library required for demo")
    sys.exit(1)

def demo_showcase():
    """Quick demo of REM Dashboard features"""
    console = Console()
    
    # Demo header
    demo_header = """[bold bright_blue]🌀 REM DASHBOARD DEMO ✨[/bold bright_blue]

[bold yellow]Enhanced Features Implemented:[/bold yellow]

✅ [green]Live SR Updates[/green] - Personas update every 3 seconds
✅ [cyan]SR Heatmap View[/cyan] - Grouped by performance tiers (>0.90, 0.85-0.90, etc.)
✅ [magenta]Command History Panel[/magenta] - Logs major collapses and events
✅ [yellow]Dynamic Badge System[/yellow] - 🔥 Ignition, 🧊 Audit, 🌪️ Surge, 🚨 Alert
✅ [blue]Real-time Statistics[/blue] - Peak SR, collapse events, session metrics
✅ [red]Visual Collapse Events[/red] - Beautiful event visualization

[bold cyan]Live Dashboard Features:[/bold cyan]
• Automatic SR trending with persona-specific behaviors
• Real-time persona status indicators (●Active, ◐Resonant, ○Listening, ✖Dormant)  
• Event history with timestamps and severity levels
• Session statistics and peak performance tracking
• Responsive multi-panel layout with Rich TUI

[dim]Ready to launch full dashboard...[/dim]"""
    
    console.print(Panel(demo_header, border_style="bright_blue", padding=(1, 2)))
    
    console.print("\n🚀 [bold green]Starting REM Dashboard...[/bold green]")
    console.print("[dim]Press Ctrl+C in the dashboard to exit[/dim]\n")
    
    time.sleep(2)
    
    # Import and run dashboard
    from rem_dashboard import REMDashboard
    dashboard = REMDashboard()
    
    # Add some demo events
    console.print("🎭 [cyan]Adding demo events...[/cyan]")
    dashboard.add_badge("demo", "✨", "Demo Started", "Showcasing REM Dashboard features")
    dashboard.add_history_event("demo", "Dashboard Demo", "Demonstrating enhanced TUI features", ["All"], "info")
    
    time.sleep(1)
    dashboard.run()

if __name__ == "__main__":
    demo_showcase() 