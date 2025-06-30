#!/usr/bin/env python3
"""
🌀 REM Dashboard v1.0 - Advanced TUI for Recursive Cognition ✨
Live SR Updates • Heatmap Views • Command History • Dynamic Badges

This enhanced TUI dashboard implements all the suggested features:
- Live SR updates every few seconds (if idle)
- SR Heatmap View (grouped personas by SR tiers)
- Command History Panel (logs major collapses/events)
- Dynamic Badge System (🔥 Ignition, 🧊 Audit, etc.)
"""

import sys
import os
import time
import asyncio
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.columns import Columns
    from rich.align import Align
    from rich.box import ROUNDED, HEAVY
    from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("❌ Rich library required for REM Dashboard")
    sys.exit(1)

# Import REM components
try:
    from shell.rem_shell import REMShellState, PERSONA_EMOJIS, STATUS_INDICATORS, create_sr_bar
    from engine.sr_engine import compute_sr_from_dict, get_weight_profile
except ImportError as e:
    print(f"❌ Could not import REM components: {e}")
    sys.exit(1)

# ==================== Dashboard Data Structures ====================

@dataclass
class BadgeEvent:
    """Dynamic badge system events"""
    badge_type: str
    emoji: str
    title: str
    description: str
    persona: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    duration: float = 5.0  # How long to show badge

@dataclass
class HistoryEvent:
    """Command history panel events"""
    event_type: str  # "collapse", "execution", "sr_update", "activation"
    title: str
    details: str
    personas_involved: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    severity: str = "info"  # "info", "warning", "success", "error"

