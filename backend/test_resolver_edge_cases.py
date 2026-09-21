import copy
import app.services.workload_resolver as wr
from app.services.workload_resolver import resolve_benchmark_workload


def algo(name=None, family=None, confidence=0.96, specificity="specific"):
    return {
        "workload_type": family or "custom",
        "algorithm_family": family or "custom",
        "algorithm_name": name or "custom",
        "specificity": specificity,
        "confidence": confidence,
        "evidence": ["structural test evidence"],
    }


def contract(kind="integer-array", confidence=0.99):
    return {"contract_type": kind, "confidence": confidence}


def patch_input(monkeypatch, kind="integer-array", confidence=0.99):
    monkeypatch.setattr(wr, "normalize_input_structure_from_contract", lambda c: {
        "status": "known",
        "workload_type": kind,
        "schema": {"type": kind},
        "contract": c,
    })
    monkeypatch.setattr(wr, "workload_generation_capability", lambda s: {
        "can_generate": True, "reason": None,
    })


def test_A_binary_search_integer_array_specific(monkeypatch):
    patch_input(monkeypatch)
    monkeypatch.setattr(wr, "_analyze_algorithm_with_intelligence",
                        lambda code: algo("binary-search", "searching", 0.96))
    r = resolve_benchmark_workload("Search", "Search ordered array", "code", input_contract=contract())
    m = r["benchmark_metadata"]
    assert r["can_generate"] is True
    assert m["name"] == "Binary Search — Integer Array"
    assert m["category"] == "Searching"
    assert m["confidence"]["level"] == "high"


def test_B_sorting_integer_array(monkeypatch):
    patch_input(monkeypatch)
    monkeypatch.setattr(wr, "_analyze_algorithm_with_intelligence",
                        lambda code: algo("merge-sort", "sorting", 0.94))
    r = resolve_benchmark_workload("Sort", "Sort integer array", "code", input_contract=contract())
    assert r["benchmark_metadata"]["category"] == "Sorting"
    assert "Merge Sort" in r["benchmark_metadata"]["name"]


def test_C_unknown_algorithm_never_hallucinates(monkeypatch):
    patch_input(monkeypatch)
    monkeypatch.setattr(wr, "_analyze_algorithm_with_intelligence", lambda code: None)
    r = resolve_benchmark_workload("Array", "Process integer array", "code", input_contract=contract())
    m = r["benchmark_metadata"]
    assert r["can_generate"] is True
    assert m["provenance"]["algorithm"]["name"] in (None, "unknown", "custom")
    assert "Integer Array" in m["name"]


def test_D_binary_search_incompatible_matrix_blocks_generation(monkeypatch):
    patch_input(monkeypatch, "matrix")
    monkeypatch.setattr(wr, "_analyze_algorithm_with_intelligence",
                        lambda code: algo("binary-search", "searching", 0.96))
    r = resolve_benchmark_workload("Search", "Search matrix", "code", input_contract=contract("matrix"))
    assert r["can_generate"] is False
    assert r["resolution"]["decision"] == "reject-conflicting-evidence"
    assert r["detection"]["evidence"]["compatibility"]["status"] == "contradiction"


def test_E_strong_input_weak_algorithm_does_not_promote_algorithm(monkeypatch):
    patch_input(monkeypatch, "integer-array", 0.99)
    monkeypatch.setattr(wr, "_analyze_algorithm_with_intelligence",
                        lambda code: algo("binary-search", "searching", 0.40, "specific"))
    r = resolve_benchmark_workload("Search", "Search array", "code", input_contract=contract("integer-array", 0.99))
    assert r["can_generate"] is True
    assert r["resolution"]["decision"] == "verified-input-only"
    assert r["resolution"]["confidence"] <= 0.75
    assert r["benchmark_metadata"]["confidence"]["level"] in {"low", "medium"}


def test_F_no_input_contract_disables_generation(monkeypatch):
    monkeypatch.setattr(wr, "_analyze_algorithm_with_intelligence",
                        lambda code: algo("binary-search", "searching", 0.96))
    r = resolve_benchmark_workload("Search", "Search integer array", "code")
    assert r["can_generate"] is False
    assert r["detection"]["method"] == "unverified-input-contract"


def test_G_malformed_metadata_disables_generation(monkeypatch):
    patch_input(monkeypatch)
    monkeypatch.setattr(wr, "_analyze_algorithm_with_intelligence",
                        lambda code: algo("binary-search", "searching", 0.96))
    monkeypatch.setattr(wr, "generate_benchmark_metadata", lambda **kwargs: {"name": "broken"})
    r = resolve_benchmark_workload("Search", "Search", "code", input_contract=contract())
    assert r["resolver"]["metadata_validation"]["valid"] is False
    assert r["can_generate"] is False


def test_H_identical_input_is_deterministic(monkeypatch):
    patch_input(monkeypatch)
    monkeypatch.setattr(wr, "_analyze_algorithm_with_intelligence",
                        lambda code: algo("binary-search", "searching", 0.96))
    kwargs = dict(benchmark_name="Search", description="Search ordered array", reference_code="same code",
                  input_contract=contract())
    r1 = resolve_benchmark_workload(**kwargs)
    r2 = resolve_benchmark_workload(**kwargs)
    assert r1 == r2
