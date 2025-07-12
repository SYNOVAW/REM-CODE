#!/usr/bin/env python3
"""
Debug script to compare signature generation and verification
"""

from constitutional.signature_manager import SignatureManager, SignatureType
import json

def debug_signature():
    """Debug signature generation and verification"""
    manager = SignatureManager()
    
    # Generate signature
    signature = manager.generate_signature(
        signature_type=SignatureType.CONSENSUS,
        signer_persona="Ana",
        sr_value=0.85,
        decision_id="TEST_002"
    )
    
    print("=== GENERATED SIGNATURE ===")
    print(f"Hash: {signature.signature_hash}")
    print(f"Metadata: {signature.metadata}")
    
    # Check if in cache
    print(f"\n=== CACHE CHECK ===")
    print(f"In cache: {signature.signature_hash in manager.signature_cache}")
    
    # Try verification
    print(f"\n=== VERIFICATION ===")
    result = manager.verify_signature(signature.signature_hash)
    print(f"Verification result: {result}")
    
    # Debug the verification process
    if signature.signature_hash in manager.signature_cache:
        cached_sig = manager.signature_cache[signature.signature_hash]
        
        # Recreate generation data
        gen_data = {
            "type": signature.signature_type.value,
            "persona": signature.signer_persona,
            "sr_value": signature.sr_value,
            "timestamp": signature.timestamp,
            "decision_id": signature.decision_id,
            "action_name": signature.metadata.get("action_name", ""),
            "reasoning": signature.metadata.get("reasoning", ""),
            "metadata": signature.metadata
        }
        
        # Recreate verification data
        ver_data = {
            "type": cached_sig.signature_type.value,
            "persona": cached_sig.signer_persona,
            "sr_value": cached_sig.sr_value,
            "timestamp": cached_sig.timestamp,
            "decision_id": cached_sig.decision_id,
            "action_name": cached_sig.metadata.get("action_name", ""),
            "reasoning": cached_sig.metadata.get("reasoning", ""),
            "metadata": cached_sig.metadata
        }
        
        print(f"\n=== DATA COMPARISON ===")
        print(f"Generation data: {json.dumps(gen_data, sort_keys=True, indent=2)}")
        print(f"Verification data: {json.dumps(ver_data, sort_keys=True, indent=2)}")
        
        # Generate hashes
        gen_string = json.dumps(gen_data, sort_keys=True)
        ver_string = json.dumps(ver_data, sort_keys=True)
        
        import hashlib
        gen_hash = hashlib.sha256(gen_string.encode()).hexdigest()
        ver_hash = hashlib.sha256(ver_string.encode()).hexdigest()
        
        print(f"\n=== HASH COMPARISON ===")
        print(f"Generation hash: {gen_hash}")
        print(f"Verification hash: {ver_hash}")
        print(f"Original hash: {signature.signature_hash}")
        print(f"Match: {gen_hash == signature.signature_hash}")

if __name__ == "__main__":
    debug_signature() 