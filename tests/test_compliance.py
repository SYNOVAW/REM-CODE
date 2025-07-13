import pytest
from security.compliance import ComplianceManager, ComplianceStandard, ConsentStatus, DataCategory
from datetime import timedelta, datetime

def test_gdpr_register_and_consent():
    manager = ComplianceManager()
    subject_id = manager.gdpr.register_data_subject(
        email='test@example.com',
        name='Test User',
        data_categories=[DataCategory.PERSONAL_DATA],
        processing_purposes=['test'],
        retention_period=timedelta(days=365)
    )
    assert subject_id
    updated = manager.gdpr.update_consent(subject_id, ConsentStatus.GRANTED, 'admin')
    assert updated

def test_ccpa_register_and_optout():
    manager = ComplianceManager()
    consumer_id = manager.ccpa.register_consumer(
        email='ccpa@example.com',
        name='CCPA User',
        address='123 Main St',
        phone='555-0000'
    )
    assert consumer_id
    result = manager.ccpa.opt_out_request(consumer_id, 'data_sales', 'admin')
    assert result

def test_compliance_report():
    manager = ComplianceManager()
    report = manager.generate_compliance_report()
    assert 'overall_status' in report

def test_gdpr_exercise_rights():
    manager = ComplianceManager()
    subject_id = manager.gdpr.register_data_subject(
        email='rights@example.com',
        name='Rights User',
        data_categories=[DataCategory.PERSONAL_DATA],
        processing_purposes=['test'],
        retention_period=timedelta(days=365)
    )
    
    # Exercise various rights
    assert manager.gdpr.exercise_right(subject_id, 'access', 'admin')
    assert manager.gdpr.exercise_right(subject_id, 'rectification', 'admin')
    assert manager.gdpr.exercise_right(subject_id, 'erasure', 'admin')
    
    # Check that rights were recorded
    subject = manager.gdpr.data_subjects[subject_id]
    assert 'access' in subject.rights_exercised
    assert 'rectification' in subject.rights_exercised

def test_gdpr_data_breach_notification():
    manager = ComplianceManager()
    breach_id = manager.gdpr.data_breach_notification(
        affected_subjects=['subject1', 'subject2'],
        breach_description='Test data breach',
        user_id='admin'
    )
    assert breach_id is not None

def test_ccpa_data_disclosure():
    manager = ComplianceManager()
    consumer_id = manager.ccpa.register_consumer(
        email='disclosure@example.com',
        name='Disclosure User',
        address='456 Oak St',
        phone='555-1111'
    )
    
    disclosure_data = manager.ccpa.data_disclosure_request(consumer_id, 'admin')
    assert isinstance(disclosure_data, dict)
    assert 'consumer_info' in disclosure_data

def test_compliance_assessment():
    manager = ComplianceManager()
    
    # Test GDPR assessment
    gdpr_assessment = manager.assess_compliance(ComplianceStandard.GDPR)
    assert 'status' in gdpr_assessment
    assert 'score' in gdpr_assessment
    
    # Test CCPA assessment
    ccpa_assessment = manager.assess_compliance(ComplianceStandard.CCPA)
    assert 'status' in ccpa_assessment
    assert 'score' in ccpa_assessment
    
    # Test SOC2 assessment
    soc2_assessment = manager.assess_compliance(ComplianceStandard.SOC2)
    assert 'status' in soc2_assessment
    assert 'score' in soc2_assessment

def test_compliance_alerts():
    manager = ComplianceManager()
    alerts = manager.get_compliance_alerts()
    assert isinstance(alerts, list)

def test_export_compliance_data():
    manager = ComplianceManager()
    
    # Export GDPR data
    gdpr_data = manager.export_compliance_data(ComplianceStandard.GDPR)
    assert isinstance(gdpr_data, str)
    
    # Export CCPA data
    ccpa_data = manager.export_compliance_data(ComplianceStandard.CCPA)
    assert isinstance(ccpa_data, str)

def test_data_subject_serialization():
    from security.compliance import DataSubject
    from datetime import datetime, timedelta
    
    subject = DataSubject(
        subject_id='test123',
        email='serial@example.com',
        name='Serial User',
        consent_status=ConsentStatus.GRANTED,
        consent_date=datetime.now(),
        data_categories=[DataCategory.PERSONAL_DATA],
        processing_purposes=['test'],
        retention_period=timedelta(days=365)
    )
    
    # Test to_dict
    subject_dict = subject.to_dict()
    assert 'subject_id' in subject_dict
    assert 'email' in subject_dict
    assert subject_dict['email'] == 'serial@example.com'

def test_compliance_event():
    from security.compliance import ComplianceEvent
    
    event = ComplianceEvent(
        event_id='event123',
        timestamp=datetime.now(),
        standard=ComplianceStandard.GDPR,
        event_type='DATA_SUBJECT_REGISTERED',
        description='Test event',
        severity='INFO',
        user_id='admin'
    )
    
    # Test to_dict
    event_dict = event.to_dict()
    assert 'event_id' in event_dict
    assert 'standard' in event_dict
    assert event_dict['standard'] == 'GDPR' 