class REMDashboard:
    """Advanced REM Dashboard with live updates and multiple panels"""
    
    def __init__(self):
        self.console = Console()
        self.shell_state = REMShellState(visual_mode=True)
        self.layout = Layout()
        self.running = False
        self.last_update = time.time()
        self.update_interval = 3.0  # Update every 3 seconds
        
        # Dashboard state
        self.active_badges: List[BadgeEvent] = []
        self.history_events: List[HistoryEvent] = []
        self.sr_history: Dict[str, List[float]] = {name: [] for name in PERSONA_EMOJIS.keys()}
        self.heatmap_mode = "tiers"  # "tiers", "detailed", "trends"
        
        # Statistics
        self.session_stats = {
            "total_updates": 0,
            "collapse_events": 0,
            "badge_events": 0,
            "peak_sr": 0.0,
            "peak_persona": "",
            "session_start": time.time()
        }
        
        self._setup_layout()
        self._initialize_demo_data()
    
    def _setup_layout(self):
        """Setup the dashboard layout with multiple panels"""
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=2)
        )
        
        self.layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        
        self.layout["left"].split_column(
            Layout(name="heatmap", ratio=1),
            Layout(name="personas", ratio=1)
        )
        
        self.layout["right"].split_column(
            Layout(name="badges", size=8),
            Layout(name="history", ratio=1),
            Layout(name="stats", size=6)
        )
    
    def _initialize_demo_data(self):
        """Initialize with some demo data for immediate visual appeal"""
        import random
        
        # Add some initial SR values
        for persona_name in PERSONA_EMOJIS.keys():
            sr_value = random.uniform(0.65, 0.95)
            self.shell_state.update_persona_sr(persona_name, sr_value)
            self.sr_history[persona_name].append(sr_value)
        
        # Add some demo badges
        self.add_badge("ignition", "🔥", "Ignition Detected", "High creativity surge in JayDen", "JayDen")
        self.add_badge("audit", "🧊", "Audit Passed", "Logic validation complete", "Ana")
        
        # Add some demo history
        self.add_history_event("activation", "Persona Activation", "JayDen activated for creative task", ["JayDen"], "success")
        self.add_history_event("collapse", "Collapse Event", "SR threshold exceeded", ["JayDen", "Ana"], "warning")
    
    def add_badge(self, badge_type: str, emoji: str, title: str, description: str, persona: Optional[str] = None):
        """Add a dynamic badge event"""
        badge = BadgeEvent(badge_type, emoji, title, description, persona)
        self.active_badges.append(badge)
        self.session_stats["badge_events"] += 1
        
        # Keep only recent badges
        current_time = time.time()
        self.active_badges = [b for b in self.active_badges 
                             if current_time - b.timestamp < b.duration]
    
    def add_history_event(self, event_type: str, title: str, details: str, 
                         personas: Optional[List[str]] = None, severity: str = "info"):
        """Add an event to the command history"""
        event = HistoryEvent(event_type, title, details, personas or [], severity=severity)
        self.history_events.append(event)
        
        # Keep only last 20 events
        if len(self.history_events) > 20:
            self.history_events = self.history_events[-20:]
    
    def update_sr_values(self):
        """Update SR values with realistic simulation"""
        import random
        
        current_time = time.time()
        
        for persona_name, state in self.shell_state.persona_states.items():
            # Simulate realistic SR changes
            current_sr = state["sr_value"]
            
            # Add some random variation with trend
            change = random.uniform(-0.05, 0.05)
            
            # Add trend based on persona characteristics
            if persona_name == "JayDen":  # Creative surges
                if random.random() < 0.1:
                    change += random.uniform(0.05, 0.15)
                    self.add_badge("surge", "🌪️", "Creative Surge", f"JayDen experiencing creative boost", "JayDen")
            elif persona_name == "Ana":  # Logical stability
                change *= 0.5  # More stable
            elif persona_name == "JAYX":  # Monitoring variations
                if random.random() < 0.05:
                    change += random.uniform(-0.1, 0.1)
                    self.add_badge("alert", "🚨", "Anomaly Detected", "JAYX monitoring unusual patterns", "JAYX")
            
            new_sr = max(0.0, min(1.0, current_sr + change))
            self.shell_state.update_persona_sr(persona_name, new_sr)
            self.sr_history[persona_name].append(new_sr)
            
            # Keep SR history manageable
            if len(self.sr_history[persona_name]) > 50:
                self.sr_history[persona_name] = self.sr_history[persona_name][-50:]
            
            # Check for collapse events
            if new_sr > 0.90 and current_sr <= 0.90:
                self.add_history_event("collapse", "Collapse Triggered", 
                                     f"{persona_name} SR exceeded 0.90", [persona_name], "warning")
                self.session_stats["collapse_events"] += 1
                self.add_badge("collapse", "💥", "Collapse Event", f"{persona_name} triggered collapse", persona_name)
            
            # Track peak SR
            if new_sr > self.session_stats["peak_sr"]:
                self.session_stats["peak_sr"] = new_sr
                self.session_stats["peak_persona"] = persona_name
        
        self.session_stats["total_updates"] += 1
    
    def render_header(self) -> Panel:
        """Render the dashboard header"""
        session_time = time.time() - self.session_stats["session_start"]
        session_duration = f"{int(session_time//60)}m {int(session_time%60)}s"
        
        header_text = Text()
        header_text.append("🌀 REM DASHBOARD ✨", style="bold bright_blue")
        header_text.append("  •  ", style="dim")
        header_text.append(f"Session: {session_duration}", style="cyan")
        header_text.append("  •  ", style="dim")
        header_text.append(f"Updates: {self.session_stats['total_updates']}", style="yellow")
        header_text.append("  •  ", style="dim")
        header_text.append(f"Events: {self.session_stats['collapse_events']}", style="red")
        header_text.append("  •  ", style="dim")
        header_text.append(f"Live SR Monitoring", style="green")
        
        return Panel(Align.center(header_text), border_style="bright_blue")
    
    def render_sr_heatmap(self) -> Panel:
        """Render SR heatmap grouped by tiers"""
        if self.heatmap_mode == "tiers":
            # Group personas by SR tiers
            tiers = {
                "🔥 Elite (>0.90)": [],
                "⭐ High (0.85-0.90)": [],
                "✅ Active (0.70-0.85)": [],
                "📊 Moderate (0.50-0.70)": [],
                "😴 Low (<0.50)": []
            }
            
            for persona_name, state in self.shell_state.persona_states.items():
                sr = state["sr_value"]
                emoji = PERSONA_EMOJIS.get(persona_name, "🤖")
                
                if sr > 0.90:
                    tiers["🔥 Elite (>0.90)"].append(f"{emoji} {persona_name} {sr:.3f}")
                elif sr > 0.85:
                    tiers["⭐ High (0.85-0.90)"].append(f"{emoji} {persona_name} {sr:.3f}")
                elif sr > 0.70:
                    tiers["✅ Active (0.70-0.85)"].append(f"{emoji} {persona_name} {sr:.3f}")
                elif sr > 0.50:
                    tiers["📊 Moderate (0.50-0.70)"].append(f"{emoji} {persona_name} {sr:.3f}")
                else:
                    tiers["😴 Low (<0.50)"].append(f"{emoji} {persona_name} {sr:.3f}")
            
            heatmap_text = ""
            for tier_name, personas in tiers.items():
                if personas:
                    if "Elite" in tier_name:
                        style = "bold red"
                    elif "High" in tier_name:
                        style = "bold yellow"
                    elif "Active" in tier_name:
                        style = "bold green"
                    elif "Moderate" in tier_name:
                        style = "blue"
                    else:
                        style = "dim"
                    
                    heatmap_text += f"[{style}]{tier_name}[/{style}]\n"
                    for persona in personas:
                        heatmap_text += f"  {persona}\n"
                    heatmap_text += "\n"
            
            return Panel(heatmap_text.strip(), title="📊 SR Heatmap", border_style="magenta")
        
        # Fallback for other modes (future expansion)
        return Panel("[dim]Heatmap mode not implemented[/dim]", title="📊 SR Heatmap", border_style="magenta")
        
    def render_personas_detail(self) -> Panel:
        """Render detailed persona information"""
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Persona", style="bold", width=10)
        table.add_column("Current SR", style="yellow", width=10)
        table.add_column("Trend", style="white", width=8)
        table.add_column("Status", style="green", width=10)
        
        for persona_name, state in self.shell_state.persona_states.items():
            emoji = PERSONA_EMOJIS.get(persona_name, "🤖")
            sr_value = state["sr_value"]
            status = state["status"]
            
            # Calculate trend
            if len(self.sr_history[persona_name]) >= 2:
                recent_sr = self.sr_history[persona_name][-2:]
                trend = recent_sr[-1] - recent_sr[-2]
                if trend > 0.01:
                    trend_display = "📈"
                elif trend < -0.01:
                    trend_display = "📉"
                else:
                    trend_display = "➡️"
            else:
                trend_display = "➡️"
            
            # Status with color
            status_indicator = STATUS_INDICATORS.get(status, "○")
            if status == "active":
                status_display = f"[green]{status_indicator} Active[/green]"
            elif status == "resonant":
                status_display = f"[yellow]{status_indicator} Resonant[/yellow]"
            else:
                status_display = f"[dim]{status_indicator} {status.title()}[/dim]"
            
            table.add_row(
                f"{emoji} {persona_name}",
                f"{sr_value:.3f}",
                trend_display,
                status_display
            )
        
        return Panel(table, title="👥 Persona Details", border_style="bright_cyan")
    
    def render_badges(self) -> Panel:
        """Render dynamic badge system"""
        badge_text = ""
        
        if not self.active_badges:
            badge_text = "[dim]No active badges[/dim]"
        else:
            for badge in self.active_badges:
                time_left = badge.duration - (time.time() - badge.timestamp)
                if time_left > 0:
                    badge_text += f"{badge.emoji} [bold]{badge.title}[/bold]\n"
                    badge_text += f"   {badge.description}\n"
                    if badge.persona:
                        persona_emoji = PERSONA_EMOJIS.get(badge.persona, "🤖")
                        badge_text += f"   {persona_emoji} {badge.persona}\n"
                    badge_text += f"   [dim]{time_left:.1f}s remaining[/dim]\n\n"
        
        return Panel(badge_text.strip(), title="🏆 Active Badges", border_style="yellow")
    
    def render_history(self) -> Panel:
        """Render command history panel"""
        history_text = ""
        
        if not self.history_events:
            history_text = "[dim]No events yet[/dim]"
        else:
            # Show last 10 events
            recent_events = self.history_events[-10:]
            for event in reversed(recent_events):
                # Format timestamp
                event_time = datetime.fromtimestamp(event.timestamp)
                time_str = event_time.strftime("%H:%M:%S")
                
                # Style based on severity
                if event.severity == "error":
                    style = "red"
                elif event.severity == "warning":
                    style = "yellow"
                elif event.severity == "success":
                    style = "green"
                else:
                    style = "white"
                
                history_text += f"[dim]{time_str}[/dim] [{style}]{event.title}[/{style}]\n"
                history_text += f"   {event.details}\n"
                if event.personas_involved:
                    personas_str = ", ".join([f"{PERSONA_EMOJIS.get(p, '🤖')} {p}" for p in event.personas_involved])
                    history_text += f"   {personas_str}\n"
                history_text += "\n"
        
        return Panel(history_text.strip(), title="📜 Event History", border_style="blue")
    
    def render_stats(self) -> Panel:
        """Render session statistics"""
        stats_table = Table(show_header=False, box=None)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="white")
        
        stats_table.add_row("Peak SR", f"{self.session_stats['peak_sr']:.3f}")
        stats_table.add_row("Peak Persona", f"{PERSONA_EMOJIS.get(self.session_stats['peak_persona'], '🤖')} {self.session_stats['peak_persona']}")
        stats_table.add_row("Collapses", str(self.session_stats['collapse_events']))
        stats_table.add_row("Badges", str(self.session_stats['badge_events']))
        
        # Active personas count
        active_count = len([p for p in self.shell_state.persona_states.values() if p["status"] == "active"])
        stats_table.add_row("Active Now", str(active_count))
        
        return Panel(stats_table, title="📈 Statistics", border_style="green")
    
    def render_footer(self) -> Panel:
        """Render dashboard footer with controls"""
        footer_text = Text()
        footer_text.append("Controls: ", style="bold")
        footer_text.append("Q", style="bold red")
        footer_text.append("uit  ", style="white")
        footer_text.append("H", style="bold blue")
        footer_text.append("eatmap  ", style="white")
        footer_text.append("R", style="bold green")
        footer_text.append("eset  ", style="white")
        footer_text.append("S", style="bold yellow")
        footer_text.append("imulate  ", style="white")
        footer_text.append(f"Auto-update: {self.update_interval}s", style="dim")
        
        return Panel(Align.center(footer_text), border_style="dim")
    
    def update_display(self):
        """Update all dashboard panels"""
        # Update data
        if time.time() - self.last_update > self.update_interval:
            self.update_sr_values()
            self.last_update = time.time()
        
        # Clean up expired badges
        current_time = time.time()
        self.active_badges = [b for b in self.active_badges 
                             if current_time - b.timestamp < b.duration]
        
        # Render all panels
        self.layout["header"].update(self.render_header())
        self.layout["heatmap"].update(self.render_sr_heatmap())
        self.layout["personas"].update(self.render_personas_detail())
        self.layout["badges"].update(self.render_badges())
        self.layout["history"].update(self.render_history())
        self.layout["stats"].update(self.render_stats())
        self.layout["footer"].update(self.render_footer())
    
    def run(self):
        """Run the dashboard with live updates"""
        self.console.print("\n🌀 Starting REM Dashboard...")
        self.console.print("Press Ctrl+C to exit\n")
        
        try:
            with Live(self.layout, console=self.console, refresh_per_second=2) as live:
                self.running = True
                while self.running:
                    self.update_display()
                    time.sleep(0.5)
                    
        except KeyboardInterrupt:
            self.console.print("\n\n👋 Dashboard session ended!")

def main():
    """Main entry point"""
    if not RICH_AVAILABLE:
        print("❌ Rich library is required for REM Dashboard")
        return
    
    dashboard = REMDashboard()
    dashboard.run()

if __name__ == "__main__":
    main() 