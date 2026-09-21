from app.services.algorithm_intelligence import analyze_algorithm
from app.services.input_contract_analyzer import detect_input_contract
from app.services.workload_resolver import resolve_benchmark_workload


BINARY_SEARCH = """
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
"""


LINEAR_SEARCH = """
def locate(arr, target):
    for value in arr:
        if value == target:
            return True
    return False
"""


MERGE_SORT = """
def completely_random_name(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = completely_random_name(arr[:mid])
    right = completely_random_name(arr[mid:])

    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
"""


MATRIX = """
def matrix_sum(matrix):
    total = 0

    for row in matrix:
        for value in row:
            total += value

    return total
"""


GRAPH = """
def bfs(graph, start):
    visited = {start}
    queue = [start]

    while queue:
        node = queue.pop(0)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited
"""


def _resolve(code):
    algorithm = analyze_algorithm(code, "python")

    contract = detect_input_contract(
        code,
        language="python",
    )

    result = resolve_benchmark_workload(
    benchmark_name="Production Contract Matrix",
    description="Production integration test workload",
    reference_code=code,
    input_contract=contract,
)

    return algorithm, contract, result


def test_binary_search_production_contract():
    algorithm, contract, result = _resolve(BINARY_SEARCH)

    assert algorithm["algorithm"]["name"] == "binary-search"
    assert contract["contract_type"] == "array-plus-target"

    assert result["algorithm"]["name"] == "binary-search"
    assert result["input_structure"]["workload_type"] == "array-plus-target"


def test_linear_search_production_contract():
    algorithm, contract, result = _resolve(LINEAR_SEARCH)

    assert algorithm["algorithm"]["name"] == "linear-search"
    assert contract["contract_type"] == "array-plus-target"

    assert result["algorithm"]["name"] == "linear-search"
    assert result["input_structure"]["workload_type"] == "array-plus-target"


def test_merge_sort_production_contract():
    algorithm, contract, result = _resolve(MERGE_SORT)

    assert algorithm["algorithm"]["name"] == "merge-sort"

    assert contract["contract_type"] == "integer-array"

    assert result["algorithm"]["name"] == "merge-sort"
    assert result["input_structure"]["workload_type"] == "integer-array"


def test_matrix_production_contract():
    algorithm, contract, result = _resolve(MATRIX)

    assert algorithm["algorithm"]["name"] == "matrix-processing"
    assert contract["contract_type"] == "matrix"

    assert result["input_structure"]["workload_type"] == "matrix"


def test_graph_production_contract():
    algorithm, contract, result = _resolve(GRAPH)

    assert algorithm["algorithm"]["name"] in {
        "graph-traversal",
        "graph-algorithm",
    }

    assert contract["contract_type"] == "graph"

    assert result["input_structure"]["workload_type"] == "graph"