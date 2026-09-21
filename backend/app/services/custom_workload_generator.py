from __future__ import annotations

import csv
import io
import json
import random
import string
from typing import Any

# ============================================================
# CONTRACT FIELD HELPERS
# ============================================================

def _contract_value_type(field: dict[str, Any]) -> str:
    return str(
        field.get("type", "string")
    ).strip().lower()


def _generate_integer(
    rng: random.Random,
    minimum: int = 1,
    maximum: int = 1000,
) -> int:
    return rng.randint(
        minimum,
        maximum,
    )


def _generate_float(
    rng: random.Random,
) -> float:
    return round(
        rng.uniform(1.0, 1000.0),
        3,
    )


def _generate_character(
    rng: random.Random,
) -> str:
    return rng.choice(
        string.ascii_lowercase
    )


def _generate_string(
    rng: random.Random,
    min_length: int = 5,
    max_length: int = 12,
) -> str:
    length = rng.randint(
        min_length,
        max_length,
    )

    return "".join(
        rng.choice(
            string.ascii_lowercase
        )
        for _ in range(length)
    )


# ============================================================
# EXACT INPUT CONTRACT GENERATOR
# ============================================================

def generate_from_input_contract(
    input_contract: dict[str, Any],
    input_size: int | None,
    seed: int = 42,
    algorithm: str | None = None,
) -> str:
    """
    Generate stdin directly from the exact Input Contract.

    The Input Contract is authoritative for:
    - field order
    - field type
    - field role
    - exact contract structure
    """

    if not input_contract:
        raise ValueError(
            "Input contract is required."
        )

    contract_type = (
        str(
            input_contract.get(
                "contract_type",
                "",
            )
        )
        .strip()
        .lower()
    )

    fields = input_contract.get(
        "fields",
        [],
    )

    rng = random.Random(seed)

    size = max(
        1,
        int(
            input_size
            if input_size is not None
            else 10
        ),
    )

    # --------------------------------------------------------
    # NO INPUT
    # --------------------------------------------------------

    if contract_type == "no-input":
        return ""

    # --------------------------------------------------------
    # INTEGER SCALAR
    # --------------------------------------------------------

    if contract_type == "integer-scalar":

        return (
            f"{_generate_integer(rng)}\n"
        )

    # --------------------------------------------------------
    # FLOAT SCALAR
    # --------------------------------------------------------

    if contract_type == "float-scalar":

        return (
            f"{_generate_float(rng)}\n"
        )

    # --------------------------------------------------------
    # CHARACTER SCALAR
    # --------------------------------------------------------

    if contract_type == "character-scalar":

        return (
            f"{_generate_character(rng)}\n"
        )

    # --------------------------------------------------------
    # INTEGER SCALARS
    # --------------------------------------------------------

    if contract_type == "integer-scalars":

        values = [
            str(
                _generate_integer(rng)
            )
            for _ in fields
        ]

        return (
            " ".join(values)
            + "\n"
        )

    # --------------------------------------------------------
    # FLOAT SCALARS
    # --------------------------------------------------------

    if contract_type == "float-scalars":

        values = [
            str(
                _generate_float(rng)
            )
            for _ in fields
        ]

        return (
            " ".join(values)
            + "\n"
        )

    # --------------------------------------------------------
    # MIXED SCALARS
    # --------------------------------------------------------

    if contract_type == "mixed-scalars":

        values = []

        for field in fields:

            value_type = (
                _contract_value_type(
                    field
                )
            )

            if value_type in {
                "integer",
                "int",
                "long",
            }:
                values.append(
                    str(
                        _generate_integer(rng)
                    )
                )

            elif value_type in {
                "float",
                "double",
                "decimal",
            }:
                values.append(
                    str(
                        _generate_float(rng)
                    )
                )

            elif value_type in {
                "character",
                "char",
            }:
                values.append(
                    _generate_character(rng)
                )

            else:
                values.append(
                    _generate_string(rng)
                )

        return (
            " ".join(values)
            + "\n"
        )

        # --------------------------------------------------------
    # STRING TOKEN
    # --------------------------------------------------------

    if contract_type == "string-token":

        return (
            f"{_generate_string(rng)}\n"
        )

    # --------------------------------------------------------
    # STRING LINE
    # --------------------------------------------------------

    if contract_type == "string-line":

        return (
            f"{_generate_string(rng)}\n"
        )

    # --------------------------------------------------------
    # STRING ARRAY
    # --------------------------------------------------------

    if contract_type == "string-array":

        values = [
            _generate_string(rng)
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + " ".join(values)
            + "\n"
        )

    # --------------------------------------------------------
    # STRING LINES
    # --------------------------------------------------------

    if contract_type == "string-lines":

        values = [
            _generate_string(rng)
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + "\n".join(values)
            + "\n"
        )

    # --------------------------------------------------------
    # SCALAR + LINE
    # --------------------------------------------------------

    if contract_type == "scalar-plus-line":

        scalar_value = _generate_integer(rng)
        line_value = _generate_string(rng)

        return (
            f"{scalar_value}\n"
            f"{line_value}\n"
        )

    # --------------------------------------------------------
    # SIZE + STRING
    # --------------------------------------------------------

    if contract_type == "size-plus-string":

        string_value = _generate_string(rng)

        return (
            f"{size}\n"
            f"{string_value}\n"
        )

    # --------------------------------------------------------
    # SIZE + TWO STRINGS
    # --------------------------------------------------------

    if contract_type == "size-plus-two-strings":

        first = _generate_string(rng)
        second = _generate_string(rng)

        return (
            f"{size}\n"
            f"{first}\n"
            f"{second}\n"
        )

    # --------------------------------------------------------
    # SIZE + STRINGS
    # --------------------------------------------------------

    if contract_type == "size-plus-strings":

        values = [
            _generate_string(rng)
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + "\n".join(values)
            + "\n"
        )

    # --------------------------------------------------------
    # CHARACTER STREAM
    # --------------------------------------------------------

    if contract_type == "character-stream":

        characters = [
            _generate_character(rng)
            for _ in range(size)
        ]

        return (
            "".join(characters)
            + "\n"
        )

            # --------------------------------------------------------
    # INTEGER ARRAY
    # --------------------------------------------------------

    if contract_type == "integer-array":

        values = [
            _generate_integer(rng)
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + " ".join(
                map(str, values)
            )
            + "\n"
        )

    # --------------------------------------------------------
    # FLOAT ARRAY
    # --------------------------------------------------------

    if contract_type == "float-array":

        values = [
            _generate_float(rng)
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + " ".join(
                map(str, values)
            )
            + "\n"
        )

    # --------------------------------------------------------
    # CHARACTER ARRAY
    # --------------------------------------------------------

    if contract_type == "character-array":

        values = [
            _generate_character(rng)
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + " ".join(values)
            + "\n"
        )

    # --------------------------------------------------------
    # JAGGED ARRAY
    # --------------------------------------------------------

    if contract_type == "jagged-array":

        rows = max(
            1,
            min(size, 20),
        )

        lines = [
            str(rows)
        ]

        for row_index in range(rows):

            row_size = max(
                1,
                min(
                    2 + (row_index % 5),
                    size,
                ),
            )

            values = [
                _generate_integer(rng)
                for _ in range(row_size)
            ]

            lines.append(
                str(row_size)
            )

            lines.append(
                " ".join(
                    map(str, values)
                )
            )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # ARRAY + TARGET
    # --------------------------------------------------------

    if contract_type == "array-plus-target":

        normalized_algorithm = (
            str(algorithm or "")
            .strip()
            .lower()
            .replace("_", "-")
            .replace(" ", "-")
        )

        # Search workloads must satisfy the semantic preconditions
        # of the detected algorithm.  In particular, binary search
        # requires an ordered sequence; generic search workloads do not.
        if normalized_algorithm == "binary-search":
            values = sorted(
                _generate_integer(rng, 1, 1_000_000)
                for _ in range(size)
            )
        else:
            values = [
                _generate_integer(rng, 1, 1_000_000)
                for _ in range(size)
            ]

        # Use a deterministic in-range target. This creates a valid
        # positive search case while preserving the exact contract shape.
        target_index = rng.randrange(len(values))
        target = values[target_index]

        return (
            f"{size}\n"
            + " ".join(
                map(str, values)
            )
            + "\n"
            + f"{target}\n"
        )

    # --------------------------------------------------------
    # MULTIPLE ARRAYS
    # --------------------------------------------------------

    if contract_type == "multiple-arrays":

        first = [
            _generate_integer(rng)
            for _ in range(size)
        ]

        second = [
            _generate_integer(rng)
            for _ in range(size)
        ]

        return (
            f"{size}\n"
            + " ".join(
                map(str, first)
            )
            + "\n"
            + " ".join(
                map(str, second)
            )
            + "\n"
        )

    # --------------------------------------------------------
    # ARRAY WITH QUERIES
    # --------------------------------------------------------

    if contract_type == "array-with-queries":

        values = [
            _generate_integer(rng)
            for _ in range(size)
        ]

        query_count = max(
            1,
            min(size, 20),
        )

        query_lines = []

        for _ in range(query_count):

            index = rng.randint(
                1,
                size,
            )

            query_lines.append(
                str(index)
            )

        return (
            f"{size}\n"
            + " ".join(
                map(str, values)
            )
            + "\n"
            + f"{query_count}\n"
            + "\n".join(query_lines)
            + "\n"
        )

    # --------------------------------------------------------
    # ARRAY WITH RANGE QUERIES
    # --------------------------------------------------------

    if contract_type == "array-with-range-queries":

        values = [
            _generate_integer(rng)
            for _ in range(size)
        ]

        query_count = max(
            1,
            min(size, 20),
        )

        lines = [
            str(size),
            " ".join(
                map(str, values)
            ),
            str(query_count),
        ]

        for _ in range(query_count):

            left = rng.randint(
                1,
                size,
            )

            right = rng.randint(
                left,
                size,
            )

            lines.append(
                f"{left} {right}"
            )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # MATRIX
    # --------------------------------------------------------

    if contract_type == "matrix":

        rows = size
        cols = size

        lines = [
            f"{rows} {cols}"
        ]

        for _ in range(rows):

            values = [
                _generate_integer(rng)
                for _ in range(cols)
            ]

            lines.append(
                " ".join(
                    map(str, values)
                )
            )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # MATRIX + TARGET
    # --------------------------------------------------------

    if contract_type == "matrix-plus-target":

        rows = size
        cols = size

        lines = [
            f"{rows} {cols}"
        ]

        for _ in range(rows):

            values = [
                _generate_integer(rng)
                for _ in range(cols)
            ]

            lines.append(
                " ".join(
                    map(str, values)
                )
            )

        target = _generate_integer(rng)

        lines.append(
            str(target)
        )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # CHARACTER GRID
    # --------------------------------------------------------

    if contract_type == "character-grid":

        rows = size
        cols = size

        lines = [
            f"{rows} {cols}"
        ]

        for _ in range(rows):

            values = [
                _generate_character(rng)
                for _ in range(cols)
            ]

            lines.append(
                "".join(values)
            )

        return (
            "\n".join(lines)
            + "\n"
        )

        # --------------------------------------------------------
    # JAGGED MATRIX
    # --------------------------------------------------------

    if contract_type == "jagged-matrix":

        rows = max(
            1,
            min(size, 20),
        )

        lines = [
            str(rows)
        ]

        for row_index in range(rows):

            cols = max(
                1,
                min(
                    2 + (row_index % 5),
                    size,
                ),
            )

            values = [
                _generate_integer(rng)
                for _ in range(cols)
            ]

            lines.append(
                str(cols)
            )

            lines.append(
                " ".join(
                    map(str, values)
                )
            )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # ADJACENCY MATRIX
    # --------------------------------------------------------

    if contract_type == "adjacency-matrix":

        vertices = size

        lines = [
            str(vertices)
        ]

        for row in range(vertices):

            values = []

            for column in range(vertices):

                if row == column:
                    values.append("0")

                else:
                    values.append(
                        str(
                            rng.choice(
                                [0, 1]
                            )
                        )
                    )

            lines.append(
                " ".join(values)
            )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # TEST CASES - ARRAY
    # --------------------------------------------------------

    if contract_type == "test-cases-array":

        test_cases = max(
            1,
            min(size, 10),
        )

        lines = [
            str(test_cases)
        ]

        for _ in range(test_cases):

            case_size = max(
                1,
                min(size, 100),
            )

            values = [
                _generate_integer(rng)
                for _ in range(case_size)
            ]

            lines.append(
                str(case_size)
            )

            lines.append(
                " ".join(
                    map(str, values)
                )
            )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # TEST CASES - MATRIX
    # --------------------------------------------------------

    if contract_type == "test-cases-matrix":

        test_cases = max(
            1,
            min(size, 10),
        )

        lines = [
            str(test_cases)
        ]

        for _ in range(test_cases):

            rows = max(
                1,
                min(size, 20),
            )

            cols = max(
                1,
                min(size, 20),
            )

            lines.append(
                f"{rows} {cols}"
            )

            for _ in range(rows):

                values = [
                    _generate_integer(rng)
                    for _ in range(cols)
                ]

                lines.append(
                    " ".join(
                        map(str, values)
                    )
                )

        return (
            "\n".join(lines)
            + "\n"
        )


            # --------------------------------------------------------
    # GRAPH
    # Format:
    # n m
    # u v
    # ...
    # --------------------------------------------------------

    if contract_type == "graph":

        vertices = max(
            2,
            size,
        )

        max_edges = (
            vertices * (vertices - 1)
        ) // 2

        edge_count = min(
            max_edges,
            max(1, vertices * 2),
        )

        edges: set[tuple[int, int]] = set()

        while len(edges) < edge_count:

            u = rng.randint(
                1,
                vertices,
            )

            v = rng.randint(
                1,
                vertices,
            )

            if u == v:
                continue

            edges.add(
                tuple(
                    sorted(
                        (u, v)
                    )
                )
            )

        lines = [
            f"{vertices} {len(edges)}"
        ]

        lines.extend(
            f"{u} {v}"
            for u, v in sorted(edges)
        )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # WEIGHTED GRAPH
    # Format:
    # n m
    # u v weight
    # ...
    # --------------------------------------------------------

    if contract_type == "weighted-graph":

        vertices = max(
            2,
            size,
        )

        max_edges = (
            vertices * (vertices - 1)
        ) // 2

        edge_count = min(
            max_edges,
            max(1, vertices * 2),
        )

        edges: set[tuple[int, int]] = set()

        while len(edges) < edge_count:

            u = rng.randint(
                1,
                vertices,
            )

            v = rng.randint(
                1,
                vertices,
            )

            if u == v:
                continue

            edges.add(
                tuple(
                    sorted(
                        (u, v)
                    )
                )
            )

        lines = [
            f"{vertices} {len(edges)}"
        ]

        for u, v in sorted(edges):

            weight = _generate_integer(
                rng
            )

            lines.append(
                f"{u} {v} {weight}"
            )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # GRAPH WITH SOURCE
    # Format:
    # n m
    # u v
    # ...
    # source
    # --------------------------------------------------------

    if contract_type == "graph-with-source":

        vertices = max(
            2,
            size,
        )

        max_edges = (
            vertices * (vertices - 1)
        ) // 2

        edge_count = min(
            max_edges,
            max(1, vertices * 2),
        )

        edges: set[tuple[int, int]] = set()

        while len(edges) < edge_count:

            u = rng.randint(
                1,
                vertices,
            )

            v = rng.randint(
                1,
                vertices,
            )

            if u == v:
                continue

            edges.add(
                tuple(
                    sorted(
                        (u, v)
                    )
                )
            )

        source = rng.randint(
            1,
            vertices,
        )

        lines = [
            f"{vertices} {len(edges)}"
        ]

        lines.extend(
            f"{u} {v}"
            for u, v in sorted(edges)
        )

        lines.append(
            str(source)
        )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # WEIGHTED GRAPH WITH SOURCE
    # Format:
    # n m
    # u v weight
    # ...
    # source
    # --------------------------------------------------------

    if contract_type == "weighted-graph-with-source":

        vertices = max(
            2,
            size,
        )

        max_edges = (
            vertices * (vertices - 1)
        ) // 2

        edge_count = min(
            max_edges,
            max(1, vertices * 2),
        )

        edges: set[tuple[int, int]] = set()

        while len(edges) < edge_count:

            u = rng.randint(
                1,
                vertices,
            )

            v = rng.randint(
                1,
                vertices,
            )

            if u == v:
                continue

            edges.add(
                tuple(
                    sorted(
                        (u, v)
                    )
                )
            )

        source = rng.randint(
            1,
            vertices,
        )

        lines = [
            f"{vertices} {len(edges)}"
        ]

        for u, v in sorted(edges):

            weight = _generate_integer(
                rng
            )

            lines.append(
                f"{u} {v} {weight}"
            )

        lines.append(
            str(source)
        )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # TREE
    # Format:
    # n
    # parent child
    # ...
    # --------------------------------------------------------

    if contract_type == "tree":

        nodes = max(
            1,
            size,
        )

        lines = [
            str(nodes)
        ]

        for child in range(
            2,
            nodes + 1,
        ):

            parent = rng.randint(
                1,
                child - 1,
            )

            lines.append(
                f"{parent} {child}"
            )

        return (
            "\n".join(lines)
            + "\n"
        )

    # --------------------------------------------------------
    # PARENT ARRAY TREE
    # Format:
    # n
    # parent[1] parent[2] ... parent[n]
    # --------------------------------------------------------

    if contract_type == "parent-array-tree":

        nodes = max(
            1,
            size,
        )

        parents = []

        for node in range(
            1,
            nodes + 1,
        ):

            if node == 1:
                parents.append(
                    "0"
                )
            else:
                parents.append(
                    str(
                        rng.randint(
                            1,
                            node - 1,
                        )
                    )
                )

        return (
            f"{nodes}\n"
            + " ".join(parents)
            + "\n"
        )

    # --------------------------------------------------------
    # BINARY TREE - LEVEL ORDER
    # Format:
    # n
    # values...
    #
    # Use -1 as a deterministic null-node marker.
    # --------------------------------------------------------

    if contract_type == "binary-tree-level-order":

        slots = max(
            1,
            min(size, 100),
        )

        values = []

        for index in range(slots):

            # Keep root non-null.
            if index == 0:
                values.append(
                    str(
                        _generate_integer(rng)
                    )
                )
                continue

            # Deterministic sparse tree.
            if rng.random() < 0.20:
                values.append(
                    "-1"
                )
            else:
                values.append(
                    str(
                        _generate_integer(rng)
                    )
                )

        return (
            f"{slots}\n"
            + " ".join(values)
            + "\n"
        )

        # ============================================================
    # EOF STREAM
    # ============================================================
    if contract_type == "eof-stream":
        count = max(3, min(size, 20))

        values = [
            _generate_integer(rng)
            for _ in range(count)
        ]

        return (
            "\n".join(map(str, values))
            + "\n"
        )

    # ============================================================
    # EOF RECORDS
    # ============================================================
    if contract_type == "eof-records":
        count = max(3, min(size, 20))

        records = []

        for _ in range(count):
            values = []

            for field in fields:
                field_type = _contract_value_type(field)

                if field_type in {
                    "integer",
                    "int",
                    "long",
                    "long-long",
                    "number",
                }:
                    values.append(
                        str(_generate_integer(rng))
                    )

                elif field_type in {
                    "float",
                    "double",
                    "decimal",
                }:
                    values.append(
                        str(_generate_float(rng))
                    )

                elif field_type in {
                    "character",
                    "char",
                }:
                    values.append(
                        _generate_character(rng)
                    )

                elif field_type in {
                    "string",
                    "text",
                }:
                    values.append(
                        _generate_string(rng)
                    )

                else:
                    values.append(
                        str(_generate_integer(rng))
                    )

            records.append(
                " ".join(values)
            )

        return "\n".join(records) + "\n"

    # ============================================================
    # EOF LINES
    # ============================================================
    if contract_type == "eof-lines":
        count = max(3, min(size, 20))

        lines = [
            _generate_string(rng, min_length=8, max_length=16)
            for _ in range(count)
        ]

        return "\n".join(lines) + "\n"

    # ============================================================
    # SENTINEL STREAM
    # ============================================================
    if contract_type == "sentinel-stream":
        value_field = next(
            (
                field
                for field in fields
                if field.get("role") != "terminator"
            ),
            None,
        )

        sentinel_field = next(
            (
                field
                for field in fields
                if field.get("role") == "terminator"
            ),
            None,
        )

        field_type = _contract_value_type(
            value_field or {}
        )

        if field_type in {
            "float",
            "double",
            "decimal",
        }:
            values = [
                str(_generate_float(rng))
                for _ in range(max(3, min(size, 20)))
            ]
        elif field_type in {
            "character",
            "char",
        }:
            values = [
                _generate_character(rng)
                for _ in range(max(3, min(size, 20)))
            ]
        elif field_type in {
            "string",
            "text",
        }:
            values = [
                _generate_string(rng)
                for _ in range(max(3, min(size, 20)))
            ]
        else:
            values = [
                str(_generate_integer(rng))
                for _ in range(max(3, min(size, 20)))
            ]

        sentinel = (
            sentinel_field.get("value")
            if sentinel_field
            else "-1"
        )

        return (
            "\n".join(values)
            + "\n"
            + str(sentinel)
            + "\n"
        )

    # ============================================================
    # SENTINEL RECORDS
    # ============================================================
    if contract_type == "sentinel-records":
        value_fields = [
            field
            for field in fields
            if field.get("role") != "terminator"
        ]

        terminator_fields = [
            field
            for field in fields
            if field.get("role") == "terminator"
        ]

        count = max(3, min(size, 20))
        records = []

        for _ in range(count):
            values = []

            for field in value_fields:
                field_type = _contract_value_type(field)

                if field_type in {
                    "float",
                    "double",
                    "decimal",
                }:
                    values.append(
                        str(_generate_float(rng))
                    )
                elif field_type in {
                    "character",
                    "char",
                }:
                    values.append(
                        _generate_character(rng)
                    )
                elif field_type in {
                    "string",
                    "text",
                }:
                    values.append(
                        _generate_string(rng)
                    )
                else:
                    values.append(
                        str(_generate_integer(rng))
                    )

            records.append(
                " ".join(values)
            )

        # Generate terminator record from literal fields.
        terminator_values = []

        for field in terminator_fields:
            terminator_values.append(
                str(field.get("value", "-1"))
            )

        if not terminator_values:
            terminator_values = ["-1"]

        records.append(
            " ".join(terminator_values)
        )

        return "\n".join(records) + "\n"

    # ============================================================
    # PAIRS / PAIR RECORDS
    # ============================================================
    if contract_type in {
        "pairs",
        "pair-records",
    }:
        count = max(3, min(size, 20))

        records = []

        for _ in range(count):
            first = _generate_integer(rng)
            second = _generate_integer(rng)

            records.append(
                f"{first} {second}"
            )

        return (
            f"{count}\n"
            + "\n".join(records)
            + "\n"
        )

    # ============================================================
    # TRIPLES / TRIPLE RECORDS
    # ============================================================
    if contract_type in {
        "triples",
        "triple-records",
    }:
        count = max(3, min(size, 20))

        records = []

        for _ in range(count):
            first = _generate_integer(rng)
            second = _generate_integer(rng)
            third = _generate_integer(rng)

            records.append(
                f"{first} {second} {third}"
            )

        return (
            f"{count}\n"
            + "\n".join(records)
            + "\n"
        )

    # ============================================================
    # TUPLE RECORDS
    # ============================================================
    if contract_type == "tuple-records":
        count = max(3, min(size, 20))

        records = []

        for _ in range(count):
            values = []

            for field in fields:
                field_type = _contract_value_type(field)

                if field_type in {
                    "float",
                    "double",
                    "decimal",
                }:
                    values.append(
                        str(_generate_float(rng))
                    )
                elif field_type in {
                    "string",
                    "text",
                }:
                    values.append(
                        _generate_string(rng)
                    )
                elif field_type in {
                    "character",
                    "char",
                }:
                    values.append(
                        _generate_character(rng)
                    )
                else:
                    values.append(
                        str(_generate_integer(rng))
                    )

            records.append(
                " ".join(values)
            )

        return (
            f"{count}\n"
            + "\n".join(records)
            + "\n"
        )

    # ============================================================
    # STRUCTURED RECORDS
    # ============================================================
    if contract_type == "structured-records":
        count = max(3, min(size, 20))

        records = []

        for index in range(count):
            values = []

            for field in fields:
                field_type = _contract_value_type(field)

                if field_type in {
                    "float",
                    "double",
                    "decimal",
                }:
                    values.append(
                        str(_generate_float(rng))
                    )
                elif field_type in {
                    "string",
                    "text",
                }:
                    values.append(
                        _generate_string(rng)
                    )
                elif field_type in {
                    "character",
                    "char",
                }:
                    values.append(
                        _generate_character(rng)
                    )
                else:
                    values.append(
                        str(index + 1)
                    )

            records.append(
                " ".join(values)
            )

        return (
            f"{count}\n"
            + "\n".join(records)
            + "\n"
        )

    # ============================================================
    # KEY-VALUE RECORDS
    # ============================================================
    if contract_type == "key-value-records":
        count = max(3, min(size, 20))

        records = []

        for _ in range(count):
            key = _generate_string(
                rng,
                min_length=5,
                max_length=10,
            )
            value = _generate_integer(rng)

            records.append(
                f"{key} {value}"
            )

        return (
            f"{count}\n"
            + "\n".join(records)
            + "\n"
        )

    # ============================================================
    # QUERY STREAM
    # ============================================================
    if contract_type == "query-stream":
        count = max(3, min(size, 20))

        lines = []

        for _ in range(count):
            lines.append(
                str(_generate_integer(rng, 0, 1000))
            )

        return (
            f"{count}\n"
            + "\n".join(lines)
            + "\n"
        )

    # ============================================================
    # RANGE QUERIES
    # ============================================================
    if contract_type == "range-queries":
        n = max(3, min(size, 50))

        array = [
            _generate_integer(rng)
            for _ in range(n)
        ]

        query_count = max(2, min(size, 10))

        queries = []

        for _ in range(query_count):
            left = rng.randint(0, n - 1)
            right = rng.randint(left, n - 1)

            queries.append(
                f"{left} {right}"
            )

        return (
            f"{n}\n"
            + " ".join(map(str, array))
            + "\n"
            + f"{query_count}\n"
            + "\n".join(queries)
            + "\n"
        )

    # ============================================================
    # COMMAND STREAM
    # ============================================================
    if contract_type == "command-stream":
        command_count = max(4, min(size, 20))

        commands = []

        for index in range(command_count):
            if index % 3 == 0:
                commands.append(
                    f"ADD {_generate_integer(rng)}"
                )
            elif index % 3 == 1:
                commands.append(
                    f"REMOVE {_generate_integer(rng)}"
                )
            else:
                commands.append("PRINT")

        return (
            f"{command_count}\n"
            + "\n".join(commands)
            + "\n"
        )

    # ============================================================
    # DELIMITED LINES
    # ============================================================
    if contract_type == "delimited-lines":
        count = max(3, min(size, 20))

        lines = []

        for _ in range(count):
            values = [
                _generate_integer(rng),
                _generate_integer(rng),
                _generate_integer(rng),
            ]

            lines.append(
                ",".join(map(str, values))
            )

        return "\n".join(lines) + "\n"

    # ============================================================
    # SCANF INPUT
    # ============================================================
    if contract_type == "scanf-input":
        values = []

        for field in fields:
            field_type = _contract_value_type(field)

            if field_type in {
                "float",
                "double",
                "decimal",
            }:
                values.append(
                    str(_generate_float(rng))
                )
            elif field_type in {
                "character",
                "char",
            }:
                values.append(
                    _generate_character(rng)
                )
            elif field_type in {
                "string",
                "text",
            }:
                values.append(
                    _generate_string(rng)
                )
            else:
                values.append(
                    str(_generate_integer(rng))
                )

        return " ".join(values) + "\n"

    # ============================================================
    # STACK INPUT
    # ============================================================
    if contract_type == "stack-input":
        count = max(3, min(size, 20))

        values = [
            _generate_integer(rng)
            for _ in range(count)
        ]

        return (
            f"{count}\n"
            + " ".join(map(str, values))
            + "\n"
        )

    # ============================================================
    # QUEUE INPUT
    # ============================================================
    if contract_type == "queue-input":
        count = max(3, min(size, 20))

        values = [
            _generate_integer(rng)
            for _ in range(count)
        ]

        return (
            f"{count}\n"
            + " ".join(map(str, values))
            + "\n"
        )

    # ============================================================
    # SET INPUT
    # ============================================================
    if contract_type == "set-input":
        count = max(3, min(size, 20))

        values = set()

        while len(values) < count:
            values.add(
                _generate_integer(rng)
            )

        return (
            f"{count}\n"
            + " ".join(map(str, values))
            + "\n"
        )

    raise ValueError(
        "No contract generator is currently "
        f"implemented for '{contract_type}'."
    )

