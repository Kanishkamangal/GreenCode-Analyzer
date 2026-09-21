import tempfile
import shutil
from pathlib import Path

from app.services.compiler_runner import (
    validate_syntax,
)


tests = {
    "Valid C++": """
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    cout << n;
    return 0;
}
""",

    "Invalid C++": """
#include <iostream>
using namespace std;

int main() {
    int n
    cin >> n;
    cout << n;
    return 0;
}
""",
}


for name, code in tests.items():

    temp_dir = tempfile.mkdtemp(
        prefix="greencode_syntax_test_"
    )

    try:

        source_file = (
            Path(temp_dir) / "source.cpp"
        )

        source_file.write_text(
            code,
            encoding="utf-8",
        )

        result = validate_syntax(
            language="cpp",
            source_file=str(source_file),
            output_dir=temp_dir,
        )

        print(f"\n{name}")
        print(
            "syntax_valid:",
            result["syntax_valid"]
        )
        print(
            "syntax_errors:",
            result["syntax_errors"]
        )

    finally:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True,
        )