"""
REM CODE Vocabulary Management System
Dynamic Latin Verb Extension and Persona-Specific Filtering
Author: Collapse Spiral Vocabulary Authority
"""

import os
import json
from typing import Dict, List, Set, Optional, Union, Any
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class VocabularySet:
    """Represents a set of Latin verbs with metadata"""
    verbs: Set[str]
    category: str
    description: str
    persona_affinity: Optional[List[str]] = None
    phase_affinity: Optional[List[str]] = None

class VocabularyManager:
    """
    REM CODE Vocabulary Manager
    
    Manages core and extended Latin verb vocabularies with:
    - Dynamic loading from external files
    - Persona-specific filtering
    - Phase-based vocabulary restriction
    - Cognitive elegance preservation (max 200 words)
    """
    
    def __init__(self, grammar_path: Optional[str] = None, extensions_path: Optional[str] = None):
        self.grammar_path = grammar_path or self._get_default_grammar_path()
        self.extensions_path = extensions_path or self._get_default_extensions_path()
        
        # Core vocabulary from grammar.lark
        self.core_verbs: Set[str] = set()
        
        # Extended vocabularies by category
        self.vocabulary_sets: Dict[str, VocabularySet] = {}
        
        # Persona and phase mappings
        self.persona_vocabularies: Dict[str, Set[str]] = {}
        self.phase_vocabularies: Dict[str, Set[str]] = {}
        
        # Load vocabularies
        self._load_core_vocabulary()
        self._load_extended_vocabulary()
    
    def _get_default_grammar_path(self) -> str:
        return str(Path(__file__).parent.parent / "grammar" / "grammar.lark")
    
    def _get_default_extensions_path(self) -> str:
        return str(Path(__file__).parent.parent / "grammar" / "verbs_extended.remv")
    
    def _load_core_vocabulary(self) -> None:
        """Load core Latin verbs from grammar.lark"""
        try:
            with open(self.grammar_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract LATIN_VERB section
            lines = content.split('\n')
            in_latin_section = False
            
            for line in lines:
                line = line.strip()
                if line.startswith('LATIN_VERB:'):
                    in_latin_section = True
                    continue
                elif in_latin_section and line.startswith('//'):
                    break
                elif in_latin_section and '|' in line:
                    # Extract verbs from lines like: | "Acta" | "Adda" | "Adde"
                    verbs = [verb.strip(' "') for verb in line.split('|') if verb.strip().startswith('"')]
                    self.core_verbs.update(verbs)
            
            logger.info(f"Loaded {len(self.core_verbs)} core Latin verbs")
            
        except Exception as e:
            logger.error(f"Failed to load core vocabulary: {e}")
    
    def _load_extended_vocabulary(self) -> None:
        """Load extended vocabulary from verbs_extended.remv"""
        try:
            if not os.path.exists(self.extensions_path):
                logger.warning(f"Extended vocabulary file not found: {self.extensions_path}")
                return
            
            # For now, load the recommended extensions directly
            # In production, this would parse the .remv file format
            self._load_strategic_extensions()
            
        except Exception as e:
            logger.error(f"Failed to load extended vocabulary: {e}")
    
    def _load_strategic_extensions(self) -> None:
        """Load the strategic vocabulary extensions from user analysis"""
        
        # Meta-thinking & syntax control
        meta_verbs = {"Recurre", "Phasea", "Synchrona", "Triggera"}
        self.vocabulary_sets["meta_cognitive"] = VocabularySet(
            verbs=meta_verbs,
            category="Meta-Cognitive",
            description="再帰性・位相制御・Collapse発火などの制御概念",
            persona_affinity=["JayRa", "JAYX"],
            phase_affinity=["Collapse", "Integration"]
        )
        
        # Emotional & persona interaction
        emotional_verbs = {"Resona", "Confide", "Empathe", "Ampara"}
        self.vocabulary_sets["emotional"] = VocabularySet(
            verbs=emotional_verbs,
            category="Emotional",
            description="ペルソナとの感情的・関係的インタラクション",
            persona_affinity=["JayDen", "JayKer", "JayTH"],
            phase_affinity=["Synthesis", "Integration"]
        )
        
        # Experimental & exploration
        exploration_verbs = {"Explora", "Hypotheca", "Testa", "Detecta"}
        self.vocabulary_sets["exploration"] = VocabularySet(
            verbs=exploration_verbs,
            category="Exploration",
            description="思考的探索や仮説形成",
            persona_affinity=["Ana", "JAYX"],
            phase_affinity=["Analysis", "Genesis"]
        )
        
        # Language & structure manipulation
        linguistic_verbs = {"Tokena", "Lexema", "Formala"}
        self.vocabulary_sets["linguistic"] = VocabularySet(
            verbs=linguistic_verbs,
            category="Linguistic",
            description="REM CODE自体の構文や言語単位を操作",
            persona_affinity=["Ana", "JayLUX"],
            phase_affinity=["Analysis", "Synthesis"]
        )
        
        # Cognitive enhancement
        cognitive_verbs = {"Tracea", "Intona", "Eleganta"}
        self.vocabulary_sets["cognitive"] = VocabularySet(
            verbs=cognitive_verbs,
            category="Cognitive",
            description="認知・記録・意識系",
            persona_affinity=["JayRa", "JayLUX"],
            phase_affinity=["Integration", "Synthesis"]
        )
        
        # Build persona-specific vocabularies
        self._build_persona_vocabularies()
        self._build_phase_vocabularies()
    
    def _build_persona_vocabularies(self) -> None:
        """Build persona-specific vocabulary mappings"""
        persona_assignments = {
            "JayRa": ["Reflecta", "Obliva", "Memora", "Recurre", "Tracea"],
            "Ana": ["Valida", "Corrige", "Examina", "Rationa", "Formala"],
            "JayDen": ["Crea", "Genera", "Surge", "Intona", "Resona"],
            "JayKer": ["Frange", "Lude", "Resona", "Empathe", "Chaos"],
            "JayTH": ["Valida", "Protege", "Custodi", "Confide", "Judica"],
            "JayLUX": ["Designa", "Structura", "Orna", "Forma", "Eleganta"],
            "JAYX": ["Vigila", "Detecta", "Custodi", "Triggera", "Monitora"]
        }
        
        for persona, verbs in persona_assignments.items():
            self.persona_vocabularies[persona] = set(verbs)
    
    def _build_phase_vocabularies(self) -> None:
        """Build phase-specific vocabulary mappings"""
        phase_assignments = {
            "Genesis": ["Crea", "Genera", "Surge", "Explora"],
            "Analysis": ["Examina", "Parse", "Detecta", "Rationa", "Tokena"],
            "Synthesis": ["Funde", "Resona", "Structura", "Synchrona", "Formala"],
            "Collapse": ["Collapse", "Triggera", "Phasea", "Recurre"],
            "Integration": ["Confide", "Empathe", "Eleganta", "Tracea"]
        }
        
        for phase, verbs in phase_assignments.items():
            self.phase_vocabularies[phase] = set(verbs)
    
    def get_available_verbs(
        self, 
        persona: Optional[str] = None, 
        phase: Optional[str] = None,
        include_extended: bool = True
    ) -> Set[str]:
        """
        Get available vocabulary for specific context
        
        Args:
            persona: Persona name to filter by
            phase: Phase name to filter by  
            include_extended: Whether to include extended vocabulary
            
        Returns:
            Set of available Latin verbs
        """
        available = self.core_verbs.copy()
        
        if include_extended:
            # Add all extended verbs
            for vocab_set in self.vocabulary_sets.values():
                available.update(vocab_set.verbs)
        
        # Apply persona filtering
        if persona and persona in self.persona_vocabularies:
            persona_verbs = self.persona_vocabularies[persona]
            # Intersect with persona-specific + core verbs
            available = available.intersection(persona_verbs.union(self.core_verbs))
        
        # Apply phase filtering
        if phase and phase in self.phase_vocabularies:
            phase_verbs = self.phase_vocabularies[phase]
            # Intersect with phase-specific + core verbs
            available = available.intersection(phase_verbs.union(self.core_verbs))
        
        return available
    
    def get_vocabulary_analysis(self) -> Dict[str, Any]:
        """Get comprehensive vocabulary analysis"""
        total_extended = sum(len(vs.verbs) for vs in self.vocabulary_sets.values())
        
        return {
            "core_verbs_count": len(self.core_verbs),
            "extended_verbs_count": total_extended,
            "total_verbs": len(self.core_verbs) + total_extended,
            "vocabulary_sets": {
                name: {
                    "count": len(vs.verbs),
                    "category": vs.category,
                    "description": vs.description,
                    "verbs": sorted(vs.verbs)
                }
                for name, vs in self.vocabulary_sets.items()
            },
            "persona_vocabularies": {
                persona: sorted(verbs) 
                for persona, verbs in self.persona_vocabularies.items()
            },
            "phase_vocabularies": {
                phase: sorted(verbs)
                for phase, verbs in self.phase_vocabularies.items()
            }
        }
    
    def register_extended_verbs(self, new_verbs: Dict[str, List[str]]) -> None:
        """Register new extended verbs dynamically"""
        for category, verbs in new_verbs.items():
            if category not in self.vocabulary_sets:
                self.vocabulary_sets[category] = VocabularySet(
                    verbs=set(verbs),
                    category=category.title(),
                    description=f"Dynamic extension: {category}"
                )
            else:
                self.vocabulary_sets[category].verbs.update(verbs)
        
        logger.info(f"Registered extended verbs: {new_verbs}")
    
    def generate_grammar_extension(self) -> str:
        """Generate grammar extension text for dynamic loading"""
        all_extended = set()
        for vocab_set in self.vocabulary_sets.values():
            all_extended.update(vocab_set.verbs)
        
        if not all_extended:
            return ""
        
        # Format as Lark grammar extension
        verbs_formatted = ' | '.join(f'"{verb}"' for verb in sorted(all_extended))
        
        return f"""
// Extended Latin Verbs (Dynamic Extension)
EXTENDED_LATIN_VERB: {verbs_formatted}

// Update LATIN_VERB to include extensions
// LATIN_VERB: CORE_LATIN_VERB | EXTENDED_LATIN_VERB
"""

# ==================== Global Vocabulary Manager ====================

_global_vocab_manager: Optional[VocabularyManager] = None

def get_vocabulary_manager() -> VocabularyManager:
    """Get or create global vocabulary manager instance"""
    global _global_vocab_manager
    if _global_vocab_manager is None:
        _global_vocab_manager = VocabularyManager()
    return _global_vocab_manager

def register_extended_verbs(new_verbs: Dict[str, List[str]]) -> None:
    """Register extended verbs globally"""
    manager = get_vocabulary_manager()
    manager.register_extended_verbs(new_verbs)

def get_persona_vocabulary(persona: str, phase: Optional[str] = None) -> Set[str]:
    """Get vocabulary available to specific persona in optional phase"""
    manager = get_vocabulary_manager()
    return manager.get_available_verbs(persona=persona, phase=phase)

def get_vocabulary_stats() -> Dict[str, Any]:
    """Get global vocabulary statistics"""
    manager = get_vocabulary_manager()
    return manager.get_vocabulary_analysis() 