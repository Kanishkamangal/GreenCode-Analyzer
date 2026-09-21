from app.services.algorithm_intelligence import analyze_algorithm
from app.services.input_contract_analyzer import detect_input_contract


def assert_algorithm(code, expected_name, expected_family):
    result = analyze_algorithm(code, "Python")["algorithm"]
    assert result["name"] == expected_name, result
    assert result["family"] == expected_family, result
    assert result["specificity"] in {"specific", "family"}, result
    assert result["confidence"] >= 0.70, result


def test_linear_search_arbitrary_function_name():
    code = '''
def mystery(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1
'''
    assert_algorithm(code, "linear-search", "searching")
    assert detect_input_contract(code, "Python")["contract_type"] == "array-plus-target"


def test_merge_sort_beats_generic_recursion():
    code = '''
def process(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = process(data[:mid])
    right = process(data[mid:])
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
'''
    assert_algorithm(code, "merge-sort", "sorting")
    assert detect_input_contract(code, "Python")["contract_type"] == "integer-array"


def test_bubble_sort_arbitrary_function_name():
    code = '''
def process(values):
    n = len(values)
    for i in range(n):
        for j in range(n - i - 1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
    return values
'''
    assert_algorithm(code, "bubble-sort", "sorting")


def test_quick_sort_arbitrary_function_name():
    code = '''
def partition_data(values, low, high):
    pivot = values[high]
    i = low - 1
    for j in range(low, high):
        if values[j] < pivot:
            i += 1
            values[i], values[j] = values[j], values[i]
    values[i + 1], values[high] = values[high], values[i + 1]
    return i + 1

def process(values, low, high):
    if low < high:
        p = partition_data(values, low, high)
        process(values, low, p - 1)
        process(values, p + 1, high)
    return values
'''
    assert_algorithm(code, "quick-sort", "sorting")


def test_library_sort_is_generic_sorting():
    code = '''
def completely_unrelated_name(values):
    return sorted(values)
'''
    result = analyze_algorithm(code, "Python")["algorithm"]
    assert result["name"] == "sorting", result
    assert result["family"] == "sorting", result
    assert result["specificity"] == "family", result


def test_matrix_function_parameter_is_not_no_input():
    code = '''
def aggregate(grid):
    total = 0
    for row in grid:
        for value in row:
            total += value
    return total
'''
    contract = detect_input_contract(code, "Python")
    assert contract["contract_type"] == "matrix", contract
    assert contract["confidence"] >= 0.90, contract


def test_stdin_contract_remains_supported():
    code = '''
n = int(input())
arr = list(map(int, input().split()))
arr.sort()
print(*arr)
'''
    contract = detect_input_contract(code, "Python")
    assert contract["contract_type"] != "no-input", contract
