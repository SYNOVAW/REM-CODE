# functions/functions.py
"""
Enhanced REM CODE Functions Manager
Provides comprehensive function management with modern AST processing and execution
"""

import json
import os
import time
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path

# Import REM CODE components with fallback handling
try:
    from engine.rem_executor import execute_function, REMExecutor, create_executor
    from engine.ast_generator import create_ast_generator, generate_ast_from_lines
    from engine.interpreter import REMInterpreter, get_global_interpreter
    from engine.persona_router import PersonaRouter, get_global_router
except ImportError as e:
    logging.warning(f"Some REM CODE components not available: {e}")
    # Fallback imports for basic functionality
    execute_function = lambda lines, sr: [f"Basic execution: {len(lines)} lines"]
    create_ast_generator = lambda: None
    REMInterpreter = None

try:
    from zine.generator import generate_zine_from_function
except ImportError:
    generate_zine_from_function = lambda name, lines: f"ZINE for {name}: {len(lines)} lines"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== Enhanced Data Structures ====================

@dataclass
class FunctionMetadata:
    """Enhanced function metadata with comprehensive tracking"""
    name: str
    body: List[str]
    
    # Creation and modification tracking
    created_at: float = field(default_factory=time.time)
    modified_at: float = field(default_factory=time.time)
    version: int = 1
    
    # Execution tracking
    call_count: int = 0
    last_called: Optional[float] = None
    total_execution_time: float = 0.0
    
    # Analysis data
    ast_cache: Optional[Any] = None
    ast_generation_time: Optional[float] = None
    line_count: int = field(init=False)
    
    # Tags and categorization
    tags: List[str] = field(default_factory=list)
    description: str = ""
    author: str = "Unknown"
    
    def __post_init__(self):
        """Calculate derived fields"""
        self.line_count = len([line for line in self.body if line.strip()])
    
    def update_body(self, new_body: List[str]):
        """Update function body and metadata"""
        self.body = new_body
        self.modified_at = time.time()
        self.version += 1
        self.line_count = len([line for line in new_body if line.strip()])
        self.ast_cache = None  # Invalidate AST cache
    
    def record_execution(self, execution_time: float = 0.0):
        """Record function execution"""
        self.call_count += 1
        self.last_called = time.time()
        self.total_execution_time += execution_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "body": self.body,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "version": self.version,
            "call_count": self.call_count,
            "last_called": self.last_called,
            "total_execution_time": self.total_execution_time,
            "line_count": self.line_count,
            "tags": self.tags,
            "description": self.description,
            "author": self.author
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FunctionMetadata':
        """Create from dictionary"""
        return cls(
            name=data["name"],
            body=data["body"],
            created_at=data.get("created_at", time.time()),
            modified_at=data.get("modified_at", time.time()),
            version=data.get("version", 1),
            call_count=data.get("call_count", 0),
            last_called=data.get("last_called"),
            total_execution_time=data.get("total_execution_time", 0.0),
            tags=data.get("tags", []),
            description=data.get("description", ""),
            author=data.get("author", "Unknown")
        )

# ==================== Enhanced Function Manager ====================

