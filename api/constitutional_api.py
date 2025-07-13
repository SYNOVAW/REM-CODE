#!/usr/bin/env python3
"""
REM-CODE Lite Constitutional API
REST API for constitutional programming operations
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import asdict

try:
    from fastapi import FastAPI, HTTPException, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from constitutional.constitutional_engine import ConstitutionalEngine, ConstitutionalAction
from constitutional.authority_validator import AuthorityValidator, AuthorityLevel, AuthorityContext
from constitutional.sr_threshold_checker import SRThresholdChecker, DecisionType
from constitutional.signature_manager import SignatureManager, SignatureType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for API
class AuthorityRequest(BaseModel):
    persona: str
    authority_level: str
    action: str
    branch: Optional[str] = None

class ConsensusRequest(BaseModel):
    decision_type: str
    sr_values: Dict[str, float]

class SignatureRequest(BaseModel):
    action_name: str
    persona: str
    sr_value: float
    decision_id: str
    reasoning: str
    signature_type: str = "execution"

class ConstitutionalActionRequest(BaseModel):
    action_type: str
    personas: List[str]
    authority_level: str
    consensus_threshold: float
    description: str
    metadata: Optional[Dict[str, Any]] = None

class ConstitutionalAPI:
    """REST API for constitutional programming operations"""
    
    def __init__(self):
        if not FASTAPI_AVAILABLE:
            raise ImportError("FastAPI is required for Constitutional API")
            
        self.app = FastAPI(
            title="REM-CODE Lite Constitutional API",
            description="REST API for constitutional programming and democratic multi-agent systems",
            version="2.4.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize constitutional components
        self.constitutional_engine = ConstitutionalEngine()
        self.authority_validator = AuthorityValidator()
        self.sr_checker = SRThresholdChecker()
        self.signature_manager = SignatureManager()
        
        # Setup routes
        self._setup_routes()
        
        logger.info("🏛️ Constitutional API initialized")
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            return {
                "message": "REM-CODE Lite Constitutional API",
                "version": "2.4.0",
                "docs": "/docs",
                "endpoints": [
                    "/authority/validate",
                    "/consensus/check", 
                    "/signatures/create",
                    "/constitutional/execute",
                    "/status"
                ]
            }
        
        @self.app.get("/status")
        async def get_status():
            """Get API status and statistics"""
            authority_summary = self.authority_validator.get_authority_summary()
            sr_summary = self.sr_checker.get_threshold_summary()
            signature_summary = self.signature_manager.get_signature_summary()
            
            return {
                "status": "operational",
                "timestamp": datetime.now().isoformat(),
                "authority": authority_summary,
                "consensus": sr_summary,
                "signatures": signature_summary
            }
        
        @self.app.post("/authority/validate")
        async def validate_authority(request: AuthorityRequest):
            """Validate persona authority for an action"""
            try:
                # Convert string to AuthorityLevel
                authority_level = AuthorityLevel(request.authority_level.lower())
                
                context = AuthorityContext(
                    persona=request.persona,
                    requested_authority=authority_level,
                    action=request.action,
                    branch=request.branch
                )
                
                is_valid = self.authority_validator.validate_authority(context)
                persona_authority = self.authority_validator.get_persona_authority(request.persona)
                persona_branch = self.authority_validator.get_persona_branch(request.persona)
                
                return {
                    "valid": is_valid,
                    "persona": request.persona,
                    "requested_authority": request.authority_level,
                    "persona_authority": persona_authority.value,
                    "persona_branch": persona_branch,
                    "action": request.action,
                    "timestamp": datetime.now().isoformat()
                }
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid authority level: {request.authority_level}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/consensus/check")
        async def check_consensus(request: ConsensusRequest):
            """Check SR consensus for a decision"""
            try:
                # Convert string to DecisionType
                decision_type = DecisionType(request.decision_type.lower())
                
                consensus_reached, collective_sr, required_threshold = self.sr_checker.check_consensus(
                    decision_type, request.sr_values
                )
                
                return {
                    "consensus_reached": consensus_reached,
                    "collective_sr": collective_sr,
                    "required_threshold": required_threshold,
                    "decision_type": request.decision_type,
                    "participant_count": len(request.sr_values),
                    "participants": list(request.sr_values.keys()),
                    "timestamp": datetime.now().isoformat()
                }
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid decision type: {request.decision_type}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/signatures/create")
        async def create_signature(request: SignatureRequest):
            """Create a constitutional signature"""
            try:
                # Convert string to SignatureType
                signature_type = SignatureType(request.signature_type.lower())
                
                signature = self.signature_manager.generate_signature(
                    signature_type=signature_type,
                    signer_persona=request.persona,
                    sr_value=request.sr_value,
                    decision_id=request.decision_id,
                    action_name=request.action_name,
                    reasoning=request.reasoning
                )
                
                return {
                    "signature_hash": signature.signature_hash,
                    "signature_type": signature.signature_type.value,
                    "signer_persona": signature.signer_persona,
                    "sr_value": signature.sr_value,
                    "decision_id": signature.decision_id,
                    "action_name": request.action_name,
                    "reasoning": request.reasoning,
                    "timestamp": signature.timestamp
                }
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid signature type: {request.signature_type}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/signatures/{signature_hash}/verify")
        async def verify_signature(signature_hash: str):
            """Verify a signature hash"""
            try:
                is_valid = self.signature_manager.verify_signature(signature_hash)
                
                if signature_hash in self.signature_manager.signature_cache:
                    signature = self.signature_manager.signature_cache[signature_hash]
                    signature_data = {
                        "signature_type": signature.signature_type.value,
                        "signer_persona": signature.signer_persona,
                        "sr_value": signature.sr_value,
                        "decision_id": signature.decision_id,
                        "timestamp": signature.timestamp,
                        "metadata": signature.metadata
                    }
                else:
                    signature_data = None
                
                return {
                    "valid": is_valid,
                    "signature_hash": signature_hash,
                    "signature_data": signature_data,
                    "verification_timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/constitutional/execute")
        async def execute_constitutional_action(request: ConstitutionalActionRequest):
            """Execute a complete constitutional action with validation"""
            try:
                # Convert string to AuthorityLevel
                authority_level = AuthorityLevel(request.authority_level.lower())
                
                # Create constitutional action
                action = ConstitutionalAction(
                    action_type=request.action_type,
                    personas=request.personas,
                    authority_level=authority_level,
                    consensus_threshold=request.consensus_threshold,
                    description=request.description,
                    metadata=request.metadata or {}
                )
                
                # Execute through constitutional engine
                result = self.constitutional_engine.execute_constitutional_action(action)
                
                return {
                    "action_id": action.action_id,
                    "success": result.success,
                    "message": result.message,
                    "execution_details": result.execution_details,
                    "signatures": [sig.signature_hash for sig in result.signatures] if result.signatures else [],
                    "timestamp": datetime.now().isoformat()
                }
                
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid authority level: {request.authority_level}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/personas")
        async def get_personas():
            """Get list of available constitutional personas"""
            authority_summary = self.authority_validator.get_authority_summary()
            
            personas = []
            for branch, branch_info in authority_summary["branch_structure"].items():
                for persona in branch_info["personas"]:
                    persona_authority = self.authority_validator.get_persona_authority(persona)
                    personas.append({
                        "name": persona,
                        "branch": branch,
                        "authority": persona_authority.value,
                        "powers": self.authority_validator.get_persona_powers(persona)
                    })
            
            return {
                "personas": personas,
                "trinity_authority": authority_summary["trinity_authority"],
                "emergency_authority": authority_summary["emergency_authority"],
                "total_personas": authority_summary["total_personas"]
            }
        
        @self.app.get("/examples")
        async def get_examples():
            """Get constitutional programming examples"""
            examples = [
                {
                    "name": "Basic Authority",
                    "file": "01_basic_authority.remc",
                    "description": "Learn basic authority validation",
                    "concepts": ["authority", "signatures", "constitutional_validation"]
                },
                {
                    "name": "Democratic Consensus", 
                    "file": "02_consensus_democracy.remc",
                    "description": "Democratic decision-making through SR consensus",
                    "concepts": ["consensus", "synchrony_rate", "democratic_process"]
                },
                {
                    "name": "Emergency Protocols",
                    "file": "03_emergency_protocols.remc", 
                    "description": "Constitutional crisis management",
                    "concepts": ["emergency", "trinity_authority", "crisis_management"]
                },
                {
                    "name": "Multi-Branch Governance",
                    "file": "04_multi_branch_governance.remc",
                    "description": "Separation of powers implementation",
                    "concepts": ["governance", "separation_of_powers", "inter_branch_coordination"]
                },
                {
                    "name": "Validation & Compliance",
                    "file": "05_validation_compliance.remc",
                    "description": "Comprehensive constitutional compliance",
                    "concepts": ["validation", "compliance", "accountability"]
                }
            ]
            
            return {"examples": examples}

def create_app() -> FastAPI:
    """Factory function to create FastAPI app"""
    if not FASTAPI_AVAILABLE:
        raise ImportError("FastAPI is required for Constitutional API. Install with: pip install fastapi uvicorn")
    
    api = ConstitutionalAPI()
    return api.app

def main():
    """Main entry point for API server"""
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI is required for Constitutional API")
        print("Install with: pip install fastapi uvicorn")
        return
    
    try:
        import uvicorn
        app = create_app()
        
        print("🌀 Starting REM-CODE Lite Constitutional API...")
        print("📚 Documentation: http://localhost:8000/docs")
        print("🔧 ReDoc: http://localhost:8000/redoc")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except ImportError:
        print("❌ uvicorn is required to run the API server")
        print("Install with: pip install uvicorn")
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")

if __name__ == "__main__":
    main()