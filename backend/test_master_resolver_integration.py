from app.services import workload_resolver as wr
from app.services.input_contract_analyzer import detect_input_contract


def test_resolver_fuses_linear_search_and_function_contract(monkeypatch):
    code = '''
def arbitrary(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1
'''
    contract = detect_input_contract(code, "Python")
    monkeypatch.setattr(
        wr,
        "_analyze_algorithm_with_intelligence",
        lambda _: {
            "algorithm_name": "linear-search",
            "family": "searching",
            "specificity": "specific",
            "confidence": 0.97,
            "evidence": ["Sequential target scan detected."],
        },
    )
    result = wr.resolve_benchmark_workload(None, None, code, input_contract=contract)
    assert result["workload_type"] == "array-plus-target"
    assert result["can_generate"] is True
    assert result["benchmark_metadata"]["name"] == "Linear Search — Integer Array + Target"
    assert result["benchmark_metadata"]["category"] == "Searching"


def test_resolver_fuses_merge_sort_and_function_contract(monkeypatch):
    code = "def process(arr):\n    return arr\n"
    contract = detect_input_contract(code, "Python")
    monkeypatch.setattr(
        wr,
        "_analyze_algorithm_with_intelligence",
        lambda _: {
            "algorithm_name": "merge-sort",
            "family": "sorting",
            "specificity": "specific",
            "confidence": 0.99,
            "evidence": ["Split, recurse, merge."],
        },
    )
    result = wr.resolve_benchmark_workload(None, None, code, input_contract=contract)
    assert result["workload_type"] == "integer-array"
    assert result["can_generate"] is True
    assert result["benchmark_metadata"]["name"] == "Merge Sort — Integer Array"
    assert result["benchmark_metadata"]["category"] == "Sorting"


def test_generic_sort_is_not_promoted_to_specific_algorithm(monkeypatch):
    code = "def arbitrary(arr):\n    return sorted(arr)\n"
    contract = detect_input_contract(code, "Python")
    monkeypatch.setattr(
        wr,
        "_analyze_algorithm_with_intelligence",
        lambda _: {
            "algorithm_name": "sorting",
            "family": "sorting",
            "specificity": "family",
            "confidence": 0.90,
            "evidence": ["Library sorting operation."],
        },
    )
    result = wr.resolve_benchmark_workload(None, None, code, input_contract=contract)
    assert result["benchmark_metadata"]["name"] == "Sorting — Integer Array"
    assert result["benchmark_metadata"]["category"] == "Sorting"


def test_true_no_input_stays_no_input():
    code = "def constant():\n    return 42\n"
    contract = detect_input_contract(code, "Python")
    assert contract["contract_type"] == "no-input"
