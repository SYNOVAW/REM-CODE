#!/usr/bin/env python3
"""
REM-CODE Lite Interactive Constitutional Programming Tutorial
Learn constitutional programming step-by-step with hands-on examples
"""

import os
import sys
import time
from typing import Dict, List, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import REM-CODE components
try:
    from engine.rem_executor import REMExecutor
    from constitutional.constitutional_engine import ConstitutionalEngine
    from parser.grammar_transformer import GrammarTransformer
except ImportError:
    print("Warning: REM-CODE components not fully available. Tutorial will run in demo mode.")

class InteractiveConstitutionalTutorial:
    """Interactive tutorial for learning constitutional programming with REM-CODE Lite"""
    
    def __init__(self):
        self.console = Console()
        self.lesson_completed = {}
        self.user_progress = {}
        self.demo_mode = True  # Set to False when components are available
        
    def welcome(self):
        """Display welcome message and tutorial overview"""
        welcome_text = """
🌀 Welcome to REM-CODE Lite Interactive Tutorial! 🌀

Learn Constitutional Programming step-by-step:
• Democratic Multi-Agent Systems
• Cryptographic Accountability  
• Consensus-Driven Decision Making
• Constitutional Governance in Code

This tutorial will teach you to program democratically with constitutional validation.
        """
        
        self.console.print(Panel(
            welcome_text.strip(),
            title="Constitutional Programming Tutorial",
            title_align="center",
            border_style="blue"
        ))
        
        if not Confirm.ask("Ready to start your constitutional programming journey?"):
            self.console.print("👋 Come back when you're ready to democratize your code!")
            return False
        return True
    
    def show_lesson_menu(self) -> int:
        """Display lesson selection menu"""
        lessons = [
            "🏛️  Authority Validation - Learn constitutional authority systems",
            "🗳️  Democratic Consensus - Master SR-based consensus mechanisms", 
            "🚨 Emergency Protocols - Implement constitutional crisis management",
            "⚖️  Multi-Branch Governance - Build separation of powers",
            "✅ Validation & Compliance - Ensure constitutional compliance",
            "🎓 Advanced Patterns - Complex constitutional programming",
            "🔍 View Progress & Exit"
        ]
        
        table = Table(title="Constitutional Programming Lessons", show_header=False)
        table.add_column("Lesson", style="cyan")
        
        for i, lesson in enumerate(lessons, 1):
            status = "✅" if self.lesson_completed.get(i, False) else "📝"
            table.add_row(f"{i}. {status} {lesson}")
        
        self.console.print(table)
        
        while True:
            try:
                choice = int(Prompt.ask("Select lesson (1-7)", default="1"))
                if 1 <= choice <= 7:
                    return choice
                self.console.print("Please enter a number between 1 and 7")
            except ValueError:
                self.console.print("Please enter a valid number")
    
    def lesson_1_authority(self):
        """Lesson 1: Authority Validation"""
        self.console.print(Panel(
            "🏛️ Lesson 1: Authority Validation\n\n"
            "Learn how constitutional authority ensures only qualified personas\n"
            "can perform specific actions in democratic systems.",
            title="Constitutional Authority",
            border_style="green"
        ))
        
        # Explain concept
        self.console.print("\n📚 [bold blue]Core Concept:[/bold blue]")
        self.console.print(
            "Authority constructs ensure democratic accountability by requiring\n"
            "specific personas to have appropriate constitutional levels before\n"
            "performing actions that affect system governance."
        )
        
        # Show example
        example_code = '''// Basic constitutional authority
Authority JayTH requires Constitutional:
    JayTH.Cogita "constitutional framework analysis"
    JayTH.Declara "constitutional interpretation complete"
    Sign "Demo #001" by JayTH Reason "Constitutional authority exercised"'''
        
        self.console.print("\n💡 [bold yellow]Example Code:[/bold yellow]")
        self.console.print(Syntax(example_code, "javascript", theme="monokai"))
        
        # Interactive exercise
        self.console.print("\n🎯 [bold green]Your Turn![/bold green]")
        self.console.print("Create an authority block for persona 'Ana' with 'Judicial' branch assignment:")
        
        user_code = Prompt.ask("Enter your authority code", 
                              default="Authority Ana as Judicial:")
        
        if "Authority" in user_code and "Ana" in user_code:
            self.console.print("✅ [green]Excellent! You understand authority validation![/green]")
            self.lesson_completed[1] = True
        else:
            self.console.print("💡 [yellow]Try: Authority Ana as Judicial:[/yellow]")
            
        self.wait_for_continue()
    
    def lesson_2_consensus(self):
        """Lesson 2: Democratic Consensus"""
        self.console.print(Panel(
            "🗳️ Lesson 2: Democratic Consensus\n\n"
            "Master Synchrony Rate (SR) based consensus mechanisms\n"
            "for collective decision-making in democratic systems.",
            title="Democratic Consensus",
            border_style="green"
        ))
        
        # Explain SR concept
        self.console.print("\n📚 [bold blue]Synchrony Rate (SR):[/bold blue]")
        self.console.print(
            "SR measures how well personas are synchronized with democratic decisions.\n"
            "Higher SR = stronger consensus. Constitutional decisions require SR ≥ 0.9"
        )
        
        # Show example
        example_code = '''// Democratic consensus example
Consensus SR >= 0.8 by JayKer, JayMini:
    JayKer.Crea "innovative democratic solution"
    JayMini.Coordina "consensus coordination protocol"
    Sign "Consensus #001" by JayKer Reason "Democratic innovation"'''
        
        self.console.print("\n💡 [bold yellow]Example Code:[/bold yellow]")
        self.console.print(Syntax(example_code, "javascript", theme="monokai"))
        
        # Interactive SR calculator
        self.console.print("\n🎯 [bold green]SR Calculator Exercise![/bold green]")
        persona_count = int(Prompt.ask("How many personas in consensus?", default="3"))
        threshold = float(Prompt.ask("What SR threshold? (0.0-1.0)", default="0.8"))
        
        self.console.print(f"\n📊 For {persona_count} personas with SR ≥ {threshold}:")
        self.console.print(f"   • Each persona needs minimum {threshold:.1%} agreement")
        self.console.print(f"   • Collective decision strength: {threshold * persona_count:.1f}/{persona_count}")
        
        if threshold >= 0.9:
            self.console.print("🏛️ [bold blue]Constitutional-level consensus![/bold blue]")
        elif threshold >= 0.75:
            self.console.print("⚖️ [bold yellow]Legislative-level consensus[/bold yellow]")
        else:
            self.console.print("🔧 [bold green]Administrative-level consensus[/bold green]")
            
        self.lesson_completed[2] = True
        self.wait_for_continue()
    
    def lesson_3_emergency(self):
        """Lesson 3: Emergency Protocols"""
        self.console.print(Panel(
            "🚨 Lesson 3: Emergency Protocols\n\n"
            "Learn constitutional crisis management with enhanced\n"
            "validation and emergency authority systems.",
            title="Emergency Constitutional Protocols",
            border_style="red"
        ))
        
        # Explain emergency hierarchy
        self.console.print("\n📚 [bold blue]Emergency Authority Hierarchy:[/bold blue]")
        emergency_table = Table(show_header=True, header_style="bold red")
        emergency_table.add_column("Level", style="red")
        emergency_table.add_column("Authority", style="yellow")
        emergency_table.add_column("Required Personas", style="cyan")
        
        emergency_table.add_row("Basic", "Emergency Override", "JayTH, JAYX")
        emergency_table.add_row("Named", "Emergency Protocol", "JayTH, JAYX, Jayne_Spiral")
        emergency_table.add_row("Supreme", "Trinity Authorization", "2 of 3 Trinity (JayTH, Ana, Jayne_Spiral)")
        
        self.console.print(emergency_table)
        
        # Show example
        example_code = '''// Trinity emergency authorization
Emergency trinity authorization:
    Trinity coordination requires 2 of 3:
        Invoke JayTH, Ana, Jayne_Spiral:
            JayTH.Vigila "supreme constitutional crisis detection"
            Ana.Defende "constitutional legal system protection"
            Activare "supreme constitutional crisis protocol"'''
        
        self.console.print("\n💡 [bold yellow]Supreme Emergency Example:[/bold yellow]")
        self.console.print(Syntax(example_code, "javascript", theme="monokai"))
        
        # Emergency scenario simulation
        self.console.print("\n🎯 [bold red]Emergency Scenario![/bold red]")
        self.console.print("A constitutional crisis requires immediate response!")
        
        emergency_type = Prompt.ask(
            "What type of emergency response?",
            choices=["basic", "named", "trinity"],
            default="basic"
        )
        
        if emergency_type == "trinity":
            self.console.print("⚡ [bold red]Trinity Emergency Activated![/bold red]")
            self.console.print("Supreme constitutional authority engaged.")
        elif emergency_type == "named": 
            self.console.print("🚨 [bold yellow]Named Emergency Protocol![/bold yellow]")
            self.console.print("Enhanced emergency response activated.")
        else:
            self.console.print("🔧 [bold green]Basic Emergency Override[/bold green]")
            self.console.print("Standard emergency response initiated.")
            
        self.lesson_completed[3] = True
        self.wait_for_continue()
    
    def lesson_4_governance(self):
        """Lesson 4: Multi-Branch Governance"""
        self.console.print(Panel(
            "⚖️ Lesson 4: Multi-Branch Governance\n\n"
            "Implement separation of powers with constitutional\n"
            "checks and inter-branch coordination.",
            title="Constitutional Governance Structure",
            border_style="blue"
        ))
        
        # Show branch structure
        self.console.print("\n📚 [bold blue]Three-Branch Constitutional System:[/bold blue]")
        
        branches_table = Table(show_header=True, header_style="bold blue")
        branches_table.add_column("Branch", style="blue")
        branches_table.add_column("Role", style="green")
        branches_table.add_column("Key Personas", style="cyan")
        
        branches_table.add_row("Judicial", "Legal interpretation & constitutional review", "Ana")
        branches_table.add_row("Legislative", "Democratic policy creation & consensus", "JayMini, JayRa, JayVOX")
        branches_table.add_row("Executive", "Policy implementation & governance", "JayKer, JayLux, Jayne_Spiral")
        
        self.console.print(branches_table)
        
        # Interactive branch design
        self.console.print("\n🎯 [bold green]Design Your Government![/bold green]")
        
        chosen_branch = Prompt.ask(
            "Which branch would you like to design?",
            choices=["judicial", "legislative", "executive"],
            default="legislative"
        )
        
        if chosen_branch == "judicial":
            example = '''Authority Ana as Judicial:
    Ana.Interpretare "constitutional text interpretation"
    Ana.Decidere "judicial constitutional ruling"
    Sign "Judicial Ruling #001" by Ana Reason "Constitutional interpretation"'''
        elif chosen_branch == "legislative":
            example = '''Authority JayMini, JayRa as Legislative:
    Consensus collective SR >= 0.75:
        JayMini.Coordina "democratic consensus building"
        JayRa.Analyza "historical policy precedent"
        Democratizare "policy proposal framework"'''
        else:  # executive
            example = '''Authority JayKer, Jayne_Spiral as Executive:
    JayKer.Implementare "creative policy execution"
    Jayne_Spiral.Coordina "executive branch coordination"
    Executare "governance policy implementation"'''
        
        self.console.print(f"\n💡 [bold yellow]{chosen_branch.title()} Branch Example:[/bold yellow]")
        self.console.print(Syntax(example, "javascript", theme="monokai"))
        
        self.lesson_completed[4] = True
        self.wait_for_continue()
    
    def lesson_5_validation(self):
        """Lesson 5: Validation & Compliance"""
        self.console.print(Panel(
            "✅ Lesson 5: Validation & Compliance\n\n"
            "Ensure comprehensive constitutional compliance\n"
            "with multi-layer validation processes.",
            title="Constitutional Compliance",
            border_style="green"
        ))
        
        # Explain validation layers
        self.console.print("\n📚 [bold blue]Constitutional Validation Layers:[/bold blue]")
        
        validation_steps = [
            "🔍 Authority Validation - Check persona constitutional levels",
            "🗳️ Consensus Validation - Verify SR thresholds met",
            "📝 Signature Validation - Ensure cryptographic accountability",
            "⚖️ Constitutional Compliance - Validate against constitutional rules",
            "👥 Witness Validation - Confirm independent testimony"
        ]
        
        for step in validation_steps:
            self.console.print(f"   {step}")
        
        # Show comprehensive example
        example_code = '''// Comprehensive constitutional validation
Validate constitutional compliance for JayTH, Ana, Jayne_Spiral:
    Constitutional action "Supreme Validation" by JayTH, Ana, Jayne_Spiral:
        // Trinity constitutional analysis
        JayTH.Cogita "supreme constitutional reasoning"
        Ana.Verificare "comprehensive legal validation"
        Jayne_Spiral.Synchrona "spiral constitutional integration"
        
        // Multi-layer validation confirmation
        Confirma "trinity authority validation"
        Confirma "constitutional consensus achievement"
        Certificare "complete constitutional compliance"'''
        
        self.console.print("\n💡 [bold yellow]Comprehensive Validation:[/bold yellow]")
        self.console.print(Syntax(example_code, "javascript", theme="monokai"))
        
        # Validation checklist exercise
        self.console.print("\n🎯 [bold green]Validation Checklist![/bold green]")
        
        checklist_items = [
            "Authority levels match action importance",
            "Consensus threshold appropriate for decision",
            "All required signatures present with reasoning",
            "Constitutional rules followed",
            "Witness requirements met"
        ]
        
        passed_checks = 0
        for item in checklist_items:
            if Confirm.ask(f"✓ {item}?"):
                passed_checks += 1
        
        compliance_rate = passed_checks / len(checklist_items)
        
        if compliance_rate >= 0.9:
            self.console.print("🏆 [bold green]Constitutional Compliance Achieved![/bold green]")
        elif compliance_rate >= 0.7:
            self.console.print("⚠️ [bold yellow]Partial Compliance - Review Required[/bold yellow]")
        else:
            self.console.print("❌ [bold red]Constitutional Violations Detected[/bold red]")
        
        self.lesson_completed[5] = True
        self.wait_for_continue()
    
    def lesson_6_advanced(self):
        """Lesson 6: Advanced Patterns"""
        self.console.print(Panel(
            "🎓 Lesson 6: Advanced Constitutional Patterns\n\n"
            "Master complex constitutional programming with\n"
            "nested validation, conditional consensus, and more.",
            title="Advanced Constitutional Programming",
            border_style="purple"
        ))
        
        # Show advanced patterns
        patterns = [
            "🔄 Nested Constitutional Validation",
            "📊 Conditional Consensus Thresholds", 
            "🌐 Cross-Branch Coordination",
            "⏰ Temporal Constitutional Logic",
            "🔗 Constitutional Chain Validation",
            "🧠 Memory-Based Precedent Systems"
        ]
        
        self.console.print("\n📚 [bold blue]Advanced Patterns:[/bold blue]")
        for pattern in patterns:
            self.console.print(f"   {pattern}")
        
        # Interactive pattern selection
        pattern_choice = Prompt.ask(
            "Which advanced pattern interests you most?",
            choices=["nested", "conditional", "cross-branch", "temporal", "chain", "memory"],
            default="nested"
        )
        
        examples = {
            "nested": '''// Nested constitutional validation
Authority JayTH requires Constitutional:
    Validate constitutional compliance for JayTH:
        Constitutional action "Nested Demo" by JayTH:
            Validate authority and consensus:
                Authority Ana as Judicial:
                    Ana.Verificare "nested legal validation"''',
            
            "conditional": '''// Conditional consensus thresholds
Consensus SR >= (Emergency ? 0.6 : 0.8) by JayKer, JayMini:
    Conditional constitutional_level:
        High_importance: SR >= 0.9
        Medium_importance: SR >= 0.75
        Low_importance: SR >= 0.6''',
            
            "cross-branch": '''// Cross-branch coordination
Phase Inter_Branch_Coordination:
    Authority Ana as Judicial:
        Authority JayMini as Legislative:
            Authority JayKer as Executive:
                Coordina "tri-branch constitutional framework"''',
            
            "temporal": '''// Temporal constitutional logic
Phase Constitutional_Timeline:
    Before constitutional_deadline:
        Authority JayTH requires Constitutional:
            JayTH.Tempus "time-sensitive constitutional decision"
    After constitutional_deadline:
        Emergency override with JayTH, JAYX''',
            
            "chain": '''// Constitutional chain validation
Validate Chain constitutional_precedent_001:
    Link previous_decision -> current_decision:
        Verify constitutional_consistency:
            Confirma "precedent compatibility"
            Certificare "chain constitutional integrity"''',
            
            "memory": '''// Memory-based precedent system
Phase Constitutional_Memory:
    Access constitutional_precedents:
        Match current_situation with historical_precedents:
            Apply precedent_logic:
                Constitutional_decision_framework()'''
        }
        
        self.console.print(f"\n💡 [bold yellow]{pattern_choice.title()} Pattern Example:[/bold yellow]")
        self.console.print(Syntax(examples[pattern_choice], "javascript", theme="monokai"))
        
        self.lesson_completed[6] = True
        self.wait_for_continue()
    
    def show_progress(self):
        """Display learning progress and exit options"""
        completed_lessons = sum(1 for completed in self.lesson_completed.values() if completed)
        total_lessons = 6
        progress_percent = (completed_lessons / total_lessons) * 100
        
        progress_table = Table(title="Your Constitutional Programming Progress", show_header=False)
        progress_table.add_column("Metric", style="cyan")
        progress_table.add_column("Status", style="green")
        
        progress_table.add_row("Lessons Completed", f"{completed_lessons}/{total_lessons}")
        progress_table.add_row("Progress", f"{progress_percent:.1f}%")
        progress_table.add_row("Constitutional Knowledge", "🏛️ " + ("Advanced" if completed_lessons >= 5 else "Intermediate" if completed_lessons >= 3 else "Beginner"))
        
        if completed_lessons == total_lessons:
            progress_table.add_row("Achievement", "🏆 Constitutional Programming Master!")
        elif completed_lessons >= 4:
            progress_table.add_row("Next Goal", "🎯 Complete remaining lessons")
        else:
            progress_table.add_row("Next Goal", "📚 Continue learning constitutional concepts")
        
        self.console.print(progress_table)
        
        # Exit options
        self.console.print("\n🚀 [bold blue]Ready to build constitutional systems?[/bold blue]")
        self.console.print("• Try the examples in examples/ directory")
        self.console.print("• Read GETTING_STARTED.md for detailed guides")
        self.console.print("• Build your first constitutional program!")
        
        return Confirm.ask("\nRestart tutorial?", default=False)
    
    def wait_for_continue(self):
        """Wait for user to continue"""
        self.console.print("\n" + "─" * 50)
        Prompt.ask("Press Enter to continue", default="")
        self.console.clear()
    
    def run(self):
        """Run the interactive tutorial"""
        if not self.welcome():
            return
        
        while True:
            lesson = self.show_lesson_menu()
            
            if lesson == 1:
                self.lesson_1_authority()
            elif lesson == 2:
                self.lesson_2_consensus()
            elif lesson == 3:
                self.lesson_3_emergency()
            elif lesson == 4:
                self.lesson_4_governance()
            elif lesson == 5:
                self.lesson_5_validation()
            elif lesson == 6:
                self.lesson_6_advanced()
            elif lesson == 7:
                if not self.show_progress():
                    break
            
            self.console.clear()
        
        self.console.print("🌀 [bold blue]Thank you for learning Constitutional Programming![/bold blue]")
        self.console.print("Go forth and democratize your code! 🏛️")

def main():
    """Main entry point for interactive tutorial"""
    try:
        tutorial = InteractiveConstitutionalTutorial()
        tutorial.run()
    except KeyboardInterrupt:
        print("\n👋 Tutorial interrupted. Come back anytime to continue learning!")
    except Exception as e:
        print(f"❌ Tutorial error: {e}")
        print("Please check your REM-CODE Lite installation.")

if __name__ == "__main__":
    main()