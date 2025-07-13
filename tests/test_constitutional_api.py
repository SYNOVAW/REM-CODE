#!/usr/bin/env python3
"""
REM-CODE Constitutional API Tests
Covers ConstitutionalAPI and Pydantic models
"""
import pytest
from unittest.mock import Mock, patch

# Mock FastAPI and Pydantic if not available
try:
    from api.constitutional_api import (
        ConstitutionalAPI, AuthorityRequest, ConsensusRequest, 
        SignatureRequest, ConstitutionalActionRequest
    )
    API_AVAILABLE = True
except (ImportError, NameError):
    API_AVAILABLE = False

@pytest.fixture
def authority_request():
    if not API_AVAILABLE:
        pytest.skip("API not available")
    return AuthorityRequest(
        persona="Ana",
        authority_level="Security",
        action="audit_system",
        branch="Judicial"
    )

@pytest.fixture
def consensus_request():
    if not API_AVAILABLE:
        pytest.skip("API not available")
    return ConsensusRequest(
        decision_type="Significant",
        sr_values={"Ana": 0.8, "JayTH": 0.9, "JayDen": 0.7}
    )

@pytest.fixture
def signature_request():
    if not API_AVAILABLE:
        pytest.skip("API not available")
    return SignatureRequest(
        action_name="system_audit",
        persona="Ana",
        sr_value=0.85,
        decision_id="decision_123",
        reasoning="Security compliance check",
        signature_type="execution"
    )

@pytest.fixture
def constitutional_action_request():
    if not API_AVAILABLE:
        pytest.skip("API not available")
    return ConstitutionalActionRequest(
        action_type="security_audit",
        personas=["Ana", "JayTH"],
        authority_level="Security",
        consensus_threshold=0.8,
        description="System security audit",
        metadata={"priority": "high"}
    )

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_authority_request_creation(authority_request):
    assert authority_request.persona == "Ana"
    assert authority_request.authority_level == "Security"
    assert authority_request.action == "audit_system"
    assert authority_request.branch == "Judicial"

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_consensus_request_creation(consensus_request):
    assert consensus_request.decision_type == "Significant"
    assert len(consensus_request.sr_values) == 3
    assert consensus_request.sr_values["Ana"] == 0.8

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_signature_request_creation(signature_request):
    assert signature_request.action_name == "system_audit"
    assert signature_request.persona == "Ana"
    assert signature_request.sr_value == 0.85
    assert signature_request.signature_type == "execution"

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_constitutional_action_request_creation(constitutional_action_request):
    assert constitutional_action_request.action_type == "security_audit"
    assert len(constitutional_action_request.personas) == 2
    assert constitutional_action_request.consensus_threshold == 0.8
    assert constitutional_action_request.metadata["priority"] == "high"