class REMFunctionManager:
    """Enhanced REM CODE function manager with comprehensive features"""
    
    def __init__(self, memory_path: Optional[str] = None):
        """Initialize function manager"""
        self.memory_path = memory_path or self._get_default_memory_path()
        self.functions: Dict[str, FunctionMetadata] = {}
        
        # Initialize components
        self.ast_generator = create_ast_generator() if create_ast_generator else None
        self.executor = create_executor() if 'create_executor' in globals() else None
        self.interpreter = REMInterpreter() if REMInterpreter else None
        self.persona_router = PersonaRouter() if 'PersonaRouter' in globals() else None
        
        # Load existing functions
        self.load_memory()
        
        # Execution history
        self.execution_history: List[Dict[str, Any]] = []
    
    def _get_default_memory_path(self) -> str:
        """Get default memory file path"""
        base_dir = Path(__file__).parent.parent
        memory_dir = base_dir / "memory"
        memory_dir.mkdir(exist_ok=True)
        return str(memory_dir / "functions.json")
    
    def load_memory(self) -> None:
        """Load functions from persistent storage"""
        try:
            if os.path.exists(self.memory_path):
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Handle legacy format
                if "functions" in data:
                    legacy_functions = data["functions"]
                    for name, func_data in legacy_functions.items():
                        if isinstance(func_data, dict) and "body" in func_data:
                            body = func_data["body"]
                        else:
                            body = func_data
                        
                        # Ensure body is a list
                        if isinstance(body, str):
                            body = body.strip().split("\n")
                        
                        self.functions[name] = FunctionMetadata(name=name, body=body)
                else:
                    # New format
                    for name, func_data in data.items():
                        self.functions[name] = FunctionMetadata.from_dict(func_data)
                
                logger.info(f"Loaded {len(self.functions)} functions from {self.memory_path}")
            else:
                logger.info("No existing memory file found, starting with empty function registry")
                
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            self.functions = {}
    
    def save_memory(self) -> None:
        """Save functions to persistent storage"""
        try:
            # Create backup if file exists
            if os.path.exists(self.memory_path):
                backup_path = f"{self.memory_path}.backup"
                os.rename(self.memory_path, backup_path)
            
            # Save current state
            data = {name: func.to_dict() for name, func in self.functions.items()}
            
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Saved {len(self.functions)} functions to {self.memory_path}")
            
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def define_function(self, name: str, lines: Union[str, List[str]], 
                       description: str = "", tags: List[str] = None,
                       author: str = "Unknown") -> str:
        """
        Define or update a function with enhanced metadata
        
        Args:
            name: Function name
            lines: Function body (string or list of lines)
            description: Function description
            tags: Function tags for categorization
            author: Function author
            
        Returns:
            Status message
        """
        # Normalize lines input
        if isinstance(lines, str):
            body = lines.strip().split("\n")
        else:
            body = lines
        
        # Clean empty lines
        body = [line for line in body if line.strip()]
        
        if not body:
            return f"❌ Cannot define empty function '{name}'"
        
        # Check if function exists
        is_update = name in self.functions
        
        if is_update:
            # Update existing function
            self.functions[name].update_body(body)
            self.functions[name].description = description
            self.functions[name].tags = tags or []
            self.functions[name].author = author
            status = f"✅ Function '{name}' updated (v{self.functions[name].version})"
        else:
            # Create new function
            self.functions[name] = FunctionMetadata(
                name=name, body=body, description=description,
                tags=tags or [], author=author
            )
            status = f"✅ Function '{name}' defined ({len(body)} lines)"
        
        # Save to persistent storage
        self.save_memory()
        
        logger.info(f"Function defined: {name} ({'updated' if is_update else 'created'})")
        return status
    
    def call_function(self, name: str, sr_value: float = 0.0, 
                     use_enhanced_execution: bool = True) -> List[str]:
        """
        Call a function with enhanced execution tracking
        
        Args:
            name: Function name
            sr_value: Synchronization Ratio for execution
            use_enhanced_execution: Use enhanced executor if available
            
        Returns:
            Execution results
        """
        if name not in self.functions:
            return [f"❌ Function '{name}' not found"]
        
        func = self.functions[name]
        start_time = time.time()
        
        try:
            if use_enhanced_execution and self.interpreter:
                # Use enhanced interpreter
                code = "\n".join(func.body)
                results = self.interpreter.run_rem_code(code, use_enhanced_executor=True)
            else:
                # Use legacy execution
                results = execute_function(func.body, sr_value=sr_value)
            
            execution_time = time.time() - start_time
            
            # Record execution
            func.record_execution(execution_time)
            
            # Add to execution history
            self.execution_history.append({
                "function_name": name,
                "sr_value": sr_value,
                "execution_time": execution_time,
                "timestamp": time.time(),
                "result_count": len(results) if isinstance(results, list) else 1
            })
            
            # Save updated metadata
            self.save_memory()
            
            logger.info(f"Function executed: {name} (SR: {sr_value}, Time: {execution_time:.3f}s)")
            return results
            
        except Exception as e:
            error_msg = f"❌ Error executing function '{name}': {e}"
            logger.error(error_msg)
            return [error_msg]
    
    def list_functions(self, include_metadata: bool = False) -> Union[List[str], Dict[str, Dict]]:
        """
        List all functions with optional metadata
        
        Args:
            include_metadata: If True, return detailed metadata
            
        Returns:
            Function list or metadata dictionary
        """
        if include_metadata:
            return {name: func.to_dict() for name, func in self.functions.items()}
        else:
            return list(self.functions.keys())
    
    def generate_ast(self, name: str, use_enhanced: bool = True) -> Dict[str, Any]:
        """
        Generate AST for a function with caching
        
        Args:
            name: Function name
            use_enhanced: Use enhanced AST generator if available
            
        Returns:
            AST or error dictionary
        """
        if name not in self.functions:
            return {"error": f"Function '{name}' not found"}
        
        func = self.functions[name]
        
        # Check if AST is cached
        if func.ast_cache is not None:
            return {
                "ast": func.ast_cache,
                "cached": True,
                "generation_time": func.ast_generation_time
            }
        
        try:
            start_time = time.time()
            
            if use_enhanced and self.ast_generator:
                # Use enhanced AST generator
                ast = self.ast_generator.generate_ast(func.body)
            else:
                # Use legacy parser
                try:
                    from parser.grammar_transformer import parse_lines
                    ast = parse_lines(func.body)
                except ImportError:
                    # Final fallback
                    ast = generate_ast_from_lines(func.body) if 'generate_ast_from_lines' in globals() else {"error": "No AST generator available"}
            
            generation_time = time.time() - start_time
            
            # Cache the result
            func.ast_cache = ast
            func.ast_generation_time = generation_time
            
            return {
                "ast": ast,
                "cached": False,
                "generation_time": generation_time
            }
            
        except Exception as e:
            error_msg = f"Parse error for function '{name}': {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def generate_zine(self, name: str) -> str:
        """
        Generate ZINE output for a function
        
        Args:
            name: Function name
            
        Returns:
            ZINE content or error message
        """
        if name not in self.functions:
            return f"❌ Function '{name}' not found"
        
        func = self.functions[name]
        
        try:
            return generate_zine_from_function(name, func.body)
        except Exception as e:
            error_msg = f"❌ Error generating ZINE for '{name}': {e}"
            logger.error(error_msg)
            return error_msg
    
    def delete_function(self, name: str) -> str:
        """Delete a function"""
        if name not in self.functions:
            return f"❌ Function '{name}' not found"
        
        del self.functions[name]
        self.save_memory()
        
        logger.info(f"Function deleted: {name}")
        return f"✅ Function '{name}' deleted"
    
    def search_functions(self, query: str, search_in: List[str] = None) -> List[str]:
        """
        Search functions by name, description, or content
        
        Args:
            query: Search query
            search_in: Fields to search in ['name', 'description', 'body', 'tags']
            
        Returns:
            List of matching function names
        """
        if search_in is None:
            search_in = ['name', 'description', 'body']
        
        query_lower = query.lower()
        matches = []
        
        for name, func in self.functions.items():
            match_found = False
            
            if 'name' in search_in and query_lower in name.lower():
                match_found = True
            elif 'description' in search_in and query_lower in func.description.lower():
                match_found = True
            elif 'body' in search_in and any(query_lower in line.lower() for line in func.body):
                match_found = True
            elif 'tags' in search_in and any(query_lower in tag.lower() for tag in func.tags):
                match_found = True
            
            if match_found:
                matches.append(name)
        
        return matches
    
    def get_function_stats(self) -> Dict[str, Any]:
        """Get comprehensive function statistics"""
        if not self.functions:
            return {"error": "No functions defined"}
        
        total_functions = len(self.functions)
        total_lines = sum(func.line_count for func in self.functions.values())
        total_calls = sum(func.call_count for func in self.functions.values())
        total_execution_time = sum(func.total_execution_time for func in self.functions.values())
        
        # Most called function
        most_called = max(self.functions.values(), key=lambda f: f.call_count)
        
        # Recently modified
        recently_modified = sorted(self.functions.values(), key=lambda f: f.modified_at, reverse=True)[:5]
        
        return {
            "total_functions": total_functions,
            "total_lines": total_lines,
            "total_calls": total_calls,
            "total_execution_time": total_execution_time,
            "average_lines_per_function": total_lines / total_functions,
            "most_called_function": {
                "name": most_called.name,
                "call_count": most_called.call_count
            },
            "recently_modified": [f.name for f in recently_modified]
        }
    
    def export_functions(self, export_path: str = None) -> str:
        """Export all functions to a file"""
        if export_path is None:
            export_path = f"rem_functions_export_{int(time.time())}.json"
        
        try:
            export_data = {
                "export_timestamp": time.time(),
                "total_functions": len(self.functions),
                "functions": {name: func.to_dict() for name, func in self.functions.items()}
            }
            
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return f"✅ Exported {len(self.functions)} functions to {export_path}"
        except Exception as e:
            return f"❌ Export failed: {e}"
    
    def import_functions(self, import_path: str, overwrite: bool = False) -> str:
        """Import functions from a file"""
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "functions" not in data:
                return "❌ Invalid import file format"
            
            imported_count = 0
            skipped_count = 0
            
            for name, func_data in data["functions"].items():
                if name in self.functions and not overwrite:
                    skipped_count += 1
                    continue
                
                self.functions[name] = FunctionMetadata.from_dict(func_data)
                imported_count += 1
            
            self.save_memory()
            
            return f"✅ Imported {imported_count} functions, skipped {skipped_count}"
        except Exception as e:
            return f"❌ Import failed: {e}"

