"""
REM-CODE Audit Framework
Comprehensive audit logging for enterprise security compliance
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import hmac
import os
from pathlib import Path


class AuditLevel(Enum):
    """Audit log levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    SECURITY = "SECURITY"


class AuditCategory(Enum):
    """Audit event categories"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATA_ACCESS = "data_access"
    SYSTEM_OPERATION = "system_operation"
    SECURITY_EVENT = "security_event"
    COMPLIANCE = "compliance"
    USER_ACTION = "user_action"
    ADMIN_ACTION = "admin_action"


@dataclass
class AuditEvent:
    """Audit event data structure"""
    timestamp: datetime
    event_id: str
    user_id: str
    session_id: str
    category: AuditCategory
    level: AuditLevel
    action: str
    resource: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['category'] = self.category.value
        data['level'] = self.level.value
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), default=str)


class AuditLogger:
    """
    Comprehensive audit logging system for enterprise security
    """
    
    def __init__(self, 
                 log_dir: str = "logs/audit",
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 max_files: int = 10,
                 retention_days: int = 90):
        """
        Initialize audit logger
        
        Args:
            log_dir: Directory for audit logs
            max_file_size: Maximum size of log files in bytes
            max_files: Maximum number of log files to keep
            retention_days: Days to retain audit logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_file_size = max_file_size
        self.max_files = max_files
        self.retention_days = retention_days
        
        # Initialize logging
        self._setup_logging()
        
        # Audit statistics
        self.stats = {
            'total_events': 0,
            'events_by_level': {},
            'events_by_category': {},
            'events_by_user': {},
            'security_events': 0,
            'errors': 0
        }
        
        # Start cleanup task
        self._cleanup_old_logs()
    
    def _setup_logging(self):
        """Setup audit logging configuration"""
        log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('REM_AUDIT')
    
    def _generate_event_id(self, user_id: str, action: str) -> str:
        """Generate unique event ID"""
        timestamp = str(int(time.time() * 1000))
        data = f"{user_id}:{action}:{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _cleanup_old_logs(self):
        """Clean up old audit logs"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        for log_file in self.log_dir.glob("audit_*.log"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                try:
                    log_file.unlink()
                    self.logger.info(f"Cleaned up old audit log: {log_file}")
                except Exception as e:
                    self.logger.error(f"Failed to cleanup log file {log_file}: {e}")
    
    def log_event(self,
                  user_id: str,
                  session_id: str,
                  category: AuditCategory,
                  level: AuditLevel,
                  action: str,
                  resource: str,
                  details: Dict[str, Any],
                  ip_address: Optional[str] = None,
                  user_agent: Optional[str] = None,
                  success: bool = True,
                  error_message: Optional[str] = None) -> AuditEvent:
        """
        Log an audit event
        
        Args:
            user_id: ID of the user performing the action
            session_id: Session ID
            category: Event category
            level: Event level
            action: Action being performed
            resource: Resource being accessed
            details: Additional event details
            ip_address: IP address of the user
            user_agent: User agent string
            success: Whether the action was successful
            error_message: Error message if action failed
            
        Returns:
            AuditEvent: The created audit event
        """
        event_id = self._generate_event_id(user_id, action)
        
        event = AuditEvent(
            timestamp=datetime.now(),
            event_id=event_id,
            user_id=user_id,
            session_id=session_id,
            category=category,
            level=level,
            action=action,
            resource=resource,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=error_message
        )
        
        # Log the event
        log_message = self._format_log_message(event)
        
        if level == AuditLevel.CRITICAL:
            self.logger.critical(log_message)
        elif level == AuditLevel.ERROR:
            self.logger.error(log_message)
        elif level == AuditLevel.WARNING:
            self.logger.warning(log_message)
        elif level == AuditLevel.SECURITY:
            self.logger.warning(f"[SECURITY] {log_message}")
        else:
            self.logger.info(log_message)
        
        # Update statistics
        self._update_stats(event)
        
        return event
    
    def _format_log_message(self, event: AuditEvent) -> str:
        """Format audit event for logging"""
        status = "SUCCESS" if event.success else "FAILURE"
        return (f"Event[{event.event_id}] {status} | "
                f"User[{event.user_id}] Session[{event.session_id}] | "
                f"Action[{event.action}] Resource[{event.resource}] | "
                f"Category[{event.category.value}] Level[{event.level.value}] | "
                f"IP[{event.ip_address or 'N/A'}] | "
                f"Details: {json.dumps(event.details)}")
    
    def _update_stats(self, event: AuditEvent):
        """Update audit statistics"""
        self.stats['total_events'] += 1
        
        # Update level stats
        level_key = event.level.value
        self.stats['events_by_level'][level_key] = self.stats['events_by_level'].get(level_key, 0) + 1
        
        # Update category stats
        category_key = event.category.value
        self.stats['events_by_category'][category_key] = self.stats['events_by_category'].get(category_key, 0) + 1
        
        # Update user stats
        self.stats['events_by_user'][event.user_id] = self.stats['events_by_user'].get(event.user_id, 0) + 1
        
        # Update security events
        if event.level == AuditLevel.SECURITY:
            self.stats['security_events'] += 1
        
        # Update error count
        if not event.success:
            self.stats['errors'] += 1
    
    def log_authentication(self,
                          user_id: str,
                          session_id: str,
                          success: bool,
                          method: str,
                          ip_address: Optional[str] = None,
                          user_agent: Optional[str] = None,
                          error_message: Optional[str] = None):
        """Log authentication events"""
        level = AuditLevel.SECURITY if not success else AuditLevel.INFO
        action = "LOGIN_SUCCESS" if success else "LOGIN_FAILURE"
        
        details = {
            'method': method,
            'timestamp': datetime.now().isoformat()
        }
        
        return self.log_event(
            user_id=user_id,
            session_id=session_id,
            category=AuditCategory.AUTHENTICATION,
            level=level,
            action=action,
            resource="auth_system",
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=error_message
        )
    
    def log_authorization(self,
                         user_id: str,
                         session_id: str,
                         action: str,
                         resource: str,
                         success: bool,
                         permission: str,
                         ip_address: Optional[str] = None,
                         error_message: Optional[str] = None):
        """Log authorization events"""
        level = AuditLevel.SECURITY if not success else AuditLevel.INFO
        
        details = {
            'permission': permission,
            'timestamp': datetime.now().isoformat()
        }
        
        return self.log_event(
            user_id=user_id,
            session_id=session_id,
            category=AuditCategory.AUTHORIZATION,
            level=level,
            action=action,
            resource=resource,
            details=details,
            ip_address=ip_address,
            success=success,
            error_message=error_message
        )
    
    def log_data_access(self,
                       user_id: str,
                       session_id: str,
                       action: str,
                       resource: str,
                       data_type: str,
                       record_count: int,
                       ip_address: Optional[str] = None):
        """Log data access events"""
        details = {
            'data_type': data_type,
            'record_count': record_count,
            'timestamp': datetime.now().isoformat()
        }
        
        return self.log_event(
            user_id=user_id,
            session_id=session_id,
            category=AuditCategory.DATA_ACCESS,
            level=AuditLevel.INFO,
            action=action,
            resource=resource,
            details=details,
            ip_address=ip_address
        )
    
    def log_security_event(self,
                          user_id: str,
                          session_id: str,
                          action: str,
                          resource: str,
                          threat_level: str,
                          details: Dict[str, Any],
                          ip_address: Optional[str] = None):
        """Log security events"""
        details.update({
            'threat_level': threat_level,
            'timestamp': datetime.now().isoformat()
        })
        
        return self.log_event(
            user_id=user_id,
            session_id=session_id,
            category=AuditCategory.SECURITY_EVENT,
            level=AuditLevel.SECURITY,
            action=action,
            resource=resource,
            details=details,
            ip_address=ip_address
        )
    
    def get_audit_report(self, 
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None,
                        user_id: Optional[str] = None,
                        category: Optional[AuditCategory] = None) -> Dict[str, Any]:
        """
        Generate audit report
        
        Args:
            start_date: Start date for report
            end_date: End date for report
            user_id: Filter by user ID
            category: Filter by category
            
        Returns:
            Dictionary containing audit report
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        report = {
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'summary': {
                'total_events': self.stats['total_events'],
                'security_events': self.stats['security_events'],
                'errors': self.stats['errors']
            },
            'breakdown': {
                'by_level': self.stats['events_by_level'],
                'by_category': self.stats['events_by_category'],
                'by_user': self.stats['events_by_user']
            },
            'filters': {
                'user_id': user_id,
                'category': category.value if category else None
            }
        }
        
        return report
    
    def export_audit_logs(self,
                          output_file: str,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          format: str = "json") -> str:
        """
        Export audit logs to file
        
        Args:
            output_file: Output file path
            start_date: Start date for export
            end_date: End date for export
            format: Export format (json, csv)
            
        Returns:
            Path to exported file
        """
        # This would read from actual log files and export
        # For now, return a placeholder
        return f"Audit logs exported to {output_file}"
    
    def get_security_alerts(self) -> List[Dict[str, Any]]:
        """Get current security alerts"""
        alerts = []
        
        # Check for unusual patterns
        if self.stats['security_events'] > 10:
            alerts.append({
                'type': 'HIGH_SECURITY_EVENTS',
                'message': f"High number of security events: {self.stats['security_events']}",
                'severity': 'WARNING'
            })
        
        if self.stats['errors'] > 50:
            alerts.append({
                'type': 'HIGH_ERROR_RATE',
                'message': f"High error rate: {self.stats['errors']} errors",
                'severity': 'CRITICAL'
            })
        
        return alerts


# Convenience functions for quick audit logging
def log_auth_event(user_id: str, session_id: str, success: bool, **kwargs):
    """Quick authentication event logging"""
    logger = AuditLogger()
    return logger.log_authentication(user_id, session_id, success, **kwargs)


def log_access_event(user_id: str, session_id: str, action: str, resource: str, **kwargs):
    """Quick access event logging"""
    logger = AuditLogger()
    return logger.log_authorization(user_id, session_id, action, resource, True, "access", **kwargs)


def log_security_alert(user_id: str, session_id: str, action: str, resource: str, **kwargs):
    """Quick security alert logging"""
    logger = AuditLogger()
    return logger.log_security_event(user_id, session_id, action, resource, "MEDIUM", kwargs) 