@patch('api.constitutional_api.FASTAPI_AVAILABLE', False)
def test_constitutional_api_fastapi_unavailable():
    """Test that ConstitutionalAPI raises ImportError when FastAPI is not available"""
    with pytest.raises(ImportError, match="FastAPI is required"):
        ConstitutionalAPI()

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
@patch('api.constitutional_api.FASTAPI_AVAILABLE', True)
@patch('api.constitutional_api.FastAPI')
@patch('api.constitutional_api.ConstitutionalEngine')
@patch('api.constitutional_api.AuthorityValidator')
@patch('api.constitutional_api.SRThresholdChecker')
@patch('api.constitutional_api.SignatureManager')
def test_constitutional_api_init(mock_signature_manager, mock_sr_checker, 
                               mock_authority_validator, mock_constitutional_engine, 
                               mock_fastapi):
    """Test ConstitutionalAPI initialization"""
    mock_app = Mock()
    mock_fastapi.return_value = mock_app
    
    api = ConstitutionalAPI()
    
    assert api.app == mock_app
    assert api.constitutional_engine is not None
    assert api.authority_validator is not None
    assert api.sr_checker is not None
    assert api.signature_manager is not None

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
@patch('api.constitutional_api.FASTAPI_AVAILABLE', True)
@patch('api.constitutional_api.FastAPI')
@patch('api.constitutional_api.ConstitutionalEngine')
@patch('api.constitutional_api.AuthorityValidator')
@patch('api.constitutional_api.SRThresholdChecker')
@patch('api.constitutional_api.SignatureManager')
def test_constitutional_api_root_route(mock_signature_manager, mock_sr_checker,
                                     mock_authority_validator, mock_constitutional_engine,
                                     mock_fastapi):
    """Test root route setup"""
    mock_app = Mock()
    mock_fastapi.return_value = mock_app
    
    api = ConstitutionalAPI()
    
    # Verify that routes were set up
    mock_app.get.assert_called()

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
@patch('api.constitutional_api.FASTAPI_AVAILABLE', True)
@patch('api.constitutional_api.FastAPI')
@patch('api.constitutional_api.ConstitutionalEngine')
@patch('api.constitutional_api.AuthorityValidator')
@patch('api.constitutional_api.SRThresholdChecker')
@patch('api.constitutional_api.SignatureManager')
def test_constitutional_api_status_route(mock_signature_manager, mock_sr_checker,
                                       mock_authority_validator, mock_constitutional_engine,
                                       mock_fastapi):
    """Test status route setup"""
    mock_app = Mock()
    mock_fastapi.return_value = mock_app
    
    api = ConstitutionalAPI()
    
    # Verify that status route was set up
    mock_app.get.assert_called()

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
@patch('api.constitutional_api.FASTAPI_AVAILABLE', True)
@patch('api.constitutional_api.FastAPI')
@patch('api.constitutional_api.ConstitutionalEngine')
@patch('api.constitutional_api.AuthorityValidator')
@patch('api.constitutional_api.SRThresholdChecker')
@patch('api.constitutional_api.SignatureManager')
def test_constitutional_api_authority_route(mock_signature_manager, mock_sr_checker,
                                          mock_authority_validator, mock_constitutional_engine,
                                          mock_fastapi):
    """Test authority validation route setup"""
    mock_app = Mock()
    mock_fastapi.return_value = mock_app
    
    api = ConstitutionalAPI()
    
    # Verify that POST route was set up
    mock_app.post.assert_called()

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
@patch('api.constitutional_api.FASTAPI_AVAILABLE', True)
@patch('api.constitutional_api.FastAPI')
@patch('api.constitutional_api.ConstitutionalEngine')
@patch('api.constitutional_api.AuthorityValidator')
@patch('api.constitutional_api.SRThresholdChecker')
@patch('api.constitutional_api.SignatureManager')
def test_constitutional_api_consensus_route(mock_signature_manager, mock_sr_checker,
                                           mock_authority_validator, mock_constitutional_engine,
                                           mock_fastapi):
    """Test consensus check route setup"""
    mock_app = Mock()
    mock_fastapi.return_value = mock_app
    
    api = ConstitutionalAPI()
    
    # Verify that POST route was set up
    mock_app.post.assert_called()

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
@patch('api.constitutional_api.FASTAPI_AVAILABLE', True)
@patch('api.constitutional_api.FastAPI')
@patch('api.constitutional_api.ConstitutionalEngine')
@patch('api.constitutional_api.AuthorityValidator')
@patch('api.constitutional_api.SRThresholdChecker')
@patch('api.constitutional_api.SignatureManager')
def test_constitutional_api_signature_route(mock_signature_manager, mock_sr_checker,
                                           mock_authority_validator, mock_constitutional_engine,
                                           mock_fastapi):
    """Test signature creation route setup"""
    mock_app = Mock()
    mock_fastapi.return_value = mock_app
    
    api = ConstitutionalAPI()
    
    # Verify that POST route was set up
    mock_app.post.assert_called()

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
@patch('api.constitutional_api.FASTAPI_AVAILABLE', True)
@patch('api.constitutional_api.FastAPI')
@patch('api.constitutional_api.ConstitutionalEngine')
@patch('api.constitutional_api.AuthorityValidator')
@patch('api.constitutional_api.SRThresholdChecker')
@patch('api.constitutional_api.SignatureManager')
def test_constitutional_api_constitutional_route(mock_signature_manager, mock_sr_checker,
                                                mock_authority_validator, mock_constitutional_engine,
                                                mock_fastapi):
    """Test constitutional action route setup"""
    mock_app = Mock()
    mock_fastapi.return_value = mock_app
    
    api = ConstitutionalAPI()
    
    # Verify that POST route was set up
    mock_app.post.assert_called()

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_authority_request_optional_fields():
    """Test AuthorityRequest with optional fields"""
    request = AuthorityRequest(
        persona="Ana",
        authority_level="Security",
        action="audit"
    )
    assert request.branch is None

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_signature_request_default_signature_type():
    """Test SignatureRequest with default signature type"""
    request = SignatureRequest(
        action_name="test_action",
        persona="Ana",
        sr_value=0.8,
        decision_id="test_decision",
        reasoning="test reasoning"
    )
    assert request.signature_type == "execution"

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_constitutional_action_request_optional_metadata():
    """Test ConstitutionalActionRequest with optional metadata"""
    request = ConstitutionalActionRequest(
        action_type="test_action",
        personas=["Ana"],
        authority_level="General",
        consensus_threshold=0.7,
        description="test description"
    )
    assert request.metadata is None 