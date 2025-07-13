#!/usr/bin/env python3
"""
REM-CODE Core Engine Tests
Comprehensive test suite for engine modules with low coverage
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from engine.interpreter import REMInterpreter
from engine.rem_executor import REMExecutor, create_executor, execute_function
from engine.persona_router import PersonaRouter, get_global_router, route_personas
from engine.sr_engine import (
    compute_sr, compute_sr_from_dict, compute_sr_trace,
    compute_contextual_sr, compute_multi_persona_sr,
    SRTrace, DEFAULT_WEIGHTS
)
from engine.memory_manager import load_memory, save_memory, add_function, list_functions, get_function_by_name


class TestREMExecutor:
    """Test REM Executor functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.executor = REMExecutor()
    
    def test_executor_creation(self):
        """Test executor creation and initialization"""
        assert self.executor is not None
        assert hasattr(self.executor, 'context')
    
    def test_create_executor(self):
        """Test create_executor factory function"""
        executor = create_executor()
        assert isinstance(executor, REMExecutor)
    
    def test_execute_basic(self):
        """Test basic execution"""
        statements = [('phase', 'Ana', ['print("Hello World")'])]
        result = self.executor.execute(statements, 0.8)
        assert isinstance(result, list)
    
    def test_execute_with_sr(self):
        """Test execution with SR parameter"""
        statements = [('function_def', 'test_func', ['def test():', '    return "test"'])]
        result = self.executor.execute(statements, 0.9)
        assert isinstance(result, list)
    
    def test_execute_function_global(self):
        """Test global execute_function function"""
        lines = ["print('Hello World')", "return 'success'"]
        result = execute_function(lines, 0.8)
        assert isinstance(result, list)
    
    def test_error_handling(self):
        """Test error handling in executor"""
        # Test with empty input
        result = self.executor.execute([], 0.5)
        assert isinstance(result, list)
        
        # Test with invalid statement
        result = self.executor.execute([('invalid', 'test')], 0.5)
        assert isinstance(result, list)


class TestPersonaRouter:
    """Test Persona Router functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.router = PersonaRouter()
    
    def test_router_initialization(self):
        """Test router initialization"""
        assert self.router is not None
        assert hasattr(self.router, 'personas')
    
    def test_get_global_router(self):
        """Test global router access"""
        router = get_global_router()
        assert isinstance(router, PersonaRouter)
    
    def test_route_personas(self):
        """Test persona routing logic"""
        # Test with high SR
        result = self.router.route_personas({"Ana": 0.9, "JayDen": 0.8})
        assert isinstance(result, dict)
        assert len(result) > 0
    
    def test_route_personas_global(self):
        """Test global route_personas function"""
        # Test global function
        route_personas(0.8, 0.7, 0.9, 0.6, 0.8)
        # Function should execute without error
    
    def test_persona_summaries(self):
        """Test persona summaries"""
        summaries = self.router.get_persona_summaries()
        assert isinstance(summaries, list)
    
    def test_routing_analytics(self):
        """Test routing analytics"""
        analytics = self.router.get_routing_analytics()
        assert isinstance(analytics, dict)


class TestSREngine:
    """Test SR Engine functionality"""
    
    def test_compute_sr_basic(self):
        """Test basic SR computation"""
        sr = compute_sr(0.8, 0.7, 0.9, 0.6, 0.8)
        assert isinstance(sr, float)
        assert 0 <= sr <= 1
    
    def test_compute_sr_from_dict(self):
        """Test SR computation from dictionary"""
        metrics = {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8}
        sr = compute_sr_from_dict(metrics)
        assert isinstance(sr, float)
        assert 0 <= sr <= 1
    
    def test_compute_sr_trace(self):
        """Test SR trace computation"""
        metrics = {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8}
        trace = compute_sr_trace("Ana", metrics)
        assert isinstance(trace, SRTrace)
        assert trace.persona == "Ana"
        assert 0 <= trace.sr_value <= 1
    
    def test_compute_contextual_sr(self):
        """Test contextual SR computation"""
        metrics = {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8}
        
        # Test audit context
        audit_sr = compute_contextual_sr(metrics, ".audit", "Ana")
        assert isinstance(audit_sr, float)
        assert 0 <= audit_sr <= 1
        
        # Test memory context
        memory_sr = compute_contextual_sr(metrics, "@memory", "Ana")
        assert isinstance(memory_sr, float)
        assert 0 <= memory_sr <= 1
        
        # Test correlation context
        corr_sr = compute_contextual_sr(metrics, "|JayTH", "Ana")
        assert isinstance(corr_sr, float)
        assert 0 <= corr_sr <= 1
    
    def test_compute_multi_persona_sr(self):
        """Test multi-persona SR computation"""
        multi_metrics = {
            "Ana": {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8},
            "JayDen": {"PHS": 0.9, "SYM": 0.8, "VAL": 0.7, "EMO": 0.8, "FX": 0.7}
        }
        result = compute_multi_persona_sr(multi_metrics)
        assert isinstance(result, dict)
        assert "Ana" in result
        assert "JayDen" in result
        for sr in result.values():
            assert 0 <= sr <= 1
    
    def test_default_weights(self):
        """Test default weight configuration"""
        assert isinstance(DEFAULT_WEIGHTS, dict)
        assert "PHS" in DEFAULT_WEIGHTS
        assert "SYM" in DEFAULT_WEIGHTS
        assert "VAL" in DEFAULT_WEIGHTS
        assert "EMO" in DEFAULT_WEIGHTS
        assert "FX" in DEFAULT_WEIGHTS


class TestMemoryManager:
    """Test Memory Manager functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Initialize memory with proper structure
        initial_memory = {"functions": []}
        save_memory(initial_memory)
    
    def test_memory_operations(self):
        """Test memory operations"""
        # Test adding function
        add_function("test_func", ["def test():", "    return 'hello'"], "Ana", 0.8)
        
        # Test listing functions
        functions = list_functions()
        assert isinstance(functions, list)
        
        # Test getting function by name
        stored_func = get_function_by_name("test_func")
        assert stored_func is not None
        assert stored_func["name"] == "test_func"
    
    def test_memory_persistence(self):
        """Test memory persistence operations"""
        # Test loading memory
        memory_data = load_memory()
        assert isinstance(memory_data, dict)
        assert "functions" in memory_data
        
        # Test saving memory
        test_data = {"functions": [{"name": "test", "code": ["def test(): pass"]}]}
        save_memory(test_data)
        
        # Verify save worked
        loaded_data = load_memory()
        assert "test" in [f["name"] for f in loaded_data.get("functions", [])]


