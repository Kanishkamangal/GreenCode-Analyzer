"""
GreenCode Analyzer - benchmark source generator.

Run from backend:
    python generator/generate_benchmarks.py

It creates:
    backend/benchmarks/<benchmark>/<language-file>

Contract:
- Frontend sends only small/medium/large.
- Backend resolves the size in input_sizes.py.
- Backend generates ONE deterministic input dataset.
- The same stdin is piped to every selected language.
- Benchmark programs only execute the algorithm and print a compact result.
"""
from pathlib import Path
import json, os, re, shutil, stat

HERE = Path(__file__).resolve().parent
BACKEND = HERE.parent
OUTPUT = BACKEND / "benchmarks"

LANGUAGES = {
    "c": "c.c", "cpp": "cpp.cpp", "java": "java.java",
    "python": "python.py", "javascript": "javascript.js",
    "csharp": "csharp.cs", "go": "go.go", "rust": "rust.rs",
    "kotlin": "kotlin.kt", "php": "php.php"
}

def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower().replace("0/1","zero_one")).strip("_")

# Import the generated implementation builder.
from implementations import build_program

def main():
    benchmarks = json.loads((HERE/"benchmarks.json").read_text(encoding="utf-8"))
    def on_rm_error(func, path, exc_info):
        # On Windows, retry removal after making the file writable.
        try:
            os.chmod(path, stat.S_IWRITE)
        except Exception:
            pass
        func(path)

    if OUTPUT.exists():
        for p in OUTPUT.iterdir():
            if p.is_dir():
                shutil.rmtree(p, onerror=on_rm_error)
            elif p.is_file():
                try:
                    p.unlink()
                except PermissionError:
                    p.chmod(stat.S_IWRITE)
                    p.unlink()
    OUTPUT.mkdir(parents=True, exist_ok=True)

    files = 0
    for b in benchmarks:
        folder = OUTPUT / b["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        for lang, filename in LANGUAGES.items():
            (folder/filename).write_text(
                build_program(lang, b["slug"], b["bench_name"], b["category"]),
                encoding="utf-8"
            )
            files += 1

    print(f"Done! {len(benchmarks)} benchmark folders created.")
    print(f"{files} language files generated with actual executable implementations.")
    print(f"Output: {OUTPUT}")

if __name__ == "__main__":
    main()
