import pytest

from app.services.workload_resolver import (
    # ALGORITHMIC_WORKLOAD_TYPES,
    # detect_algorithm_workload,
    detect_input_structure_from_content,
    detect_reference_input_structure,
    detect_reference_input_workload,
)
from app.services.workload_resolver import resolve_benchmark_workload
import app.services.workload_resolver as workload_resolver


# ============================================================
# RETIRED LEGACY ALGORITHM TESTS
# ============================================================
#
# These tests are intentionally kept commented out.
#
# The old heuristic-based algorithm detector has been retired.
# Algorithm detection is now owned by Algorithm Intelligence.
#
# Do NOT uncomment these tests unless the architecture is
# intentionally changed back to the legacy detector.
#
# ============================================================

# ALGORITHM_CASES = [
#     (
#         "sorting",
#         """
#         #include <bits/stdc++.h>
#         using namespace std;
#         int main() {
#             int n; cin >> n;
#             vector<int> a(n);
#             for (int &x : a) cin >> x;
#             sort(a.begin(), a.end());
#             return 0;
#         }
#         """,
#     ),
#     (
#         "searching",
#         """
#         int binarySearch(vector<int>& a, int target) {
#             int lo = 0, hi = (int)a.size() - 1;
#             while (lo <= hi) {
#                 int mid = (lo + hi) / 2;
#                 if (a[mid] == target) return mid;
#                 if (a[mid] < target) lo = mid + 1;
#                 else hi = mid - 1;
#             }
#             return -1;
#         }
#         """,
#     ),
#     (
#         "string-processing",
#         """
#         string s;
#         cin >> s;
#         string t = s;
#         reverse(t.begin(), t.end());
#         for (char c : s) {
#             if (isalpha(c)) cout << (char)tolower(c);
#         }
#         """,
#     ),
#     (
#         "two-pointers",
#         """
#         int left = 0, right = n - 1;
#         while (left < right) {
#             if (a[left] + a[right] < target) ++left;
#             else --right;
#         }
#         """,
#     ),
#     (
#         "sliding-window",
#         """
#         int left = 0, best = 0;
#         map<char, int> freq;
#         for (int right = 0; right < n; ++right) {
#             freq[s[right]]++;
#             while (freq[s[right]] > 1) {
#                 freq[s[left++]]--;
#             }
#             best = max(best, right - left + 1);
#         }
#         """,
#     ),
#     (
#         "prefix-sum",
#         """
#         vector<long long> prefix(n + 1);
#         for (int i = 0; i < n; ++i)
#             prefix[i + 1] = prefix[i] + a[i];
#         """,
#     ),
#     (
#         "hashing",
#         """
#         unordered_map<int, int> freq;
#         for (int x : a) freq[x]++;
#         """,
#     ),
#     (
#         "stack",
#         """
#         stack<char> st;
#         for (char c : s) {
#             if (c == '(') st.push(c);
#             else if (!st.empty()) st.pop();
#         }
#         """,
#     ),
#     (
#         "queue",
#         """
#         queue<int> q;
#         q.push(0);
#         while (!q.empty()) {
#             int u = q.front();
#             q.pop();
#         }
#         """,
#     ),
#     (
#         "recursion",
#         """
#         int factorial(int n) {
#             if (n <= 1) return 1;
#             return n * factorial(n - 1);
#         }
#         """,
#     ),
#     (
#         "backtracking",
#         """
#         void backtrack(int pos) {
#             if (pos == n) return;
#             choose(pos);
#             backtrack(pos + 1);
#             undo(pos);
#         }
#         """,
#     ),
#     (
#         "greedy",
#         """
#         sort(intervals.begin(), intervals.end(), byEnd);
#         int best = 0;
#         for (auto x : intervals) {
#             if (x.start >= end) {
#                 best++;
#                 end = x.end;
#             }
#         }
#         """,
#     ),
#     (
#         "dynamic-programming",
#         """
#         vector<int> dp(n + 1, 0);
#         for (int i = 1; i <= n; ++i) {
#             dp[i] = max(dp[i - 1], dp[i - 2] + value[i]);
#         }
#         """,
#     ),
#     (
#         "tree-traversal",
#         """
#         void inorder(Node* root) {
#             if (!root) return;
#             inorder(root->left);
#             visit(root);
#             inorder(root->right);
#         }
#         """,
#     ),
#     (
#         "graph-traversal",
#         """
#         vector<vector<int>> adj(n);
#         vector<int> visited(n, 0);
#         queue<int> q;
#         visited[src] = 1;
#         q.push(src);
#         while (!q.empty()) {
#             int u = q.front(); q.pop();
#             for (int v : adj[u]) {
#                 if (!visited[v]) {
#                     visited[v] = 1;
#                     q.push(v);
#                 }
#             }
#         }
#         """,
#     ),
#     (
#         "graph-algorithm",
#         """
#         // Dijkstra's shortest path
#         priority_queue<pair<int,int>> pq;
#         """,
#     ),
#     (
#         "matrix-processing",
#         """
#         for (int i = 0; i < n; ++i) {
#             for (int j = 0; j < n; ++j) {
#                 ans[i][j] = a[i][j] + b[i][j];
#             }
#         }
#         """,
#     ),
# ]


