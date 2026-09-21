import random
import string


BENCHMARK_SIZE_MAPPING = {
    "bubble_sort": {
        "small": 1000,
        "medium": 5000,
        "large": 10000,
    },
        "selection_sort": {
        "small": 1000,
        "medium": 3000,
        "large": 5000,
    },
    "insertion_sort": {
        "small": 1000,
        "medium": 3000,
        "large": 5000,
    },
    "merge_sort": {
        "small": 10000,
        "medium": 50000,
        "large": 100000,
    },
    "quick_sort": {
        "small": 10000,
        "medium": 50000,
        "large": 100000,
    },
    "heap_sort": {
        "small": 10000,
        "medium": 50000,
        "large": 100000,
    },
    "shell_sort": {
        "small": 5000,
        "medium": 20000,
        "large": 50000,
    },
    "counting_sort": {
        "small": 10000,
        "medium": 50000,
        "large": 100000,
    },
    "radix_sort": {
        "small": 10000,
        "medium": 50000,
        "large": 100000,
    },
    "bucket_sort": {
        "small": 10000,
        "medium": 50000,
        "large": 100000,
    },
    "binary_search": {
        "small": 10000,
        "medium": 100000,
        "large": 1000000,
    },
        "linear_search": {
        "small": 10000,
        "medium": 100000,
        "large": 1000000,
    },
    "jump_search": {
        "small": 10000,
        "medium": 100000,
        "large": 1000000,
    },
    "anagram_check": {
        "small": 1000,
        "medium": 10000,
        "large": 100000,
    },
        "palindrome_check": {
        "small": 1000,
        "medium": 10000,
        "large": 100000,
    },
    "string_reverse": {
        "small": 1000,
        "medium": 10000,
        "large": 100000,
    },
    "substring_search": {
        "small": 5000,
        "medium": 20000,
        "large": 50000,
    },
    "longest_common_prefix": {
        "small": 1000,
        "medium": 5000,
        "large": 10000,
    },
    "longest_palindromic_substring": {
        "small": 500,
        "medium": 1500,
        "large": 3000,
    },
    "longest_common_subsequence": {
        "small": 200,
        "medium": 600,
        "large": 1200,
    },
        "vowel_consonant_check": {
        "small": 1,
        "medium": 1,
        "large": 1,
    },
    "character_frequency_count": {
        "small": 10000,
        "medium": 100000,
        "large": 1000000,
    },
    "bfs_traversal": {
        "small": 1000,
        "medium": 5000,
        "large": 10000,
    },
    "knapsack_01": {
        "small": 100,
        "medium": 500,
        "large": 1000,
    },
}


def get_input_size(benchmark_key: str, bench_size: str) -> int:
    benchmark_key = benchmark_key.lower().strip()
    bench_size = bench_size.lower().strip()

    if benchmark_key not in BENCHMARK_SIZE_MAPPING:
        raise ValueError(
            f"Unsupported benchmark: {benchmark_key}"
        )

    if bench_size not in BENCHMARK_SIZE_MAPPING[benchmark_key]:
        raise ValueError(
            "Invalid benchmark size. Use small, medium, or large."
        )

    return BENCHMARK_SIZE_MAPPING[benchmark_key][bench_size]


def generate_bubble_sort_input(bench_size: str, seed: int = 42):
    n = get_input_size("bubble_sort", bench_size)
    rng = random.Random(seed)

    return [
        rng.randint(0, 1_000_000)
        for _ in range(n)
    ]

def generate_sorting_input(
    benchmark_key: str,
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        benchmark_key,
        bench_size,
    )

    rng = random.Random(seed)

    if benchmark_key == "counting_sort":
        return [
            rng.randint(-10000, 10000)
            for _ in range(n)
        ]

    if benchmark_key == "radix_sort":
        return [
            rng.randint(-1_000_000, 1_000_000)
            for _ in range(n)
        ]

    if benchmark_key == "bucket_sort":
        return [
            rng.randint(0, 1_000_000)
            for _ in range(n)
        ]

    return [
        rng.randint(0, 1_000_000)
        for _ in range(n)
    ]

