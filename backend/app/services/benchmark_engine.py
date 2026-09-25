from pathlib import Path
from collections import deque
import tempfile
import shutil

from app.services.input_generator import (
    generate_bubble_sort_input,
    generate_sorting_input,
    generate_binary_search_input,
    generate_search_input,
    generate_anagram_check_input,
    generate_palindrome_check_input,
    generate_string_reverse_input,
    generate_substring_search_input,
    generate_longest_common_prefix_input,
    generate_longest_palindromic_substring_input,
    generate_lcs_input,
    generate_vowel_consonant_input,
    generate_character_frequency_count_input,
    generate_bfs_input,
    generate_knapsack_input,
    bubble_sort_input_to_string,
    sorting_input_to_string,
    binary_search_input_to_string,
    search_input_to_string,
    anagram_input_to_string,
    single_string_input_to_string,
    substring_search_input_to_string,
    longest_common_prefix_input_to_string,
    lcs_input_to_string,
    vowel_consonant_input_to_string,
    character_frequency_count_input_to_string,
    bfs_input_to_string,
    knapsack_input_to_string,
)
from app.services.compiler_runner import compile_program
from app.services.metrics_monitor import execute_with_monitor


BASE_DIR = Path(__file__).resolve().parents[2]
BENCHMARKS_DIR = BASE_DIR / "benchmarks"


LANGUAGE_FILES = {
    "c": "c.c",
    "cpp": "cpp.cpp",
    "java": "java.java",
    "python": "python.py",
    "javascript": "javascript.js",
    "go": "go.go",
    "rust": "rust.rs",
    "csharp": "csharp.cs",
    "kotlin": "kotlin.kt",
    "php": "php.php",
}


LANGUAGE_NAME_MAP = {
    "c": "c",
    "c++": "cpp",
    "java": "java",
    "python": "python",
    "javascript": "javascript",
    "go": "go",
    "rust": "rust",
    "c#": "csharp",
    "kotlin": "kotlin",
    "php": "php",
}


BENCHMARK_NAMES = {
    "bubble_sort": "Bubble Sort",
    "selection_sort": "Selection Sort",
    "insertion_sort": "Insertion Sort",
    "merge_sort": "Merge Sort",
    "quick_sort": "Quick Sort",
    "heap_sort": "Heap Sort",
    "shell_sort": "Shell Sort",
    "counting_sort": "Counting Sort",
    "radix_sort": "Radix Sort",
    "bucket_sort": "Bucket Sort",

    "linear_search": "Linear Search",
    "binary_search": "Binary Search",
    "jump_search": "Jump Search",

    "anagram_check": "Anagram Check",
    "palindrome_check": "Palindrome Check",
    "string_reverse": "String Reverse",
    "substring_search": "Substring Search",
    "longest_common_prefix": "Longest Common Prefix",
    "longest_palindromic_substring": "Longest Palindromic Substring",
    "longest_common_subsequence": "Longest Common Subsequence",

    "vowel_consonant_check": "Vowel or Consonant Check",
    "character_frequency_count": "Character Frequency Count",

    "bfs_traversal": "BFS Traversal",
    "knapsack_01": "0/1 Knapsack",
}


def normalize_language(language: str) -> str:
    language_key = language.lower().strip()

    normalized = LANGUAGE_NAME_MAP.get(language_key)

    if normalized is None or normalized not in LANGUAGE_FILES:
        raise ValueError(
            f"Unsupported language: {language}"
        )

    return normalized


def verify_bubble_sort_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual = int(output.strip())
    except ValueError:
        return False

    expected = max(data) if data else 0

    return actual == expected

def verify_sorting_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual = int(output.strip())
    except ValueError:
        return False

    expected = max(data) if data else 0

    return actual == expected

def verify_binary_search_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual_index = int(output.strip())
    except ValueError:
        return False

    values = data["values"]
    target = data["target"]

    if actual_index < 0 or actual_index >= len(values):
        return False

    return values[actual_index] == target

def verify_search_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual_index = int(output.strip())
    except ValueError:
        return False

    values = data["values"]
    target = data["target"]

    if actual_index < 0 or actual_index >= len(values):
        return False

    return values[actual_index] == target

