from app.services.compiler_runner import compile_program
from app.services.metrics_monitor import execute_with_monitor
from app.services.input_generator import (
    generate_bubble_sort_input,
    input_to_string
)

import tempfile


languages = [
    "c",
    "cpp",
    "python",
    "java",
    "javascript",
    "go",
    "rust",
    "csharp",
    "kotlin",
    "php"
]

files = {
    "c": "benchmarks/bubble_sort/c.c",
    "cpp": "benchmarks/bubble_sort/cpp.cpp",
    "python": "benchmarks/bubble_sort/python.py",
    "java": "benchmarks/bubble_sort/java.java",
    "javascript": "benchmarks/bubble_sort/javascript.js",
    "go": "benchmarks/bubble_sort/go.go",
    "rust": "benchmarks/bubble_sort/rust.rs",
    "csharp": "benchmarks/bubble_sort/csharp.cs",
    "kotlin": "benchmarks/bubble_sort/kotlin.kt",
    "php": "benchmarks/bubble_sort/php.php"
}


# Generate SAME deterministic input
data = generate_bubble_sort_input("small")
input_data = input_to_string(data)

expected_output = max(data)

print(f"Input size: {len(data)}")
print(f"Expected output: {expected_output}")
print()


for language in languages:

    print(f"===== {language.upper()} =====")

    try:

        output_dir = tempfile.mkdtemp()

        command = compile_program(
            language,
            files[language],
            output_dir
        )

        result = execute_with_monitor(
            command,
            input_data
        )

        print(f"Output: {result['stdout']}")
        print(
            f"Execution Time: "
            f"{result['execution_time']:.3f} ms"
        )
        print(
            f"CPU Usage: "
            f"{result['cpu_usage']:.2f} %"
        )
        print(
            f"Memory Usage: "
            f"{result['memory_usage']:.2f} MB"
        )
        print(
            f"Energy Consumption: "
            f"{result['energy_consumption']:.9f} J"
        )

        if result["stdout"] == str(expected_output):
            print("STATUS: PASS")
        else:
            print("STATUS: FAIL")

    except Exception as e:

        print("STATUS: ERROR")
        print(e)

    print()


print("===== ALL TESTS COMPLETED =====")