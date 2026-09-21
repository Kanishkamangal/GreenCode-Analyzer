from app.services.algorithm_intelligence import (
    analyze_algorithm,
)


def test_empty_code_is_custom():
    result = analyze_algorithm(
        "",
        "python",
    )

    assert result["algorithm"]["name"] == "custom"


def test_sort_api_is_detected():
    code = """
arr = list(map(int, input().split()))
arr.sort()
print(*arr)
"""

    result = analyze_algorithm(
        code,
        "python",
    )

    assert result["algorithm"]["family"] == "sorting"


def test_sort_word_in_string_is_not_sorting():
    code = """
text = "sort this later"
print(text)
"""

    result = analyze_algorithm(
        code,
        "python",
    )

    assert result["algorithm"]["name"] == "custom"


def test_mid_variable_alone_is_not_binary_search():
    code = """
mid = 10
print(mid)
"""

    result = analyze_algorithm(
        code,
        "python",
    )

    assert result["algorithm"]["name"] != "binary-search"


def test_comment_does_not_create_algorithm():
    code = """
# binary search
x = int(input())
print(x)
"""

    result = analyze_algorithm(
        code,
        "python",
    )

    assert result["algorithm"]["name"] != "binary-search"


def test_nested_loop_is_structurally_visible():
    code = """
n = int(input())
total = 0

for i in range(n):
    for j in range(n):
        total += i + j

print(total)
"""

    result = analyze_algorithm(
        code,
        "python",
    )

    assert result["complexity"]["time"] == "O(n²)"
