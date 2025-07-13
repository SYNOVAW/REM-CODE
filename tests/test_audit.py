import pytest
from security.audit import AuditLogger, AuditCategory, AuditLevel

@pytest.fixture
def audit_logger():
    return AuditLogger(log_dir='logs/test_audit')

def test_log_event(audit_logger):
    event = audit_logger.log_event(
        user_id='testuser',
        session_id='sess1',
        category=AuditCategory.AUTHENTICATION,
        level=AuditLevel.INFO,
        action='LOGIN',
        resource='test_resource',
        details={'test': True}
    )
    assert event.user_id == 'testuser'
    assert event.action == 'LOGIN'

def test_audit_report(audit_logger):
    audit_logger.log_event(
        user_id='testuser',
        session_id='sess2',
        category=AuditCategory.AUTHENTICATION,
        level=AuditLevel.INFO,
        action='LOGIN',
        resource='test_resource',
        details={'test': True}
    )
    report = audit_logger.get_audit_report()
    assert 'summary' in report

def test_log_authentication(audit_logger):
    event = audit_logger.log_authentication(
        user_id='authuser',
        session_id='sess3',
        success=True,
        method='password',
        ip_address='192.168.1.100'
    )
    assert event.category == AuditCategory.AUTHENTICATION
    assert event.success is True

def test_log_authorization(audit_logger):
    event = audit_logger.log_authorization(
        user_id='authzuser',
        session_id='sess4',
        action='READ_DATA',
        resource='database',
        success=True,
        permission='read'
    )
    assert event.category == AuditCategory.AUTHORIZATION
    assert event.success is True

def test_log_data_access(audit_logger):
    event = audit_logger.log_data_access(
        user_id='datauser',
        session_id='sess5',
        action='READ_RECORDS',
        resource='user_database',
        data_type='personal',
        record_count=100
    )
    assert event.category == AuditCategory.DATA_ACCESS
    assert event.level == AuditLevel.INFO

def test_log_security_event(audit_logger):
    event = audit_logger.log_security_event(
        user_id='securityuser',
        session_id='sess6',
        action='UNAUTHORIZED_ACCESS',
        resource='admin_panel',
        threat_level='HIGH',
        details={'ip': '192.168.1.200'}
    )
    assert event.category == AuditCategory.SECURITY_EVENT
    assert event.level == AuditLevel.SECURITY

def test_audit_event_serialization(audit_logger):
    event = audit_logger.log_event(
        user_id='serialuser',
        session_id='sess7',
        category=AuditCategory.AUTHENTICATION,
        level=AuditLevel.INFO,
        action='LOGIN',
        resource='test_resource',
        details={'test': True}
    )
    
    # Test to_dict
    event_dict = event.to_dict()
    assert 'timestamp' in event_dict
    assert 'user_id' in event_dict
    assert event_dict['user_id'] == 'serialuser'
    
    # Test to_json
    event_json = event.to_json()
    assert isinstance(event_json, str)
    assert 'serialuser' in event_json

def test_security_alerts(audit_logger):
    # Log many events to trigger alerts
    for i in range(15):
        audit_logger.log_security_event(
            user_id=f'alertuser{i}',
            session_id=f'sess{i}',
            action='SECURITY_ALERT',
            resource='test_resource',
            threat_level='MEDIUM',
            details={'test': i}
        )
    
    alerts = audit_logger.get_security_alerts()
    assert isinstance(alerts, list)

def test_export_audit_logs(audit_logger):
    audit_logger.log_event(
        user_id='exportuser',
        session_id='sess8',
        category=AuditCategory.AUTHENTICATION,
        level=AuditLevel.INFO,
        action='LOGIN',
        resource='test_resource',
        details={'test': True}
    )
    
    result = audit_logger.export_audit_logs('test_export.json')
    assert 'test_export.json' in result 