# ============================================================
# WORKLOAD REGISTRY
# ============================================================

WORKLOAD_REGISTRY = {}


def register_workload(
    workload_type: str,
    generator,
):
    """
    Register a workload generator.

    The registry is intentionally extensible so new workload
    generators can be added without changing generate_workload().
    """

    if not workload_type:
        raise ValueError(
            "Workload type cannot be empty."
        )

    if not callable(generator):
        raise TypeError(
            f"Generator for '{workload_type}' must be callable."
        )

    WORKLOAD_REGISTRY[workload_type] = generator

# ============================================================
# MAIN WORKLOAD GENERATOR
# ============================================================

def generate_workload(
    workload_type: str,
    input_size: int,
    seed: int = 42,
) -> str:
    """
    Generate deterministic input for a custom benchmark.

    The same generated workload is returned for every target
    implementation participating in the comparison.
    """

    if input_size <= 0:
        raise ValueError(
            "Input size must be greater than 0."
        )

    workload_type = (
        workload_type
        .lower()
        .strip()
    )

    generator = WORKLOAD_REGISTRY.get(
        workload_type
    )

    if generator is None:
        raise ValueError(
            "Unsupported workload type: "
            f"{workload_type}. "
            "Supported types: "
            + ", ".join(
                get_supported_workload_types()
            )
        )

    random.seed(seed)

    return generator(input_size)