def verify_anagram_output(data, output: str) -> bool:
    if not output:
        return False

    normalized = output.strip().lower()

    valid_true = {
        "1",
        "true",
        "yes",
        "anagram",
    }

    return normalized in valid_true

def verify_palindrome_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual = int(output.strip())
    except ValueError:
        return False

    value = data["value"]

    expected = 1 if value == value[::-1] else 0

    return actual == expected


def verify_string_reverse_output(data, output: str) -> bool:
    actual = output.strip()

    expected = data["value"][::-1]

    return actual == expected


def verify_substring_search_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual = int(output.strip())
    except ValueError:
        return False

    expected = data["text"].find(
        data["pattern"]
    )

    return actual == expected


def verify_longest_common_prefix_output(
    data,
    output: str,
) -> bool:
    values = data["values"]

    if not values:
        return output.strip() == ""

    prefix = values[0]

    for value in values[1:]:
        limit = min(
            len(prefix),
            len(value),
        )

        index = 0

        while (
            index < limit
            and prefix[index] == value[index]
        ):
            index += 1

        prefix = prefix[:index]

        if not prefix:
            break

    return output.strip() == prefix


def expected_longest_palindromic_substring(
    value: str,
) -> str:
    if not value:
        return ""

    best_start = 0
    best_length = 1

    for center in range(len(value)):
        left = center
        right = center

        while (
            left >= 0
            and right < len(value)
            and value[left] == value[right]
        ):
            length = right - left + 1

            if length > best_length:
                best_start = left
                best_length = length

            left -= 1
            right += 1

        left = center
        right = center + 1

        while (
            left >= 0
            and right < len(value)
            and value[left] == value[right]
        ):
            length = right - left + 1

            if length > best_length:
                best_start = left
                best_length = length

            left -= 1
            right += 1

    return value[
        best_start:
        best_start + best_length
    ]


def verify_longest_palindromic_substring_output(
    data,
    output: str,
) -> bool:
    expected = (
        expected_longest_palindromic_substring(
            data["value"]
        )
    )

    return output.strip() == expected


def expected_lcs_length(
    first: str,
    second: str,
) -> int:
    previous = [0] * (
        len(second) + 1
    )

    current = [0] * (
        len(second) + 1
    )

    for i in range(
        1,
        len(first) + 1,
    ):
        current[0] = 0

        for j in range(
            1,
            len(second) + 1,
        ):
            if (
                first[i - 1]
                == second[j - 1]
            ):
                current[j] = (
                    previous[j - 1] + 1
                )
            else:
                current[j] = max(
                    previous[j],
                    current[j - 1],
                )

        previous, current = (
            current,
            previous,
        )

    return previous[len(second)]


def verify_lcs_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual = int(output.strip())
    except ValueError:
        return False

    expected = expected_lcs_length(
        data["first"],
        data["second"],
    )

    return actual == expected

def expected_bfs_traversal(data):
    n = data["n"]
    edges = data["edges"]
    start = data["start"]

    graph = [[] for _ in range(n)]

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    for neighbours in graph:
        neighbours.sort()

    visited = [False] * n
    queue = deque([start])
    visited[start] = True

    traversal = []

    while queue:
        node = queue.popleft()
        traversal.append(node)

        for neighbour in graph[node]:
            if not visited[neighbour]:
                visited[neighbour] = True
                queue.append(neighbour)

    return traversal


def verify_bfs_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual = [
            int(value)
            for value in output.split()
        ]
    except ValueError:
        return False

    expected = expected_bfs_traversal(data)

    return actual == expected


def expected_knapsack_result(data):
    capacity = data["capacity"]
    weights = data["weights"]
    values = data["values"]

    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for current_capacity in range(
            capacity,
            weight - 1,
            -1
        ):
            dp[current_capacity] = max(
                dp[current_capacity],
                dp[current_capacity - weight] + value,
            )

    return dp[capacity]


def verify_knapsack_output(data, output: str) -> bool:
    if not output:
        return False

    try:
        actual = int(output.strip())
    except ValueError:
        return False

    expected = expected_knapsack_result(data)

    return actual == expected