# @pytest.mark.parametrize("expected, code", ALGORITHM_CASES)
# def test_algorithm_detection(expected, code):
#     result = detect_algorithm_workload(code)
#     assert result is not None
#     assert result["workload_type"] == expected
#     assert result["workload_type"] in ALGORITHMIC_WORKLOAD_TYPES


# def test_comment_does_not_trigger_sorting():
#     code = """
#     // sort(a.begin(), a.end())
#     int main() { return 0; }
#     """
#     assert detect_algorithm_workload(code) is None


# def test_container_name_alone_does_not_trigger_graph_algorithm():
#     code = """
#     vector<int> graph;
#     cin >> n;
#     for (int i = 0; i < n; ++i) cin >> graph[i];
#     """
#     result = detect_algorithm_workload(code)
#     assert result is None or result["workload_type"] not in {
#         "graph-traversal",
#         "graph-algorithm",
#     }


# ============================================================
# EXISTING ARCHITECTURE REGRESSION TESTS
# ============================================================


def test_resolver_uses_algorithm_intelligence_without_legacy_fallback(
    monkeypatch,
):
    code = """
    #include <iostream>
    #include <vector>
    #include <algorithm>

    using namespace std;

    int main() {
        int n;
        cin >> n;

        vector<int> a(n);

        for (int i = 0; i < n; ++i) {
            cin >> a[i];
        }

        sort(a.begin(), a.end());

        for (int x : a) {
            cout << x << " ";
        }

        return 0;
    }
    """

    result = resolve_benchmark_workload(
        benchmark_name="Sort Array",
        description="Sort an array of integers.",
        reference_code=code,
    )

    assert result["algorithm"]["workload_type"] == "sorting"

    assert (
        result["algorithm"]["detection_method"]
        == "tree-sitter-structural"
    )


def test_algorithm_failure_does_not_fallback_to_heuristics(
    monkeypatch,
):
    code = """
    int main() {
        int a = 10;
        int b = 20;
        return a + b;
    }
    """

    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: None,
    )

    result = resolve_benchmark_workload(
        benchmark_name="Simple Program",
        description="Simple arithmetic program.",
        reference_code=code,
    )

    assert result["algorithm"] is None


def test_legacy_algorithm_detector_is_retired():
    assert not hasattr(
        workload_resolver,
        "detect_algorithm_workload",
    )


def test_legacy_algorithm_type_registry_is_retired():
    assert not hasattr(
        workload_resolver,
        "ALGORITHMIC_WORKLOAD_TYPES",
    )


def test_old_reference_alias_still_works():
    assert (
        detect_reference_input_workload
        is detect_reference_input_structure
    )


def test_content_alias_is_preserved():
    assert detect_input_structure_from_content is not None


# ============================================================
# PHASE 1 — RESOLVER HARDENING TESTS
# ============================================================


