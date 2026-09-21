from app.services.custom_benchmark_engine import (
    run_custom_benchmark,
)


cpp_code = r"""
#include <iostream>
using namespace std;

int main() {

    int n;
    cin >> n;

    long long target;
    int arr[1000];

    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    cin >> target;

    bool found = false;

    for (int i = 0; i < n; i++) {

        for (int j = i + 1; j < n; j++) {

            if (arr[i] + arr[j] == target) {
                found = true;
            }

        }

    }

    cout << (found ? "true" : "false");

    return 0;
}
"""


try:

    results = run_custom_benchmark(
        benchmark_name="Two Sum",

        benchmark_category=(
            "Algorithms & Data Structures"
        ),

        description=(
            "Find two numbers in an array "
            "whose sum equals target."
        ),

        # IMPORTANT:
        # Do NOT provide workload_type.
        workload_type=None,

        input_size=5,

        reference_language="C++",

        reference_code=cpp_code,

        target_languages=[
            "Java"
        ],
    )

    print(
        "\n===== AUTOMATIC WORKLOAD "
        "BENCHMARK RESULTS =====\n"
    )

    for result in results:

        print(
            "Language:",
            result["language"]
        )

        print(
            "Reference:",
            result["is_reference"]
        )

        print(
            "Generated:",
            result["generated"]
        )

        print(
            "Output verified:",
            result["output_verified"]
        )

        print(
            "Execution time:",
            result["execution_time"],
            "ms"
        )

        print(
            "CPU:",
            result["cpu_usage"],
            "%"
        )

        print(
            "Memory:",
            result["memory_usage"],
            "MB"
        )

        print(
            "Energy:",
            result["energy_consumption"],
            "J"
        )

        print("-" * 50)


except Exception as e:

    print(
        "\nAUTOMATIC WORKLOAD "
        "BENCHMARK FAILED:"
    )

    print(e)