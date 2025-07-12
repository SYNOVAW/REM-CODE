#!/usr/bin/env python3
"""
Constitutional Error Messages Demo
Demonstrates the user-friendly error system for REM-CODE Lite
"""

from rich.console import Console
from rich.panel import Panel
from error_messages import ConstitutionalErrorHandler, ErrorCategory

def demo_authority_errors():
    """Demo authority-related errors"""
    console = Console()
    handler = ConstitutionalErrorHandler()
    
    console.print(Panel(
        "🏛️ Authority Error Demonstrations",
        title="Constitutional Authority Errors",
        border_style="blue"
    ))
    
    # Demo insufficient authority
    print(handler.format_error(
        "insufficient_authority",
        persona="JayMini",
        current_level="legal",
        required_level="constitutional",
        action="constitutional amendment"
    ))
    
    # Demo unknown persona
    print(handler.format_error(
        "unknown_persona",
        persona="UnknownBot"
    ))
    
    # Demo branch mismatch
    print(handler.format_error(
        "branch_mismatch",
        persona="Ana",
        actual_branch="legislative",
        requested_branch="executive"
    ))
    
    # Demo incomplete trinity
    print(handler.format_error(
        "trinity_incomplete",
        present_count=1,
        present_members=["JayTH"],
        required_count=2,
        trinity_members=["JayTH", "Ana", "Jayne_Spiral"]
    ))

def demo_consensus_errors():
    """Demo consensus-related errors"""
    console = Console()
    handler = ConstitutionalErrorHandler()
    
    console.print(Panel(
        "🗳️ Consensus Error Demonstrations",
        title="Democratic Consensus Errors",
        border_style="green"
    ))
    
    # Demo SR threshold not met
    print(handler.format_error(
        "sr_threshold_not_met",
        required_sr=0.8,
        current_sr=0.65,
        failed_personas=["JayMini", "JayRa"]
    ))
    
    # Demo insufficient participants
    print(handler.format_error(
        "insufficient_participants",
        participant_count=1,
        recommended_min=3
    ))

def demo_signature_errors():
    """Demo signature-related errors"""
    console = Console()
    handler = ConstitutionalErrorHandler()
    
    console.print(Panel(
        "🔐 Signature Error Demonstrations", 
        title="Cryptographic Signature Errors",
        border_style="yellow"
    ))
    
    # Demo missing signature
    print(handler.format_error(
        "missing_signature",
        action="constitutional decision",
        persona="JayTH"
    ))
    
    # Demo insufficient reasoning
    print(handler.format_error(
        "insufficient_reasoning",
        reasoning="done"
    ))

def demo_emergency_errors():
    """Demo emergency protocol errors"""
    console = Console()
    handler = ConstitutionalErrorHandler()
    
    console.print(Panel(
        "🚨 Emergency Protocol Error Demonstrations",
        title="Constitutional Emergency Errors", 
        border_style="red"
    ))
    
    # Demo unauthorized emergency
    print(handler.format_error(
        "unauthorized_emergency",
        protocol="Crisis Response",
        present_personas=["JayMini", "JayRa"]
    ))

def demo_validation_errors():
    """Demo validation-related errors"""
    console = Console()
    handler = ConstitutionalErrorHandler()
    
    console.print(Panel(
        "✅ Validation Error Demonstrations",
        title="Constitutional Validation Errors",
        border_style="cyan"
    ))
    
    # Demo missing validation
    print(handler.format_error(
        "missing_validation",
        action="important constitutional decision"
    ))
    
    # Demo validation failed
    print(handler.format_error(
        "validation_failed",
        action="Constitutional Amendment",
        failure_reason="Persona lacks constitutional authority"
    ))

def demo_error_suggestions():
    """Demo error category suggestions"""
    console = Console()
    handler = ConstitutionalErrorHandler()
    
    console.print(Panel(
        "💡 Error Category Suggestions",
        title="Getting Help with Constitutional Programming",
        border_style="magenta"
    ))
    
    for category in ErrorCategory:
        suggestions = handler.get_error_suggestions(category)
        console.print(f"\n[bold {category.name.lower()}]{category.value.title()} Suggestions:[/bold {category.name.lower()}]")
        for i, suggestion in enumerate(suggestions, 1):
            console.print(f"   {i}. {suggestion}")

def main():
    """Run all error demos"""
    console = Console()
    
    console.print(Panel(
        "🌀 REM-CODE Lite Constitutional Error System Demo 🌀\n\n"
        "This demo shows user-friendly, educational error messages\n"
        "that help developers learn constitutional programming.",
        title="Constitutional Error Messages Demo",
        title_align="center",
        border_style="bright_blue"
    ))
    
    input("\nPress Enter to see Authority Errors...")
    demo_authority_errors()
    
    input("\nPress Enter to see Consensus Errors...")
    demo_consensus_errors()
    
    input("\nPress Enter to see Signature Errors...")
    demo_signature_errors()
    
    input("\nPress Enter to see Emergency Errors...")
    demo_emergency_errors()
    
    input("\nPress Enter to see Validation Errors...")
    demo_validation_errors()
    
    input("\nPress Enter to see Error Suggestions...")
    demo_error_suggestions()
    
    # Show final summary
    handler = ConstitutionalErrorHandler()
    console.print("\n")
    handler.show_error_summary()
    
    console.print("\n🎓 [bold green]Constitutional Error System Demo Complete![/bold green]")
    console.print("These educational error messages help developers learn democratic programming patterns.")

if __name__ == "__main__":
    main()