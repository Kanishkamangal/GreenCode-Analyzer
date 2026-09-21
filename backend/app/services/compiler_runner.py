import os
import shutil
import subprocess
import tempfile
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

        try:
            result = subprocess.run(
                [
                    "gcc",
                    source_file,
                    "-O2",
                    "-fno-lto",
                    "-o",
                    executable
                ],
                capture_output=True,
                text=True
            )
        except FileNotFoundError:
            raise RuntimeError(
                "GCC compiler not found. Please install MinGW or ensure GCC is in your PATH."
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

        try:
            result = subprocess.run(
                [
                "g++",
                "-O2",
                "-fno-lto",
                "-std=c++17",
                source_file,
                "-o",
                executable
            ],
                capture_output=True,
                text=True
            )
        except FileNotFoundError:
            raise RuntimeError(
                "G++ compiler not found. Please install MinGW or ensure G++ is in your PATH."
            )

        if result.returncode != 0:
            raise RuntimeError(
                f"C++ compilation failed:\n{result.stderr}"
            )

        return [executable]

    elif language == "java":

        # Java source files in our benchmark library may be named
        # java.java, but the implementation uses:
        #
        # public class Main
        #
        # Java requires the public class name to match the filename.
        # Therefore create a temporary Main.java.

        java_source = Path(source_file)

        main_file = Path(output_dir) / "Main.java"

        with open(java_source, "r", encoding="utf-8") as src:
            java_code = src.read()

        with open(main_file, "w", encoding="utf-8") as dst:
            dst.write(java_code)

        # Find javac in PATH or use specific locations
        javac_path = shutil.which("javac")
        if not javac_path:
            # Try common JDK locations
            for jdk_path in [
                r"C:\Program Files\Microsoft\jdk-25.0.4.101-hotspot\bin\javac.exe",
                r"C:\Program Files\Java\jdk-25\bin\javac.exe",
                r"C:\Program Files\Java\jdk-24\bin\javac.exe",
            ]:
                if os.path.exists(jdk_path):
                    javac_path = jdk_path
                    break

        if not javac_path:
            raise RuntimeError(
                "Java JDK not found. Please install JDK or ensure javac is in your PATH."
            )

        try:
            result = subprocess.run(
                [
                    javac_path,
                    "Main.java"
                ],
                cwd=output_dir,
                capture_output=True,
                text=True
            )
        except FileNotFoundError:
            raise RuntimeError(
                f"Java compiler not found at {javac_path}"
            )

        if result.returncode != 0:
            raise RuntimeError(
                f"Java compilation failed:\n{result.stderr}"
            )

        # Find java in PATH
        java_exe = shutil.which("java")
        if not java_exe:
            # Try common JDK locations
            for jdk_path in [
                r"C:\Program Files\Microsoft\jdk-25.0.4.101-hotspot\bin\java.exe",
                r"C:\Program Files\Java\jdk-25\bin\java.exe",
                r"C:\Program Files\Java\jdk-24\bin\java.exe",
            ]:
                if os.path.exists(jdk_path):
                    java_exe = jdk_path
                    break

        if not java_exe:
            raise RuntimeError(
                "Java runtime not found. Please install JDK or ensure java is in your PATH."
            )

        return [
            java_exe,
            "-cp",
            output_dir,
            "Main"
        ]

    elif language == "go":

        executable = os.path.join(
            output_dir,
            "program.exe"
        )

        try:
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
        except FileNotFoundError:
            raise RuntimeError(
                "Go compiler not found. Please install Go or ensure it is in your PATH."
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

        try:
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
        except FileNotFoundError:
            raise RuntimeError(
                "Rustc compiler not found. Please install Rust or ensure it is in your PATH."
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

        kotlinc_path = shutil.which("kotlinc")
        if not kotlinc_path:
            for kotlin_path in [
                r"C:\Kotlin\kotlinc\kotlinc\bin\kotlinc.bat",
            ]:
                if os.path.exists(kotlin_path):
                    kotlinc_path = kotlin_path
                    break

        if not kotlinc_path:
            raise RuntimeError(
                "Kotlin compiler not found. Please install Kotlin or ensure kotlinc is in your PATH."
            )

        java_exe = shutil.which("java")
        if not java_exe:
            for jdk_path in [
                r"C:\Program Files\Microsoft\jdk-25.0.4.101-hotspot\bin\java.exe",
                r"C:\Program Files\Java\jdk-25\bin\java.exe",
                r"C:\Program Files\Java\jdk-24\bin\java.exe",
            ]:
                if os.path.exists(jdk_path):
                    java_exe = jdk_path
                    break

        if not java_exe:
            raise RuntimeError(
                "Java runtime not found. Please install a JDK or ensure java is in your PATH."
            )

        try:
            result = subprocess.run(
                [
                    os.environ.get("COMSPEC", "cmd.exe"),
                    "/c",
                    kotlinc_path,
                    source_file,
                    "-include-runtime",
                    "-d",
                    executable
                ],
                capture_output=True,
                text=True
            )
        except FileNotFoundError:
            raise RuntimeError(
                "Kotlin compiler not found. Please install Kotlin or ensure kotlinc is in your PATH."
            )

        if result.returncode != 0:
                raise RuntimeError(
                    f"Kotlin compilation failed:\n{result.stderr}"
                )

        return [
                java_exe,
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