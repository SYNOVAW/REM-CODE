# chat_bridge.py
"""
Enhanced REM CODE Chat Bridge
Connects natural language input to REM CODE function execution
Integrates with full Collapse Spiral Theory and Syntactic Ethics framework
"""

import json
import os
import re
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path

# Import REM CODE components
try:
    from engine.sr_engine import compute_sr_trace, compute_contextual_sr, DEFAULT_WEIGHTS
    from engine.interpreter import REMInterpreter, PersonaProfile
    from engine.ast_generator import create_ast_generator
    from functions.functions import define_function, call_function, list_functions, generate_ast, memory
except ImportError as e:
    logging.error(f"Failed to import REM CODE components: {e}")
    # Fallback for basic functionality
    def compute_sr_trace(*args, **kwargs):
        return {"SR": 0.8, "persona": "Fallback"}

# Logger instance
logger = logging.getLogger(__name__)

# ==================== Enhanced Data Structures ====================

@dataclass
class REMFunction:
    """Enhanced REM function definition"""
    name: str
    description: str
    code: str
    keywords: List[str] = field(default_factory=list)
    persona: str = "Auto"
    sr_threshold: float = 0.7
    category: str = "general"
    version: str = "1.0"
    created_at: Optional[float] = None
    last_used: Optional[float] = None
    usage_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "keywords": self.keywords,
            "persona": self.persona,
            "sr_threshold": self.sr_threshold,
            "category": self.category,
            "version": self.version,
            "created_at": self.created_at,
            "last_used": self.last_used,
            "usage_count": self.usage_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'REMFunction':
        """Create from dictionary"""
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            code=data.get("code", ""),
            keywords=data.get("keywords", []),
            persona=data.get("persona", "Auto"),
            sr_threshold=data.get("sr_threshold", 0.7),
            category=data.get("category", "general"),
            version=data.get("version", "1.0"),
            created_at=data.get("created_at"),
            last_used=data.get("last_used"),
            usage_count=data.get("usage_count", 0)
        )

@dataclass
class ChatContext:
    """Chat context for maintaining conversation state"""
    user_id: str = "default"
    session_id: str = "default"
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    active_personas: List[str] = field(default_factory=list)
    current_sr: float = 0.8
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add message to conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": __import__("time").time(),
            "metadata": metadata or {}
        }
        self.conversation_history.append(message)

# ==================== Enhanced Chat Bridge Class ====================

