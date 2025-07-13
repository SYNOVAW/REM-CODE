#!/usr/bin/env python3
# vocab_demo.py
"""
REM CODE Vocabulary Extension System Demo
Demonstrates strategic Latin verb expansion with persona-specific filtering
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from engine.vocabulary_manager import (
    get_vocabulary_manager, 
    get_persona_vocabulary, 
    get_vocabulary_stats,
    register_extended_verbs
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box

def create_demo_display():
    """Create beautiful demo display of vocabulary system"""
    console = Console()
    
    # Get vocabulary manager
    vocab_manager = get_vocabulary_manager()
    stats = get_vocabulary_stats()
    
    # Title
    console.print()
    console.print(Panel.fit(
        "🌀 REM CODE Strategic Vocabulary Extension System Demo",
        style="bold cyan",
        border_style="cyan"
    ))
    
    # Overall statistics
    console.print(f"\n📊 [bold]Overall Vocabulary Statistics[/bold]")
    stats_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Count", justify="right", style="green")
    
    stats_table.add_row("Core Latin Verbs", str(stats["core_verbs_count"]))
    stats_table.add_row("Extended Verbs", str(stats["extended_verbs_count"]))
    stats_table.add_row("Total Vocabulary", str(stats["total_verbs"]))
    
    console.print(stats_table)
    
    # Extended vocabulary sets by category
    console.print(f"\n🔠 [bold]Strategic Vocabulary Categories[/bold]")
    
    for category_name, category_data in stats["vocabulary_sets"].items():
        category_table = Table(
            title=f"{category_data['category']} ({category_data['count']} verbs)",
            show_header=False,
            box=box.SIMPLE
        )
        category_table.add_column("Verb", style="yellow")
        category_table.add_column("Description", style="dim")
        
        # Add description row
        category_table.add_row("[italic]Category:[/italic]", category_data['description'])
        category_table.add_row("", "")  # Spacer
        
        # Add verbs
        for verb in category_data['verbs']:
            meaning = get_verb_meaning(verb)
            category_table.add_row(f"[bold]{verb}[/bold]", meaning)
        
        console.print(category_table)
        console.print()
    
    # Persona-specific vocabularies
    console.print(f"👥 [bold]Persona-Specific Vocabulary Assignments[/bold]")
    
    persona_table = Table(show_header=True, header_style="bold blue", box=box.ROUNDED)
    persona_table.add_column("Persona", style="cyan", width=12)
    persona_table.add_column("Specialized Verbs", style="yellow")
    persona_table.add_column("Cognitive Focus", style="green")
    
    persona_focuses = {
        "JayRa": "Memory, reflection, recursion",
        "Ana": "Logic, validation, structure",
        "JayDen": "Creation, ignition, expression",
        "JayKer": "Humor, disruption, resonance",
        "JayTH": "Ethics, protection, trust",
        "JayLUX": "Design, elegance, form",
        "JAYX": "Monitoring, detection, vigilance"
    }
    
    for persona, verbs in stats["persona_vocabularies"].items():
        verb_list = ", ".join(verbs[:5]) + ("..." if len(verbs) > 5 else "")
        focus = persona_focuses.get(persona, "General cognitive processing")
        persona_table.add_row(persona, verb_list, focus)
    
    console.print(persona_table)
    
    # Phase-based vocabularies
    console.print(f"\n🌀 [bold]Cognitive Phase Vocabularies[/bold]")
    
    phase_table = Table(show_header=True, header_style="bold purple", box=box.ROUNDED)
    phase_table.add_column("Phase", style="magenta", width=12)
    phase_table.add_column("Priority Verbs", style="yellow")
    phase_table.add_column("Cognitive Purpose", style="green")
    
    phase_purposes = {
        "Genesis": "Initial creation and ideation",
        "Analysis": "Examination and parsing",
        "Synthesis": "Integration and harmony",
        "Collapse": "Recursive triggering",
        "Integration": "Final convergence"
    }
    
    for phase, verbs in stats["phase_vocabularies"].items():
        verb_list = ", ".join(sorted(verbs))
        purpose = phase_purposes.get(phase, "General processing")
        phase_table.add_row(phase, verb_list, purpose)
    
    console.print(phase_table)
    
    # Dynamic extension demo
    console.print(f"\n⚡ [bold]Dynamic Extension Capability Demo[/bold]")
    
    # Register some new verbs dynamically
    new_verbs = {
        "experimental": ["Experimenta", "Hypothesiza", "Valida"],
        "aesthetic": ["Beautifica", "Harmonica", "Poetica"]
    }
    
    register_extended_verbs(new_verbs)
    console.print("[green]✅ Successfully registered new verb categories![/green]")
    console.print(f"   • [cyan]Experimental:[/cyan] {', '.join(new_verbs['experimental'])}")
    console.print(f"   • [cyan]Aesthetic:[/cyan] {', '.join(new_verbs['aesthetic'])}")
    
    # Show persona filtering demo
    console.print(f"\n🎯 [bold]Persona Filtering Demo[/bold]")
    
    example_persona = "Ana"
    ana_verbs = get_persona_vocabulary(example_persona)
    console.print(f"Available vocabulary for [cyan]{example_persona}[/cyan]: {len(ana_verbs)} verbs")
    console.print(f"Sample: {', '.join(list(ana_verbs)[:8])}...")
    
    # Grammar extension preview
    console.print(f"\n📜 [bold]Grammar Extension Preview[/bold]")
    extension = vocab_manager.generate_grammar_extension()
    if extension.strip():
        console.print(Panel(
            extension.strip(), 
            title="Generated Grammar Extension",
            style="dim"
        ))
    
    console.print(f"\n[green]🎉 REM CODE vocabulary system ready for cognitive elegance![/green]")

def get_verb_meaning(verb: str) -> str:
    """Get meaning for demonstration purposes"""
    meanings = {
        "Recurre": "再帰せよ",
        "Phasea": "位相遷移せよ",
        "Synchrona": "同期せよ", 
        "Triggera": "発火させよ",
        "Resona": "共鳴せよ",
        "Confide": "信頼せよ",
        "Empathe": "共感せよ",
        "Ampara": "擁護せよ",
        "Explora": "探索せよ",
        "Hypotheca": "仮説を立てよ",
        "Testa": "試せ",
        "Detecta": "検出せよ",
        "Tokena": "トークン化せよ",
        "Lexema": "語彙単位に分解せよ",
        "Formala": "形式化せよ",
        "Tracea": "記録・トレースせよ",
        "Intona": "音を与えよ",
        "Eleganta": "優雅にせよ"
    }
    return meanings.get(verb, "操作的思考単位")

if __name__ == "__main__":
    try:
        create_demo_display()
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc() 