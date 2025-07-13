"""
Tests for rem_shell.py
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open
import time

# Add the project root to the path
sys.path.insert(0, '.')

# Mock rich imports for testing
with patch.dict('sys.modules', {
    'rich.console': MagicMock(),
    'rich.panel': MagicMock(),
    'rich.table': MagicMock(),
    'rich.text': MagicMock(),
    'rich.box': MagicMock(),
    'rich.prompt': MagicMock()
}):
    from shell.rem_shell import (
        Colors, colored, safe_print, PERSONA_EMOJIS, STATUS_INDICATORS,
        create_sr_bar, get_persona_status, REMShellState,
        display_header, display_persona_grid, display_collapse_event,
        create_enhanced_prompt, handle_sr_command, handle_execute_command,
        handle_function_command, handle_config_command, handle_stats_command,
        handle_history_command, handle_personas_command, handle_help_command,
        clear_screen, main_shell_loop, main
    )


class TestColors:
    """Test cases for Colors class"""
    
    def test_colors_attributes(self):
        """Test that all color attributes exist"""
        assert hasattr(Colors, 'RED')
        assert hasattr(Colors, 'GREEN')
        assert hasattr(Colors, 'YELLOW')
        assert hasattr(Colors, 'BLUE')
        assert hasattr(Colors, 'MAGENTA')
        assert hasattr(Colors, 'CYAN')
        assert hasattr(Colors, 'WHITE')
        assert hasattr(Colors, 'RESET')
    
    def test_colors_values(self):
        """Test that color values are strings"""
        assert isinstance(Colors.RED, str)
        assert isinstance(Colors.GREEN, str)
        assert isinstance(Colors.YELLOW, str)
        assert isinstance(Colors.BLUE, str)
        assert isinstance(Colors.MAGENTA, str)
        assert isinstance(Colors.CYAN, str)
        assert isinstance(Colors.WHITE, str)
        assert isinstance(Colors.RESET, str)


class TestColoredFunction:
    """Test cases for colored function"""
    
    def test_colored_valid_color(self):
        """Test colored function with valid color"""
        result = colored("test", "red")
        assert "test" in result
        assert Colors.RED in result
    
    def test_colored_bold(self):
        """Test colored function with bold"""
        result = colored("test", "green", bold=True)
        assert "test" in result
        assert Colors.GREEN in result
        assert '\033[1m' in result
    
    def test_colored_invalid_color(self):
        """Test colored function with invalid color"""
        result = colored("test", "invalid_color")
        assert result == "test"
    
    def test_colored_all_colors(self):
        """Test colored function with all colors"""
        colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        for color in colors:
            result = colored("test", color)
            assert "test" in result


class TestSafePrint:
    """Test cases for safe_print function"""
    
    @patch('shell.rem_shell.console')
    @patch('shell.rem_shell.RICH_AVAILABLE', True)
    def test_safe_print_with_rich(self, mock_console):
        """Test safe_print with rich available"""
        safe_print("test message")
        mock_console.print.assert_called_with("test message")
    
    @patch('shell.rem_shell.RICH_AVAILABLE', False)
    @patch('builtins.print')
    def test_safe_print_without_rich(self, mock_print):
        """Test safe_print without rich"""
        safe_print("test message")
        mock_print.assert_called()
    
    @patch('shell.rem_shell.RICH_AVAILABLE', False)
    @patch('builtins.print')
    def test_safe_print_rich_markup_removal(self, mock_print):
        """Test safe_print removes rich markup"""
        safe_print("[bold]test[/bold] message")
        # Should remove rich markup
        mock_print.assert_called()


class TestPersonaEmojis:
    """Test cases for PERSONA_EMOJIS"""
    
    def test_persona_emojis_exist(self):
        """Test that all expected personas have emojis"""
        expected_personas = [
            "Ana", "JayDen", "JayTH", "JayRa", "JayLUX", 
            "JayMini", "JAYX", "JayKer", "JayVOX", "JayVue", 
            "JayNis", "Jayne"
        ]
        
        for persona in expected_personas:
            assert persona in PERSONA_EMOJIS
            assert isinstance(PERSONA_EMOJIS[persona], str)
    
    def test_persona_emojis_unique(self):
        """Test that all emojis are unique"""
        emojis = list(PERSONA_EMOJIS.values())
        assert len(emojis) == len(set(emojis))


class TestStatusIndicators:
    """Test cases for STATUS_INDICATORS"""
    
    def test_status_indicators_exist(self):
        """Test that all status indicators exist"""
        expected_statuses = ["active", "resonant", "listening", "dormant"]
        
        for status in expected_statuses:
            assert status in STATUS_INDICATORS
            assert isinstance(STATUS_INDICATORS[status], str)


class TestCreateSrBar:
    """Test cases for create_sr_bar function"""
    
    def test_create_sr_bar_basic(self):
        """Test create_sr_bar with basic values"""
        result = create_sr_bar(0.5, 10)
        assert isinstance(result, str)
        assert len(result) == 10
    
    def test_create_sr_bar_full(self):
        """Test create_sr_bar with full value"""
        result = create_sr_bar(1.0, 10)
        assert "█" in result
        assert "░" not in result
    
    def test_create_sr_bar_empty(self):
        """Test create_sr_bar with empty value"""
        result = create_sr_bar(0.0, 10)
        assert "█" not in result
        assert "░" in result
    
    def test_create_sr_bar_different_widths(self):
        """Test create_sr_bar with different widths"""
        for width in [5, 10, 20]:
            result = create_sr_bar(0.5, width)
            assert len(result) == width
    
    @patch('shell.rem_shell.RICH_AVAILABLE', True)
    def test_create_sr_bar_with_rich(self):
        """Test create_sr_bar with rich available"""
        result = create_sr_bar(0.8, 10)
        assert isinstance(result, str)
    
    @patch('shell.rem_shell.RICH_AVAILABLE', False)
    def test_create_sr_bar_without_rich(self):
        """Test create_sr_bar without rich"""
        result = create_sr_bar(0.8, 10)
        assert isinstance(result, str)


class TestGetPersonaStatus:
    """Test cases for get_persona_status function"""
    
    def test_get_persona_status_active(self):
        """Test get_persona_status for active status"""
        assert get_persona_status(0.9) == "active"
        assert get_persona_status(0.85) == "active"
    
    def test_get_persona_status_resonant(self):
        """Test get_persona_status for resonant status"""
        assert get_persona_status(0.8) == "resonant"
        assert get_persona_status(0.7) == "resonant"
    
    def test_get_persona_status_listening(self):
        """Test get_persona_status for listening status"""
        assert get_persona_status(0.6) == "listening"
        assert get_persona_status(0.4) == "listening"
    
    def test_get_persona_status_dormant(self):
        """Test get_persona_status for dormant status"""
        assert get_persona_status(0.3) == "dormant"
        assert get_persona_status(0.0) == "dormant"
    
    def test_get_persona_status_custom_threshold(self):
        """Test get_persona_status with custom threshold"""
        assert get_persona_status(0.8, threshold=0.9) == "resonant"
        assert get_persona_status(0.9, threshold=0.8) == "active"


class TestREMShellState:
    """Test cases for REMShellState class"""
    
    def test_init_default(self):
        """Test REMShellState initialization with defaults"""
        state = REMShellState()
        
        assert state.session_history == []
        assert state.current_phase == "Interactive"
        assert state.visual_mode is True or state.visual_mode is False
        assert isinstance(state.persona_states, dict)
        assert isinstance(state.active_personas, list)
        assert isinstance(state.current_sr_values, dict)
        assert isinstance(state.config, dict)
        assert isinstance(state.stats, dict)
    
    def test_init_visual_mode_false(self):
        """Test REMShellState initialization with visual_mode=False"""
        state = REMShellState(visual_mode=False)
        assert state.visual_mode is False
    
    def test_persona_states_initialization(self):
        """Test that persona states are properly initialized"""
        state = REMShellState()
        
        # Check that all expected personas are initialized
        expected_personas = list(PERSONA_EMOJIS.keys())
        for persona in expected_personas:
            assert persona in state.persona_states
            assert "sr_value" in state.persona_states[persona]
            assert "status" in state.persona_states[persona]
            assert "last_active" in state.persona_states[persona]
            assert "command_count" in state.persona_states[persona]
    
    def test_update_persona_sr(self):
        """Test update_persona_sr method"""
        state = REMShellState()
        persona_name = "Ana"
        new_sr = 0.8
        
        state.update_persona_sr(persona_name, new_sr)
        
        assert state.persona_states[persona_name]["sr_value"] == new_sr
        assert state.current_sr_values[persona_name] == new_sr
    
    def test_update_persona_sr_invalid_persona(self):
        """Test update_persona_sr with invalid persona"""
        state = REMShellState()
        invalid_persona = "InvalidPersona"
        new_sr = 0.8
        
        # Should not raise an exception
        state.update_persona_sr(invalid_persona, new_sr)
    
    def test_activate_persona(self):
        """Test activate_persona method"""
        state = REMShellState()
        persona_name = "Ana"
        
        state.activate_persona(persona_name)
        
        assert persona_name in state.active_personas
        assert state.persona_states[persona_name]["command_count"] == 1
        assert state.persona_states[persona_name]["last_active"] is not None
    
    def test_activate_persona_multiple_times(self):
        """Test activate_persona multiple times"""
        state = REMShellState()
        persona_name = "Ana"
        
        state.activate_persona(persona_name)
        state.activate_persona(persona_name)
        
        assert state.active_personas.count(persona_name) == 1  # Should not duplicate
        assert state.persona_states[persona_name]["command_count"] == 2


class TestDisplayFunctions:
    """Test cases for display functions"""
    
    def test_display_header(self):
        """Test display_header function"""
        state = REMShellState()
        
        # Should not raise an exception
        display_header(state)
    
    def test_display_persona_grid(self):
        """Test display_persona_grid function"""
        state = REMShellState()
        
        # Should not raise an exception
        display_persona_grid(state)
    
    def test_display_persona_grid_visual_mode_false(self):
        """Test display_persona_grid with visual_mode=False"""
        state = REMShellState(visual_mode=False)
        
        # Should not raise an exception
        display_persona_grid(state)
    
    def test_display_collapse_event_triggered(self):
        """Test display_collapse_event with triggered=True"""
        persona_name = "Ana"
        sr_value = 0.9
        threshold = 0.8
        
        # Should not raise an exception
        display_collapse_event(persona_name, sr_value, threshold, triggered=True)
    
    def test_display_collapse_event_not_triggered(self):
        """Test display_collapse_event with triggered=False"""
        persona_name = "Ana"
        sr_value = 0.7
        threshold = 0.8
        
        # Should not raise an exception
        display_collapse_event(persona_name, sr_value, threshold, triggered=False)


class TestCreateEnhancedPrompt:
    """Test cases for create_enhanced_prompt function"""
    
    def test_create_enhanced_prompt_with_active_personas(self):
        """Test create_enhanced_prompt with active personas"""
        state = REMShellState()
        state.persona_states["Ana"]["status"] = "active"
        
        result = create_enhanced_prompt(state)
        
        assert isinstance(result, str)
        assert "Ana" in result
    
    def test_create_enhanced_prompt_without_active_personas(self):
        """Test create_enhanced_prompt without active personas"""
        state = REMShellState()
        # Set all personas to dormant
        for persona in state.persona_states.values():
            persona["status"] = "dormant"
        
        result = create_enhanced_prompt(state)
        
        assert isinstance(result, str)
        assert "🌀" in result
    
    def test_create_enhanced_prompt_visual_mode_false(self):
        """Test create_enhanced_prompt with visual_mode=False"""
        state = REMShellState(visual_mode=False)
        
        result = create_enhanced_prompt(state)
        
        assert result == "rem> "


class TestCommandHandlers:
    """Test cases for command handlers"""
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_sr_command_quick(self, mock_shell_state):
        """Test handle_sr_command with quick mode"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        mock_state.visual_mode = True
        mock_state.persona_states = {"Ana": {"sr_value": 0.8, "status": "active"}}
        mock_state.config = {"sr_weight_profile": "default"}
        mock_state.stats = {"sr_calculations": 0, "commands_executed": 0, "collapse_events": 0}
        
        # Should not raise an exception
        handle_sr_command(["quick"])
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_sr_command_standard(self, mock_shell_state):
        """Test handle_sr_command with standard mode"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        mock_state.visual_mode = False
        mock_state.config = {"sr_weight_profile": "default"}
        mock_state.stats = {"sr_calculations": 0, "commands_executed": 0}
        
        # Should not raise an exception
        handle_sr_command([])
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_execute_command(self, mock_shell_state):
        """Test handle_execute_command"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        mock_state.interpreter = MagicMock()
        mock_state.interpreter.run_rem_code.return_value = ["Test output"]
        mock_state.stats = {"commands_executed": 0}
        
        # Should not raise an exception
        handle_execute_command(["test code"])
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_function_command(self, mock_shell_state):
        """Test handle_function_command"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        
        # Should not raise an exception
        handle_function_command(["list"])
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_config_command(self, mock_shell_state):
        """Test handle_config_command"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        mock_state.config = {"test": "value"}
        
        # Should not raise an exception
        handle_config_command(["show"])
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_stats_command(self, mock_shell_state):
        """Test handle_stats_command"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        mock_state.stats = {"commands_executed": 5}
        
        # Should not raise an exception
        handle_stats_command([])
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_history_command(self, mock_shell_state):
        """Test handle_history_command"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        mock_state.session_history = [{"command": "test", "output": "result"}]
        
        # Should not raise an exception
        handle_history_command([])
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_personas_command(self, mock_shell_state):
        """Test handle_personas_command"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        mock_state.persona_states = {"Ana": {"sr_value": 0.8, "status": "active"}}
        
        # Should not raise an exception
        handle_personas_command([])
    
    @patch('shell.rem_shell.shell_state')
    def test_handle_help_command(self, mock_shell_state):
        """Test handle_help_command"""
        mock_state = MagicMock()
        mock_shell_state.return_value = mock_state
        
        # Should not raise an exception
        handle_help_command([])


class TestUtilityFunctions:
    """Test cases for utility functions"""
    
    @patch('os.system')
    def test_clear_screen(self, mock_system):
        """Test clear_screen function"""
        clear_screen()
        mock_system.assert_called()
    
    @patch('builtins.input')
    @patch('shell.rem_shell.handle_sr_command')
    def test_main_shell_loop(self, mock_handle_sr, mock_input):
        """Test main_shell_loop function"""
        mock_input.return_value = "sr quick"
        
        # Should not raise an exception
        main_shell_loop(visual_mode=False)
    
    @patch('argparse.ArgumentParser')
    def test_main(self, mock_parser):
        """Test main function"""
        mock_parser_instance = MagicMock()
        mock_parser.return_value = mock_parser_instance
        mock_parser_instance.parse_args.return_value = MagicMock(visual_mode=True)
        
        # Should not raise an exception
        main()


if __name__ == "__main__":
    pytest.main([__file__]) 