def test_resolver_accepts_reliable_compatible_algorithm_and_input(
    monkeypatch,
):
    algorithm = {
        "workload_type": "searching",
        "algorithm_family": "searching",
        "algorithm_name": "binary-search",
        "specificity": "specific",
        "confidence": 0.96,
        "reason": "Binary-search control flow detected.",
        "evidence": [
            "ordered search interval",
            "midpoint update",
        ],
        "complexity": {
            "time": "O(log n)",
            "space": "O(1)",
        },
        "detection_method": "tree-sitter-structural",
        "parser": "tree-sitter",
        "parse_success": True,
        "parse_error_count": 0,
    }

    input_structure = {
        "status": "known",
        "workload_type": "integer-array",
        "schema": {
            "type": "integer-array",
        },
    }

    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: algorithm,
    )

    monkeypatch.setattr(
        workload_resolver,
        "normalize_input_structure_from_contract",
        lambda contract: input_structure,
    )

    monkeypatch.setattr(
        workload_resolver,
        "workload_generation_capability",
        lambda input_structure: {
            "can_generate": True,
            "reason": None,
        },
    )

    monkeypatch.setattr(
        workload_resolver,
        "generate_benchmark_metadata",
        lambda input_structure, algorithm: {
            "name": "Binary Search — Integer Array",
            "category": "Searching",
            "description": (
                "Benchmarks binary search over an ordered "
                "integer array using a target value."
            ),
            "source": "automatic",
            "confidence": {
                "score": 0.96,
                "level": "high",
            },
            "provenance": {
                "algorithm": {
                    "source": "algorithm_intelligence",
                    "name": "binary-search",
                    "family": "searching",
                    "specificity": "specific",
                },
                "input": {
                    "source": "input_contract_analyzer",
                    "contract_type": "integer-array",
                },
            },
            "generation": {
                "strategy": "deterministic-template",
                "version": 1,
            },
            "schema_version": 1,
        },
    )

    result = resolve_benchmark_workload(
        benchmark_name="Search",
        description="Search an ordered array.",
        reference_code="binary search program",
        input_contract={
            "contract_type": "integer-array",
            "confidence": 0.99,
        },
    )

    assert result["status"] == "known"
    assert result["can_generate"] is True

    assert (
        result["algorithm"]["algorithm_name"]
        == "binary-search"
    )

    assert result["resolver"]["schema_version"] == 2
    assert result["resolver"]["validated"] is True

    assert (
        result["benchmark_metadata"]["name"]
        == "Binary Search — Integer Array"
    )


def test_resolver_blocks_incompatible_algorithm_and_input(
    monkeypatch,
):
    algorithm = {
        "workload_type": "searching",
        "algorithm_family": "searching",
        "algorithm_name": "binary-search",
        "specificity": "specific",
        "confidence": 0.96,
        "evidence": [
            "binary-search control flow",
        ],
    }

    input_structure = {
        "status": "known",
        "workload_type": "matrix",
        "schema": {
            "type": "matrix",
        },
    }

    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: algorithm,
    )

    monkeypatch.setattr(
        workload_resolver,
        "normalize_input_structure_from_contract",
        lambda contract: input_structure,
    )

    result = resolve_benchmark_workload(
        benchmark_name="Binary Search",
        description="Search workload",
        reference_code="binary search program",
        input_contract={
            "contract_type": "matrix",
            "confidence": 0.99,
        },
    )

    assert result["status"] == "mismatch"
    assert result["can_generate"] is False

    assert (
        result["detection"]["method"]
        == "resolver-compatibility-validation"
    )

    assert result["detection"]["confidence"] == 0.0

    assert (
        result["detection"]["evidence"]["compatibility"]["status"]
        == "contradiction"
    )


def test_unknown_algorithm_does_not_hallucinate_specific_algorithm(
    monkeypatch,
):
    input_structure = {
        "status": "known",
        "workload_type": "integer-array",
        "schema": {
            "type": "integer-array",
        },
    }

    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: None,
    )

    monkeypatch.setattr(
        workload_resolver,
        "normalize_input_structure_from_contract",
        lambda contract: input_structure,
    )

    result = resolve_benchmark_workload(
        benchmark_name="Custom Workload",
        description="Process an integer array.",
        reference_code="unknown program",
        input_contract={
            "contract_type": "integer-array",
            "confidence": 0.95,
        },
    )

    metadata = result["benchmark_metadata"]

    assert metadata["source"] == "automatic"

    assert metadata["name"]
    assert metadata["category"]
    assert metadata["description"]

    # No invented algorithm should appear.
    assert "binary" not in metadata["name"].lower()
    assert "search" not in metadata["name"].lower()
    assert "sort" not in metadata["name"].lower()

    assert result["algorithm"] is None


def test_resolver_is_deterministic(
    monkeypatch,
):
    algorithm = {
        "workload_type": "searching",
        "algorithm_family": "searching",
        "algorithm_name": "binary-search",
        "specificity": "specific",
        "confidence": 0.96,
        "evidence": [
            "binary-search control flow",
        ],
    }

    input_structure = {
        "status": "known",
        "workload_type": "integer-array",
        "schema": {
            "type": "integer-array",
        },
    }

    metadata = {
        "name": "Binary Search — Integer Array",
        "category": "Searching",
        "description": (
            "Benchmarks binary search over an ordered "
            "integer array using a target value."
        ),
        "source": "automatic",
        "confidence": {
            "score": 0.96,
            "level": "high",
        },
        "provenance": {},
        "generation": {
            "strategy": "deterministic-template",
            "version": 1,
        },
        "schema_version": 1,
    }

    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: algorithm,
    )

    monkeypatch.setattr(
        workload_resolver,
        "normalize_input_structure_from_contract",
        lambda contract: input_structure,
    )

    monkeypatch.setattr(
        workload_resolver,
        "workload_generation_capability",
        lambda input_structure: {
            "can_generate": True,
            "reason": None,
        },
    )

    monkeypatch.setattr(
        workload_resolver,
        "generate_benchmark_metadata",
        lambda input_structure, algorithm: metadata.copy(),
    )

    kwargs = {
        "benchmark_name": "Search",
        "description": "Search an ordered array.",
        "reference_code": "same reference code",
        "input_contract": {
            "contract_type": "integer-array",
            "confidence": 0.99,
        },
    }

    result_1 = resolve_benchmark_workload(**kwargs)
    result_2 = resolve_benchmark_workload(**kwargs)

    assert (
        result_1["benchmark_metadata"]
        == result_2["benchmark_metadata"]
    )

    assert result_1["resolution"] == result_2["resolution"]


