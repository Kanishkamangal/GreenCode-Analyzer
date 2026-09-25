import os
import re
import subprocess
import time
from pathlib import Path


LANGUAGE_CONFIG = {
    "c": {
        "extension": ".c",
    },

    "cpp": {
        "extension": ".cpp",
    },

    "java": {
        "extension": ".java",
    },

    "python": {
        "extension": ".py",
    },

    "javascript": {
        "extension": ".js",
    },

    "go": {
        "extension": ".go",
    },

    "rust": {
        "extension": ".rs",
    },

    "csharp": {
        "extension": ".cs",
    },

    "kotlin": {
        "extension": ".kt",
    },

    "php": {
        "extension": ".php",
    },
}


def compile_program(
    language: str,
    source_file: str,
    output_dir: str
):
    """
    Compile languages that require compilation.

    Returns:
        executable command
    """

    language = language.lower()

    if language == "c":

        executable = os.path.join(
            output_dir,
            "program.exe"
        )

        result = subprocess.run(
            [
                "gcc",
                source_file,
                "-O2",
                "-o",
                executable
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"C compilation failed:\n{result.stderr}"
            )

        return [executable]

    elif language == "cpp":

        executable = os.path.join(
            output_dir,
            "program.exe"
        )

        result = subprocess.run(
            [
                "g++",
                "-O2",
                "-std=c++17",
                source_file,
                "-o",
                executable
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"C++ compilation failed:\n{result.stderr}"
            )

        return [executable]

    elif language == "java":

        java_source = Path(source_file)

        result = subprocess.run(
            [
                r"C:\Program Files\Java\jdk-24\bin\javac.exe",
                java_source.name,
            ],
            cwd=str(java_source.parent),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Java compilation failed:\n{result.stderr}"
            )

        # Determine the class containing the main method.
        java_code = java_source.read_text(encoding="utf-8")

        class_match = re.search(
            r"\bpublic\s+(?:final\s+|abstract\s+)?class\s+"
            r"([A-Za-z_$][A-Za-z0-9_$]*)",
            java_code,
        )

        if not class_match:
            class_match = re.search(
                r"\bclass\s+([A-Za-z_$][A-Za-z0-9_$]*)",
                java_code,
            )

        if not class_match:
            raise RuntimeError(
                "Java compilation succeeded but no class name could be determined."
            )

        class_name = class_match.group(1)

        java_exe = r"C:\Program Files\Java\jdk-24\bin\java.exe"

        return [
            java_exe,
            "-cp",
            str(java_source.parent),
            class_name,
        ]

    elif language == "go":

        executable = os.path.join(
            output_dir,
            "program.exe"
        )

        result = subprocess.run(
            [
                "go",
                "build",
                "-o",
                executable,
                source_file
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Go compilation failed:\n{result.stderr}"
            )

        return [executable]

    elif language == "rust":

        executable = os.path.join(
            output_dir,
            "program.exe"
        )

        result = subprocess.run(
            [
                "rustc",
                "-O",
                source_file,
                "-o",
                executable
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Rust compilation failed:\n{result.stderr}"
            )

        return [executable]

    elif language == "csharp":

        project_dir = Path(output_dir) / "csharp_project"
        project_dir.mkdir(parents=True, exist_ok=True)

        csproj_file = project_dir / "Benchmark.csproj"
        program_file = project_dir / "Program.cs"

        # Copy benchmark source into Program.cs
        with open(source_file, "r", encoding="utf-8") as src:
            code = src.read()

        with open(program_file, "w", encoding="utf-8") as dst:
            dst.write(code)

        # Create a minimal .NET console project
        csproj_content = """<Project Sdk="Microsoft.NET.Sdk">
    <PropertyGroup>
        <OutputType>Exe</OutputType>
        <TargetFramework>net10.0</TargetFramework>
        <ImplicitUsings>enable</ImplicitUsings>
        <Nullable>disable</Nullable>
    </PropertyGroup>
    </Project>
    """

        with open(csproj_file, "w", encoding="utf-8") as f:
            f.write(csproj_content)

        result = subprocess.run(
            [
                "dotnet",
                "build",
                str(csproj_file),
                "-c",
                "Release",
                "--nologo"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"C# compilation failed:\n{result.stdout}\n{result.stderr}"
            )

        dll_file = (
            project_dir
            / "bin"
            / "Release"
            / "net10.0"
            / "Benchmark.dll"
        )

        if not dll_file.exists():
            raise RuntimeError(
                "C# build succeeded but Benchmark.dll was not found."
            )

        return [
            "dotnet",
            str(dll_file)
        ]
        
    elif language == "kotlin":
        executable = os.path.join(
            output_dir,
            "program.jar"
        )

        result = subprocess.run(
            [
                r"C:\Kotlin\kotlinc\bin\kotlinc.bat",
                source_file,
                "-include-runtime",
                "-d",
                executable
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
                raise RuntimeError(
                    f"Kotlin compilation failed:\n{result.stderr}"
                )

        return [
            r"C:\Program Files\Java\jdk-24\bin\java.exe",
            "-jar",
            executable
        ]

    elif language == "python":

        return [
            "python",
            source_file
        ]

    elif language == "javascript":

        return [
            "node",
            source_file
        ]

    elif language == "php":

        return [
            "php",
            source_file
        ]

    else:

        raise ValueError(
            f"Unsupported language: {language}"
        )


def execute_program(
    command,
    input_data: str,
    timeout: int = 120
):
    """
    Execute compiled/interpreted program.
    """

    start_time = time.perf_counter()

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:

        stdout, stderr = process.communicate(
            input=input_data,
            timeout=timeout
        )

    except subprocess.TimeoutExpired:

        process.kill()

        stdout, stderr = process.communicate()

        raise TimeoutError(
            "Benchmark execution timed out."
        )

    end_time = time.perf_counter()

    if process.returncode != 0:

        raise RuntimeError(
            f"Program execution failed:\n{stderr}"
        )

    execution_time = (
        end_time - start_time
    ) * 1000

    return {
        "stdout": stdout.strip(),
        "stderr": stderr.strip(),
        "return_code": process.returncode,
        "execution_time": execution_time,
    }

def validate_syntax(
    language: str,
    source_file: str,
    output_dir: str,
):
    """
    Validate source-code syntax without executing the program.

    Returns:
        {
            "syntax_valid": bool,
            "syntax_errors": list[str]
        }
    """

    language = language.lower().strip()

    try:

        # --------------------------------------------------
        # COMPILED LANGUAGES
        # --------------------------------------------------

        if language in {
            "c",
            "cpp",
            "java",
            "go",
            "rust",
            "csharp",
            "kotlin",
        }:

            compile_program(
                language=language,
                source_file=source_file,
                output_dir=output_dir,
            )

            return {
                "syntax_valid": True,
                "syntax_errors": [],
            }


        # --------------------------------------------------
        # PYTHON
        # --------------------------------------------------

        elif language == "python":

            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "py_compile",
                    source_file,
                ],
                capture_output=True,
                text=True,
            )


        # --------------------------------------------------
        # JAVASCRIPT
        # --------------------------------------------------

        elif language == "javascript":

            result = subprocess.run(
                [
                    "node",
                    "--check",
                    source_file,
                ],
                capture_output=True,
                text=True,
            )


        # --------------------------------------------------
        # PHP
        # --------------------------------------------------

        elif language == "php":

            result = subprocess.run(
                [
                    "php",
                    "-l",
                    source_file,
                ],
                capture_output=True,
                text=True,
            )


        else:

            return {
                "syntax_valid": False,
                "syntax_errors": [
                    f"Unsupported language: {language}"
                ],
            }


        # --------------------------------------------------
        # RESULT FOR INTERPRETED LANGUAGES
        # --------------------------------------------------

        if result.returncode == 0:

            return {
                "syntax_valid": True,
                "syntax_errors": [],
            }


        error_text = (
            result.stderr.strip()
            or result.stdout.strip()
            or "Syntax validation failed."
        )

        return {
            "syntax_valid": False,
            "syntax_errors": [
                error_text
            ],
        }


    except RuntimeError as exc:

        return {
            "syntax_valid": False,
            "syntax_errors": [
                str(exc)
            ],
        }


    except FileNotFoundError as exc:

        return {
            "syntax_valid": False,
            "syntax_errors": [
                (
                    "Required compiler or interpreter "
                    f"was not found: {exc}"
                )
            ],
        }