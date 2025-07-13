#!/usr/bin/env python3
"""
REM-CODE Vocabulary Manager Tests
Covers core, extended, persona, and phase vocabularies
"""
import pytest
from engine.vocabulary_manager import (
    VocabularyManager, get_vocabulary_manager, register_extended_verbs,
    get_persona_vocabulary, get_vocabulary_stats
)

def test_core_vocabulary_load():
    vm = VocabularyManager()
    assert isinstance(vm.core_verbs, set)
    assert len(vm.core_verbs) > 0

def test_extended_vocabulary_load():
    vm = VocabularyManager()
    assert isinstance(vm.vocabulary_sets, dict)
    assert "meta_cognitive" in vm.vocabulary_sets
    assert "emotional" in vm.vocabulary_sets

def test_persona_vocabularies():
    vm = VocabularyManager()
    for persona in ["JayRa", "Ana", "JayDen", "JayKer", "JayTH", "JayLUX", "JAYX"]:
        vocab = vm.persona_vocabularies.get(persona)
        assert isinstance(vocab, set)
        assert len(vocab) > 0

def test_phase_vocabularies():
    vm = VocabularyManager()
    for phase in ["Genesis", "Analysis", "Synthesis", "Collapse", "Integration"]:
        vocab = vm.phase_vocabularies.get(phase)
        assert isinstance(vocab, set)
        assert len(vocab) > 0

def test_get_available_verbs():
    vm = VocabularyManager()
    all_verbs = vm.get_available_verbs()
    assert isinstance(all_verbs, set)
    persona_verbs = vm.get_available_verbs(persona="Ana")
    assert isinstance(persona_verbs, set)
    phase_verbs = vm.get_available_verbs(phase="Genesis")
    assert isinstance(phase_verbs, set)
    both = vm.get_available_verbs(persona="Ana", phase="Genesis")
    assert isinstance(both, set)

def test_get_vocabulary_analysis():
    vm = VocabularyManager()
    analysis = vm.get_vocabulary_analysis()
    assert isinstance(analysis, dict)
    assert "core_verbs_count" in analysis
    assert "extended_verbs_count" in analysis

def test_register_extended_verbs():
    vm = VocabularyManager()
    new_verbs = {"test_category": ["Testa", "Demoa"]}
    vm.register_extended_verbs(new_verbs)
    assert "test_category" in vm.vocabulary_sets
    assert "Testa" in vm.vocabulary_sets["test_category"].verbs

def test_generate_grammar_extension():
    vm = VocabularyManager()
    ext = vm.generate_grammar_extension()
    assert isinstance(ext, str)
    assert "LATIN_VERB" in ext

def test_global_get_vocabulary_manager():
    vm = get_vocabulary_manager()
    assert isinstance(vm, VocabularyManager)

def test_global_register_extended_verbs():
    register_extended_verbs({"global_test": ["Globala"]})
    vm = get_vocabulary_manager()
    assert "global_test" in vm.vocabulary_sets
    assert "Globala" in vm.vocabulary_sets["global_test"].verbs

def test_global_get_persona_vocabulary():
    vocab = get_persona_vocabulary("Ana")
    assert isinstance(vocab, set)
    assert len(vocab) > 0

def test_global_get_vocabulary_stats():
    stats = get_vocabulary_stats()
    assert isinstance(stats, dict)
    assert "core_verbs_count" in stats
    assert "extended_verbs_count" in stats 