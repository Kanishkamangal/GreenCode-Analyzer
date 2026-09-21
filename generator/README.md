# GreenCode Analyzer — Benchmark Code Generation Pack

## What this pack does

It generates the **89 benchmark folders × 10 languages = 890 executable source files** under:

`backend/benchmarks/`

The frontend does **not** generate input and the language programs do **not** generate random input.

The intended architecture is:

Frontend
→ FastAPI
→ resolve `small/medium/large` using `input_sizes.py`
→ generate ONE deterministic dataset
→ pipe the SAME stdin to every selected language
→ collect execution time / CPU / memory / RAPL energy
→ compare results

## Run

Put this `generator` folder directly inside your `backend` folder.

Then from:

`C:\Users\ayush\Downloads\GreenCode\backend`

run:

```powershell
python generator\generate_benchmarks.py
```

Expected:

```text
Done! 89 benchmark folders created.
890 language files generated with actual executable implementations.
```

## Important

The generated programs are intentionally stdin/stdout based. That is what makes the benchmark runner able to feed the exact same dataset to C, C++, Java, Python, JavaScript, C#, Go, Rust, Kotlin and PHP.

For algorithm families where the exact input contract is more specialized (graphs, matrices, trees, Sudoku, etc.), the benchmark runner should use a benchmark-specific input serializer. The generator is the source-code layer; the FastAPI benchmark engine remains responsible for producing and piping the canonical dataset.