def generate_binary_search_input(bench_size: str, seed: int = 42):
    n = get_input_size("binary_search", bench_size)
    rng = random.Random(seed)

    values = sorted(
        rng.sample(range(0, n * 10), n)
    )

    target = values[n // 2]

    return {
        "n": n,
        "values": values,
        "target": target,
    }

def generate_search_input(
    benchmark_key: str,
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        benchmark_key,
        bench_size,
    )

    rng = random.Random(seed)

    values = sorted(
        rng.sample(
            range(0, n * 10),
            n,
        )
    )

    target = values[-1]

    return {
        "n": n,
        "values": values,
        "target": target,
    }

def generate_anagram_check_input(bench_size: str, seed: int = 42):
    n = get_input_size("anagram_check", bench_size)
    rng = random.Random(seed)

    first = "".join(
        rng.choice(string.ascii_lowercase)
        for _ in range(n)
    )

    second_chars = list(first)
    rng.shuffle(second_chars)
    second = "".join(second_chars)

    return {
        "first": first,
        "second": second,
    }

def generate_palindrome_check_input(
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        "palindrome_check",
        bench_size,
    )

    rng = random.Random(seed)

    half = "".join(
        rng.choice(string.ascii_lowercase)
        for _ in range(n // 2)
    )

    if n % 2 == 0:
        value = half + half[::-1]
    else:
        middle = rng.choice(
            string.ascii_lowercase
        )
        value = (
            half
            + middle
            + half[::-1]
        )

    return {
        "value": value,
    }


def generate_string_reverse_input(
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        "string_reverse",
        bench_size,
    )

    rng = random.Random(seed)

    value = "".join(
        rng.choice(
            string.ascii_lowercase
        )
        for _ in range(n)
    )

    return {
        "value": value,
    }


def generate_substring_search_input(
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        "substring_search",
        bench_size,
    )

    rng = random.Random(seed)

    pattern_length = max(
        5,
        min(100, n // 10),
    )

    prefix_length = (
        n - pattern_length
    )

    text_prefix = "".join(
        rng.choice(
            string.ascii_lowercase
        )
        for _ in range(prefix_length)
    )

    pattern = "".join(
        rng.choice(
            string.ascii_lowercase
        )
        for _ in range(pattern_length)
    )

    text = text_prefix + pattern

    return {
        "text": text,
        "pattern": pattern,
    }


def generate_longest_common_prefix_input(
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        "longest_common_prefix",
        bench_size,
    )

    rng = random.Random(seed)

    string_count = 10

    prefix_length = max(
        1,
        n // 2,
    )

    prefix = "".join(
        rng.choice(
            string.ascii_lowercase
        )
        for _ in range(prefix_length)
    )

    values = []

    for _ in range(string_count):
        suffix = "".join(
            rng.choice(
                string.ascii_lowercase
            )
            for _ in range(
                n - prefix_length
            )
        )

        values.append(
            prefix + suffix
        )

    return {
        "n": string_count,
        "values": values,
    }


def generate_longest_palindromic_substring_input(
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        "longest_palindromic_substring",
        bench_size,
    )

    rng = random.Random(seed)

    value = "".join(
        rng.choice(
            string.ascii_lowercase
        )
        for _ in range(n)
    )

    return {
        "value": value,
    }


def generate_lcs_input(
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        "longest_common_subsequence",
        bench_size,
    )

    rng = random.Random(seed)

    first = "".join(
        rng.choice(
            string.ascii_lowercase
        )
        for _ in range(n)
    )

    second = "".join(
        rng.choice(
            string.ascii_lowercase
        )
        for _ in range(n)
    )

    return {
        "first": first,
        "second": second,
    }

def generate_vowel_consonant_input(
    bench_size: str,
    seed: int = 42,
):
    get_input_size(
        "vowel_consonant_check",
        bench_size,
    )

    rng = random.Random(seed)

    return {
        "character": rng.choice(
            string.ascii_letters
        ),
    }


def generate_character_frequency_count_input(
    bench_size: str,
    seed: int = 42,
):
    n = get_input_size(
        "character_frequency_count",
        bench_size,
    )

    rng = random.Random(seed)

    target = "a"

    value = "".join(
        target
        if i % 10 == 0
        else rng.choice(
            "bcdefghijklmnopqrstuvwxyz"
        )
        for i in range(n)
    )

    return {
        "value": value,
        "target": target,
    }

def generate_bfs_input(bench_size: str):
    n = get_input_size("bfs_traversal", bench_size)

    edges = []

    for i in range(n - 1):
        edges.append((i, i + 1))

    return {
        "n": n,
        "edges": edges,
        "start": 0,
    }


def generate_knapsack_input(bench_size: str, seed: int = 42):
    n = get_input_size("knapsack_01", bench_size)
    rng = random.Random(seed)

    weights = [
        rng.randint(1, 100)
        for _ in range(n)
    ]

    values = [
        rng.randint(1, 1000)
        for _ in range(n)
    ]

    capacity = max(1, sum(weights) // 4)

    return {
        "n": n,
        "capacity": capacity,
        "weights": weights,
        "values": values,
    }


def bubble_sort_input_to_string(data) -> str:
    return " ".join(map(str, data)) + "\n"


def binary_search_input_to_string(data) -> str:
    return (
        f"{data['n']}\n"
        + " ".join(map(str, data["values"]))
        + "\n"
        + f"{data['target']}\n"
    )


def anagram_input_to_string(data) -> str:
    return (
        f"{data['first']}\n"
        f"{data['second']}\n"
    )


def bfs_input_to_string(data) -> str:
    lines = [
        f"{data['n']} {len(data['edges'])}"
    ]

    for u, v in data["edges"]:
        lines.append(f"{u} {v}")

    lines.append(str(data["start"]))

    return "\n".join(lines) + "\n"


def knapsack_input_to_string(data) -> str:
    return (
        f"{data['n']} {data['capacity']}\n"
        + " ".join(map(str, data["weights"]))
        + "\n"
        + " ".join(map(str, data["values"]))
        + "\n"
    )

def sorting_input_to_string(data) -> str:
    return " ".join(
        map(str, data)
    ) + "\n"


def search_input_to_string(data) -> str:
    return (
        f"{data['n']}\n"
        + " ".join(
            map(str, data["values"])
        )
        + "\n"
        + f"{data['target']}\n"
    )


def single_string_input_to_string(data) -> str:
    return f"{data['value']}\n"


def substring_search_input_to_string(data) -> str:
    return (
        f"{data['text']}\n"
        f"{data['pattern']}\n"
    )


def longest_common_prefix_input_to_string(data) -> str:
    return (
        f"{data['n']}\n"
        + "\n".join(
            data["values"]
        )
        + "\n"
    )


def lcs_input_to_string(data) -> str:
    return (
        f"{data['first']}\n"
        f"{data['second']}\n"
    )


def vowel_consonant_input_to_string(data) -> str:
    return (
        f"{data['character']}\n"
    )


def character_frequency_count_input_to_string(data) -> str:
    return (
        f"{data['value']}\n"
        f"{data['target']}\n"
    )