class TestInterpreterIntegration:
    """Test interpreter integration with other components"""
    
    def test_interpreter_basic(self):
        """Test basic interpreter functionality"""
        interpreter = REMInterpreter()
        
        # Test basic REM code execution
        test_code = "Phase Ana:\n    print('Hello from Ana')"
        result = interpreter.run_rem_code(test_code)
        assert isinstance(result, list)
    
    def test_interpreter_with_executor(self):
        """Test interpreter integration with executor"""
        interpreter = REMInterpreter()
        executor = create_executor()
        
        # Test basic integration
        test_code = "Phase Ana:\n    print('Hello from Ana')"
        result = interpreter.run_rem_code(test_code)
        assert isinstance(result, list)
    
    def test_interpreter_with_router(self):
        """Test interpreter integration with persona router"""
        interpreter = REMInterpreter()
        router = get_global_router()
        
        # Test persona routing integration
        test_code = "Invoke Ana, JayDen:\n    print('Multi-persona test')"
        result = interpreter.run_rem_code(test_code)
        assert isinstance(result, list)
    
    def test_interpreter_with_sr_engine(self):
        """Test interpreter integration with SR engine"""
        interpreter = REMInterpreter()
        
        # Test SR computation integration
        test_code = "sr Ana: 0.8\nPhase Ana:\n    print('SR-based execution')"
        result = interpreter.run_rem_code(test_code)
        assert isinstance(result, list)


class TestErrorHandling:
    """Test error handling across engine components"""
    
    def test_executor_error_handling(self):
        """Test executor error handling"""
        executor = REMExecutor()
        
        # Test with invalid function code
        result = executor.execute([("invalid", "syntax")], 0.8)
        assert isinstance(result, list)
    
    def test_router_error_handling(self):
        """Test router error handling"""
        router = PersonaRouter()
        
        # Test with invalid SR values
        result = router.route_personas({"Invalid": 0.0})
        assert isinstance(result, dict)
    
    def test_sr_engine_error_handling(self):
        """Test SR engine error handling"""
        # Test with invalid metrics
        result = compute_sr_from_dict({"invalid": 0.0})
        assert isinstance(result, float)
        assert 0 <= result <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 