# ==================== Global Manager Instance ====================

_global_manager = None

def get_global_manager() -> REMFunctionManager:
    """Get or create global function manager"""
    global _global_manager
    if _global_manager is None:
        _global_manager = REMFunctionManager()
    return _global_manager

# ==================== Legacy Compatibility Functions ====================

# Global memory for backward compatibility
memory = {"functions": {}}

def define_function(name: str, lines: Union[str, List[str]]) -> str:
    """Legacy compatibility function"""
    manager = get_global_manager()
    result = manager.define_function(name, lines)
    
    # Update legacy memory
    memory["functions"][name] = {"body": lines}
    
    return result

def call_function(name: str, sr_value: float = 0.0) -> List[str]:
    """Legacy compatibility function"""
    manager = get_global_manager()
    return manager.call_function(name, sr_value)

def list_functions() -> List[str]:
    """Legacy compatibility function"""
    manager = get_global_manager()
    return manager.list_functions()

def generate_ast(name: str) -> Dict[str, Any]:
    """Legacy compatibility function"""
    manager = get_global_manager()
    result = manager.generate_ast(name)
    return result.get("ast", result)

def generate_ast_from_lines(lines: List[str]) -> Dict[str, Any]:
    """Legacy compatibility function for direct line parsing"""
    manager = get_global_manager()
    if manager.ast_generator:
        try:
            return manager.ast_generator.generate_ast(lines)
        except Exception as e:
            return {"error": f"Parse error: {str(e)}"}
    else:
        # Fallback
        try:
            from parser.grammar_transformer import parse_lines
            return parse_lines(lines)
        except Exception as e:
            return {"error": f"Parse error: {str(e)}"}