# ============================================================
# NUMERIC ARRAY
# ============================================================

def generate_numeric_array(
    input_size: int,
) -> str:
    """
    Existing Array Sum compatible workload.

    Format:

    n
    value1 value2 value3 ...

    Example:

    5
    10 20 30 40 50
    """

    data = [
        random.randint(
            0,
            1_000_000
        )
        for _ in range(input_size)
    ]

    return (
        f"{input_size}\n"
        + " ".join(
            map(str, data)
        )
        + "\n"
    )


# ============================================================
# TEXT
# ============================================================

def generate_text(
    input_size: int,
) -> str:
    """
    Generate deterministic plain-text workload.

    Format:

    n
    word1 word2 word3 ...

    Useful for:
    - string processing
    - searching
    - counting
    - tokenization
    """

    words = []

    alphabet = string.ascii_lowercase

    for _ in range(input_size):

        length = random.randint(
            5,
            12
        )

        word = "".join(
            random.choice(alphabet)
            for _ in range(length)
        )

        words.append(word)

    return (
        f"{input_size}\n"
        + " ".join(words)
        + "\n"
    )


# ============================================================
# URL
# ============================================================

def generate_urls(
    input_size: int,
) -> str:
    """
    Generate deterministic URL strings.

    This is a URL-processing workload only.
    It does NOT perform HTTP requests.
    """

    urls = []

    for index in range(
        input_size
    ):

        urls.append(
            f"https://example.com/"
            f"users/{index}"
            f"?page={index % 10}"
        )

    return (
        f"{input_size}\n"
        + "\n".join(urls)
        + "\n"
    )


# ============================================================
# HTML
# ============================================================

def generate_html(
    input_size: int,
) -> str:
    """
    Generate deterministic HTML elements.

    This tests HTML/string processing.

    It does NOT make network requests
    or render the HTML in a browser.
    """

    elements = []

    for index in range(
        input_size
    ):

        elements.append(
            f"<div class=\"item\">"
            f"<h2>Product {index}</h2>"
            f"<p>Item description {index}</p>"
            f"</div>"
        )

    return (
        f"{input_size}\n"
        + "\n".join(elements)
        + "\n"
    )


# ============================================================
# JSON
# ============================================================

def generate_json(
    input_size: int,
) -> str:
    """
    Generate a JSON array containing deterministic records.

    Useful for:
    - JSON parsing
    - serialization/deserialization
    - object traversal
    """

    records = []

    for index in range(
        input_size
    ):

        records.append({
            "id": index + 1,
            "name": f"User {index + 1}",
            "active": index % 2 == 0,
            "score": random.randint(
                0,
                100
            ),
        })

    return (
        json.dumps(
            records,
            separators=(
                ",",
                ":"
            )
        )
        + "\n"
    )


# ============================================================
# CSV
# ============================================================

def generate_csv(
    input_size: int,
) -> str:
    """
    Generate deterministic CSV data.

    Format:

    id,name,score,active
    1,User 1,80,true
    ...
    """

    output = io.StringIO()

    writer = csv.writer(
        output,
        lineterminator="\n"
    )

    writer.writerow([
        "id",
        "name",
        "score",
        "active",
    ])

    for index in range(
        input_size
    ):

        writer.writerow([
            index + 1,
            f"User {index + 1}",
            random.randint(
                0,
                100
            ),
            str(
                index % 2 == 0
            ).lower(),
        ])

    return output.getvalue()


# ============================================================
# MATRIX
# ============================================================

def generate_matrix(
    input_size: int,
) -> str:
    """
    Generate a square numeric matrix.

    Matrix dimensions:

        input_size x input_size

    Format:

    n
    row 1
    row 2
    ...
    """

    rows = []

    for _ in range(
        input_size
    ):

        row = [
            random.randint(
                0,
                100
            )
            for _ in range(
                input_size
            )
        ]

        rows.append(
            " ".join(
                map(str, row)
            )
        )

    return (
        f"{input_size}\n"
        + "\n".join(rows)
        + "\n"
    )


# ============================================================
# GRAPH
# ============================================================

def generate_graph(
    input_size: int,
) -> str:
    """
    Generate a deterministic undirected graph.

    Format:

    vertices edges
    u1 v1
    u2 v2
    ...

    The graph contains input_size vertices.

    Approximately 2 * input_size edges are generated,
    while avoiding duplicate/self edges.
    """

    vertices = input_size

    max_edges = (
        vertices
        * (vertices - 1)
        // 2
    )

    desired_edges = min(
        max_edges,
        max(
            0,
            vertices * 2
        )
    )

    edges = set()

    attempts = 0
    max_attempts = max(
        100,
        desired_edges * 10
    )

    while (
        len(edges) < desired_edges
        and attempts < max_attempts
    ):

        u = random.randint(
            1,
            vertices
        )

        v = random.randint(
            1,
            vertices
        )

        attempts += 1

        if u == v:
            continue

        edge = tuple(
            sorted(
                (u, v)
            )
        )

        edges.add(edge)

    edge_lines = [
        f"{u} {v}"
        for u, v in sorted(edges)
    ]

    return (
        f"{vertices} {len(edge_lines)}\n"
        + "\n".join(edge_lines)
        + "\n"
    )


# ============================================================
# TREE
# ============================================================

def generate_tree(
    input_size: int,
) -> str:
    """
    Generate a deterministic rooted tree.

    Format:

    n
    parent child
    parent child
    ...

    Node 1 is the root.

    Every node from 2..n has exactly one parent.
    """

    if input_size == 1:

        return (
            "1\n"
        )

    edges = []

    for child in range(
        2,
        input_size + 1
    ):

        parent = random.randint(
            1,
            child - 1
        )

        edges.append(
            f"{parent} {child}"
        )

    return (
        f"{input_size}\n"
        + "\n".join(edges)
        + "\n"
    )


# ============================================================
# MULTIPLE ARRAYS
# ============================================================

def generate_multiple_arrays(
    input_size: int,
) -> str:
    """
    Generate two deterministic numeric arrays.

    Format:

    n
    array-A
    array-B
    """

    array_a = [
        random.randint(
            0,
            1_000_000
        )
        for _ in range(input_size)
    ]

    array_b = [
        random.randint(
            0,
            1_000_000
        )
        for _ in range(input_size)
    ]

    return (
        f"{input_size}\n"
        + " ".join(
            map(str, array_a)
        )
        + "\n"
        + " ".join(
            map(str, array_b)
        )
        + "\n"
    )

# ============================================================
# REGISTER BUILT-IN WORKLOAD GENERATORS
# ============================================================

register_workload(
    "numeric-array",
    generate_numeric_array,
)

register_workload(
    "text",
    generate_text,
)

register_workload(
    "url",
    generate_urls,
)

register_workload(
    "html",
    generate_html,
)

register_workload(
    "json",
    generate_json,
)

register_workload(
    "csv",
    generate_csv,
)

register_workload(
    "matrix",
    generate_matrix,
)

register_workload(
    "graph",
    generate_graph,
)

register_workload(
    "tree",
    generate_tree,
)

register_workload(
    "multiple-arrays",
    generate_multiple_arrays,
)

# ============================================================
# INPUT CONTRACT GENERATOR COVERAGE AUDIT
# ============================================================

INPUT_CONTRACT_GENERATOR_COVERAGE = {
    "no-input": True,
    "stdin-present": False,

    "integer-scalar": True,
    "integer-scalars": True,
    "float-scalar": True,
    "float-scalars": True,
    "character-scalar": True,
    "mixed-scalars": True,

    "string-token": True,
    "string-line": True,
    "string-array": True,
    "string-lines": True,
    "scalar-plus-line": True,
    "size-plus-string": True,
    "size-plus-two-strings": True,
    "size-plus-strings": True,
    "character-stream": True,

    "integer-array": True,
    "float-array": True,
    "character-array": True,
    "jagged-array": True,
    "array-plus-target": True,
    "multiple-arrays": True,
    "array-with-queries": True,
    "array-with-range-queries": True,

    "matrix": True,
    "matrix-plus-target": True,
    "jagged-matrix": True,
    "character-grid": True,
    "adjacency-matrix": True,

    "graph": True,
    "weighted-graph": True,
    "graph-with-source": True,
    "weighted-graph-with-source": True,

    "tree": True,
    "parent-array-tree": True,
    "binary-tree-level-order": True,

    "test-cases": False,
    "test-cases-array": True,
    "test-cases-matrix": True,

    "eof-stream": True,
    "eof-records": True,
    "eof-lines": True,

    "sentinel-stream": True,
    "sentinel-records": True,

    "pair-records": True,
    "triple-records": True,
    "pairs": True,
    "triples": True,
    "tuple-records": True,
    "structured-records": True,
    "key-value-records": True,

    "query-stream": True,
    "range-queries": True,
    "command-stream": True,
    "delimited-lines": True,
    "scanf-input": True,

    "stack-input": True,
    "queue-input": True,
    "set-input": True,
}

# ============================================================
# REALISTIC CONTRACT SMOKE TEST DATA
# ============================================================