def test_resolver_fuses_algorithm_and_input_confidence(
    monkeypatch,
):
    algorithm = {
        "workload_type": "searching",
        "algorithm_family": "searching",
        "algorithm_name": "binary-search",
        "specificity": "specific",
        "confidence": 0.88,
        "evidence": [
            "binary-search control flow",
        ],
    }

    input_structure = {
        "status": "known",
        "workload_type": "integer-array",
        "schema": {
            "type": "integer-array",
        },
    }

    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: algorithm,
    )

    monkeypatch.setattr(
        workload_resolver,
        "normalize_input_structure_from_contract",
        lambda contract: input_structure,
    )

    monkeypatch.setattr(
        workload_resolver,
        "workload_generation_capability",
        lambda input_structure: {
            "can_generate": True,
            "reason": None,
        },
    )

    result = resolve_benchmark_workload(
        benchmark_name="Search",
        description="Search",
        reference_code="binary search",
        input_contract={
            "contract_type": "integer-array",
            "confidence": 0.92,
        },
    )

    fusion = result["resolution"]["confidence"]

    assert fusion <= 0.92
    assert fusion <= 0.88


def test_resolver_propagates_algorithm_and_input_provenance(
    monkeypatch,
):
    algorithm = {
        "workload_type": "searching",
        "algorithm_family": "searching",
        "algorithm_name": "binary-search",
        "specificity": "specific",
        "confidence": 0.96,
        "evidence": [
            "ordered search interval",
            "midpoint calculation",
        ],
    }

    input_structure = {
        "status": "known",
        "workload_type": "integer-array",
        "schema": {
            "type": "integer-array",
        },
    }

    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: algorithm,
    )

    monkeypatch.setattr(
        workload_resolver,
        "normalize_input_structure_from_contract",
        lambda contract: input_structure,
    )

    monkeypatch.setattr(
        workload_resolver,
        "workload_generation_capability",
        lambda input_structure: {
            "can_generate": True,
            "reason": None,
        },
    )

    result = resolve_benchmark_workload(
        benchmark_name="Search",
        description="Search",
        reference_code="binary search",
        input_contract={
            "contract_type": "integer-array",
            "confidence": 0.97,
        },
    )

    evidence = result["resolution"]["evidence"]

    assert evidence["algorithm"]["name"] == "binary-search"
    assert evidence["algorithm"]["family"] == "searching"
    assert evidence["algorithm"]["specificity"] == "specific"

    assert (
        evidence["input_contract"]["workload_type"]
        == "integer-array"
    )


def test_low_confidence_input_disables_generation(
    monkeypatch,
):
    algorithm = {
        "workload_type": "searching",
        "algorithm_family": "searching",
        "algorithm_name": "binary-search",
        "specificity": "specific",
        "confidence": 0.96,
        "evidence": [
            "binary-search control flow",
        ],
    }

    input_structure = {
        "status": "known",
        "workload_type": "integer-array",
        "schema": {
            "type": "integer-array",
        },
    }

    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: algorithm,
    )

    monkeypatch.setattr(
        workload_resolver,
        "normalize_input_structure_from_contract",
        lambda contract: input_structure,
    )

    result = resolve_benchmark_workload(
        benchmark_name="Search",
        description="Search",
        reference_code="binary search",
        input_contract={
            "contract_type": "integer-array",
            "confidence": 0.40,
        },
    )

    assert result["can_generate"] is False


def test_resolver_exposes_schema_version(
    monkeypatch,
):
    monkeypatch.setattr(
        workload_resolver,
        "_analyze_algorithm_with_intelligence",
        lambda reference_code: None,
    )

    result = resolve_benchmark_workload(
        benchmark_name="Custom",
        description="Custom workload",
        reference_code="int main() { return 0; }",
    )

    assert "resolver" in result

    assert (
        result["resolver"]["schema_version"]
        == 2
    )

    assert (
        "metadata_validation"
        in result["resolver"]
    )