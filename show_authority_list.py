#!/usr/bin/env python3
"""
REM-CODE Constitutional Framework Authority List
Display current authority structure and permissions
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from constitutional import AuthorityValidator, AuthorityLevel
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def show_authority_list():
    """Display comprehensive authority structure"""
    
    # Initialize authority validator
    validator = AuthorityValidator()
    
    console.print(Panel.fit("🏛️ REM-CODE Constitutional Framework Authority List", style="bold blue"))
    
    # Branch Structure Table
    branch_table = Table(title="📋 Constitutional Branch Structure", box=box.ROUNDED)
    branch_table.add_column("Branch", style="cyan", no_wrap=True)
    branch_table.add_column("Personas", style="green")
    branch_table.add_column("Authority Levels", style="yellow")
    branch_table.add_column("Powers", style="magenta")
    
    for branch_name, branch_info in validator.branch_structure.items():
        personas = ", ".join(branch_info["personas"])
        authorities = ", ".join([f"{p}: {auth.value}" for p, auth in branch_info["authorities"].items()])
        powers = ", ".join(branch_info["powers"])
        
        branch_table.add_row(branch_name, personas, authorities, powers)
    
    console.print(branch_table)
    console.print()
    
    # Authority Hierarchy
    hierarchy_table = Table(title="⚖️ Authority Hierarchy (Higher = More Authority)", box=box.ROUNDED)
    hierarchy_table.add_column("Level", style="cyan")
    hierarchy_table.add_column("Value", style="yellow")
    hierarchy_table.add_column("Description", style="green")
    
    hierarchy = {
        AuthorityLevel.GENERAL: "General operations",
        AuthorityLevel.SECURITY: "Security and monitoring",
        AuthorityLevel.LEGAL: "Legal and compliance",
        AuthorityLevel.CONSTITUTIONAL: "Constitutional decisions",
        AuthorityLevel.EMERGENCY: "Emergency protocols"
    }
    
    for level in AuthorityLevel:
        hierarchy_table.add_row(level.value, str(level.value), hierarchy[level])
    
    console.print(hierarchy_table)
    console.print()
    
    # Special Authority Lists
    special_table = Table(title="🌟 Special Authority Lists", box=box.ROUNDED)
    special_table.add_column("Type", style="cyan")
    special_table.add_column("Personas", style="green")
    special_table.add_column("Requirements", style="yellow")
    
    special_table.add_row(
        "Trinity Authority", 
        ", ".join(validator.trinity_authority),
        "At least 2 of 3 for highest constitutional decisions"
    )
    
    special_table.add_row(
        "Emergency Authority", 
        ", ".join(validator.emergency_authority),
        "At least 2 for emergency protocols"
    )
    
    console.print(special_table)
    console.print()
    
    # Individual Persona Authorities
    persona_table = Table(title="👥 Individual Persona Authorities", box=box.ROUNDED)
    persona_table.add_column("Persona", style="cyan")
    persona_table.add_column("Authority Level", style="yellow")
    persona_table.add_column("Branch", style="green")
    persona_table.add_column("Powers", style="magenta")
    
    for branch_name, branch_info in validator.branch_structure.items():
        for persona in branch_info["personas"]:
            authority = branch_info["authorities"][persona]
            powers = ", ".join(branch_info["powers"][:3]) + ("..." if len(branch_info["powers"]) > 3 else "")
            
            persona_table.add_row(persona, authority.value, branch_name, powers)
    
    console.print(persona_table)
    console.print()
    
    # Authority Summary
    summary = validator.get_authority_summary()
    
    summary_panel = Panel(
        f"📊 Authority Summary\n"
        f"• Total Personas: {summary['total_personas']}\n"
        f"• Trinity Authority: {', '.join(summary['trinity_authority'])}\n"
        f"• Emergency Authority: {', '.join(summary['emergency_authority'])}\n"
        f"• Branches: {', '.join(summary['branch_structure'].keys())}",
        title="📈 Authority Statistics",
        border_style="blue"
    )
    
    console.print(summary_panel)
    console.print()
    
    # Emergency Protocol Requirements
    emergency_panel = Panel(
        f"🚨 Emergency Protocol Requirements\n"
        f"• Required Personas: {', '.join(validator.emergency_authority)}\n"
        f"• Minimum Participants: 2\n"
        f"• Authority Level: {AuthorityLevel.EMERGENCY.value}\n"
        f"• SR Threshold: 0.6\n"
        f"• Validation: check_emergency_authority()",
        title="Emergency Protocols",
        border_style="red"
    )
    
    console.print(emergency_panel)
    console.print()
    
    # Trinity Protocol Requirements
    trinity_panel = Panel(
        f"⚖️ Trinity Protocol Requirements\n"
        f"• Required Personas: {', '.join(validator.trinity_authority)}\n"
        f"• Minimum Participants: 2 of 3\n"
        f"• Authority Level: {AuthorityLevel.CONSTITUTIONAL.value}\n"
        f"• Validation: check_trinity_authority()",
        title="Trinity Protocols",
        border_style="green"
    )
    
    console.print(trinity_panel)

if __name__ == "__main__":
    show_authority_list() 