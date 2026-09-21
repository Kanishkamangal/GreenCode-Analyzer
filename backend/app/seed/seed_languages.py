from app.database.database import SessionLocal

# Registers all models
import app.models

from app.models.programming_language import ProgrammingLanguage
db = SessionLocal()

languages = [
    {
        "lang_name": "C",
        "compiler": "gcc",
        "version": "latest",
        "compile_command": "gcc {source} -o {output}",
        "run_command": "./{output}"
    },
    {
        "lang_name": "C++",
        "compiler": "g++",
        "version": "latest",
        "compile_command": "g++ {source} -o {output}",
        "run_command": "./{output}"
    },
    {
        "lang_name": "Java",
        "compiler": "javac",
        "version": "24.0.1",
        "compile_command": "javac {source}",
        "run_command": "java {classname}"
    },
    {
        "lang_name": "Python",
        "compiler": "python",
        "version": "3.14",
        "compile_command": None,
        "run_command": "python {source}"
    },
    {
        "lang_name": "JavaScript",
        "compiler": "node",
        "version": "latest",
        "compile_command": None,
        "run_command": "node {source}"
    },
    {
        "lang_name": "Go",
        "compiler": "go",
        "version": "latest",
        "compile_command": "go build -o {output} {source}",
        "run_command": "./{output}"
    },
    {
        "lang_name": "Rust",
        "compiler": "rustc",
        "version": "latest",
        "compile_command": "rustc {source} -o {output}",
        "run_command": "./{output}"
    },
    {
        "lang_name": "C#",
        "compiler": "dotnet",
        "version": "latest",
        "compile_command": "dotnet build",
        "run_command": "dotnet run"
    },
    {
        "lang_name": "Kotlin",
        "compiler": "kotlinc",
        "version": "2.4.10",
        "compile_command": "kotlinc {source} -include-runtime -d {output}.jar",
        "run_command": "java -jar {output}.jar"
    },
    {
        "lang_name": "PHP",
        "compiler": "php",
        "version": "8.5.9",
        "compile_command": None,
        "run_command": "php {source}"
    }
]

for lang in languages:
    existing = db.query(ProgrammingLanguage).filter_by(
        lang_name=lang["lang_name"]
    ).first()

    if not existing:
        db.add(ProgrammingLanguage(**lang))
        print(f"Inserted: {lang['lang_name']}")
    else:
        print(f"Already exists: {lang['lang_name']}")

db.commit()
db.close()

print("\n✅ Programming languages seeded successfully!")