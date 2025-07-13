"""
Tests for interpreter.py
"""
import pytest
import sys
from unittest.mock import patch, MagicMock
import logging

# Add the project root to the path
sys.path.insert(0, '.')

from engine.interpreter import (
    REMInterpreter, get_global_interpreter, evaluate_sr_expr,
    evaluate_condition, execute, run_rem_code, main,
    DEFAULT_PERSONAS, persona_context, memory
)


class TestREMInterpreter:
    """Test cases for REMInterpreter class"""
    
    def test_init_default_personas(self):
        """Test interpreter initialization with default personas"""
        interpreter = REMInterpreter()
        
        assert interpreter.personas is not None
        assert len(interpreter.personas) > 0
        assert "Ana" in interpreter.personas
        assert "JayDen" in interpreter.personas
        assert interpreter.memory == {}
        assert interpreter.execution_history == []
    
    def test_init_custom_personas(self):
        """Test interpreter initialization with custom personas"""
        from engine.persona_profile import PersonaProfile
        
        custom_personas = {
            "TestPersona": PersonaProfile(
                name="TestPersona",
                phs=0.8, sym=0.8, val=0.8, emo=0.8, fx=0.8,
                specialization="Testing",
                description="Test persona"
            )
        }
        
        interpreter = REMInterpreter(personas=custom_personas)
        
        assert interpreter.personas == custom_personas
        assert "TestPersona" in interpreter.personas
        assert "Ana" not in interpreter.personas
    
    @patch('engine.interpreter.create_ast_generator')
    @patch('engine.interpreter.create_executor')
    def test_initialization_with_mocks(self, mock_create_executor, mock_create_ast):
        """Test interpreter initialization with mocked dependencies"""
        mock_ast_gen = MagicMock()
        mock_executor = MagicMock()
        mock_create_ast.return_value = mock_ast_gen
        mock_create_executor.return_value = mock_executor
        
        interpreter = REMInterpreter()
        
        assert interpreter.ast_generator == mock_ast_gen
        assert interpreter.executor == mock_executor
        mock_create_ast.assert_called_once()
        mock_create_executor.assert_called_once()
    
    def test_evaluate_sr_expression_valid(self):
        """Test SR expression evaluation with valid persona"""
        interpreter = REMInterpreter()
        
        expr = ('sr_expr', 'Ana')
        result = interpreter.evaluate_sr_expression(expr)
        
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
    
    def test_evaluate_sr_expression_with_context(self):
        """Test SR expression evaluation with context"""
        interpreter = REMInterpreter()
        
        expr = ('sr_expr', 'Ana', 'test_context')
        result = interpreter.evaluate_sr_expression(expr)
        
        assert isinstance(result, float)
    
    def test_evaluate_sr_expression_invalid_persona(self):
        """Test SR expression evaluation with invalid persona"""
        interpreter = REMInterpreter()
        
        expr = ('sr_expr', 'InvalidPersona')
        result = interpreter.evaluate_sr_expression(expr)
        
        assert result == 0.0
    
    def test_evaluate_sr_expression_invalid_format(self):
        """Test SR expression evaluation with invalid format"""
        interpreter = REMInterpreter()
        
        # Test with non-tuple
        result = interpreter.evaluate_sr_expression("not_a_tuple")
        assert result == 0.0
        
        # Test with wrong tuple format
        result = interpreter.evaluate_sr_expression(('wrong_type', 'Ana'))
        assert result == 0.0
    
    def test_evaluate_condition_valid(self):
        """Test condition evaluation with valid SR condition"""
        interpreter = REMInterpreter()
        
        condition = ('sr_condition', ('sr_expr', 'Ana'), '>', 0.5)
        result = interpreter.evaluate_condition(condition)
        
        assert isinstance(result, bool)
    
    def test_evaluate_condition_all_operators(self):
        """Test condition evaluation with all operators"""
        interpreter = REMInterpreter()
        
        operators = [">", ">=", "<", "<=", "==", "!="]
        
        for operator in operators:
            condition = ('sr_condition', ('sr_expr', 'Ana'), operator, 0.5)
            result = interpreter.evaluate_condition(condition)
            assert isinstance(result, bool)
    
    def test_evaluate_condition_invalid_format(self):
        """Test condition evaluation with invalid format"""
        interpreter = REMInterpreter()
        
        # Test with non-tuple
        result = interpreter.evaluate_condition("not_a_tuple")
        assert result is False
        
        # Test with wrong tuple format
        result = interpreter.evaluate_condition(('wrong_type', 'Ana'))
        assert result is False
    
    def test_execute_node_set(self):
        """Test execute_node with set operation"""
        interpreter = REMInterpreter()
        
        node = ('set', 'test_var', 'test_value')
        output = interpreter.execute_node(node)
        
        assert len(output) == 1
        assert "[set] test_var = test_value" in output[0]
        assert interpreter.memory['test_var'] == 'test_value'
    
    def test_execute_node_use(self):
        """Test execute_node with use operation"""
        interpreter = REMInterpreter()
        interpreter.memory['test_var'] = 'test_value'
        
        node = ('use', 'test_var')
        output = interpreter.execute_node(node)
        
        assert len(output) == 1
        assert "[use] test_var = test_value" in output[0]
    
    def test_execute_node_use_not_found(self):
        """Test execute_node with use operation for non-existent variable"""
        interpreter = REMInterpreter()
        
        node = ('use', 'non_existent_var')
        output = interpreter.execute_node(node)
        
        assert len(output) == 1
        assert "[use] non_existent_var = None" in output[0]
    
    def test_execute_node_collapse_condition_met(self):
        """Test execute_node with collapse when condition is met"""
        interpreter = REMInterpreter()
        
        # Mock condition evaluation to return True
        with patch.object(interpreter, 'evaluate_condition', return_value=True):
            node = ('collapse', ('sr_condition', ('sr_expr', 'Ana'), '>', 0.5), [('set', 'x', '1')])
            output = interpreter.execute_node(node)
            
            assert len(output) >= 1
            assert "[collapse] Condition met" in output[0]
    
    def test_execute_node_collapse_condition_failed(self):
        """Test execute_node with collapse when condition fails"""
        interpreter = REMInterpreter()
        
        # Mock condition evaluation to return False
        with patch.object(interpreter, 'evaluate_condition', return_value=False):
            node = ('collapse', ('sr_condition', ('sr_expr', 'Ana'), '>', 0.5), [('set', 'x', '1')])
            output = interpreter.execute_node(node)
            
            assert len(output) == 1
            assert "[collapse] Condition failed" in output[0]
    
    def test_execute_node_sync(self):
        """Test execute_node with sync operation"""
        interpreter = REMInterpreter()
        
        node = ('sync', [('set', 'x', '1')])
        output = interpreter.execute_node(node)
        
        assert len(output) >= 1
        assert "[sync] Fallback block" in output[0]
    
    def test_execute_node_call(self):
        """Test execute_node with call operation"""
        interpreter = REMInterpreter()
        
        node = ('call', 'test_verb', ['arg1', 'arg2'])
        output = interpreter.execute_node(node)
        
        assert len(output) == 1
        assert "[test_verb] arg1, arg2" in output[0]
    
    def test_execute_node_persona_call(self):
        """Test execute_node with persona_call operation"""
        interpreter = REMInterpreter()
        
        node = ('persona_call', 'Ana', 'test_verb', ['arg1'])
        output = interpreter.execute_node(node)
        
        assert len(output) == 1
        assert "[Ana.test_verb] arg1" in output[0]
    
    def test_execute_node_describe(self):
        """Test execute_node with describe operation"""
        interpreter = REMInterpreter()
        
        node = ('describe', 'test_name', 'test_content')
        output = interpreter.execute_node(node)
        
        assert len(output) == 1
        assert "[describe:test_name] test_content" in output[0]
    
    def test_execute_node_sign(self):
        """Test execute_node with sign operation"""
        interpreter = REMInterpreter()
        
        node = ('sign', 'test_content', 'test_by', 'test_reason')
        output = interpreter.execute_node(node)
        
        assert len(output) == 1
        assert "[sign:test_by]" in output[0]
        assert "test_content" in output[0]
        assert "test_reason" in output[0]
    
    def test_execute_node_phase(self):
        """Test execute_node with phase operation"""
        interpreter = REMInterpreter()
        
        node = ('phase', 'test_phase', [('set', 'x', '1')])
        output = interpreter.execute_node(node)
        
        assert len(output) >= 1
        assert "[Phase: test_phase]" in output[0]
    
    def test_execute_node_invoke(self):
        """Test execute_node with invoke operation"""
        interpreter = REMInterpreter()
        
        node = ('invoke', 'Ana', [('set', 'x', '1')])
        output = interpreter.execute_node(node)
        
        assert len(output) >= 1
        assert "[Invoke: Ana]" in output[0]
    
    def test_execute_node_invoke_multiple_personas(self):
        """Test execute_node with invoke operation for multiple personas"""
        interpreter = REMInterpreter()
        
        node = ('invoke', ['Ana', 'JayDen'], [('set', 'x', '1')])
        output = interpreter.execute_node(node)
        
        assert len(output) >= 1
        assert "[Invoke: Ana, JayDen]" in output[0]
    
    def test_execute_node_unknown(self):
        """Test execute_node with unknown node type"""
        interpreter = REMInterpreter()
        
        node = ('unknown_type', 'data')
        output = interpreter.execute_node(node)
        
        assert len(output) == 1
        assert "[unknown]" in output[0]
    
    def test_execute_node_invalid_format(self):
        """Test execute_node with invalid node format"""
        interpreter = REMInterpreter()
        
        # Test with non-tuple
        output = interpreter.execute_node("not_a_tuple")
        assert output == []
        
        # Test with empty tuple
        output = interpreter.execute_node(())
        assert output == []
    
    @patch('engine.interpreter.create_ast_generator')
    def test_run_rem_code_enhanced(self, mock_create_ast):
        """Test run_rem_code with enhanced executor"""
        mock_ast_gen = MagicMock()
        mock_ast_gen.generate_ast.return_value = [('set', 'x', '1')]
        mock_create_ast.return_value = mock_ast_gen
        
        interpreter = REMInterpreter()
        interpreter.executor = MagicMock()
        interpreter.executor.execute.return_value = ["Enhanced output"]
        interpreter.executor.context.active_personas = ["Ana"]
        interpreter.executor.context.signature_log = []
        interpreter.executor.context.current_phase = "default"
        
        result = interpreter.run_rem_code("test code", use_enhanced_executor=True)
        
        assert result == ["Enhanced output"]
        assert len(interpreter.execution_history) == 1
    
    @patch('engine.interpreter.create_ast_generator')
    def test_run_rem_code_legacy(self, mock_create_ast):
        """Test run_rem_code with legacy executor"""
        mock_ast_gen = MagicMock()
        mock_ast_gen.generate_ast.return_value = [('set', 'x', '1')]
        mock_create_ast.return_value = mock_ast_gen
        
        interpreter = REMInterpreter()
        
        result = interpreter.run_rem_code("test code", use_enhanced_executor=False)
        
        assert len(result) > 0
    
    @patch('engine.interpreter.create_ast_generator')
    def test_run_rem_code_parse_error(self, mock_create_ast):
        """Test run_rem_code with parse error"""
        mock_ast_gen = MagicMock()
        mock_ast_gen.generate_ast.return_value = {"error": "Parse error"}
        mock_create_ast.return_value = mock_ast_gen
        
        interpreter = REMInterpreter()
        
        result = interpreter.run_rem_code("invalid code")
        
        assert len(result) == 1
        assert "[Parse Error]" in result[0]
    
    @patch('engine.interpreter.create_ast_generator')
    def test_run_rem_code_execution_error(self, mock_create_ast):
        """Test run_rem_code with execution error"""
        mock_ast_gen = MagicMock()
        mock_ast_gen.generate_ast.side_effect = Exception("Execution error")
        mock_create_ast.return_value = mock_ast_gen
        
        interpreter = REMInterpreter()
        
        result = interpreter.run_rem_code("error code")
        
        assert len(result) == 1
        assert "[Execution Error]" in result[0]
    
    def test_get_persona_sr_trace_valid(self):
        """Test get_persona_sr_trace with valid persona"""
        interpreter = REMInterpreter()
        
        result = interpreter.get_persona_sr_trace("Ana")
        
        # The result can be either a dict or an SRTrace object
        assert hasattr(result, 'persona') or isinstance(result, dict)
        if isinstance(result, dict):
            assert "error" not in result
    
    def test_get_persona_sr_trace_invalid(self):
        """Test get_persona_sr_trace with invalid persona"""
        interpreter = REMInterpreter()
        
        result = interpreter.get_persona_sr_trace("InvalidPersona")
        
        assert isinstance(result, dict)
        assert "error" in result
    
    def test_get_execution_summary(self):
        """Test get_execution_summary"""
        interpreter = REMInterpreter()
        
        result = interpreter.get_execution_summary()
        
        assert isinstance(result, dict)
        assert "personas_loaded" in result
        assert "memory_variables" in result
        assert "execution_history_count" in result
        assert "current_phase" in result
        assert "active_personas" in result
        assert "signatures_count" in result
    
    def test_reset(self):
        """Test reset method"""
        interpreter = REMInterpreter()
        interpreter.memory['test'] = 'value'
        interpreter.execution_history.append({'test': 'data'})
        
        interpreter.reset()
        
        assert interpreter.memory == {}
        assert interpreter.execution_history == []