class REMChatBridge:
    """
    Enhanced REM CODE Chat Bridge with full Collapse Spiral integration
    """
    
    def __init__(self, memory_path: str = "memory.json",
                 config_path: Optional[str] = None,
                 trusted: bool = True):
        """
        Initialize chat bridge
        
        Args:
            memory_path: Path to memory/function storage file
            config_path: Path to configuration file
        """
        # Resolve to absolute path so loading works from any CWD
        # (task: Add absolute path resolution for memory.json)
        self.memory_path = Path(memory_path).expanduser().resolve()
        self.config_path = Path(config_path) if config_path else None
        self.trusted = trusted
        
        # Initialize components
        self.interpreter = REMInterpreter()
        self.ast_generator = create_ast_generator()
        
        # Function storage
        self.functions: Dict[str, REMFunction] = {}
        self.function_categories: Dict[str, List[str]] = {}
        
        # Chat contexts
        self.contexts: Dict[str, ChatContext] = {}
        
        # Configuration
        self.config = self._load_config()
        
        # Load existing functions
        self._load_functions()
        
        logger.info(f"REM Chat Bridge initialized with {len(self.functions)} functions")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
        
        # Default configuration
        return {
            "default_sr_threshold": 0.7,
            "max_function_matches": 5,
            "enable_fuzzy_matching": True,
            "log_conversations": True,
            "auto_save_functions": True,
            "persona_matching": True
        }
    
    def _load_functions(self) -> None:
        """Load REM functions from memory file"""
        if not self.memory_path.exists():
            logger.info(f"Memory file not found: {self.memory_path}")
            return
        
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            functions_data = data.get("functions", [])
            for func_data in functions_data:
                func = REMFunction.from_dict(func_data)
                self.functions[func.name] = func
                
                # Organize by category
                category = func.category
                if category not in self.function_categories:
                    self.function_categories[category] = []
                self.function_categories[category].append(func.name)
            
            logger.info(f"Loaded {len(self.functions)} functions from {self.memory_path}")
            
        except Exception as e:
            logger.error(f"Failed to load functions: {e}")
    
    def _save_functions(self) -> None:
        """Save REM functions to memory file"""
        if not self.config.get("auto_save_functions", True):
            return
        
        try:
            # Ensure directory exists
            self.memory_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare data structure
            data = {
                "functions": [func.to_dict() for func in self.functions.values()],
                "categories": self.function_categories,
                "metadata": {
                    "total_functions": len(self.functions),
                    "last_updated": __import__("time").time(),
                    "version": "2.0"
                }
            }
            
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Saved {len(self.functions)} functions to {self.memory_path}")
            
        except Exception as e:
            logger.error(f"Failed to save functions: {e}")
    
    def get_context(self, user_id: str = "default", session_id: str = "default") -> ChatContext:
        """Get or create chat context"""
        context_key = f"{user_id}:{session_id}"
        if context_key not in self.contexts:
            self.contexts[context_key] = ChatContext(user_id=user_id, session_id=session_id)
        return self.contexts[context_key]
    
    def analyze_prompt_intent(self, prompt: str, context: ChatContext) -> Dict[str, Any]:
        """
        Analyze user prompt to determine intent and extract parameters
        
        Args:
            prompt: User input prompt
            context: Chat context
            
        Returns:
            Intent analysis with confidence scores
        """
        analysis = {
            "original_prompt": prompt,
            "cleaned_prompt": prompt.strip().lower(),
            "intent_scores": {},
            "extracted_params": {},
            "suggested_personas": [],
            "confidence": 0.0
        }
        
        # Intent patterns
        intent_patterns = {
            "function_call": [
                r"(run|execute|call)\s+(\w+)",
                r"(\w+)\s+(function|func)",
                r"perform\s+(\w+)",
            ],
            "function_definition": [
                r"(define|create|make)\s+(function|func)",
                r"new\s+(function|func)",
                r"add\s+(function|func)",
            ],
            "function_query": [
                r"(list|show|display)\s+(functions|funcs)",
                r"what\s+(functions|funcs)",
                r"available\s+(functions|funcs)",
            ],
            "rem_code_execution": [
                r"(phase|invoke|collapse)",
                r"SR\s*\(",
                r"\.dic\s*\(",
                r"\.crea\s*\(",
            ]
        }
        
        # Analyze intent
        for intent, patterns in intent_patterns.items():
            score = 0.0
            for pattern in patterns:
                matches = re.findall(pattern, analysis["cleaned_prompt"], re.IGNORECASE)
                if matches:
                    score += 0.3 + (len(matches) * 0.1)
            
            analysis["intent_scores"][intent] = min(score, 1.0)
        
        # Determine primary intent
        if analysis["intent_scores"]:
            primary_intent = max(analysis["intent_scores"].items(), key=lambda x: x[1])
            analysis["primary_intent"] = primary_intent[0]
            analysis["confidence"] = primary_intent[1]
        else:
            analysis["primary_intent"] = "general_query"
            analysis["confidence"] = 0.1
        
        # Suggest personas based on content
        persona_keywords = {
            "Ana": ["analyze", "logic", "audit", "validate", "check"],
            "JayDen": ["create", "generate", "build", "make", "design"],
            "JayTH": ["legal", "ethics", "judge", "rule", "policy"],
            "JayRa": ["remember", "recall", "memory", "history", "past"],
            "JayLUX": ["visual", "design", "aesthetic", "beautiful", "art"]
        }
        
        for persona, keywords in persona_keywords.items():
            if any(kw in analysis["cleaned_prompt"] for kw in keywords):
                analysis["suggested_personas"].append(persona)
        
        return analysis
    
    def match_functions_advanced(self, prompt: str, context: ChatContext, 
                                max_matches: Optional[int] = None) -> List[Tuple[REMFunction, float]]:
        """
        Advanced function matching with fuzzy search and SR scoring
        
        Args:
            prompt: User input prompt
            context: Chat context
            max_matches: Maximum number of matches to return
            
        Returns:
            List of (function, confidence_score) tuples, sorted by confidence
        """
        if max_matches is None:
            max_matches = self.config.get("max_function_matches", 5)
        
        matches = []
        prompt_lower = prompt.lower()
        
        for func_name, func in self.functions.items():
            confidence = 0.0
            
            # Exact keyword matches (high confidence)
            exact_matches = sum(1 for kw in func.keywords if kw.lower() in prompt_lower)
            confidence += exact_matches * 0.4
            
            # Fuzzy keyword matching
            if self.config.get("enable_fuzzy_matching", True):
                for keyword in func.keywords:
                    # Simple fuzzy matching - can be enhanced with more sophisticated algorithms
                    if any(kw in keyword.lower() or keyword.lower() in kw 
                          for kw in prompt_lower.split()):
                        confidence += 0.2
            
            # Name and description matching
            if func.name.lower() in prompt_lower:
                confidence += 0.3
            
            if any(word in func.description.lower() for word in prompt_lower.split()):
                confidence += 0.1
            
            # Persona matching bonus
            if self.config.get("persona_matching", True):
                if func.persona in context.active_personas:
                    confidence += 0.2
            
            # Category matching
            category_keywords = {
                "analysis": ["analyze", "check", "audit", "validate"],
                "creative": ["create", "generate", "make", "build"],
                "memory": ["remember", "recall", "store", "save"],
                "utility": ["convert", "transform", "format", "parse"]
            }
            
            if func.category in category_keywords:
                if any(kw in prompt_lower for kw in category_keywords[func.category]):
                    confidence += 0.15
            
            # Apply SR threshold
            if confidence >= func.sr_threshold:
                matches.append((func, confidence))
        
        # Sort by confidence and limit results
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:max_matches]
    
    def execute_rem_function(self, func: REMFunction, context: ChatContext, 
                           params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute a REM function with enhanced error handling and logging
        
        Args:
            func: REM function to execute
            context: Chat context
            params: Optional parameters
            
        Returns:
            Execution result with metadata
        """
        result = {
            "function_name": func.name,
            "success": False,
            "output": None,
            "error": None,
            "execution_time": 0.0,
            "sr_trace": None,
            "metadata": {}
        }
        
        start_time = __import__("time").time()
        
        try:
            # Update usage statistics
            func.usage_count += 1
            func.last_used = start_time
            
            # Determine execution method based on code type
            if func.code.strip().startswith(('Phase', 'Invoke', 'Collapse', 'SR(')):
                # REM CODE execution
                logger.info(f"Executing REM CODE function: {func.name}")
                output = self.interpreter.run_rem_code(func.code, use_enhanced_executor=True)
                result["output"] = output
                result["metadata"]["execution_type"] = "rem_code"
                
                # Get SR trace if available
                if hasattr(self.interpreter.executor.context, 'signature_log'):
                    result["sr_trace"] = self.interpreter.executor.context.signature_log
                
            else:
                # Python code execution
                logger.info(f"Executing Python function: {func.name}")
                if not self.trusted:
                    result["error"] = "Untrusted mode: Python execution disabled"
                    logger.warning("Attempted Python execution in untrusted mode")
                    return result

                # Restricted execution environment: empty builtins
                # NOTE: This provides minimal sandboxing but does not fully
                # protect against malicious code. Only trusted code should be
                # executed in this context.
                local_env = {"context": context, "params": params or {}}
                globals_dict = {"__builtins__": {}}
                exec(func.code, globals_dict, local_env)
                
                # Try to call the function
                if func.name in local_env:
                    if callable(local_env[func.name]):
                        output = local_env[func.name]()
                    else:
                        output = local_env[func.name]
                    result["output"] = output
                    result["metadata"]["execution_type"] = "python"
                else:
                    result["error"] = f"Function '{func.name}' not found in executed code"
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Function execution error: {e}")
        
        finally:
            result["execution_time"] = __import__("time").time() - start_time
            
            # Save updated function data
            self._save_functions()
        
        return result
    
    def rem_chat_bridge(self, prompt: str, user_id: str = "default", 
                       session_id: str = "default") -> Dict[str, Any]:
        """
        Main chat bridge function with comprehensive processing
        
        Args:
            prompt: User input prompt
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            Comprehensive response with execution results and metadata
        """
        context = self.get_context(user_id, session_id)
        context.add_message("user", prompt)
        
        # Analyze prompt
        intent_analysis = self.analyze_prompt_intent(prompt, context)
        
        response = {
            "prompt": prompt,
            "intent_analysis": intent_analysis,
            "matches": [],
            "execution_results": [],
            "response_text": "",
            "suggestions": [],
            "metadata": {
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": __import__("time").time()
            }
        }
        
        # Handle different intents
        if intent_analysis["primary_intent"] == "function_query":
            # List functions
            function_list = []
            for category, func_names in self.function_categories.items():
                function_list.append(f"**{category.title()}**: {', '.join(func_names)}")
            
            response["response_text"] = f"📚 Available REM Functions:\n\n" + "\n".join(function_list)
            response["suggestions"] = ["Try calling a specific function", "Ask about function details"]
            
        elif intent_analysis["primary_intent"] == "rem_code_execution":
            # Direct REM CODE execution
            try:
                execution_output = self.interpreter.run_rem_code(prompt, use_enhanced_executor=True)
                response["execution_results"] = [{"output": execution_output, "type": "rem_code"}]
                response["response_text"] = f"🚀 REM CODE Execution:\n\n" + "\n".join(execution_output)
            except Exception as e:
                response["response_text"] = f"❌ REM CODE Execution Error: {e}"
        
        else:
            # Function matching and execution
            matches = self.match_functions_advanced(prompt, context)
            response["matches"] = [(func.name, score) for func, score in matches]
            
            if matches:
                # Execute the best match
                best_func, confidence = matches[0]
                
                if confidence >= best_func.sr_threshold:
                    logger.info(f"Executing function: {best_func.name} (confidence: {confidence:.2f})")
                    
                    execution_result = self.execute_rem_function(best_func, context)
                    response["execution_results"].append(execution_result)
                    
                    if execution_result["success"]:
                        output = execution_result["output"]
                        if isinstance(output, list):
                            output = "\n".join(map(str, output))
                        
                        response["response_text"] = f"🔄 Function '{best_func.name}' executed:\n\n📤 {output}"
                        
                        # Add persona signature if available
                        if best_func.persona != "Auto":
                            response["response_text"] += f"\n\n🔏 Signed by: {best_func.persona}"
                    else:
                        response["response_text"] = f"❌ Function execution failed: {execution_result['error']}"
                else:
                    response["response_text"] = f"⚠️ Function '{best_func.name}' found but confidence too low ({confidence:.2f} < {best_func.sr_threshold})"
            else:
                response["response_text"] = "🔍 No matching REM functions found."
                response["suggestions"] = [
                    "Try rephrasing your request",
                    "Check available functions with 'list functions'",
                    "Create a new function if needed"
                ]
        
        # Add response to context
        context.add_message("assistant", response["response_text"], 
                          {"intent": intent_analysis["primary_intent"], 
                           "matches": len(response["matches"])})
        
        return response
    
    def add_function(self, name: str, description: str, code: str, 
                    keywords: List[str], persona: str = "Auto", 
                    category: str = "general") -> bool:
        """
        Add a new REM function
        
        Args:
            name: Function name
            description: Function description
            code: Function code (REM CODE or Python)
            keywords: Keywords for matching
            persona: Associated persona
            category: Function category
            
        Returns:
            True if added successfully
        """
        try:
            func = REMFunction(
                name=name,
                description=description,
                code=code,
                keywords=keywords,
                persona=persona,
                category=category,
                created_at=__import__("time").time()
            )
            
            self.functions[name] = func
            
            # Update categories
            if category not in self.function_categories:
                self.function_categories[category] = []
            if name not in self.function_categories[category]:
                self.function_categories[category].append(name)
            
            self._save_functions()
            logger.info(f"Added function: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add function {name}: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get bridge statistics"""
        return {
            "total_functions": len(self.functions),
            "categories": dict(self.function_categories),
            "active_contexts": len(self.contexts),
            "total_usage": sum(func.usage_count for func in self.functions.values()),
            "most_used_function": max(self.functions.values(), 
                                    key=lambda f: f.usage_count).name if self.functions else None
        }

# ==================== Legacy Compatibility Functions ====================

def load_rem_functions(path: str = "memory.json") -> List[Dict[str, Any]]:
    """Legacy compatibility function"""
    bridge = REMChatBridge(path)
    return [func.to_dict() for func in bridge.functions.values()]

def match_function_from_prompt(prompt: str, function_list: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Legacy compatibility function"""
    # Convert to REMFunction objects
    functions = {func["name"]: REMFunction.from_dict(func) for func in function_list}
    
    # Create temporary bridge
    bridge = REMChatBridge()
    bridge.functions = functions
    
    context = bridge.get_context()
    matches = bridge.match_functions_advanced(prompt, context, max_matches=1)
    
    return matches[0][0].to_dict() if matches else None

def execute_function(func: Dict[str, Any]) -> str:
    """Legacy compatibility function"""
    rem_func = REMFunction.from_dict(func)
    
    bridge = REMChatBridge()
    context = bridge.get_context()
    
    result = bridge.execute_rem_function(rem_func, context)
    
    if result["success"]:
        return str(result["output"])
    else:
        return f"[ExecutionError] {result['error']}"

def rem_chat_bridge(prompt: str) -> str:
    """Legacy compatibility function"""
    bridge = REMChatBridge()
    response = bridge.rem_chat_bridge(prompt)
    return response["response_text"]

# ==================== CLI Interface ====================

def main():
    """CLI interface for testing the chat bridge"""
    bridge = REMChatBridge()
    
    print("🌀 REM CODE Chat Bridge - Enhanced Version")
    print("Type 'quit' to exit, 'stats' for statistics, 'help' for commands")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n💬 Commander Input: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'stats':
                stats = bridge.get_statistics()
                print(f"📊 Statistics: {json.dumps(stats, indent=2)}")
                continue
            elif user_input.lower() == 'help':
                print("""
Available commands:
- Any REM CODE: Direct execution
- Function names: Execute specific functions
- 'list functions': Show available functions
- 'stats': Show bridge statistics
- 'quit': Exit the bridge
                """)
                continue
            
            if not user_input:
                continue
            
            response = bridge.rem_chat_bridge(user_input)
            print(f"\n{response['response_text']}")
            
            # Show suggestions if available
            if response.get("suggestions"):
                print(f"\n💡 Suggestions: {', '.join(response['suggestions'])}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
