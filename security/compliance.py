"""
REM-CODE Compliance Framework
Enterprise compliance management for GDPR, CCPA, SOC2, ISO27001, HIPAA
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from pathlib import Path


class ComplianceStandard(Enum):
    """Compliance standards"""
    GDPR = "GDPR"
    CCPA = "CCPA"
    SOC2 = "SOC2"
    ISO27001 = "ISO27001"
    HIPAA = "HIPAA"
    PCI_DSS = "PCI_DSS"
    SOX = "SOX"


class DataCategory(Enum):
    """Data categories for compliance"""
    PERSONAL_DATA = "personal_data"
    SENSITIVE_DATA = "sensitive_data"
    FINANCIAL_DATA = "financial_data"
    HEALTH_DATA = "health_data"
    TECHNICAL_DATA = "technical_data"
    ANONYMIZED_DATA = "anonymized_data"


class ConsentStatus(Enum):
    """Consent status for data processing"""
    GRANTED = "granted"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"
    PENDING = "pending"


@dataclass
class DataSubject:
    """Data subject information for GDPR compliance"""
    subject_id: str
    email: str
    name: str
    consent_status: ConsentStatus
    consent_date: datetime
    data_categories: List[DataCategory]
    processing_purposes: List[str]
    retention_period: timedelta
    rights_exercised: List[str] = None
    
    def __post_init__(self):
        if self.rights_exercised is None:
            self.rights_exercised = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['consent_date'] = self.consent_date.isoformat()
        data['retention_period'] = self.retention_period.total_seconds()
        data['consent_status'] = self.consent_status.value
        data['data_categories'] = [cat.value for cat in self.data_categories]
        return data


@dataclass
class ComplianceEvent:
    """Compliance event record"""
    event_id: str
    timestamp: datetime
    standard: ComplianceStandard
    event_type: str
    description: str
    severity: str
    user_id: str
    data_subject_id: Optional[str] = None
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['standard'] = self.standard.value
        return data


class GDPRCompliance:
    """GDPR compliance management"""
    
    def __init__(self):
        self.data_subjects: Dict[str, DataSubject] = {}
        self.events: List[ComplianceEvent] = []
        self.data_processing_records: Dict[str, Dict[str, Any]] = {}
    
    def register_data_subject(self, 
                             email: str,
                             name: str,
                             data_categories: List[DataCategory],
                             processing_purposes: List[str],
                             retention_period: timedelta) -> str:
        """Register a new data subject"""
        subject_id = str(uuid.uuid4())
        
        data_subject = DataSubject(
            subject_id=subject_id,
            email=email,
            name=name,
            consent_status=ConsentStatus.PENDING,
            consent_date=datetime.now(),
            data_categories=data_categories,
            processing_purposes=processing_purposes,
            retention_period=retention_period
        )
        
        self.data_subjects[subject_id] = data_subject
        
        # Log compliance event
        self._log_event(
            ComplianceStandard.GDPR,
            "DATA_SUBJECT_REGISTERED",
            f"Data subject {email} registered",
            "INFO",
            "system",
            subject_id
        )
        
        return subject_id
    
    def update_consent(self, 
                      subject_id: str,
                      consent_status: ConsentStatus,
                      user_id: str) -> bool:
        """Update consent status for a data subject"""
        if subject_id not in self.data_subjects:
            return False
        
        data_subject = self.data_subjects[subject_id]
        old_status = data_subject.consent_status
        data_subject.consent_status = consent_status
        data_subject.consent_date = datetime.now()
        
        # Log compliance event
        self._log_event(
            ComplianceStandard.GDPR,
            "CONSENT_UPDATED",
            f"Consent updated for {data_subject.email}: {old_status.value} -> {consent_status.value}",
            "INFO",
            user_id,
            subject_id
        )
        
        return True
    
    def exercise_right(self,
                      subject_id: str,
                      right: str,
                      user_id: str) -> bool:
        """Exercise GDPR rights (access, rectification, erasure, etc.)"""
        if subject_id not in self.data_subjects:
            return False
        
        data_subject = self.data_subjects[subject_id]
        if right not in data_subject.rights_exercised:
            data_subject.rights_exercised.append(right)
        
        # Log compliance event
        self._log_event(
            ComplianceStandard.GDPR,
            f"RIGHT_EXERCISED_{right.upper()}",
            f"Right '{right}' exercised for {data_subject.email}",
            "INFO",
            user_id,
            subject_id
        )
        
        return True
    
    def data_breach_notification(self,
                                affected_subjects: List[str],
                                breach_description: str,
                                user_id: str) -> str:
        """Record data breach notification"""
        breach_id = str(uuid.uuid4())
        
        # Log compliance event
        self._log_event(
            ComplianceStandard.GDPR,
            "DATA_BREACH_NOTIFICATION",
            f"Data breach notification: {breach_description}",
            "CRITICAL",
            user_id,
            details={
                'breach_id': breach_id,
                'affected_subjects': affected_subjects,
                'breach_description': breach_description
            }
        )
        
        return breach_id
    
    def _log_event(self,
                   standard: ComplianceStandard,
                   event_type: str,
                   description: str,
                   severity: str,
                   user_id: str,
                   data_subject_id: Optional[str] = None,
                   details: Optional[Dict[str, Any]] = None):
        """Log compliance event"""
        event = ComplianceEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            standard=standard,
            event_type=event_type,
            description=description,
            severity=severity,
            user_id=user_id,
            data_subject_id=data_subject_id,
            details=details or {}
        )
        
        self.events.append(event)


class CCPACompliance:
    """CCPA compliance management"""
    
    def __init__(self):
        self.consumers: Dict[str, Dict[str, Any]] = {}
        self.events: List[ComplianceEvent] = []
    
    def register_consumer(self,
                         email: str,
                         name: str,
                         address: str,
                         phone: str) -> str:
        """Register a CCPA consumer"""
        consumer_id = str(uuid.uuid4())
        
        consumer = {
            'consumer_id': consumer_id,
            'email': email,
            'name': name,
            'address': address,
            'phone': phone,
            'registration_date': datetime.now(),
            'opt_out_status': False,
            'data_sales_opt_out': False,
            'rights_exercised': []
        }
        
        self.consumers[consumer_id] = consumer
        
        # Log compliance event
        self._log_event(
            ComplianceStandard.CCPA,
            "CONSUMER_REGISTERED",
            f"CCPA consumer {email} registered",
            "INFO",
            "system"
        )
        
        return consumer_id
    
    def opt_out_request(self,
                       consumer_id: str,
                       opt_out_type: str,
                       user_id: str) -> bool:
        """Process opt-out request"""
        if consumer_id not in self.consumers:
            return False
        
        consumer = self.consumers[consumer_id]
        
        if opt_out_type == "data_sales":
            consumer['data_sales_opt_out'] = True
        else:
            consumer['opt_out_status'] = True
        
        # Log compliance event
        self._log_event(
            ComplianceStandard.CCPA,
            "OPT_OUT_REQUEST",
            f"Opt-out request processed for {consumer['email']}",
            "INFO",
            user_id,
            details={'opt_out_type': opt_out_type}
        )
        
        return True
    
    def data_disclosure_request(self,
                               consumer_id: str,
                               user_id: str) -> Dict[str, Any]:
        """Process data disclosure request"""
        if consumer_id not in self.consumers:
            return {}
        
        consumer = self.consumers[consumer_id]
        consumer['rights_exercised'].append('data_disclosure')
        
        # Log compliance event
        self._log_event(
            ComplianceStandard.CCPA,
            "DATA_DISCLOSURE_REQUEST",
            f"Data disclosure request for {consumer['email']}",
            "INFO",
            user_id
        )
        
        return {
            'consumer_info': consumer,
            'data_categories': ['personal', 'commercial', 'biometric'],
            'data_sources': ['direct_collection', 'third_party'],
            'business_purposes': ['service_provision', 'security', 'compliance']
        }
    
    def _log_event(self,
                   standard: ComplianceStandard,
                   event_type: str,
                   description: str,
                   severity: str,
                   user_id: str,
                   details: Optional[Dict[str, Any]] = None):
        """Log compliance event"""
        event = ComplianceEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            standard=standard,
            event_type=event_type,
            description=description,
            severity=severity,
            user_id=user_id,
            details=details or {}
        )
        
        self.events.append(event)


class ComplianceManager:
    """
    Comprehensive compliance management system
    """
    
    def __init__(self):
        self.gdpr = GDPRCompliance()
        self.ccpa = CCPACompliance()
        self.compliance_status = {}
        self.audit_trails = {}
        self.risk_assessments = {}
        
        # Initialize compliance status
        self._initialize_compliance_status()
    
    def _initialize_compliance_status(self):
        """Initialize compliance status for all standards"""
        for standard in ComplianceStandard:
            self.compliance_status[standard.value] = {
                'status': 'COMPLIANT',
                'last_assessment': datetime.now(),
                'next_assessment': datetime.now() + timedelta(days=90),
                'issues': [],
                'score': 100
            }
    
    def assess_compliance(self, standard: ComplianceStandard) -> Dict[str, Any]:
        """Assess compliance for a specific standard"""
        assessment = {
            'standard': standard.value,
            'assessment_date': datetime.now(),
            'status': 'COMPLIANT',
            'score': 100,
            'findings': [],
            'recommendations': []
        }
        
        if standard == ComplianceStandard.GDPR:
            assessment.update(self._assess_gdpr_compliance())
        elif standard == ComplianceStandard.CCPA:
            assessment.update(self._assess_ccpa_compliance())
        elif standard == ComplianceStandard.SOC2:
            assessment.update(self._assess_soc2_compliance())
        elif standard == ComplianceStandard.ISO27001:
            assessment.update(self._assess_iso27001_compliance())
        elif standard == ComplianceStandard.HIPAA:
            assessment.update(self._assess_hipaa_compliance())
        
        # Update compliance status
        self.compliance_status[standard.value].update({
            'status': assessment['status'],
            'last_assessment': assessment['assessment_date'],
            'next_assessment': datetime.now() + timedelta(days=90),
            'score': assessment['score']
        })
        
        return assessment
    
    def _assess_gdpr_compliance(self) -> Dict[str, Any]:
        """Assess GDPR compliance"""
        findings = []
        recommendations = []
        score = 100
        
        # Check data subject registration
        if len(self.gdpr.data_subjects) == 0:
            findings.append("No data subjects registered")
            recommendations.append("Implement data subject registration system")
            score -= 20
        
        # Check consent management
        pending_consents = sum(1 for ds in self.gdpr.data_subjects.values() 
                             if ds.consent_status == ConsentStatus.PENDING)
        if pending_consents > 0:
            findings.append(f"{pending_consents} pending consent requests")
            recommendations.append("Process pending consent requests")
            score -= 10
        
        # Check data breach procedures
        if not any(e.event_type == "DATA_BREACH_NOTIFICATION" 
                  for e in self.gdpr.events):
            findings.append("No data breach notification procedures tested")
            recommendations.append("Test data breach notification procedures")
            score -= 15
        
        status = "COMPLIANT" if score >= 80 else "NON_COMPLIANT"
        
        return {
            'status': status,
            'score': score,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _assess_ccpa_compliance(self) -> Dict[str, Any]:
        """Assess CCPA compliance"""
        findings = []
        recommendations = []
        score = 100
        
        # Check consumer registration
        if len(self.ccpa.consumers) == 0:
            findings.append("No CCPA consumers registered")
            recommendations.append("Implement consumer registration system")
            score -= 20
        
        # Check opt-out mechanisms
        opt_out_requests = sum(1 for e in self.ccpa.events 
                             if e.event_type == "OPT_OUT_REQUEST")
        if opt_out_requests == 0:
            findings.append("No opt-out mechanisms tested")
            recommendations.append("Test opt-out request mechanisms")
            score -= 15
        
        status = "COMPLIANT" if score >= 80 else "NON_COMPLIANT"
        
        return {
            'status': status,
            'score': score,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _assess_soc2_compliance(self) -> Dict[str, Any]:
        """Assess SOC2 compliance"""
        findings = []
        recommendations = []
        score = 100
        
        # Check security controls
        security_events = sum(1 for e in self.gdpr.events + self.ccpa.events
                            if e.severity == "CRITICAL")
        if security_events == 0:
            findings.append("No security incident monitoring")
            recommendations.append("Implement security incident monitoring")
            score -= 25
        
        # Check access controls
        access_events = sum(1 for e in self.gdpr.events + self.ccpa.events
                          if "ACCESS" in e.event_type)
        if access_events == 0:
            findings.append("No access control monitoring")
            recommendations.append("Implement access control monitoring")
            score -= 20
        
        status = "COMPLIANT" if score >= 80 else "NON_COMPLIANT"
        
        return {
            'status': status,
            'score': score,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _assess_iso27001_compliance(self) -> Dict[str, Any]:
        """Assess ISO27001 compliance"""
        findings = []
        recommendations = []
        score = 100
        
        # Check information security management
        if len(self.gdpr.events + self.ccpa.events) < 10:
            findings.append("Insufficient security event logging")
            recommendations.append("Implement comprehensive security logging")
            score -= 30
        
        # Check risk assessment
        if not self.risk_assessments:
            findings.append("No risk assessments conducted")
            recommendations.append("Conduct regular risk assessments")
            score -= 25
        
        status = "COMPLIANT" if score >= 80 else "NON_COMPLIANT"
        
        return {
            'status': status,
            'score': score,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _assess_hipaa_compliance(self) -> Dict[str, Any]:
        """Assess HIPAA compliance"""
        findings = []
        recommendations = []
        score = 100
        
        # Check PHI handling
        phi_events = sum(1 for e in self.gdpr.events + self.ccpa.events
                        if "HEALTH" in str(e.details))
        if phi_events == 0:
            findings.append("No PHI handling procedures")
            recommendations.append("Implement PHI handling procedures")
            score -= 40
        
        # Check privacy rule compliance
        privacy_events = sum(1 for e in self.gdpr.events + self.ccpa.events
                           if "PRIVACY" in e.event_type)
        if privacy_events == 0:
            findings.append("No privacy rule compliance monitoring")
            recommendations.append("Implement privacy rule compliance monitoring")
            score -= 30
        
        status = "COMPLIANT" if score >= 80 else "NON_COMPLIANT"
        
        return {
            'status': status,
            'score': score,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        report = {
            'report_date': datetime.now().isoformat(),
            'overall_status': 'COMPLIANT',
            'standards': {},
            'summary': {
                'total_standards': len(ComplianceStandard),
                'compliant_standards': 0,
                'non_compliant_standards': 0,
                'average_score': 0
            }
        }
        
        total_score = 0
        compliant_count = 0
        
        for standard in ComplianceStandard:
            assessment = self.assess_compliance(standard)
            report['standards'][standard.value] = assessment
            
            if assessment['status'] == 'COMPLIANT':
                compliant_count += 1
            
            total_score += assessment['score']
        
        report['summary']['compliant_standards'] = compliant_count
        report['summary']['non_compliant_standards'] = len(ComplianceStandard) - compliant_count
        report['summary']['average_score'] = total_score / len(ComplianceStandard)
        
        if compliant_count < len(ComplianceStandard):
            report['overall_status'] = 'NON_COMPLIANT'
        
        return report
    
    def export_compliance_data(self,
                             standard: ComplianceStandard,
                             format: str = "json") -> str:
        """Export compliance data for a standard"""
        if standard == ComplianceStandard.GDPR:
            data = {
                'data_subjects': [ds.to_dict() for ds in self.gdpr.data_subjects.values()],
                'events': [e.to_dict() for e in self.gdpr.events]
            }
        elif standard == ComplianceStandard.CCPA:
            data = {
                'consumers': self.ccpa.consumers,
                'events': [e.to_dict() for e in self.ccpa.events]
            }
        else:
            data = {'status': 'Not implemented for this standard'}
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            return str(data)
    
    def get_compliance_alerts(self) -> List[Dict[str, Any]]:
        """Get compliance alerts"""
        alerts = []
        
        for standard, status in self.compliance_status.items():
            if status['status'] == 'NON_COMPLIANT':
                alerts.append({
                    'type': f'{standard}_NON_COMPLIANT',
                    'message': f'{standard} compliance issues detected',
                    'severity': 'CRITICAL',
                    'standard': standard
                })
            
            if status['score'] < 70:
                alerts.append({
                    'type': f'{standard}_LOW_SCORE',
                    'message': f'{standard} compliance score is {status["score"]}',
                    'severity': 'WARNING',
                    'standard': standard
                })
        
        return alerts


# Convenience functions for quick compliance operations
def check_gdpr_compliance() -> Dict[str, Any]:
    """Quick GDPR compliance check"""
    manager = ComplianceManager()
    return manager.assess_compliance(ComplianceStandard.GDPR)


def check_ccpa_compliance() -> Dict[str, Any]:
    """Quick CCPA compliance check"""
    manager = ComplianceManager()
    return manager.assess_compliance(ComplianceStandard.CCPA)


def generate_full_compliance_report() -> Dict[str, Any]:
    """Generate full compliance report"""
    manager = ComplianceManager()
    return manager.generate_compliance_report() 