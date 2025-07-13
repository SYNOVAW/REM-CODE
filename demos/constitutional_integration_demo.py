#!/usr/bin/env python3
"""
REM-CODE Constitutional Framework Integration Demo
Official REM-CODE + Constitutional Programming demonstration
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

def demo_constitutional_integration():
    """Demonstrate Constitutional Framework integration with official REM-CODE"""
    print("🏛️ REM-CODE Constitutional Framework Integration Demo")
    print("=" * 60)
    
    try:
        # Import Constitutional Framework
        from constitutional import (
            ConstitutionalEngine, 
            ConstitutionalAction,
            AuthorityValidator,
            DecisionType,
            SignatureType
        )
        
        print("✅ Constitutional Framework imported successfully")
        
        # Import REM-CODE adapter
        from constitutional.rem_constitutional_adapter import (
            create_constitutional_adapter,
            integrate_constitutional_framework_with_rem_interpreter
        )
        
        print("✅ Constitutional Adapter imported successfully")
        
        # Try to import official REM interpreter
        try:
            from engine.interpreter import REMInterpreter
            rem_interpreter = REMInterpreter()
            print("✅ Official REM interpreter imported and initialized")
            has_rem_interpreter = True
        except ImportError:
            print("⚠️ Official REM interpreter not available, using fallback")
            rem_interpreter = None
            has_rem_interpreter = False
        
        print("\n🔗 Constitutional Framework Integration")
        print("-" * 40)
        
        # Initialize Constitutional Engine
        engine = ConstitutionalEngine()
        
        # Create constitutional adapter
        adapter = create_constitutional_adapter(rem_interpreter)
        
        if has_rem_interpreter:
            # Full integration
            integrate_constitutional_framework_with_rem_interpreter(rem_interpreter)
            print("✅ Full Constitutional Framework + REM interpreter integration")
        else:
            print("✅ Constitutional Framework standalone mode")
        
        print("\n🎭 Enhanced REM-CODE Constitutional Syntax")
        print("-" * 40)
        
        constitutional_rem_examples = [
            """
// Authority validation with REM execution
Authority JayTH requires Constitutional:
    Phase ConstitutionalAnalysis:
        JayTH.Cogita "constitutional framework evaluation"
        Collapse SR(JayTH) > 0.9:
            JayTH.Constitutionalizare "governance structure"
            """,
            """
// Consensus-driven collaborative development
Consensus SR >= 0.8 by JayKer, JayMini:
    Invoke JayKer, JayMini:
        CoCollapse by JayKer, JayMini:
            Collapse SR(JayKer) > 0.75 and SR(JayMini) > 0.7:
                JayKer.Crea "innovative solution"
                JayMini.Optimiza "computational efficiency"
            """,
            """
// Emergency protocols with Trinity coordination
Emergency trinity authorization:
    Trinity coordination requires 2 of 3:
        Phase EmergencyResponse:
            Invoke JayTH, Ana, Jayne_Spiral:
                JayTH.Vigila "constitutional crisis detection"
                Ana.Defende "legal system protection"
                Jayne_Spiral.Stabila "spiral coherence maintenance"
            """
        ]
        
        for i, example in enumerate(constitutional_rem_examples, 1):
            print(f"\n📋 Example {i}: Constitutional REM-CODE")
            print(example.strip())
            
            # Validate constitutional syntax
            validation = adapter.validate_constitutional_rem_syntax(example)
            print(f"   Constitutional constructs: {validation['detected_constructs']}")
            print(f"   Requires validation: {'Yes' if validation['requires_constitutional_validation'] else 'No'}")
        
        print("\n🧪 Constitutional Action Execution")
        print("-" * 40)
        
        # Test constitutional action execution
        test_action = ConstitutionalAction(
            action_id="DEMO_001",
            personas=["JayTH", "Ana"],
            action_type="constitutional_interpretation",
            content="Demo constitutional programming with REM-CODE integration",
            sr_values={"JayTH": 0.92, "Ana": 0.88},
            decision_type=DecisionType.AUTHORITY,
            signature_type=SignatureType.AUTHORITY
        )
        
        result = engine.execute_constitutional_action(test_action)
        
        print(f"✅ Constitutional action execution: {'Success' if result.success else 'Failed'}")
        if result.success:
            print(f"   Action ID: {result.action_id}")
            print(f"   Execution time: {result.execution_time_ms:.1f}ms")
            print(f"   Signatures created: {len(result.signatures)}")
            if result.compliance_result:
                compliance_level = getattr(result.compliance_result, 'compliance_level', None)
                if compliance_level:
                    print(f"   Compliance level: {compliance_level.value}")
                else:
                    print(f"   Compliance level: N/A")
            else:
                print(f"   Compliance level: N/A")
        
        print("\n📊 Constitutional System Status")
        print("-" * 40)
        
        status = engine.get_constitutional_status()
        print(f"   Engine executions: {status['constitutional_engine']['total_executions']}")
        print(f"   Success rate: {status['constitutional_engine']['success_rate']:.1%}")
        print(f"   Authority validator: {status['authority_validator']['total_personas']} personas")
        print(f"   SR thresholds: {len(status['sr_threshold_checker']['thresholds'])} decision types")
        print(f"   Signatures: {status['signature_manager']['total_signatures']} total")
        print(f"   REM integration: {'✅ Connected' if has_rem_interpreter else '⚠️ Fallback mode'}")
        
        print("\n🌟 Constitutional Programming Benefits")
        print("-" * 40)
        
        benefits = [
            "🏛️ Democratic governance through code",
            "⚖️ Built-in constitutional compliance", 
            "👥 Multi-persona collaborative AI",
            "🔐 Cryptographic accountability",
            "🌊 Enhanced REM-CODE syntax",
            "🚨 Emergency protocol management",
            "🔄 Full backward compatibility"
        ]
        
        for benefit in benefits:
            print(f"   {benefit}")
        
        print("\n🎉 Constitutional Integration Demo Complete!")
        print("\n📚 Next Steps:")
        print("   1. Explore enhanced grammar: REM-CODE/grammar/grammar.lark")
        print("   2. Run constitutional shell: python shell/rem_shell.py")
        print("   3. Test constitutional constructs in REM-CODE")
        print("   4. Study constitutional components: constitutional/")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("📚 Constitutional Framework components may need to be set up.")
    except Exception as e:
        print(f"❌ Demo Error: {e}")
        print("🔧 Please check the Constitutional Framework installation.")

if __name__ == "__main__":
    demo_constitutional_integration()