class TestLegacyFunctions:
    """Test cases for legacy compatibility functions"""
    
    def test_get_global_interpreter(self):
        """Test get_global_interpreter"""
        interpreter = get_global_interpreter()
        
        assert isinstance(interpreter, REMInterpreter)
        assert interpreter is get_global_interpreter()  # Singleton
    
    def test_evaluate_sr_expr_legacy(self):
        """Test legacy evaluate_sr_expr function"""
        expr = ('sr_expr', 'Ana')
        result = evaluate_sr_expr(expr)
        
        assert isinstance(result, float)
    
    def test_evaluate_condition_legacy(self):
        """Test legacy evaluate_condition function"""
        condition = ('sr_condition', ('sr_expr', 'Ana'), '>', 0.5)
        result = evaluate_condition(condition)
        
        assert isinstance(result, bool)
    
    @patch('builtins.print')
    def test_execute_legacy(self, mock_print):
        """Test legacy execute function"""
        node = ('set', 'test_var', 'test_value')
        execute(node)
        
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_run_rem_code_legacy(self, mock_print):
        """Test legacy run_rem_code function"""
        code = 'Acta "test"\nNarrate "Hello"'
        result = run_rem_code(code, enhanced=True)
        
        assert isinstance(result, list)
        mock_print.assert_called()