def generate_zine(name: str) -> str:
    """Legacy compatibility function"""
    manager = get_global_manager()
    return manager.generate_zine(name)

def save_memory() -> None:
    """Legacy compatibility function"""
    manager = get_global_manager()
    manager.save_memory()

# ==================== CLI Interface ====================

def main():
    """CLI interface for function management"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python functions.py <command> [args...]")
        print("Commands: list, stats, search <query>, export [path], import <path>")
        return
    
    manager = get_global_manager()
    command = sys.argv[1].lower()
    
    if command == "list":
        functions = manager.list_functions(include_metadata=True)
        for name, metadata in functions.items():
            print(f"{name}: {metadata['line_count']} lines, called {metadata['call_count']} times")
    
    elif command == "stats":
        stats = manager.get_function_stats()
        for key, value in stats.items():
            print(f"{key}: {value}")
    
    elif command == "search" and len(sys.argv) > 2:
        query = sys.argv[2]
        results = manager.search_functions(query)
        print(f"Found {len(results)} functions matching '{query}':")
        for name in results:
            print(f"  - {name}")
    
    elif command == "export":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        result = manager.export_functions(path)
        print(result)
    
    elif command == "import" and len(sys.argv) > 2:
        path = sys.argv[2]
        result = manager.import_functions(path)
        print(result)
    
    else:
        print("Unknown command or missing arguments")

if __name__ == "__main__":
    main()