def prepare_benchmark(
    benchmark_key: str,
    bench_size: str,
):
    if benchmark_key == "bubble_sort":
        data = generate_bubble_sort_input(
            bench_size
        )

        return (
            data,
            bubble_sort_input_to_string(data),
            verify_bubble_sort_output,
            len(data),
        )

    sorting_benchmarks = {
        "selection_sort",
        "insertion_sort",
        "merge_sort",
        "quick_sort",
        "heap_sort",
        "shell_sort",
        "counting_sort",
        "radix_sort",
        "bucket_sort",
    }

    if benchmark_key in sorting_benchmarks:
        data = generate_sorting_input(
            benchmark_key,
            bench_size,
        )

        return (
            data,
            sorting_input_to_string(data),
            verify_sorting_output,
            len(data),
        )

    if benchmark_key == "binary_search":
        data = generate_binary_search_input(
            bench_size
        )

        return (
            data,
            binary_search_input_to_string(data),
            verify_binary_search_output,
            data["n"],
        )

    if benchmark_key in {
        "linear_search",
        "jump_search",
    }:
        data = generate_search_input(
            benchmark_key,
            bench_size,
        )

        return (
            data,
            search_input_to_string(data),
            verify_search_output,
            data["n"],
        )

    if benchmark_key == "anagram_check":
        data = generate_anagram_check_input(
            bench_size
        )

        return (
            data,
            anagram_input_to_string(data),
            verify_anagram_output,
            len(data["first"]),
        )

    if benchmark_key == "palindrome_check":
        data = generate_palindrome_check_input(
            bench_size
        )

        return (
            data,
            single_string_input_to_string(data),
            verify_palindrome_output,
            len(data["value"]),
        )

    if benchmark_key == "string_reverse":
        data = generate_string_reverse_input(
            bench_size
        )

        return (
            data,
            single_string_input_to_string(data),
            verify_string_reverse_output,
            len(data["value"]),
        )

    if benchmark_key == "substring_search":
        data = generate_substring_search_input(
            bench_size
        )

        return (
            data,
            substring_search_input_to_string(data),
            verify_substring_search_output,
            len(data["text"]),
        )

    if benchmark_key == "longest_common_prefix":
        data = generate_longest_common_prefix_input(
            bench_size
        )

        return (
            data,
            longest_common_prefix_input_to_string(
                data
            ),
            verify_longest_common_prefix_output,
            sum(
                len(value)
                for value in data["values"]
            ),
        )

    if (
        benchmark_key
        == "longest_palindromic_substring"
    ):
        data = (
            generate_longest_palindromic_substring_input(
                bench_size
            )
        )

        return (
            data,
            single_string_input_to_string(data),
            verify_longest_palindromic_substring_output,
            len(data["value"]),
        )

    if (
        benchmark_key
        == "longest_common_subsequence"
    ):
        data = generate_lcs_input(
            bench_size
        )

        return (
            data,
            lcs_input_to_string(data),
            verify_lcs_output,
            len(data["first"]),
        )

    if benchmark_key == "vowel_consonant_check":
        data = generate_vowel_consonant_input(
            bench_size
        )

        return (
            data,
            vowel_consonant_input_to_string(data),
            verify_vowel_consonant_output,
            1,
        )

    if (
        benchmark_key
        == "character_frequency_count"
    ):
        data = (
            generate_character_frequency_count_input(
                bench_size
            )
        )

        return (
            data,
            character_frequency_count_input_to_string(
                data
            ),
            verify_character_frequency_count_output,
            len(data["value"]),
        )

    if benchmark_key == "bfs_traversal":
        data = generate_bfs_input(
            bench_size
        )

        return (
            data,
            bfs_input_to_string(data),
            verify_bfs_output,
            data["n"],
        )

    if benchmark_key == "knapsack_01":
        data = generate_knapsack_input(
            bench_size
        )

        return (
            data,
            knapsack_input_to_string(data),
            verify_knapsack_output,
            data["n"],
        )

    raise ValueError(
        f"Benchmark not implemented: {benchmark_key}"
    )