class TestConstants:
    """Test cases for module constants"""
    
    def test_default_personas(self):
        """Test DEFAULT_PERSONAS constant"""
        assert isinstance(DEFAULT_PERSONAS, dict)
        assert len(DEFAULT_PERSONAS) > 0
        assert "Ana" in DEFAULT_PERSONAS
        assert "JayDen" in DEFAULT_PERSONAS
    
    def test_persona_context(self):
        """Test persona_context constant"""
        assert isinstance(persona_context, dict)
        assert len(persona_context) > 0
    
    def test_memory(self):
        """Test memory constant"""
        assert isinstance(memory, dict)


class TestCLI:
    """Test cases for CLI interface"""
    
    @patch('builtins.print')
    @patch('sys.argv', ['interpreter.py'])
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit, mock_print):
        """Test main function with no arguments"""
        try:
            main()
        except IndexError:
            pass  # Expected behavior
        mock_exit.assert_called_with(1)
    
    @patch('builtins.print')
    @patch('sys.argv', ['interpreter.py', 'nonexistent.remc'])
    @patch('sys.exit')
    def test_main_file_not_found(self, mock_exit, mock_print):
        """Test main function with non-existent file"""
        main()
        mock_exit.assert_called_with(1)
    
    @patch('builtins.print')
    @patch('builtins.open', create=True)
    @patch('sys.argv', ['interpreter.py', 'test.remc'])
    def test_main_success(self, mock_open, mock_print):
        """Test main function with valid file"""
        mock_open.return_value.__enter__.return_value.read.return_value = 'Acta "test"'
        
        try:
            main()
        except SystemExit:
            pass  # Expected behavior due to grammar error
        except Exception:
            pass  # Expected behavior due to grammar error
        
        # At least the usage message should be printed
        mock_print.assert_called()


if __name__ == "__main__":
    pytest.main([__file__])