INPUT_CONTRACT_SMOKE_TESTS = {
    "integer-scalar": {
        "contract_type": "integer-scalar",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
            }
        ],
    },

    "integer-scalars": {
        "contract_type": "integer-scalars",
        "fields": [
            {
                "name": "a",
                "type": "integer",
                "source": "stdin",
            },
            {
                "name": "b",
                "type": "integer",
                "source": "stdin",
            },
        ],
    },

    "float-scalar": {
        "contract_type": "float-scalar",
        "fields": [
            {
                "name": "x",
                "type": "float",
                "source": "stdin",
            }
        ],
    },

        "float-scalars": {
        "contract_type": "float-scalars",
        "fields": [
            {
                "name": "a",
                "type": "float",
                "source": "stdin",
            },
            {
                "name": "b",
                "type": "float",
                "source": "stdin",
            },
        ],
    },

    "character-scalar": {
        "contract_type": "character-scalar",
        "fields": [
            {
                "name": "c",
                "type": "character",
                "source": "stdin",
            },
        ],
    },

    "no-input": {
        "contract_type": "no-input",
        "fields": [],
    },

    "size-plus-string": {
        "contract_type": "size-plus-string",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "s",
                "type": "string",
                "source": "stdin",
                "role": "string-data",
            },
        ],
    },

    "size-plus-two-strings": {
        "contract_type": "size-plus-two-strings",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "s1",
                "type": "string",
                "source": "stdin",
                "role": "string-1",
            },
            {
                "name": "s2",
                "type": "string",
                "source": "stdin",
                "role": "string-2",
            },
        ],
    },

    "size-plus-strings": {
        "contract_type": "size-plus-strings",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "strings",
                "type": "string-array",
                "source": "stdin",
                "role": "string-data",
            },
        ],
    },

    "character-stream": {
        "contract_type": "character-stream",
        "fields": [
            {
                "name": "characters",
                "type": "character-stream",
                "source": "stdin",
                "role": "repeated-character",
            },
        ],
    },

    "mixed-scalars": {
        "contract_type": "mixed-scalars",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
            },
            {
                "name": "x",
                "type": "double",
                "source": "stdin",
            },
            {
                "name": "c",
                "type": "character",
                "source": "stdin",
            },
        ],
    },

    "string-token": {
        "contract_type": "string-token",
        "fields": [
            {
                "name": "s",
                "type": "string",
                "source": "stdin",
            }
        ],
    },

    "string-line": {
        "contract_type": "string-line",
        "fields": [
            {
                "name": "line",
                "type": "string",
                "source": "stdin",
            }
        ],
    },

    "string-array": {
        "contract_type": "string-array",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "values",
                "type": "string-array",
                "source": "stdin",
                "role": "array-data",
            },
        ],
    },

    "string-lines": {
        "contract_type": "string-lines",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "lines",
                "type": "string-array",
                "source": "stdin",
                "role": "line-data",
            },
        ],
    },

    "scalar-plus-line": {
        "contract_type": "scalar-plus-line",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
            },
            {
                "name": "line",
                "type": "string",
                "source": "stdin",
            },
        ],
    },

    "integer-array": {
        "contract_type": "integer-array",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "a",
                "type": "integer-array",
                "source": "stdin",
                "role": "array-data",
            },
        ],
    },

    "float-array": {
        "contract_type": "float-array",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "a",
                "type": "float-array",
                "source": "stdin",
                "role": "array-data",
            },
        ],
    },

    "character-array": {
        "contract_type": "character-array",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "a",
                "type": "character-array",
                "source": "stdin",
                "role": "array-data",
            },
        ],
    },

    "jagged-array": {
        "contract_type": "jagged-array",
        "fields": [],
    },

    "array-plus-target": {
        "contract_type": "array-plus-target",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
                "role": "size",
            },
            {
                "name": "a",
                "type": "integer-array",
                "source": "stdin",
                "role": "array-data",
            },
            {
                "name": "target",
                "type": "integer",
                "source": "stdin",
                "role": "target",
            },
        ],
    },

    "multiple-arrays": {
        "contract_type": "multiple-arrays",
        "fields": [],
    },

    "array-with-queries": {
        "contract_type": "array-with-queries",
        "fields": [],
    },

    "array-with-range-queries": {
        "contract_type": "array-with-range-queries",
        "fields": [],
    },

    "matrix": {
        "contract_type": "matrix",
        "fields": [],
    },

    "matrix-plus-target": {
        "contract_type": "matrix-plus-target",
        "fields": [],
    },

    "jagged-matrix": {
        "contract_type": "jagged-matrix",
        "fields": [],
    },

    "character-grid": {
        "contract_type": "character-grid",
        "fields": [],
    },

    "adjacency-matrix": {
        "contract_type": "adjacency-matrix",
        "fields": [],
    },

    "graph": {
        "contract_type": "graph",
        "fields": [],
    },

    "weighted-graph": {
        "contract_type": "weighted-graph",
        "fields": [],
    },

    "graph-with-source": {
        "contract_type": "graph-with-source",
        "fields": [],
    },

    "weighted-graph-with-source": {
        "contract_type": "weighted-graph-with-source",
        "fields": [],
    },

    "tree": {
        "contract_type": "tree",
        "fields": [],
    },

    "parent-array-tree": {
        "contract_type": "parent-array-tree",
        "fields": [],
    },

    "binary-tree-level-order": {
        "contract_type": "binary-tree-level-order",
        "fields": [],
    },

    "test-cases-array": {
        "contract_type": "test-cases-array",
        "fields": [],
    },

    "test-cases-matrix": {
        "contract_type": "test-cases-matrix",
        "fields": [],
    },

    "eof-stream": {
        "contract_type": "eof-stream",
        "fields": [
            {
                "name": "x",
                "type": "integer",
                "source": "stdin",
                "role": "repeated-until-eof",
            }
        ],
    },

    "eof-records": {
        "contract_type": "eof-records",
        "fields": [
            {
                "name": "a",
                "type": "integer",
                "source": "stdin",
                "role": "field-1",
            },
            {
                "name": "b",
                "type": "integer",
                "source": "stdin",
                "role": "field-2",
            },
        ],
    },

    "eof-lines": {
        "contract_type": "eof-lines",
        "fields": [
            {
                "name": "line",
                "type": "string",
                "source": "stdin",
                "role": "line-until-eof",
            }
        ],
    },

    "sentinel-stream": {
        "contract_type": "sentinel-stream",
        "fields": [
            {
                "name": "x",
                "type": "integer",
                "source": "stdin",
                "role": "repeated-value",
            },
            {
                "name": "sentinel",
                "type": "literal",
                "value": "-1",
                "source": "stdin",
                "role": "terminator",
            },
        ],
    },

    "sentinel-records": {
        "contract_type": "sentinel-records",
        "fields": [
            {
                "name": "a",
                "type": "integer",
                "source": "stdin",
                "role": "field-1",
            },
            {
                "name": "b",
                "type": "integer",
                "source": "stdin",
                "role": "field-2",
            },
            {
                "name": "sentinel",
                "type": "literal",
                "value": "-1",
                "source": "stdin",
                "role": "terminator",
            },
        ],
    },

    "pairs": {
        "contract_type": "pairs",
        "fields": [],
    },

    "pair-records": {
        "contract_type": "pair-records",
        "fields": [],
    },

    "triples": {
        "contract_type": "triples",
        "fields": [],
    },

    "triple-records": {
        "contract_type": "triple-records",
        "fields": [],
    },

    "tuple-records": {
        "contract_type": "tuple-records",
        "fields": [
            {
                "name": "a",
                "type": "integer",
                "source": "stdin",
            },
            {
                "name": "b",
                "type": "string",
                "source": "stdin",
            },
        ],
    },

    "structured-records": {
        "contract_type": "structured-records",
        "fields": [
            {
                "name": "id",
                "type": "integer",
                "source": "stdin",
            },
            {
                "name": "name",
                "type": "string",
                "source": "stdin",
            },
            {
                "name": "score",
                "type": "double",
                "source": "stdin",
            },
        ],
    },

    "key-value-records": {
        "contract_type": "key-value-records",
        "fields": [
            {
                "name": "key",
                "type": "string",
                "source": "stdin",
            },
            {
                "name": "value",
                "type": "integer",
                "source": "stdin",
            },
        ],
    },

    "query-stream": {
        "contract_type": "query-stream",
        "fields": [],
    },

    "range-queries": {
        "contract_type": "range-queries",
        "fields": [],
    },

    "command-stream": {
        "contract_type": "command-stream",
        "fields": [],
    },

    "delimited-lines": {
        "contract_type": "delimited-lines",
        "fields": [],
    },

    "scanf-input": {
        "contract_type": "scanf-input",
        "fields": [
            {
                "name": "n",
                "type": "integer",
                "source": "stdin",
            },
            {
                "name": "x",
                "type": "double",
                "source": "stdin",
            },
        ],
    },

    "stack-input": {
        "contract_type": "stack-input",
        "fields": [],
    },

    "queue-input": {
        "contract_type": "queue-input",
        "fields": [],
    },

    "set-input": {
        "contract_type": "set-input",
        "fields": [],
    },
}

def audit_input_contract_generators() -> dict[str, Any]:
    """
    Perform a strict generator coverage and determinism audit.

    The audit distinguishes:
    - intentionally unsupported fallback contracts
    - missing generator branches
    - runtime failures
    - nondeterministic generation
    """

    intentionally_unsupported = {
        "stdin-present",
        "test-cases",
    }

    missing = []
    runtime_failures = []
    nondeterministic = []

    for contract_type, expected_supported in (
        INPUT_CONTRACT_GENERATOR_COVERAGE.items()
    ):
        if contract_type in intentionally_unsupported:
            continue

        if not expected_supported:
            continue

        contract = INPUT_CONTRACT_SMOKE_TESTS.get(
            contract_type
        )

        if contract is None:
            missing.append(contract_type)
            continue

        try:
            first = generate_from_input_contract(
                contract,
                input_size=10,
                seed=42,
            )

            second = generate_from_input_contract(
                contract,
                input_size=10,
                seed=42,
            )

            if not isinstance(first, str):
                runtime_failures.append(
                    {
                        "contract_type": contract_type,
                        "reason": (
                            "Generator did not return str."
                        ),
                    }
                )
                continue

            if first != second:
                nondeterministic.append(
                    contract_type
                )

        except Exception as exc:
            runtime_failures.append(
                {
                    "contract_type": contract_type,
                    "reason": str(exc),
                }
            )

    supported_contracts = [
        contract_type
        for contract_type, supported
        in INPUT_CONTRACT_GENERATOR_COVERAGE.items()
        if supported
    ]

    return {
        "total_contracts": len(
            INPUT_CONTRACT_GENERATOR_COVERAGE
        ),
        "generator_supported": len(
            supported_contracts
        ),
        "intentionally_unsupported": sorted(
            intentionally_unsupported
        ),
        "missing": sorted(missing),
        "runtime_failures": runtime_failures,
        "nondeterministic": sorted(
            nondeterministic
        ),
        "passed": (
            not missing
            and not runtime_failures
            and not nondeterministic
        ),
    }


    # ============================================================
# INPUT CONTRACT SEMANTIC VALIDATION
# ============================================================


def _is_integer_token(value: str) -> bool:
    try:
        int(value)
        return True
    except (TypeError, ValueError):
        return False


def _is_float_token(value: str) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _is_character_token(value: str) -> bool:
    return len(value) == 1


def _tokens_from_line(line: str) -> list[str]:
    return line.strip().split()


def _validate_typed_token(
    token: str,
    field_type: str,
) -> bool:
    normalized = (
        str(field_type or "string")
        .strip()
        .lower()
    )

    if normalized in {
        "integer",
        "int",
        "long",
        "long-long",
        "number",
    }:
        return _is_integer_token(token)

    if normalized in {
        "float",
        "double",
        "decimal",
    }:
        return _is_float_token(token)

    if normalized in {
        "character",
        "char",
    }:
        return _is_character_token(token)

    if normalized in {
        "boolean",
        "bool",
    }:
        return token.lower() in {
            "true",
            "false",
            "0",
            "1",
        }

    return isinstance(token, str)