def run_benchmark(
    benchmark_name: str,
    folder_name: str,
    language: str,
    bench_size: str,
    progress_callback=None,
):
    benchmark_key = folder_name.lower().strip()

    if benchmark_key not in BENCHMARK_NAMES:
        raise ValueError(
            f"Benchmark not implemented yet: {benchmark_name}"
        )

    normalized_language = normalize_language(language)

    def report(step, status, message):
        if progress_callback is not None:
            progress_callback({
                "step": step,
                "status": status,
                "message": message,
            })

    # -----------------------------------
    # 1. Generate deterministic workload
    # -----------------------------------

    report(
        "workload",
        "processing",
        "Generating deterministic benchmark workload",
    )

    data, input_data, verifier, input_size = prepare_benchmark(
        benchmark_key,
        bench_size,
    )

    report(
        "workload",
        "completed",
        f"Generated {bench_size} benchmark workload",
    )

    # -----------------------------------
    # 2. Prepare source implementation
    # -----------------------------------

    report(
        "prepare",
        "processing",
        f"Preparing {language} implementation",
    )

    benchmark_dir = BENCHMARKS_DIR / benchmark_key

    source_filename = LANGUAGE_FILES[
        normalized_language
    ]

    source_file = benchmark_dir / source_filename

    if not source_file.exists():
        report(
            "prepare",
            "failed",
            f"{language} benchmark source not found",
        )

        raise FileNotFoundError(
            f"Benchmark source not found: {source_file}"
        )

    temp_dir = tempfile.mkdtemp(
        prefix="greencode_"
    )

    try:
        if normalized_language == "java":
            temp_filename = "Main.java"
        else:
            temp_filename = source_filename

        temp_source = (
            Path(temp_dir) / temp_filename
        )

        shutil.copy2(
            source_file,
            temp_source,
        )

        report(
            "prepare",
            "completed",
            f"{language} implementation prepared",
        )

        # -----------------------------------
        # 3. Compile / prepare runtime
        # -----------------------------------

        report(
            "compile",
            "processing",
            f"Compiling {language}",
        )

        try:
            command = compile_program(
                language=normalized_language,
                source_file=str(temp_source),
                output_dir=temp_dir,
            )
        except Exception:
            report(
                "compile",
                "failed",
                f"{language} compilation failed",
            )
            raise

        report(
            "compile",
            "completed",
            f"{language} compilation completed",
        )

        # -----------------------------------
        # 4. Execute + collect metrics
        # -----------------------------------

        report(
            "execute",
            "processing",
            f"Executing {language} and measuring metrics",
        )

        try:
            result = execute_with_monitor(
                command=command,
                input_data=input_data,
                timeout=120,
            )
        except Exception:
            report(
                "execute",
                "failed",
                f"{language} execution failed",
            )
            raise

        if result["return_code"] != 0:
            report(
                "execute",
                "failed",
                f"{language} execution returned a non-zero exit code",
            )

            raise RuntimeError(
                f"{language} benchmark execution failed "
                f"with return code {result['return_code']}."
            )

        report(
            "execute",
            "completed",
            f"{language} execution and metric collection completed",
        )

        # -----------------------------------
        # 5. Verify output
        # -----------------------------------

        report(
            "verify",
            "processing",
            f"Verifying {language} benchmark output",
        )

        output_verified = verifier(
            data,
            result["stdout"],
        )

        if not output_verified:
            report(
                "verify",
                "failed",
                f"{language} output verification failed",
            )

            raise RuntimeError(
                f"{language} benchmark produced "
                "an incorrect output."
            )

        report(
            "verify",
            "completed",
            f"{language} output verified",
        )

        return {
            "benchmark": BENCHMARK_NAMES[
                benchmark_key
            ],
            "language": normalized_language,
            "bench_size": bench_size,
            "input_size": input_size,
            "execution_time": result[
                "execution_time"
            ],
            "cpu_usage": result[
                "cpu_usage"
            ],
            "memory_usage": result[
                "memory_usage"
            ],
            "energy_consumption": result[
                "energy_consumption"
            ],
            "output": result[
                "stdout"
            ],
            "output_verified": output_verified,
            "return_code": result[
                "return_code"
            ],
        }

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True,
        )