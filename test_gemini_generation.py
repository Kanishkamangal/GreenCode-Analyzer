from app.services.ai_code_generation_service import (
    generate_equivalent_code,
)


cpp_code = r"""
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    long long sum = 0;

    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        sum += x;
    }

    cout << sum;

    return 0;
}
"""


try:

    generated_code = generate_equivalent_code(
        reference_language="C++",
        target_language="Java",
        reference_code=cpp_code,
        benchmark_name="Array Sum",
        benchmark_category="Algorithms & Data Structures",
        description="Calculate the sum of array elements.",
        input_size=1000,
    )

    print("\n===== GENERATED JAVA CODE =====\n")
    print(generated_code)

except Exception as e:

    print("\nGENERATION FAILED:")
    print(e)