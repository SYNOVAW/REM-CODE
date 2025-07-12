#!/usr/bin/env python3
"""
Constitutional Error Messages - REM-CODE Lite User-Friendly Error System
教育的で分かりやすいエラーメッセージシステム

Provides clear, educational error messages for constitutional programming mistakes
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

class ErrorSeverity(Enum):
    """Error severity levels"""
    INFO = "info"
    WARNING = "warning" 
    ERROR = "error"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Constitutional error categories"""
    AUTHORITY = "authority"
    CONSENSUS = "consensus"
    VALIDATION = "validation"
    SIGNATURE = "signature"
    EMERGENCY = "emergency"
    SYNTAX = "syntax"
    GOVERNANCE = "governance"

@dataclass
class ConstitutionalError:
    """Structured constitutional error with educational content"""
    category: ErrorCategory
    severity: ErrorSeverity
    title: str
    message: str
    suggestion: str
    example_fix: str
    learn_more: Optional[str] = None
    related_concepts: Optional[List[str]] = None

class ConstitutionalErrorHandler:
    """
    User-friendly error handler for constitutional programming
    Provides educational feedback and learning opportunities
    """
    
    def __init__(self):
        self.console = Console()
        self.error_count = 0
        self.warning_count = 0
        
    def _get_authority_errors(self) -> Dict[str, ConstitutionalError]:
        """Authority-related error messages"""
        return {
            "insufficient_authority": ConstitutionalError(
                category=ErrorCategory.AUTHORITY,
                severity=ErrorSeverity.ERROR,
                title="Insufficient Constitutional Authority",
                message="The persona '{persona}' has {current_level} authority but needs {required_level} authority to perform '{action}'.",
                suggestion="Use a persona with higher constitutional authority or delegate this action to an authorized persona.",
                example_fix="""// ❌ Insufficient authority
Authority JayMini requires Constitutional:
    JayMini.Declara "constitutional amendment"

// ✅ Correct authority  
Authority JayTH requires Constitutional:
    JayTH.Declara "constitutional amendment" """,
                learn_more="Check GETTING_STARTED.md section 'Constitutional Personas' for authority levels",
                related_concepts=["constitutional_hierarchy", "persona_delegation", "authority_validation"]
            ),
            
            "unknown_persona": ConstitutionalError(
                category=ErrorCategory.AUTHORITY,
                severity=ErrorSeverity.ERROR,
                title="Unknown Constitutional Persona",
                message="Persona '{persona}' is not recognized in the constitutional framework.",
                suggestion="Use one of the 12 constitutional personas or register a new persona with appropriate authority.",
                example_fix="""// ❌ Unknown persona
Authority UnknownPersona requires Constitutional:

// ✅ Known constitutional persona
Authority JayTH requires Constitutional:
Authority Ana as Judicial:
Authority Jayne_Spiral as Executive:""",
                learn_more="See GETTING_STARTED.md for complete list of constitutional personas",
                related_concepts=["constitutional_personas", "persona_registration", "authority_assignment"]
            ),
            
            "branch_mismatch": ConstitutionalError(
                category=ErrorCategory.AUTHORITY,
                severity=ErrorSeverity.WARNING,
                title="Constitutional Branch Mismatch",
                message="Persona '{persona}' belongs to {actual_branch} branch but is being used as {requested_branch}.",
                suggestion="Use personas in their designated branches or explicitly specify cross-branch coordination.",
                example_fix="""// ⚠️ Branch mismatch
Authority Ana as Executive:  // Ana is Judicial branch

// ✅ Correct branch assignment
Authority Ana as Judicial:
Authority Jayne_Spiral as Executive:

// ✅ Cross-branch coordination
Authority Ana as Judicial:
    Authority Jayne_Spiral as Executive:
        Coordina "inter-branch constitutional cooperation" """,
                learn_more="Read about separation of powers in the governance tutorial",
                related_concepts=["separation_of_powers", "inter_branch_coordination", "constitutional_branches"]
            ),
            
            "trinity_incomplete": ConstitutionalError(
                category=ErrorCategory.AUTHORITY,
                severity=ErrorSeverity.ERROR,
                title="Incomplete Trinity Authority",
                message="Trinity authority requires at least 2 of 3 Trinity members (JayTH, Ana, Jayne_Spiral). Only {present_count} present: {present_members}.",
                suggestion="Include at least 2 Trinity members for constitutional actions requiring Trinity authority.",
                example_fix="""// ❌ Incomplete Trinity
Authority trinity JayTH:  // Only 1 Trinity member

// ✅ Valid Trinity authority
Authority trinity JayTH, Ana:  // 2 Trinity members
Authority trinity JayTH, Ana, Jayne_Spiral:  // Full Trinity""",
                learn_more="Trinity authority is the highest constitutional level - see emergency protocols tutorial",
                related_concepts=["trinity_authority", "constitutional_hierarchy", "supreme_decisions"]
            )
        }
    
    def _get_consensus_errors(self) -> Dict[str, ConstitutionalError]:
        """Consensus-related error messages"""
        return {
            "sr_threshold_not_met": ConstitutionalError(
                category=ErrorCategory.CONSENSUS,
                severity=ErrorSeverity.ERROR,
                title="Synchrony Rate Threshold Not Met",
                message="Consensus requires SR >= {required_sr} but current collective SR is {current_sr}. {failed_personas} did not meet threshold.",
                suggestion="Improve consensus building or lower the SR threshold if appropriate for the decision importance.",
                example_fix="""// ❌ Too high threshold for this decision
Consensus SR >= 0.95 by JayKer, JayMini:  // Very high threshold

// ✅ Appropriate threshold
Consensus SR >= 0.75 by JayKer, JayMini:  // Reasonable for this action

// ✅ Constitutional threshold for important decisions
Consensus Constitutional requires 0.9:  // High threshold for constitutional matters""",
                learn_more="Learn about SR thresholds in the democratic consensus tutorial",
                related_concepts=["synchrony_rate", "consensus_building", "democratic_thresholds"]
            ),
            
            "invalid_consensus_type": ConstitutionalError(
                category=ErrorCategory.CONSENSUS,
                severity=ErrorSeverity.ERROR,
                title="Invalid Consensus Type",
                message="Consensus type '{consensus_type}' is not recognized. Valid types: SR, collective, Constitutional.",
                suggestion="Use a valid consensus type with appropriate threshold.",
                example_fix="""// ❌ Invalid consensus type
Consensus unknown >= 0.8:

// ✅ Valid consensus types
Consensus SR >= 0.8 by JayKer, JayMini:
Consensus collective SR >= 0.75:
Consensus Constitutional requires 0.9:""",
                learn_more="See consensus types in GETTING_STARTED.md",
                related_concepts=["consensus_types", "democratic_mechanisms", "threshold_validation"]
            ),
            
            "insufficient_participants": ConstitutionalError(
                category=ErrorCategory.CONSENSUS,
                severity=ErrorSeverity.WARNING,
                title="Insufficient Consensus Participants",
                message="Consensus has only {participant_count} participants. Constitutional decisions typically require {recommended_min}+ participants.",
                suggestion="Include more personas in important democratic decisions for better legitimacy.",
                example_fix="""// ⚠️ Single participant consensus
Consensus SR >= 0.8 by JayTH:  // Only one persona

// ✅ Multi-participant consensus
Consensus SR >= 0.8 by JayTH, Ana, JayMini:  // Multiple participants

// ✅ Collective consensus
Consensus collective SR >= 0.75:
    Invoke JayKer, JayMini, JayRa, JayVOX:  // Group consensus""",
                learn_more="Democratic principles suggest multiple participants for legitimacy",
                related_concepts=["democratic_participation", "consensus_legitimacy", "collective_decision_making"]
            )
        }
    
    def _get_validation_errors(self) -> Dict[str, ConstitutionalError]:
        """Validation-related error messages"""
        return {
            "missing_validation": ConstitutionalError(
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.WARNING,
                title="Missing Constitutional Validation",
                message="Constitutional action '{action}' should include validation for accountability and compliance.",
                suggestion="Add constitutional validation to ensure compliance and accountability.",
                example_fix="""// ⚠️ Missing validation
Authority JayTH requires Constitutional:
    JayTH.Declara "important constitutional decision"

// ✅ With validation
Validate constitutional compliance for JayTH:
    Constitutional action "Important Decision" by JayTH:
        JayTH.Declara "important constitutional decision"
        Sign "Decision #001" by JayTH Reason "Constitutional authority exercised" """,
                learn_more="Validation ensures constitutional compliance - see validation tutorial",
                related_concepts=["constitutional_compliance", "validation_patterns", "accountability"]
            ),
            
            "validation_failed": ConstitutionalError(
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.ERROR,
                title="Constitutional Validation Failed",
                message="Validation failed for '{action}': {failure_reason}",
                suggestion="Review the constitutional requirements and ensure all conditions are met.",
                example_fix="""// ❌ Failed validation
Validate constitutional compliance for JayMini:  // JayMini lacks Constitutional authority
    Constitutional action "Constitutional Amendment" by JayMini:

// ✅ Proper validation
Validate constitutional compliance for JayTH:  // JayTH has Constitutional authority
    Constitutional action "Constitutional Amendment" by JayTH:
        JayTH.Cogita "constitutional analysis complete" """,
                learn_more="Check persona authority levels and constitutional requirements",
                related_concepts=["validation_requirements", "constitutional_compliance", "error_prevention"]
            ),
            
            "circular_validation": ConstitutionalError(
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.ERROR,
                title="Circular Constitutional Validation",
                message="Validation creates circular dependency: {validation_chain}",
                suggestion="Restructure validation to avoid circular dependencies.",
                example_fix="""// ❌ Circular validation
Validate constitutional compliance for JayTH:
    Validate constitutional compliance for Ana:  // Circular dependency

// ✅ Linear validation
Validate constitutional compliance for JayTH, Ana:
    Constitutional action "Joint Decision" by JayTH, Ana:
        // Both validated together""",
                learn_more="Validation should be hierarchical, not circular",
                related_concepts=["validation_hierarchy", "dependency_management", "constitutional_structure"]
            )
        }
    
    def _get_signature_errors(self) -> Dict[str, ConstitutionalError]:
        """Signature-related error messages"""
        return {
            "missing_signature": ConstitutionalError(
                category=ErrorCategory.SIGNATURE,
                severity=ErrorSeverity.ERROR,
                title="Missing Constitutional Signature",
                message="Constitutional action '{action}' by {persona} requires cryptographic signature for accountability.",
                suggestion="Add signature with clear reasoning to ensure accountability and transparency.",
                example_fix="""// ❌ Missing signature
Authority JayTH requires Constitutional:
    JayTH.Declara "constitutional decision"
    // No signature - lacks accountability

// ✅ With signature
Authority JayTH requires Constitutional:
    JayTH.Declara "constitutional decision"
    Sign "Decision #001" by JayTH Reason "Constitutional authority exercised for framework enhancement" """,
                learn_more="Signatures provide cryptographic accountability in constitutional systems",
                related_concepts=["cryptographic_accountability", "signature_requirements", "transparency"]
            ),
            
            "invalid_signature_format": ConstitutionalError(
                category=ErrorCategory.SIGNATURE,
                severity=ErrorSeverity.ERROR,
                title="Invalid Signature Format",
                message="Signature format is invalid: {signature_text}. Required format: Sign \"Action Name\" by Persona Reason \"reasoning\"",
                suggestion="Use proper signature format with action name, persona, and reasoning.",
                example_fix="""// ❌ Invalid signature formats
Sign by JayTH "decision"  // Wrong order
Sign "Decision" JayTH  // Missing 'by' and 'Reason'

// ✅ Correct signature format
Sign "Constitutional Decision #001" by JayTH Reason "Authority validation complete"
Sign "Emergency Response #002" by Ana Reason "Legal framework protection" """,
                learn_more="Signature format ensures consistency and parseability",
                related_concepts=["signature_syntax", "constitutional_formatting", "parsing_requirements"]
            ),
            
            "insufficient_reasoning": ConstitutionalError(
                category=ErrorCategory.SIGNATURE,
                severity=ErrorSeverity.WARNING,
                title="Insufficient Signature Reasoning",
                message="Signature reasoning '{reasoning}' is too brief or unclear for constitutional accountability.",
                suggestion="Provide clear, detailed reasoning for constitutional signatures.",
                example_fix="""// ⚠️ Insufficient reasoning
Sign "Decision #001" by JayTH Reason "done"  // Too brief

// ✅ Clear reasoning
Sign "Constitutional Framework Update #001" by JayTH Reason "Constitutional analysis complete, democratic consensus achieved, framework enhancement approved"

// ✅ Detailed reasoning
Sign "Emergency Protocol #002" by Ana Reason "Legal framework requires protection during constitutional crisis, judicial authority activated" """,
                learn_more="Good reasoning provides context for future constitutional review",
                related_concepts=["accountability_standards", "constitutional_documentation", "transparency_principles"]
            )
        }
    
    def _get_emergency_errors(self) -> Dict[str, ConstitutionalError]:
        """Emergency protocol error messages"""
        return {
            "unauthorized_emergency": ConstitutionalError(
                category=ErrorCategory.EMERGENCY,
                severity=ErrorSeverity.CRITICAL,
                title="Unauthorized Emergency Protocol",
                message="Emergency protocol '{protocol}' requires emergency authority. Present personas {present_personas} lack emergency authorization.",
                suggestion="Emergency protocols require specific personas with emergency authority (JayTH, JAYX, Jayne_Spiral).",
                example_fix="""// ❌ Unauthorized emergency
Emergency override with JayMini, JayRa:  // Lack emergency authority

// ✅ Authorized emergency  
Emergency override with JayTH, JAYX:  // Have emergency authority
Emergency protocol "Crisis Response" by JayTH, JAYX, Jayne_Spiral:

// ✅ Trinity emergency
Emergency trinity authorization:
    Trinity coordination requires 2 of 3:  // Supreme emergency authority""",
                learn_more="Emergency protocols have strict authorization requirements - see emergency tutorial",
                related_concepts=["emergency_authority", "crisis_management", "constitutional_protection"]
            ),
            
            "invalid_emergency_level": ConstitutionalError(
                category=ErrorCategory.EMERGENCY,
                severity=ErrorSeverity.ERROR,
                title="Invalid Emergency Authorization Level",
                message="Emergency level '{level}' is not recognized. Valid levels: override, protocol, trinity.",
                suggestion="Use valid emergency authorization levels based on crisis severity.",
                example_fix="""// ❌ Invalid emergency level
Emergency unknown with JayTH:

// ✅ Valid emergency levels
Emergency override with JayTH, JAYX:  // Basic emergency
Emergency protocol "Crisis Response" by JayTH, JAYX, Jayne_Spiral:  // Named emergency
Emergency trinity authorization:  // Supreme emergency""",
                learn_more="Emergency levels correspond to crisis severity and required authority",
                related_concepts=["emergency_hierarchy", "crisis_severity", "authorization_levels"]
            )
        }
    
    def _get_all_errors(self) -> Dict[str, ConstitutionalError]:
        """Get all error message definitions"""
        all_errors = {}
        all_errors.update(self._get_authority_errors())
        all_errors.update(self._get_consensus_errors())
        all_errors.update(self._get_validation_errors())
        all_errors.update(self._get_signature_errors())
        all_errors.update(self._get_emergency_errors())
        return all_errors
    
    def format_error(self, error_key: str, **kwargs) -> str:
        """Format an error message with provided context"""
        errors = self._get_all_errors()
        if error_key not in errors:
            return f"Unknown error: {error_key}"
        
        error = errors[error_key]
        
        # Format message with provided kwargs
        try:
            formatted_message = error.message.format(**kwargs)
            formatted_suggestion = error.suggestion
            formatted_example = error.example_fix
        except KeyError as e:
            formatted_message = f"{error.message} (Missing context: {e})"
            formatted_suggestion = error.suggestion
            formatted_example = error.example_fix
        
        return self._render_error(error, formatted_message, formatted_suggestion, formatted_example)
    
    def _render_error(self, error: ConstitutionalError, message: str, suggestion: str, example: str) -> str:
        """Render error in rich format"""
        
        # Choose color and emoji based on severity
        severity_config = {
            ErrorSeverity.INFO: ("blue", "ℹ️"),
            ErrorSeverity.WARNING: ("yellow", "⚠️"),
            ErrorSeverity.ERROR: ("red", "❌"),
            ErrorSeverity.CRITICAL: ("bright_red", "🚨")
        }
        
        color, emoji = severity_config.get(error.severity, ("white", "❓"))
        
        # Build error panel content
        content_lines = [
            f"{emoji} [bold {color}]{error.title}[/bold {color}]",
            "",
            f"[{color}]Problem:[/{color}] {message}",
            "",
            f"[green]💡 Suggestion:[/green] {suggestion}",
        ]
        
        if example:
            content_lines.extend([
                "",
                "[blue]📝 Example Fix:[/blue]",
                example
            ])
        
        if error.learn_more:
            content_lines.extend([
                "",
                f"[cyan]📚 Learn More:[/cyan] {error.learn_more}"
            ])
        
        if error.related_concepts:
            content_lines.extend([
                "",
                f"[magenta]🔗 Related:[/magenta] {', '.join(error.related_concepts)}"
            ])
        
        content = "\n".join(content_lines)
        
        # Create panel
        panel = Panel(
            content,
            title=f"Constitutional {error.category.value.title()} {error.severity.value.title()}",
            title_align="center",
            border_style=color,
            padding=(1, 2)
        )
        
        with self.console.capture() as capture:
            self.console.print(panel)
        
        # Update counters
        if error.severity in [ErrorSeverity.ERROR, ErrorSeverity.CRITICAL]:
            self.error_count += 1
        elif error.severity == ErrorSeverity.WARNING:
            self.warning_count += 1
        
        return capture.get()
    
    def show_error_summary(self):
        """Show summary of errors encountered"""
        if self.error_count == 0 and self.warning_count == 0:
            self.console.print("✅ [green]No constitutional issues detected![/green]")
            return
        
        summary_table = Table(title="Constitutional Issues Summary", show_header=True)
        summary_table.add_column("Type", style="cyan")
        summary_table.add_column("Count", style="yellow")
        summary_table.add_column("Status", style="red" if self.error_count > 0 else "green")
        
        if self.error_count > 0:
            summary_table.add_row("Errors", str(self.error_count), "❌ Must Fix")
        if self.warning_count > 0:
            summary_table.add_row("Warnings", str(self.warning_count), "⚠️ Should Review")
        
        self.console.print(summary_table)
        
        if self.error_count > 0:
            self.console.print("\n🚨 [bold red]Constitutional errors must be resolved before execution.[/bold red]")
        else:
            self.console.print("\n✅ [green]Ready for constitutional execution with noted warnings.[/green]")
    
    def get_error_suggestions(self, error_category: ErrorCategory) -> List[str]:
        """Get general suggestions for error category"""
        suggestions = {
            ErrorCategory.AUTHORITY: [
                "Check persona authority levels in GETTING_STARTED.md",
                "Use appropriate constitutional personas for the action importance",
                "Consider delegating to higher authority personas",
                "Review branch assignments and separation of powers"
            ],
            ErrorCategory.CONSENSUS: [
                "Adjust SR thresholds to match decision importance",
                "Include more participants for better democratic legitimacy",
                "Build consensus gradually through discussion and compromise",
                "Use constitutional consensus (SR >= 0.9) for major decisions"
            ],
            ErrorCategory.VALIDATION: [
                "Add constitutional validation for important actions",
                "Ensure all personas meet authority requirements",
                "Structure validation hierarchically, not circularly",
                "Include compliance checking for constitutional actions"
            ],
            ErrorCategory.SIGNATURE: [
                "Always sign constitutional actions for accountability",
                "Provide clear, detailed reasoning in signatures",
                "Use proper signature format: Sign \"Name\" by Persona Reason \"reasoning\"",
                "Include context and justification for future review"
            ],
            ErrorCategory.EMERGENCY: [
                "Only use emergency protocols for actual emergencies",
                "Ensure emergency personas have proper authorization",
                "Document emergency reasoning clearly for accountability",
                "Use appropriate emergency level (override/protocol/trinity)"
            ]
        }
        
        return suggestions.get(error_category, ["Review constitutional programming documentation"])

# Global error handler instance
constitutional_error_handler = ConstitutionalErrorHandler()

def show_constitutional_error(error_key: str, **kwargs) -> str:
    """Show a constitutional error with educational formatting"""
    return constitutional_error_handler.format_error(error_key, **kwargs)

def get_error_suggestions(category: ErrorCategory) -> List[str]:
    """Get suggestions for an error category"""
    return constitutional_error_handler.get_error_suggestions(category)