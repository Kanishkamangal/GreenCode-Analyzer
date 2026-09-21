import os
import logging

from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def clean_generated_code(
    code: str
) -> str:

    """
    Remove Markdown code fences if Gemini returns them.
    """

    if not code:
        return ""

    code = code.strip()

    if code.startswith("```"):

        lines = code.splitlines()

        # Remove first ```language line
        if lines:
            lines = lines[1:]

        # Remove ending ```
        if (
            lines
            and lines[-1].strip() == "```"
        ):
            lines = lines[:-1]

        code = "\n".join(lines)

    return code.strip()


def generate_equivalent_code(
    reference_language: str,
    target_language: str,
    reference_code: str,
    benchmark_name: str,
    benchmark_category: str,
    description: str | None,
    workload_type: str | None = None,
    input_size: int | None = None,
) -> str:

    """
    Generate an equivalent implementation of the
    reference benchmark in another programming language.

    Gemini is used only for code translation.
    Actual compilation, execution and measurements
    are handled separately by the benchmark engine.
    """

    if not reference_code.strip():
        raise ValueError(
            "Reference code cannot be empty."
        )

    if (
        reference_language.lower()
        == target_language.lower()
    ):
        return reference_code

    description_text = (
        description.strip()
        if description
        else "No additional description provided."
    )
    resolved_workload_type = (
        workload_type
        if workload_type
        else "Automatically resolved from the benchmark workload."
    )

    prompt = f"""
You are an expert software engineer working on a
programming-language sustainability benchmarking system.

Convert the following {reference_language} benchmark
implementation into {target_language}.

Benchmark Name:
{benchmark_name}

Benchmark Category:
{benchmark_category}

Description:
{description_text}

Workload Type:
{resolved_workload_type}

Input Size:
{input_size}

Requirements:
- The workload type is {workload_type}.
- If the target language is Java, the public class name must be Main.
- Preserve exactly the same algorithm and workload.
- Preserve the same input format.
- Preserve the same output behavior.
- Preserve equivalent time complexity.
- Preserve equivalent space complexity where possible.
- Do not optimize the algorithm.
- Do not replace the algorithm with a built-in library solution.
- Do not add extra output, logging, prompts or debug messages.
- The program must read input from standard input.
- The program must write only the expected benchmark output
  to standard output.
- Produce standalone compilable/runnable {target_language} code.
- Return only source code.
- Do not use Markdown code fences.
- Do not include explanations.

Reference {reference_language} code:

{reference_code}
"""

    try:

        logger.info(
            "Generating benchmark code: %s -> %s",
            reference_language,
            target_language,
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        generated_code = clean_generated_code(
            response.text or ""
        )

        if not generated_code:
            raise RuntimeError(
                "Gemini returned empty generated code."
            )

        logger.info(
            "Code generation completed: %s -> %s",
            reference_language,
            target_language,
        )

        return generated_code

    except Exception as exc:

        logger.exception(
            "Gemini code generation failed: %s -> %s",
            reference_language,
            target_language,
        )

        error_text = str(exc)

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):
            raise RuntimeError(
                "AI code generation is temporarily unavailable "
                "because the Gemini API quota has been exhausted. "
                "Please try again later."
            ) from exc

        raise RuntimeError(
            "Unable to generate equivalent "
            f"{target_language} implementation: {error_text}"
        ) from exc