def validate_generated_input_against_contract(
    input_contract: dict[str, Any],
    generated_input: str,
) -> dict[str, Any]:
    """
    Independently validate generated stdin against the
    declared Input Contract.

    This validator intentionally does NOT call the generator
    and does not recreate generation logic.

    It verifies:
    - contract structure
    - line/token counts
    - declared scalar types
    - array sizes
    - matrix dimensions
    - graph record shapes
    - tree record shapes
    - sentinel termination
    - record field counts
    - query structures
    """
    contract_type = (
        str(
            input_contract.get(
                "contract_type",
                "",
            )
        )
        .strip()
        .lower()
    )

    fields = input_contract.get(
        "fields",
        [],
    )

    if not isinstance(generated_input, str):
        return {
            "valid": False,
            "contract_type": contract_type,
            "errors": [
                "Generated input must be a string."
            ],
            "observations": [],
        }

    errors: list[str] = []
    observations: list[str] = []

    raw_lines = generated_input.splitlines()
    non_empty_lines = [
        line for line in raw_lines
        if line.strip()
    ]

    def fail(message: str) -> None:
        errors.append(message)

    def require_line_count_at_least(
        minimum: int,
    ) -> bool:
        if len(non_empty_lines) < minimum:
            fail(
                f"Expected at least {minimum} "
                f"non-empty lines, received "
                f"{len(non_empty_lines)}."
            )
            return False
        return True

    def require_token_count(
        tokens: list[str],
        expected: int,
        context: str,
    ) -> bool:
        if len(tokens) != expected:
            fail(
                f"{context}: expected {expected} "
                f"tokens, received {len(tokens)}."
            )
            return False
        return True

    def require_integer(
        token: str,
        context: str,
    ) -> bool:
        if not _is_integer_token(token):
            fail(
                f"{context}: expected integer, "
                f"received '{token}'."
            )
            return False
        return True

    def require_float(
        token: str,
        context: str,
    ) -> bool:
        if not _is_float_token(token):
            fail(
                f"{context}: expected floating-point "
                f"value, received '{token}'."
            )
            return False
        return True

    def require_type(
        token: str,
        field_type: str,
        context: str,
    ) -> bool:
        if not _validate_typed_token(
            token,
            field_type,
        ):
            fail(
                f"{context}: token '{token}' does not "
                f"match type '{field_type}'."
            )
            return False
        return True

    # --------------------------------------------------------
    # NO INPUT
    # --------------------------------------------------------

    if contract_type == "no-input":
        if generated_input.strip():
            fail(
                "Contract expects no stdin input, "
                "but generated input is non-empty."
            )
        else:
            observations.append(
                "No-input contract correctly produced empty stdin."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # INTEGER / FLOAT / CHARACTER SCALARS
    # --------------------------------------------------------

    if contract_type in {
        "integer-scalar",
        "float-scalar",
        "character-scalar",
    }:
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            tokens,
            1,
            contract_type,
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        token = tokens[0]

        if contract_type == "integer-scalar":
            require_integer(
                token,
                "integer-scalar",
            )

        elif contract_type == "float-scalar":
            require_float(
                token,
                "float-scalar",
            )

        else:
            if not _is_character_token(token):
                fail(
                    "character-scalar: expected "
                    "exactly one character."
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # MULTIPLE SCALARS
    # --------------------------------------------------------

    if contract_type in {
        "integer-scalars",
        "float-scalars",
        "mixed-scalars",
    }:
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        expected_fields = len(fields)

        if expected_fields == 0:
            fail(
                f"{contract_type}: contract declares "
                "no scalar fields."
            )
        else:
            require_token_count(
                tokens,
                expected_fields,
                contract_type,
            )

            for index, field in enumerate(fields):
                if index >= len(tokens):
                    break

                field_type = _contract_value_type(
                    field
                )

                require_type(
                    tokens[index],
                    field_type,
                    f"{contract_type} field {index + 1}",
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # SINGLE / LINE STRINGS
    # --------------------------------------------------------

    if contract_type in {
        "string-token",
        "string-line",
    }:
            if not require_line_count_at_least(1):
                return {
                    "valid": False,
                    "contract_type": contract_type,
                    "errors": errors,
                    "observations": observations,
                }

            if contract_type == "string-token":
                tokens = _tokens_from_line(
                    non_empty_lines[0]
                )

                require_token_count(
                    tokens,
                    1,
                    "string-token",
                )

            else:
                if not non_empty_lines[0].strip():
                    fail(
                        "string-line: generated line "
                        "must not be empty."
                    )

            return {
                "valid": not errors,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

            # --------------------------------------------------------
        # STRING ARRAY / STRING LINES
        # --------------------------------------------------------

    if contract_type in {
        "string-array",
        "string-lines",
    }:
            if not require_line_count_at_least(2):
                return {
                    "valid": False,
                    "contract_type": contract_type,
                    "errors": errors,
                    "observations": observations,
                }

            size_tokens = _tokens_from_line(
                non_empty_lines[0]
            )

            if not require_token_count(
                size_tokens,
                1,
                f"{contract_type} size",
            ):
                return {
                    "valid": False,
                    "contract_type": contract_type,
                    "errors": errors,
                    "observations": observations,
                }

            if not require_integer(
                size_tokens[0],
                f"{contract_type} size",
            ):
                return {
                    "valid": False,
                    "contract_type": contract_type,
                    "errors": errors,
                    "observations": observations,
                }

            size_value = int(size_tokens[0])

            if size_value < 1:
                fail(
                    f"{contract_type}: size must be "
                    "greater than zero."
                )

            if contract_type == "string-array":
                if len(non_empty_lines) != 2:
                    fail(
                        "string-array: expected exactly "
                        "2 non-empty lines."
                    )
                else:
                    values = _tokens_from_line(
                        non_empty_lines[1]
                    )

                    require_token_count(
                        values,
                        size_value,
                        "string-array data",
                    )

                    for index, value in enumerate(
                        values,
                        start=1,
                    ):
                        if not value:
                            fail(
                                f"string-array element {index}: "
                                "empty string."
                            )

            else:
                expected_lines = size_value + 1

                if len(non_empty_lines) != expected_lines:
                    fail(
                        "string-lines: expected "
                        f"{expected_lines} non-empty lines "
                        f"based on size={size_value}, "
                        f"received {len(non_empty_lines)}."
                    )

                for index, line in enumerate(
                    non_empty_lines[1:],
                    start=1,
                ):
                    if not line.strip():
                        fail(
                            f"string-lines element {index}: "
                            "empty string line."
                        )

            return {
                "valid": not errors,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

    # --------------------------------------------------------
    # SCALAR + LINE
    # --------------------------------------------------------

    if contract_type == "scalar-plus-line":
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        first_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        require_token_count(
            first_tokens,
            1,
            "scalar-plus-line scalar",
        )

        require_integer(
            first_tokens[0],
            "scalar-plus-line scalar",
        )

        if not non_empty_lines[1].strip():
            fail(
                "scalar-plus-line: second line "
                "must contain text."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # SIZE + STRING
    # --------------------------------------------------------

    if contract_type in {
        "size-plus-string",
        "size-plus-two-strings",
        "size-plus-strings",
    }:
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        size_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            size_tokens,
            1,
            f"{contract_type} size",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        if not require_integer(
            size_tokens[0],
            f"{contract_type} size",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        size_value = int(size_tokens[0])

        if size_value < 1:
            fail(
                f"{contract_type}: size must be "
                "greater than zero."
            )

        if contract_type == "size-plus-string":
            if len(non_empty_lines) != 2:
                fail(
                    "size-plus-string: expected "
                    "exactly 2 non-empty lines."
                )
            elif not non_empty_lines[1].strip():
                fail(
                    "size-plus-string: string must "
                    "not be empty."
                )

        elif contract_type == "size-plus-two-strings":
            if len(non_empty_lines) != 3:
                fail(
                    "size-plus-two-strings: expected "
                    "exactly 3 non-empty lines."
                )
            else:
                if not non_empty_lines[1].strip():
                    fail(
                        "size-plus-two-strings: "
                        "first string is empty."
                    )
                if not non_empty_lines[2].strip():
                    fail(
                        "size-plus-two-strings: "
                        "second string is empty."
                    )

        else:
            expected_lines = size_value + 1

            if len(non_empty_lines) != expected_lines:
                fail(
                    "size-plus-strings: expected "
                    f"{expected_lines} non-empty lines "
                    f"based on size={size_value}, "
                    f"received {len(non_empty_lines)}."
                )

            for index, line in enumerate(
                non_empty_lines[1:],
                start=1,
            ):
                if not line.strip():
                    fail(
                        f"size-plus-strings: string "
                        f"{index} is empty."
                    )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # CHARACTER STREAM
    # --------------------------------------------------------

    if contract_type == "character-stream":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        value = raw_lines[0] if raw_lines else ""

        if not value:
            fail(
                "character-stream: stream is empty."
            )

        if any(character.isspace() for character in value):
            fail(
                "character-stream: whitespace is not allowed "
                "inside the generated character stream."
            )
        for index, character in enumerate(
            value,
            start=1,
        ):
            if not _is_character_token(character):
                fail(
                    f"character-stream: invalid "
                    f"character at position {index}."
                )
                break

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # ARRAY-LIKE CONTRACTS
    # --------------------------------------------------------

    if contract_type in {
        "integer-array",
        "float-array",
        "character-array",
    }:
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        size_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            size_tokens,
            1,
            f"{contract_type} size",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        if not require_integer(
            size_tokens[0],
            f"{contract_type} size",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        size_value = int(size_tokens[0])

        if size_value < 1:
            fail(
                f"{contract_type}: size must "
                "be greater than zero."
            )

        values = _tokens_from_line(
            non_empty_lines[1]
        )

        if not require_token_count(
            values,
            size_value,
            f"{contract_type} data",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        for index, token in enumerate(
            values,
            start=1,
        ):
            if contract_type == "integer-array":
                require_integer(
                    token,
                    f"{contract_type} element {index}",
                )
            elif contract_type == "float-array":
                require_float(
                    token,
                    f"{contract_type} element {index}",
                )
            else:
                if not _is_character_token(token):
                    fail(
                        f"{contract_type} element {index}: "
                        "expected one character."
                    )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # MULTIPLE ARRAYS
    # --------------------------------------------------------

    if contract_type == "multiple-arrays":
        if not require_line_count_at_least(3):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        size_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            size_tokens,
            1,
            "multiple-arrays size",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            size_tokens[0],
            "multiple-arrays size",
        )

        size_value = int(
            size_tokens[0]
        )

        for array_index in (1, 2):
            values = _tokens_from_line(
                non_empty_lines[array_index]
            )

            require_token_count(
                values,
                size_value,
                f"multiple-arrays array {array_index}",
            )

            for element_index, token in enumerate(
                values,
                start=1,
            ):
                require_integer(
                    token,
                    (
                        f"multiple-arrays "
                        f"array {array_index} "
                        f"element {element_index}"
                    ),
                )

        if len(non_empty_lines) != 3:
            fail(
                "multiple-arrays: expected exactly "
                "3 non-empty lines."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # ARRAY + TARGET
    # --------------------------------------------------------

    if contract_type == "array-plus-target":
        if not require_line_count_at_least(3):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        size_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            size_tokens,
            1,
            "array-plus-target size",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            size_tokens[0],
            "array-plus-target size",
        )

        size_value = int(
            size_tokens[0]
        )

        values = _tokens_from_line(
            non_empty_lines[1]
        )

        require_token_count(
            values,
            size_value,
            "array-plus-target array",
        )

        for index, token in enumerate(
            values,
            start=1,
        ):
            require_integer(
                token,
                f"array-plus-target element {index}",
            )

        target_tokens = _tokens_from_line(
            non_empty_lines[2]
        )

        require_token_count(
            target_tokens,
            1,
            "array-plus-target target",
        )

        require_integer(
            target_tokens[0],
            "array-plus-target target",
        )

        if len(non_empty_lines) != 3:
            fail(
                "array-plus-target: expected exactly "
                "3 non-empty lines."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # JAGGED ARRAY
    # --------------------------------------------------------

    if contract_type == "jagged-array":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        row_count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            row_count_tokens,
            1,
            "jagged-array row count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            row_count_tokens[0],
            "jagged-array row count",
        )

        row_count = int(
            row_count_tokens[0]
        )

        expected_lines = 1 + (row_count * 2)

        if len(non_empty_lines) != expected_lines:
            fail(
                "jagged-array: expected "
                f"{expected_lines} non-empty lines, "
                f"received {len(non_empty_lines)}."
            )

        cursor = 1

        for row_index in range(row_count):
            if cursor >= len(non_empty_lines):
                break

            row_size_tokens = _tokens_from_line(
                non_empty_lines[cursor]
            )
            cursor += 1

            if not require_token_count(
                row_size_tokens,
                1,
                f"jagged-array row {row_index + 1} size",
            ):
                break

            if not _is_integer_token(
                row_size_tokens[0]
            ):
                fail(
                    f"jagged-array row {row_index + 1}: "
                    "row size must be integer."
                )
                break

            row_size = int(
                row_size_tokens[0]
            )

            if cursor >= len(non_empty_lines):
                fail(
                    f"jagged-array row {row_index + 1}: "
                    "missing data row."
                )
                break

            values = _tokens_from_line(
                non_empty_lines[cursor]
            )
            cursor += 1

            require_token_count(
                values,
                row_size,
                (
                    f"jagged-array row "
                    f"{row_index + 1} data"
                ),
            )

            for element_index, token in enumerate(
                values,
                start=1,
            ):
                require_integer(
                    token,
                    (
                        f"jagged-array row "
                        f"{row_index + 1} "
                        f"element {element_index}"
                    ),
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # MATRICES
    # --------------------------------------------------------

    if contract_type in {
        "matrix",
        "matrix-plus-target",
    }:
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        dimension_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            dimension_tokens,
            2,
            f"{contract_type} dimensions",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        rows_valid = require_integer(
            dimension_tokens[0],
            f"{contract_type} rows",
        )

        cols_valid = require_integer(
            dimension_tokens[1],
            f"{contract_type} cols",
        )

        if not rows_valid or not cols_valid:
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        rows = int(
            dimension_tokens[0]
        )
        cols = int(
            dimension_tokens[1]
        )

        expected_lines = rows + 1
        if contract_type == "matrix-plus-target":
            expected_lines += 1

        if len(non_empty_lines) != expected_lines:
            fail(
                f"{contract_type}: expected "
                f"{expected_lines} non-empty lines, "
                f"received {len(non_empty_lines)}."
            )

        for row_index in range(rows):
            line_index = row_index + 1

            if line_index >= len(non_empty_lines):
                break

            values = _tokens_from_line(
                non_empty_lines[line_index]
            )

            require_token_count(
                values,
                cols,
                f"{contract_type} row {row_index + 1}",
            )

            for column_index, token in enumerate(
                values,
                start=1,
            ):
                require_integer(
                    token,
                    (
                        f"{contract_type} "
                        f"row {row_index + 1} "
                        f"column {column_index}"
                    ),
                )

        if contract_type == "matrix-plus-target":
            if len(non_empty_lines) > rows + 1:
                target_tokens = _tokens_from_line(
                    non_empty_lines[rows + 1]
                )

                require_token_count(
                    target_tokens,
                    1,
                    "matrix-plus-target target",
                )

                if target_tokens:
                    require_integer(
                        target_tokens[0],
                        "matrix-plus-target target",
                    )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # CHARACTER GRID
    # --------------------------------------------------------

    if contract_type == "character-grid":
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        dimensions = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            dimensions,
            2,
            "character-grid dimensions",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            dimensions[0],
            "character-grid rows",
        )
        require_integer(
            dimensions[1],
            "character-grid cols",
        )

        rows = int(dimensions[0])
        cols = int(dimensions[1])

        if len(non_empty_lines) != rows + 1:
            fail(
                "character-grid: expected "
                f"{rows + 1} non-empty lines."
            )

        for row_index in range(rows):
            line_index = row_index + 1

            if line_index >= len(non_empty_lines):
                break

            value = non_empty_lines[line_index].strip()

            if len(value) != cols:
                fail(
                    f"character-grid row {row_index + 1}: "
                    f"expected {cols} characters, "
                    f"received {len(value)}."
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # JAGGED MATRIX
    # --------------------------------------------------------

    if contract_type == "jagged-matrix":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        row_count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            row_count_tokens,
            1,
            "jagged-matrix row count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            row_count_tokens[0],
            "jagged-matrix row count",
        )

        row_count = int(
            row_count_tokens[0]
        )

        expected_lines = 1 + row_count * 2

        if len(non_empty_lines) != expected_lines:
            fail(
                "jagged-matrix: expected "
                f"{expected_lines} non-empty lines, "
                f"received {len(non_empty_lines)}."
            )

        cursor = 1

        for row_index in range(row_count):
            if cursor >= len(non_empty_lines):
                break

            cols_tokens = _tokens_from_line(
                non_empty_lines[cursor]
            )
            cursor += 1

            if not require_token_count(
                cols_tokens,
                1,
                f"jagged-matrix row {row_index + 1} size",
            ):
                break

            require_integer(
                cols_tokens[0],
                f"jagged-matrix row {row_index + 1} size",
            )

            cols = int(
                cols_tokens[0]
            )

            if cursor >= len(non_empty_lines):
                fail(
                    f"jagged-matrix row {row_index + 1}: "
                    "missing data row."
                )
                break

            values = _tokens_from_line(
                non_empty_lines[cursor]
            )
            cursor += 1

            require_token_count(
                values,
                cols,
                (
                    f"jagged-matrix row "
                    f"{row_index + 1} data"
                ),
            )

            for column_index, token in enumerate(
                values,
                start=1,
            ):
                require_integer(
                    token,
                    (
                        f"jagged-matrix row "
                        f"{row_index + 1} "
                        f"column {column_index}"
                    ),
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # ADJACENCY MATRIX
    # --------------------------------------------------------

    if contract_type == "adjacency-matrix":
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        dimension_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            dimension_tokens,
            1,
            "adjacency-matrix vertex count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            dimension_tokens[0],
            "adjacency-matrix vertex count",
        )

        vertices = int(
            dimension_tokens[0]
        )

        if len(non_empty_lines) != vertices + 1:
            fail(
                "adjacency-matrix: expected "
                f"{vertices + 1} non-empty lines."
            )

        for row_index in range(vertices):
            line_index = row_index + 1

            if line_index >= len(non_empty_lines):
                break

            values = _tokens_from_line(
                non_empty_lines[line_index]
            )

            require_token_count(
                values,
                vertices,
                f"adjacency-matrix row {row_index + 1}",
            )

            for column_index, token in enumerate(
                values,
                start=1,
            ):
                if not _is_integer_token(token):
                    fail(
                        f"adjacency-matrix row "
                        f"{row_index + 1} column "
                        f"{column_index}: expected integer."
                    )
                    continue

                if int(token) not in {0, 1}:
                    fail(
                        f"adjacency-matrix row "
                        f"{row_index + 1} column "
                        f"{column_index}: expected "
                        "0 or 1."
                    )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # GRAPH CONTRACTS
    # --------------------------------------------------------

    if contract_type in {
        "graph",
        "weighted-graph",
        "graph-with-source",
        "weighted-graph-with-source",
    }:
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        header = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            header,
            2,
            f"{contract_type} header",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            header[0],
            f"{contract_type} vertex count",
        )
        require_integer(
            header[1],
            f"{contract_type} edge count",
        )

        vertices = int(header[0])
        edges = int(header[1])

        weighted = contract_type in {
            "weighted-graph",
            "weighted-graph-with-source",
        }

        expected_edge_tokens = 3 if weighted else 2

        expected_lines = 1 + edges

        if contract_type in {
            "graph-with-source",
            "weighted-graph-with-source",
        }:
            expected_lines += 1

        if len(non_empty_lines) != expected_lines:
            fail(
                f"{contract_type}: expected "
                f"{expected_lines} non-empty lines, "
                f"received {len(non_empty_lines)}."
            )

        for edge_index in range(edges):
            line_index = edge_index + 1

            if line_index >= len(non_empty_lines):
                break

            edge = _tokens_from_line(
                non_empty_lines[line_index]
            )

            if not require_token_count(
                edge,
                expected_edge_tokens,
                f"{contract_type} edge {edge_index + 1}",
            ):
                continue

            require_integer(
                edge[0],
                (
                    f"{contract_type} edge "
                    f"{edge_index + 1} source"
                ),
            )

            require_integer(
                edge[1],
                (
                    f"{contract_type} edge "
                    f"{edge_index + 1} destination"
                ),
            )

            if (
                _is_integer_token(edge[0])
                and _is_integer_token(edge[1])
            ):
                source = int(edge[0])
                destination = int(edge[1])

                if not 1 <= source <= vertices:
                    fail(
                        f"{contract_type} edge "
                        f"{edge_index + 1}: source "
                        f"{source} is outside vertex range."
                    )

                if not 1 <= destination <= vertices:
                    fail(
                        f"{contract_type} edge "
                        f"{edge_index + 1}: destination "
                        f"{destination} is outside vertex range."
                    )

                if source == destination:
                    fail(
                        f"{contract_type} edge "
                        f"{edge_index + 1}: self-loop detected."
                    )

            if weighted:
                require_integer(
                    edge[2],
                    (
                        f"{contract_type} edge "
                        f"{edge_index + 1} weight"
                    ),
                )

        if contract_type in {
            "graph-with-source",
            "weighted-graph-with-source",
        }:
            source_index = 1 + edges

            if source_index < len(non_empty_lines):
                source_tokens = _tokens_from_line(
                    non_empty_lines[source_index]
                )

                if require_token_count(
                    source_tokens,
                    1,
                    f"{contract_type} source",
                ):
                    require_integer(
                        source_tokens[0],
                        f"{contract_type} source",
                    )

                    if _is_integer_token(
                        source_tokens[0]
                    ):
                        source = int(
                            source_tokens[0]
                        )

                        if not 1 <= source <= vertices:
                            fail(
                                f"{contract_type}: source "
                                f"{source} is outside "
                                "vertex range."
                            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # TREE
    # --------------------------------------------------------

    if contract_type == "tree":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        node_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            node_tokens,
            1,
            "tree node count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            node_tokens[0],
            "tree node count",
        )

        nodes = int(
            node_tokens[0]
        )

        expected_edges = max(
            0,
            nodes - 1,
        )

        if len(non_empty_lines) != expected_edges + 1:
            fail(
                "tree: expected "
                f"{expected_edges + 1} non-empty lines, "
                f"received {len(non_empty_lines)}."
            )

        seen_children: set[int] = set()

        for edge_index in range(expected_edges):
            line_index = edge_index + 1

            if line_index >= len(non_empty_lines):
                break

            edge = _tokens_from_line(
                non_empty_lines[line_index]
            )

            if not require_token_count(
                edge,
                2,
                f"tree edge {edge_index + 1}",
            ):
                continue

            require_integer(
                edge[0],
                f"tree edge {edge_index + 1} parent",
            )
            require_integer(
                edge[1],
                f"tree edge {edge_index + 1} child",
            )

            if (
                _is_integer_token(edge[0])
                and _is_integer_token(edge[1])
            ):
                parent = int(edge[0])
                child = int(edge[1])

                if not 1 <= parent <= nodes:
                    fail(
                        f"tree edge {edge_index + 1}: "
                        "parent outside node range."
                    )

                if not 1 <= child <= nodes:
                    fail(
                        f"tree edge {edge_index + 1}: "
                        "child outside node range."
                    )

                if child == 1:
                    fail(
                        "tree: root node 1 must not "
                        "appear as a child."
                    )

                if child in seen_children:
                    fail(
                        f"tree: node {child} has "
                        "multiple parents."
                    )

                seen_children.add(child)

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # PARENT ARRAY TREE
    # --------------------------------------------------------

    if contract_type == "parent-array-tree":
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        node_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            node_tokens,
            1,
            "parent-array-tree node count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            node_tokens[0],
            "parent-array-tree node count",
        )

        nodes = int(
            node_tokens[0]
        )

        parents = _tokens_from_line(
            non_empty_lines[1]
        )

        require_token_count(
            parents,
            nodes,
            "parent-array-tree parent array",
        )

        if parents:
            if parents[0] != "0":
                fail(
                    "parent-array-tree: root parent "
                    "must be 0."
                )

        for index, token in enumerate(
            parents,
            start=1,
        ):
            require_integer(
                token,
                f"parent-array-tree parent {index}",
            )

            if not _is_integer_token(token):
                continue

            parent = int(token)

            if index == 1:
                continue

            if not 1 <= parent <= nodes:
                fail(
                    f"parent-array-tree: parent "
                    f"of node {index} is outside "
                    "node range."
                )

            if parent == index:
                fail(
                    f"parent-array-tree: node {index} "
                    "cannot be its own parent."
                )

        if len(non_empty_lines) != 2:
            fail(
                "parent-array-tree: expected exactly "
                "2 non-empty lines."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # BINARY TREE LEVEL ORDER
    # --------------------------------------------------------

    if contract_type == "binary-tree-level-order":
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        slot_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            slot_tokens,
            1,
            "binary-tree-level-order slot count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            slot_tokens[0],
            "binary-tree-level-order slot count",
        )

        slots = int(
            slot_tokens[0]
        )

        values = _tokens_from_line(
            non_empty_lines[1]
        )

        require_token_count(
            values,
            slots,
            "binary-tree-level-order values",
        )

        if values and values[0] == "-1":
            fail(
                "binary-tree-level-order: root "
                "cannot be null (-1)."
            )

        for index, token in enumerate(
            values,
            start=1,
        ):
            if token != "-1":
                require_integer(
                    token,
                    (
                        "binary-tree-level-order "
                        f"slot {index}"
                    ),
                )

        if len(non_empty_lines) != 2:
            fail(
                "binary-tree-level-order: expected "
                "exactly 2 non-empty lines."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # TEST CASES - ARRAY
    # --------------------------------------------------------

    if contract_type == "test-cases-array":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        case_count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            case_count_tokens,
            1,
            "test-cases-array count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            case_count_tokens[0],
            "test-cases-array count",
        )

        case_count = int(
            case_count_tokens[0]
        )

        expected_lines = 1 + case_count * 2

        if len(non_empty_lines) != expected_lines:
            fail(
                "test-cases-array: expected "
                f"{expected_lines} non-empty lines."
            )

        cursor = 1

        for case_index in range(case_count):
            if cursor >= len(non_empty_lines):
                break

            size_tokens = _tokens_from_line(
                non_empty_lines[cursor]
            )
            cursor += 1

            if not require_token_count(
                size_tokens,
                1,
                f"test case {case_index + 1} size",
            ):
                break

            require_integer(
                size_tokens[0],
                f"test case {case_index + 1} size",
            )

            case_size = int(
                size_tokens[0]
            )

            if cursor >= len(non_empty_lines):
                break

            values = _tokens_from_line(
                non_empty_lines[cursor]
            )
            cursor += 1

            require_token_count(
                values,
                case_size,
                f"test case {case_index + 1} array",
            )

            for element_index, token in enumerate(
                values,
                start=1,
            ):
                require_integer(
                    token,
                    (
                        f"test case {case_index + 1} "
                        f"element {element_index}"
                    ),
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # TEST CASES - MATRIX
    # --------------------------------------------------------

    if contract_type == "test-cases-matrix":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            count_tokens,
            1,
            "test-cases-matrix count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            count_tokens[0],
            "test-cases-matrix count",
        )

        case_count = int(
            count_tokens[0]
        )

        cursor = 1

        for case_index in range(case_count):
            if cursor >= len(non_empty_lines):
                fail(
                    f"test case {case_index + 1}: "
                    "missing matrix dimensions."
                )
                break

            dimensions = _tokens_from_line(
                non_empty_lines[cursor]
            )
            cursor += 1

            if not require_token_count(
                dimensions,
                2,
                f"test case {case_index + 1} dimensions",
            ):
                break

            require_integer(
                dimensions[0],
                f"test case {case_index + 1} rows",
            )
            require_integer(
                dimensions[1],
                f"test case {case_index + 1} cols",
            )

            rows = int(
                dimensions[0]
            )
            cols = int(
                dimensions[1]
            )

            for row_index in range(rows):
                if cursor >= len(non_empty_lines):
                    fail(
                        f"test case {case_index + 1}: "
                        f"missing row {row_index + 1}."
                    )
                    break

                values = _tokens_from_line(
                    non_empty_lines[cursor]
                )
                cursor += 1

                require_token_count(
                    values,
                    cols,
                    (
                        f"test case {case_index + 1} "
                        f"row {row_index + 1}"
                    ),
                )

                for column_index, token in enumerate(
                    values,
                    start=1,
                ):
                    require_integer(
                        token,
                        (
                            f"test case {case_index + 1} "
                            f"row {row_index + 1} "
                            f"column {column_index}"
                        ),
                    )

        if cursor != len(non_empty_lines):
            fail(
                "test-cases-matrix: unexpected "
                "trailing input."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # EOF STREAM
    # --------------------------------------------------------

    if contract_type == "eof-stream":
        if not non_empty_lines:
            fail(
                "eof-stream: expected at least one value."
            )
        else:
            for index, line in enumerate(
                non_empty_lines,
                start=1,
            ):
                tokens = _tokens_from_line(line)

                require_token_count(
                    tokens,
                    1,
                    f"eof-stream record {index}",
                )

                if tokens:
                    require_integer(
                        tokens[0],
                        f"eof-stream record {index}",
                    )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # EOF RECORDS
    # --------------------------------------------------------

    if contract_type == "eof-records":
        if not fields:
            fail(
                "eof-records: contract contains "
                "no record fields."
            )
        else:
            expected_fields = len(fields)

            for record_index, line in enumerate(
                non_empty_lines,
                start=1,
            ):
                tokens = _tokens_from_line(line)

                require_token_count(
                    tokens,
                    expected_fields,
                    f"eof-records record {record_index}",
                )

                for index, field in enumerate(fields):
                    if index >= len(tokens):
                        break

                    require_type(
                        tokens[index],
                        _contract_value_type(field),
                        (
                            f"eof-records record "
                            f"{record_index} field {index + 1}"
                        ),
                    )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # EOF LINES
    # --------------------------------------------------------

    if contract_type == "eof-lines":
        if not non_empty_lines:
            fail(
                "eof-lines: expected at least one line."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # SENTINEL STREAM
    # --------------------------------------------------------

    if contract_type == "sentinel-stream":
        if not fields:
            fail(
                "sentinel-stream: contract contains "
                "no fields."
            )
        else:
            terminator_field = next(
                (
                    field
                    for field in fields
                    if field.get("role") == "terminator"
                ),
                None,
            )

            if terminator_field is None:
                fail(
                    "sentinel-stream: missing "
                    "terminator field."
                )
            else:
                expected_sentinel = str(
                    terminator_field.get(
                        "value",
                        "-1",
                    )
                )

                if not non_empty_lines:
                    fail(
                        "sentinel-stream: empty input."
                    )
                else:
                    final_tokens = _tokens_from_line(
                        non_empty_lines[-1]
                    )

                    if not require_token_count(
                        final_tokens,
                        1,
                        "sentinel-stream terminator",
                    ):
                        pass
                    elif final_tokens[0] != expected_sentinel:
                        fail(
                            "sentinel-stream: final token "
                            f"must be sentinel "
                            f"'{expected_sentinel}'."
                        )

                    for index, line in enumerate(
                        non_empty_lines[:-1],
                        start=1,
                    ):
                        tokens = _tokens_from_line(line)

                        require_token_count(
                            tokens,
                            1,
                            f"sentinel-stream value {index}",
                        )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # SENTINEL RECORDS
    # --------------------------------------------------------

    if contract_type == "sentinel-records":
        terminator_fields = [
            field
            for field in fields
            if field.get("role") == "terminator"
        ]

        value_fields = [
            field
            for field in fields
            if field.get("role") != "terminator"
        ]

        if not terminator_fields:
            fail(
                "sentinel-records: no terminator fields."
            )

        if not non_empty_lines:
            fail(
                "sentinel-records: empty input."
            )
        else:
            final_tokens = _tokens_from_line(
                non_empty_lines[-1]
            )

            expected_terminator = [
                str(
                    field.get(
                        "value",
                        "-1",
                    )
                )
                for field in terminator_fields
            ]

            if final_tokens != expected_terminator:
                fail(
                    "sentinel-records: final record does "
                    "not match the declared terminator."
                )

            expected_value_fields = len(
                value_fields
            )

            for record_index, line in enumerate(
                non_empty_lines[:-1],
                start=1,
            ):
                tokens = _tokens_from_line(line)

                require_token_count(
                    tokens,
                    expected_value_fields,
                    (
                        f"sentinel-records "
                        f"record {record_index}"
                    ),
                )

                for index, field in enumerate(
                    value_fields
                ):
                    if index >= len(tokens):
                        break

                    require_type(
                        tokens[index],
                        _contract_value_type(field),
                        (
                            f"sentinel-records "
                            f"record {record_index} "
                            f"field {index + 1}"
                        ),
                    )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # PAIRS / TRIPLES
    # --------------------------------------------------------

    if contract_type in {
        "pairs",
        "pair-records",
        "triples",
        "triple-records",
    }:
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            count_tokens,
            1,
            f"{contract_type} count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            count_tokens[0],
            f"{contract_type} count",
        )

        count = int(
            count_tokens[0]
        )

        expected_width = (
            2
            if contract_type in {
                "pairs",
                "pair-records",
            }
            else 3
        )

        if len(non_empty_lines) != count + 1:
            fail(
                f"{contract_type}: expected "
                f"{count + 1} non-empty lines."
            )

        for index, line in enumerate(
            non_empty_lines[1:],
            start=1,
        ):
            tokens = _tokens_from_line(line)

            require_token_count(
                tokens,
                expected_width,
                f"{contract_type} record {index}",
            )

            for field_index, token in enumerate(
                tokens,
                start=1,
            ):
                require_integer(
                    token,
                    (
                        f"{contract_type} "
                        f"record {index} "
                        f"field {field_index}"
                    ),
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # TUPLE / STRUCTURED / KEY-VALUE RECORDS
    # --------------------------------------------------------

    if contract_type in {
        "tuple-records",
        "structured-records",
        "key-value-records",
    }:
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            count_tokens,
            1,
            f"{contract_type} count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            count_tokens[0],
            f"{contract_type} count",
        )

        count = int(
            count_tokens[0]
        )

        expected_fields = len(fields)

        if expected_fields == 0:
            fail(
                f"{contract_type}: no fields declared."
            )

        if len(non_empty_lines) != count + 1:
            fail(
                f"{contract_type}: expected "
                f"{count + 1} non-empty lines."
            )

        for record_index, line in enumerate(
            non_empty_lines[1:],
            start=1,
        ):
            tokens = _tokens_from_line(line)

            require_token_count(
                tokens,
                expected_fields,
                f"{contract_type} record {record_index}",
            )

            for field_index, field in enumerate(
                fields
            ):
                if field_index >= len(tokens):
                    break

                require_type(
                    tokens[field_index],
                    _contract_value_type(field),
                    (
                        f"{contract_type} record "
                        f"{record_index} field "
                        f"{field_index + 1}"
                    ),
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # QUERY STREAM
    # --------------------------------------------------------

    if contract_type == "query-stream":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            count_tokens,
            1,
            "query-stream count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            count_tokens[0],
            "query-stream count",
        )

        count = int(
            count_tokens[0]
        )

        if len(non_empty_lines) != count + 1:
            fail(
                "query-stream: expected "
                f"{count + 1} non-empty lines."
            )

        for index, line in enumerate(
            non_empty_lines[1:],
            start=1,
        ):
            tokens = _tokens_from_line(line)

            require_token_count(
                tokens,
                1,
                f"query-stream query {index}",
            )

            if tokens:
                require_integer(
                    tokens[0],
                    f"query-stream query {index}",
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # RANGE QUERIES
    # --------------------------------------------------------

    if contract_type in {
        "range-queries",
        "array-with-queries",
        "array-with-range-queries",
    }:
        if not require_line_count_at_least(3):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        size_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            size_tokens,
            1,
            f"{contract_type} size",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            size_tokens[0],
            f"{contract_type} size",
        )

        size_value = int(
            size_tokens[0]
        )

        array_tokens = _tokens_from_line(
            non_empty_lines[1]
        )

        require_token_count(
            array_tokens,
            size_value,
            f"{contract_type} array",
        )

        for index, token in enumerate(
            array_tokens,
            start=1,
        ):
            require_integer(
                token,
                f"{contract_type} array element {index}",
            )

        query_count_tokens = _tokens_from_line(
            non_empty_lines[2]
        )

        if not require_token_count(
            query_count_tokens,
            1,
            f"{contract_type} query count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            query_count_tokens[0],
            f"{contract_type} query count",
        )

        query_count = int(
            query_count_tokens[0]
        )   

        expected_query_width = (
            2
            if contract_type == "range-queries"
            or contract_type == "array-with-range-queries"
            else 1
        )

        expected_lines = 3 + query_count

        if len(non_empty_lines) != expected_lines:
            fail(
                f"{contract_type}: expected "
                f"{expected_lines} non-empty lines."
            )

        for query_index, line in enumerate(
            non_empty_lines[3:],
            start=1,
        ):
            query_tokens = _tokens_from_line(line)

            require_token_count(
                query_tokens,
                expected_query_width,
                (
                    f"{contract_type} "
                    f"query {query_index}"
                ),
            )

            if not query_tokens:
                continue

            if (
                expected_query_width == 1
            ):
                require_integer(
                    query_tokens[0],
                    (
                        f"{contract_type} "
                        f"query {query_index} index"
                    ),
                )

                if _is_integer_token(
                    query_tokens[0]
                ):
                    index = int(
                        query_tokens[0]
                    )

                    if not 1 <= index <= size_value:
                        fail(
                            f"{contract_type} query "
                            f"{query_index}: index "
                            f"{index} outside "
                            f"1..{size_value}."
                        )

            else:
                require_integer(
                    query_tokens[0],
                    (
                        f"{contract_type} query "
                        f"{query_index} left"
                    ),
                )
                require_integer(
                    query_tokens[1],
                    (
                        f"{contract_type} query "
                        f"{query_index} right"
                    ),
                )

                if (
                    _is_integer_token(query_tokens[0])
                    and _is_integer_token(query_tokens[1])
                ):
                    left = int(
                        query_tokens[0]
                    )
                    right = int(
                        query_tokens[1]
                    )

                    if not (
                        0 <= left <= right < size_value
                    ) and not (
                        1 <= left <= right <= size_value
                    ):
                        fail(
                            f"{contract_type} query "
                            f"{query_index}: invalid "
                            "range bounds."
                        )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # COMMAND STREAM
    # --------------------------------------------------------

    if contract_type == "command-stream":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            count_tokens,
            1,
            "command-stream count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            count_tokens[0],
            "command-stream count",
        )

        count = int(
            count_tokens[0]
        )

        if len(non_empty_lines) != count + 1:
            fail(
                "command-stream: expected "
                f"{count + 1} non-empty lines."
            )

        allowed_commands = {
            "PRINT",
        }

        for index, line in enumerate(
            non_empty_lines[1:],
            start=1,
        ):
            tokens = _tokens_from_line(line)

            if not tokens:
                fail(
                    f"command-stream command "
                    f"{index}: empty command."
                )
                continue

            command = tokens[0].upper()

            if command in {
                "ADD",
                "REMOVE",
            }:
                if len(tokens) != 2:
                    fail(
                        f"command-stream command "
                        f"{index}: {command} expects "
                        "one argument."
                    )
                else:
                    require_integer(
                        tokens[1],
                        (
                            f"command-stream "
                            f"command {index} argument"
                        ),
                    )

            elif command not in allowed_commands:
                fail(
                    f"command-stream command "
                    f"{index}: unsupported command "
                    f"'{command}'."
                )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # DELIMITED LINES
    # --------------------------------------------------------

    if contract_type == "delimited-lines":
        if not non_empty_lines:
            fail(
                "delimited-lines: expected at least "
                "one record."
            )
        else:
            for index, line in enumerate(
                non_empty_lines,
                start=1,
            ):
                values = [
                    value.strip()
                    for value in line.split(",")
                ]

                require_token_count(
                    values,
                    3,
                    f"delimited-lines record {index}",
                )

                for field_index, value in enumerate(
                    values,
                    start=1,
                ):
                    require_integer(
                        value,
                        (
                            f"delimited-lines "
                            f"record {index} "
                            f"field {field_index}"
                        ),
                    )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # SCANF INPUT
    # --------------------------------------------------------

    if contract_type == "scanf-input":
        if not require_line_count_at_least(1):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        expected_fields = len(fields)

        if not require_token_count(
            tokens,
            expected_fields,
            "scanf-input",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        for index, field in enumerate(fields):
            require_type(
                tokens[index],
                _contract_value_type(field),
                f"scanf-input field {index + 1}",
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # STACK / QUEUE / SET
    # --------------------------------------------------------

    if contract_type in {
        "stack-input",
        "queue-input",
        "set-input",
    }:
        if not require_line_count_at_least(2):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        count_tokens = _tokens_from_line(
            non_empty_lines[0]
        )

        if not require_token_count(
            count_tokens,
            1,
            f"{contract_type} count",
        ):
            return {
                "valid": False,
                "contract_type": contract_type,
                "errors": errors,
                "observations": observations,
            }

        require_integer(
            count_tokens[0],
            f"{contract_type} count",
        )

        count = int(
            count_tokens[0]
        )

        values = _tokens_from_line(
            non_empty_lines[1]
        )

        require_token_count(
            values,
            count,
            f"{contract_type} values",
        )

        seen_values: set[str] = set()

        for index, token in enumerate(
            values,
            start=1,
        ):
            require_integer(
                token,
                f"{contract_type} value {index}",
            )

            if contract_type == "set-input":
                if token in seen_values:
                    fail(
                        f"set-input: duplicate value "
                        f"'{token}' detected."
                    )
                seen_values.add(token)

        if len(non_empty_lines) != 2:
            fail(
                f"{contract_type}: expected exactly "
                "2 non-empty lines."
            )

        return {
            "valid": not errors,
            "contract_type": contract_type,
            "errors": errors,
            "observations": observations,
        }

    # --------------------------------------------------------
    # INTENTIONALLY UNSUPPORTED CONTRACTS
    # --------------------------------------------------------

    if contract_type in {
        "stdin-present",
        "test-cases",
    }:
        observations.append(
            f"{contract_type} is intentionally "
            "unsupported by the deterministic generator."
        )

        return {
            "valid": True,
            "contract_type": contract_type,
            "errors": [],
            "observations": observations,
        }

    # --------------------------------------------------------
    # UNKNOWN CONTRACT
    # --------------------------------------------------------

    fail(
        f"No semantic validator implemented for "
        f"contract '{contract_type}'."
    )

    return {
        "valid": False,
        "contract_type": contract_type,
        "errors": errors,
        "observations": observations,
    }


# ============================================================
# FULL INPUT CONTRACT SEMANTIC AUDIT
# ============================================================


def audit_input_contract_semantics() -> dict[str, Any]:
    """
    Run semantic validation against every supported contract
    using its realistic smoke-test definition.

    This verifies generated stdin independently from the
    generator implementation.
    """
    intentionally_unsupported = {
        "stdin-present",
        "test-cases",
    }

    passed_contracts = []
    failed_contracts = []
    validation_errors = []

    for contract_type, expected_supported in (
        INPUT_CONTRACT_GENERATOR_COVERAGE.items()
    ):
        if contract_type in intentionally_unsupported:
            continue

        if not expected_supported:
            continue

        contract = INPUT_CONTRACT_SMOKE_TESTS.get(
            contract_type
        )

        if contract is None:
            failed_contracts.append(
                contract_type
            )
            validation_errors.append(
                {
                    "contract_type": contract_type,
                    "reason": (
                        "No smoke-test contract "
                        "definition exists."
                    ),
                }
            )
            continue

        try:
            generated_input = (
                generate_from_input_contract(
                    contract,
                    input_size=10,
                    seed=42,
                )
            )

            result = (
                validate_generated_input_against_contract(
                    contract,
                    generated_input,
                )
            )

            if result["valid"]:
                passed_contracts.append(
                    contract_type
                )
            else:
                failed_contracts.append(
                    contract_type
                )

                validation_errors.append(
                    {
                        "contract_type": contract_type,
                        "reason": "Semantic validation failed.",
                        "errors": result.get(
                            "errors",
                            [],
                        ),
                    }
                )

        except Exception as exc:
            failed_contracts.append(
                contract_type
            )

            validation_errors.append(
                {
                    "contract_type": contract_type,
                    "reason": (
                        "Semantic audit raised "
                        "an exception."
                    ),
                    "exception": str(exc),
                }
            )

    supported_contract_count = sum(
        1
        for contract_type, supported
        in INPUT_CONTRACT_GENERATOR_COVERAGE.items()
        if supported
        and contract_type
        not in intentionally_unsupported
    )

    return {
        "total_contracts": len(
            INPUT_CONTRACT_GENERATOR_COVERAGE
        ),
        "supported_contracts": supported_contract_count,
        "passed_contracts": len(
            passed_contracts
        ),
        "failed_contracts": len(
            failed_contracts
        ),
        "intentionally_unsupported": sorted(
            intentionally_unsupported
        ),
        "passed": (
            len(failed_contracts) == 0
            and len(validation_errors) == 0
        ),
        "failed_contract_types": sorted(
            failed_contracts
        ),
        "validation_errors": validation_errors,
    }


    # ============================================================
# INPUT CONTRACT NEGATIVE / MUTATION TESTING
# ============================================================


INPUT_CONTRACT_MUTATION_TESTS = {
    "integer-scalar": [
        {
            "name": "wrong_type",
            "mutator": lambda text: "abc\n",
        },
        {
            "name": "extra_token",
            "mutator": lambda text: "10 20\n",
        },
    ],

    "float-scalar": [
        {
            "name": "wrong_type",
            "mutator": lambda text: "abc\n",
        },
        {
            "name": "extra_token",
            "mutator": lambda text: "1.5 2.5\n",
        },
    ],

    "character-scalar": [
        {
            "name": "multi_character",
            "mutator": lambda text: "ab\n",
        },
        {
            "name": "empty",
            "mutator": lambda text: "\n",
        },
    ],

    "integer-array": [
        {
            "name": "too_few_values",
            "mutator": lambda text: (
                "10\n1 2 3\n"
            ),
        },
        {
            "name": "wrong_value_type",
            "mutator": lambda text: (
                "3\n1 abc 3\n"
            ),
        },
        {
            "name": "wrong_size",
            "mutator": lambda text: (
                "4\n1 2 3\n"
            ),
        },
    ],

    "float-array": [
        {
            "name": "wrong_value_type",
            "mutator": lambda text: (
                "3\n1.1 abc 3.3\n"
            ),
        },
        {
            "name": "wrong_count",
            "mutator": lambda text: (
                "4\n1.1 2.2 3.3\n"
            ),
        },
    ],

    "character-array": [
        {
            "name": "multi_character_element",
            "mutator": lambda text: (
                "3\na bb c\n"
            ),
        },
        {
            "name": "wrong_count",
            "mutator": lambda text: (
                "4\na b c\n"
            ),
        },
    ],

    "string-array": [
        {
            "name": "wrong_count",
            "mutator": lambda text: (
                "5\none two\n"
            ),
        },
        {
            "name": "missing_data",
            "mutator": lambda text: (
                "5\n"
            ),
        },
    ],

    "string-lines": [
        {
            "name": "wrong_line_count",
            "mutator": lambda text: (
                "5\n"
                "alpha\n"
                "beta\n"
            ),
        },
        {
            "name": "missing_line",
            "mutator": lambda text: (
                "3\n"
                "alpha\n"
                "beta\n"
            ),
        },
    ],

    "size-plus-string": [
        {
            "name": "missing_string",
            "mutator": lambda text: "10\n",
        },
        {
            "name": "wrong_size_type",
            "mutator": lambda text: (
                "abc\nhello\n"
            ),
        },
    ],

    "size-plus-two-strings": [
        {
            "name": "missing_second_string",
            "mutator": lambda text: (
                "10\nhello\n"
            ),
        },
        {
            "name": "extra_line",
            "mutator": lambda text: (
                "10\nhello\nworld\nextra\n"
            ),
        },
    ],

    "character-stream": [
        {
            "name": "whitespace",
            "mutator": lambda text: "abc def\n",
        },
        {
            "name": "empty",
            "mutator": lambda text: "\n",
        },
    ],

    "multiple-arrays": [
        {
            "name": "missing_second_array",
            "mutator": lambda text: (
                "3\n1 2 3\n"
            ),
        },
        {
            "name": "wrong_array_length",
            "mutator": lambda text: (
                "3\n1 2 3\n4 5\n"
            ),
        },
    ],

    "array-plus-target": [
        {
            "name": "missing_target",
            "mutator": lambda text: (
                "3\n1 2 3\n"
            ),
        },
        {
            "name": "invalid_target",
            "mutator": lambda text: (
                "3\n1 2 3\nabc\n"
            ),
        },
    ],

    "jagged-array": [
        {
            "name": "wrong_row_size",
            "mutator": lambda text: (
                "2\n"
                "3\n1 2\n"
                "2\n3 4\n"
            ),
        },
        {
            "name": "missing_row",
            "mutator": lambda text: (
                "2\n"
                "3\n1 2 3\n"
            ),
        },
    ],

    "matrix": [
        {
            "name": "wrong_column_count",
            "mutator": lambda text: (
                "2 3\n"
                "1 2\n"
                "3 4 5\n"
            ),
        },
        {
            "name": "missing_row",
            "mutator": lambda text: (
                "2 2\n"
                "1 2\n"
            ),
        },
        {
            "name": "invalid_dimension",
            "mutator": lambda text: (
                "abc 2\n"
                "1 2\n"
                "3 4\n"
            ),
        },
    ],

    "matrix-plus-target": [
        {
            "name": "missing_target",
            "mutator": lambda text: (
                "2 2\n"
                "1 2\n"
                "3 4\n"
            ),
        },
        {
            "name": "invalid_target",
            "mutator": lambda text: (
                "2 2\n"
                "1 2\n"
                "3 4\n"
                "abc\n"
            ),
        },
    ],

    "character-grid": [
        {
            "name": "wrong_row_length",
            "mutator": lambda text: (
                "2 3\n"
                "abc\n"
                "de\n"
            ),
        },
        {
            "name": "missing_row",
            "mutator": lambda text: (
                "2 3\n"
                "abc\n"
            ),
        },
    ],

    "adjacency-matrix": [
        {
            "name": "invalid_cell",
            "mutator": lambda text: (
                "2\n"
                "0 2\n"
                "1 0\n"
            ),
        },
        {
            "name": "wrong_row_width",
            "mutator": lambda text: (
                "2\n"
                "0\n"
                "1 0\n"
            ),
        },
    ],

    "graph": [
        {
            "name": "invalid_vertex",
            "mutator": lambda text: (
                "3 1\n"
                "1 9\n"
            ),
        },
        {
            "name": "wrong_edge_width",
            "mutator": lambda text: (
                "3 1\n"
                "1 2 3\n"
            ),
        },
    ],

    "weighted-graph": [
        {
            "name": "missing_weight",
            "mutator": lambda text: (
                "3 1\n"
                "1 2\n"
            ),
        },
        {
            "name": "invalid_weight",
            "mutator": lambda text: (
                "3 1\n"
                "1 2 abc\n"
            ),
        },
    ],

    "graph-with-source": [
        {
            "name": "invalid_source",
            "mutator": lambda text: (
                "3 1\n"
                "1 2\n"
                "9\n"
            ),
        },
        {
            "name": "missing_source",
            "mutator": lambda text: (
                "3 1\n"
                "1 2\n"
            ),
        },
    ],

    "weighted-graph-with-source": [
        {
            "name": "invalid_source",
            "mutator": lambda text: (
                "3 1\n"
                "1 2 5\n"
                "9\n"
            ),
        },
        {
            "name": "missing_weight",
            "mutator": lambda text: (
                "3 1\n"
                "1 2\n"
                "1\n"
            ),
        },
    ],

    "tree": [
        {
            "name": "invalid_parent",
            "mutator": lambda text: (
                "3\n"
                "9 2\n"
                "2 3\n"
            ),
        },
        {
            "name": "duplicate_parent_assignment",
            "mutator": lambda text: (
                "3\n"
                "1 2\n"
                "1 2\n"
            ),
        },
    ],

    "parent-array-tree": [
        {
            "name": "wrong_parent_count",
            "mutator": lambda text: (
                "4\n0 1 2\n"
            ),
        },
        {
            "name": "invalid_parent",
            "mutator": lambda text: (
                "4\n0 1 2 9\n"
            ),
        },
    ],

    "binary-tree-level-order": [
        {
            "name": "null_root",
            "mutator": lambda text: (
                "3\n-1 2 3\n"
            ),
        },
        {
            "name": "wrong_slot_count",
            "mutator": lambda text: (
                "4\n1 2 3\n"
            ),
        },
    ],

    "test-cases-array": [
        {
            "name": "wrong_case_count",
            "mutator": lambda text: (
                "2\n"
                "3\n1 2 3\n"
                "4\n1 2 3\n"
            ),
        },
        {
            "name": "wrong_case_size",
            "mutator": lambda text: (
                "1\n"
                "4\n1 2 3\n"
            ),
        },
    ],

    "test-cases-matrix": [
        {
            "name": "missing_matrix_row",
            "mutator": lambda text: (
                "1\n"
                "2 2\n"
                "1 2\n"
            ),
        },
        {
            "name": "wrong_column_count",
            "mutator": lambda text: (
                "1\n"
                "2 2\n"
                "1\n"
                "3 4\n"
            ),
        },
    ],

    "eof-stream": [
        {
            "name": "wrong_type",
            "mutator": lambda text: (
                "1\nabc\n3\n"
            ),
        },
        {
            "name": "multiple_tokens",
            "mutator": lambda text: (
                "1 2\n3\n"
            ),
        },
    ],

    "eof-records": [
        {
            "name": "wrong_field_count",
            "mutator": lambda text: (
                "1 2 3\n"
            ),
        },
        {
            "name": "wrong_field_type",
            "mutator": lambda text: (
                "abc 2\n"
            ),
        },
    ],

    "eof-lines": [
        {
            "name": "empty_input",
            "mutator": lambda text: "",
        },
    ],

    "sentinel-stream": [
        {
            "name": "missing_sentinel",
            "mutator": lambda text: (
                "1\n2\n3\n"
            ),
        },
        {
            "name": "wrong_sentinel",
            "mutator": lambda text: (
                "1\n2\n3\n99\n"
            ),
        },
    ],

    "sentinel-records": [
        {
            "name": "wrong_terminator",
            "mutator": lambda text: (
                "1 2\n"
                "3 4\n"
                "0 0\n"
            ),
        },
        {
            "name": "wrong_record_width",
            "mutator": lambda text: (
                "1\n"
                "0 0\n"
            ),
        },
    ],

    "pairs": [
        {
            "name": "wrong_record_width",
            "mutator": lambda text: (
                "2\n"
                "1 2 3\n"
                "4 5\n"
            ),
        },
        {
            "name": "wrong_count",
            "mutator": lambda text: (
                "3\n"
                "1 2\n"
                "3 4\n"
            ),
        },
    ],

    "pair-records": [
        {
            "name": "wrong_record_width",
            "mutator": lambda text: (
                "2\n"
                "1 2 3\n"
                "4 5\n"
            ),
        },
    ],

    "triples": [
        {
            "name": "wrong_record_width",
            "mutator": lambda text: (
                "2\n"
                "1 2\n"
                "3 4 5\n"
            ),
        },
    ],

    "triple-records": [
        {
            "name": "wrong_record_width",
            "mutator": lambda text: (
                "1\n"
                "1 2\n"
            ),
        },
    ],

    "tuple-records": [
        {
            "name": "wrong_field_type",
            "mutator": lambda text: (
                "2\n"
                "abc hello\n"
                "3 world\n"
            ),
        },
    ],

    "structured-records": [
        {
            "name": "wrong_field_count",
            "mutator": lambda text: (
                "1\n"
                "1 alice\n"
            ),
        },
    ],

    "key-value-records": [
        {
            "name": "wrong_value_type",
            "mutator": lambda text: (
                "2\n"
                "alice abc\n"
                "bob 10\n"
            ),
        },
    ],

    "query-stream": [
        {
            "name": "wrong_query_count",
            "mutator": lambda text: (
                "3\n"
                "10\n"
                "20\n"
            ),
        },
        {
            "name": "wrong_query_type",
            "mutator": lambda text: (
                "1\nabc\n"
            ),
        },
    ],

    "range-queries": [
        {
            "name": "invalid_range",
            "mutator": lambda text: (
                "5\n"
                "1 2 3 4 5\n"
                "1\n"
                "5 2\n"
            ),
        },
        {
            "name": "missing_query",
            "mutator": lambda text: (
                "5\n"
                "1 2 3 4 5\n"
                "2\n"
                "0 1\n"
            ),
        },
    ],

    "array-with-queries": [
        {
            "name": "wrong_query_count",
            "mutator": lambda text: (
                "3\n"
                "1 2 3\n"
                "2\n"
                "1\n"
            ),
        },
        {
            "name": "invalid_index",
            "mutator": lambda text: (
                "3\n"
                "1 2 3\n"
                "1\n"
                "9\n"
            ),
        },
    ],

    "array-with-range-queries": [
        {
            "name": "invalid_range",
            "mutator": lambda text: (
                "3\n"
                "1 2 3\n"
                "1\n"
                "3 1\n"
            ),
        },
        {
            "name": "missing_query",
            "mutator": lambda text: (
                "3\n"
                "1 2 3\n"
                "2\n"
                "1 2\n"
            ),
        },
    ],

    "command-stream": [
        {
            "name": "unknown_command",
            "mutator": lambda text: (
                "1\n"
                "UNKNOWN\n"
            ),
        },
        {
            "name": "missing_argument",
            "mutator": lambda text: (
                "1\n"
                "ADD\n"
            ),
        },
    ],

    "delimited-lines": [
        {
            "name": "wrong_field_count",
            "mutator": lambda text: (
                "1,2\n"
            ),
        },
        {
            "name": "wrong_field_type",
            "mutator": lambda text: (
                "1,abc,3\n"
            ),
        },
    ],

    "scanf-input": [
        {
            "name": "missing_field",
            "mutator": lambda text: (
                "10\n"
            ),
        },
        {
            "name": "wrong_float_type",
            "mutator": lambda text: (
                "10 abc\n"
            ),
        },
    ],

    "stack-input": [
        {
            "name": "wrong_count",
            "mutator": lambda text: (
                "4\n1 2 3\n"
            ),
        },
        {
            "name": "wrong_value_type",
            "mutator": lambda text: (
                "3\n1 abc 3\n"
            ),
        },
    ],

    "queue-input": [
        {
            "name": "wrong_count",
            "mutator": lambda text: (
                "4\n1 2 3\n"
            ),
        },
        {
            "name": "wrong_value_type",
            "mutator": lambda text: (
                "3\n1 abc 3\n"
            ),
        },
    ],

    "set-input": [
        {
            "name": "duplicate_value",
            "mutator": lambda text: (
                "3\n1 1 2\n"
            ),
        },
        {
            "name": "wrong_count",
            "mutator": lambda text: (
                "4\n1 2 3\n"
            ),
        },
    ],
}


def audit_input_contract_mutations() -> dict[str, Any]:
    """
    Verify that intentionally corrupted inputs are rejected
    by the independent semantic validator.

    A mutation test passes only when:
    - the validator reports valid=False
    - at least one meaningful validation error is returned
    """
    intentionally_unsupported = {
        "stdin-present",
        "test-cases",
    }

    passed_tests: list[dict[str, Any]] = []
    failed_tests: list[dict[str, Any]] = []
    uncovered_contracts: list[str] = []

    for contract_type, mutation_tests in (
        INPUT_CONTRACT_MUTATION_TESTS.items()
    ):
        if contract_type in intentionally_unsupported:
            continue

        base_contract = (
            INPUT_CONTRACT_SMOKE_TESTS.get(
                contract_type
            )
        )

        if base_contract is None:
            uncovered_contracts.append(
                contract_type
            )
            continue

        if not mutation_tests:
            uncovered_contracts.append(
                contract_type
            )
            continue

        for mutation in mutation_tests:
            test_name = str(
                mutation.get(
                    "name",
                    "unnamed-mutation",
                )
            )

            mutator = mutation.get(
                "mutator"
            )

            if not callable(mutator):
                failed_tests.append(
                    {
                        "contract_type": contract_type,
                        "mutation": test_name,
                        "reason": (
                            "Mutation must provide "
                            "a callable mutator."
                        ),
                    }
                )
                continue

            try:
                baseline = (
                    generate_from_input_contract(
                        base_contract,
                        input_size=10,
                        seed=42,
                    )
                )

                mutated_input = mutator(
                    baseline
                )

                result = (
                    validate_generated_input_against_contract(
                        base_contract,
                        mutated_input,
                    )
                )

                if (
                    result.get("valid") is False
                    and result.get("errors")
                ):
                    passed_tests.append(
                        {
                            "contract_type": contract_type,
                            "mutation": test_name,
                        }
                    )
                else:
                    failed_tests.append(
                        {
                            "contract_type": contract_type,
                            "mutation": test_name,
                            "reason": (
                                "Mutation was accepted "
                                "as valid."
                            ),
                        }
                    )

            except Exception as exc:
                failed_tests.append(
                    {
                        "contract_type": contract_type,
                        "mutation": test_name,
                        "reason": (
                            "Mutation test raised "
                            "an exception."
                        ),
                        "exception": str(exc),
                    }
                )

    tested_contracts = sorted(
        {
            item["contract_type"]
            for item in passed_tests
            + failed_tests
        }
    )

    return {
        "total_mutation_tests": (
            len(passed_tests)
            + len(failed_tests)
        ),
        "passed_mutation_tests": len(
            passed_tests
        ),
        "failed_mutation_tests": len(
            failed_tests
        ),
        "tested_contracts": len(
            tested_contracts
        ),
        "uncovered_contracts": sorted(
            uncovered_contracts
        ),
        "failed_tests": failed_tests,
        "passed": (
            not failed_tests
            and not uncovered_contracts
        ),
    }




