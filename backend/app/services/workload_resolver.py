# from __future__ import annotations

# from typing import Any
# # import re

# from app.services.custom_workload_generator import (
#     WORKLOAD_REGISTRY,
# )

# from app.services.algorithm_intelligence import (
#     analyze_algorithm,
# )
# from app.services.benchmark_metadata_intelligence import (
#     generate_benchmark_metadata,
# )
# # from app.services.algorithm_intelligence import analyze_algorithm


# # ============================================================
# # KNOWN WORKLOAD SCHEMAS
# # ============================================================

# WORKLOAD_SCHEMAS: dict[str, dict[str, Any]] = {

#     "numeric-array": {
#         "type": "array",
#         "item_type": "integer",
#         "count_field": "n",
#         "description": (
#             "A one-dimensional array of integers."
#         ),
#     },

#     "text": {
#         "type": "text",
#         "item_type": "string",
#         "count_field": "n",
#         "description": (
#             "A collection of plain-text strings."
#         ),
#     },

#     "url": {
#         "type": "array",
#         "item_type": "url",
#         "count_field": "n",
#         "description": (
#             "A collection of URL strings."
#         ),
#     },

#     "html": {
#         "type": "array",
#         "item_type": "html",
#         "count_field": "n",
#         "description": (
#             "A collection of HTML fragments."
#         ),
#     },

#     "json": {
#         "type": "json-array",
#         "item_type": "object",
#         "count_field": None,
#         "description": (
#             "A JSON array containing structured records."
#         ),
#     },

#     "csv": {
#         "type": "tabular",
#         "item_type": "record",
#         "count_field": None,
#         "description": (
#             "Tabular CSV records with a header row."
#         ),
#     },

#     "matrix": {
#         "type": "matrix",
#         "item_type": "integer",
#         "rows_field": "n",
#         "columns_field": "n",
#         "description": (
#             "A square two-dimensional integer matrix."
#         ),
#     },

#     "graph": {
#         "type": "graph",
#         "representation": "edge-list",
#         "node_count_field": "vertices",
#         "edge_count_field": "edges",
#         "description": (
#             "An undirected graph represented using an edge list."
#         ),
#     },

#     "tree": {
#         "type": "tree",
#         "representation": "parent-child",
#         "node_count_field": "n",
#         "description": (
#             "A rooted tree represented using parent-child edges."
#         ),
#     },

#     "multiple-arrays": {
#         "type": "multiple-arrays",
#         "arrays": [
#             {
#                 "name": "array_a",
#                 "item_type": "integer",
#             },
#             {
#                 "name": "array_b",
#                 "item_type": "integer",
#             },
#         ],
#         "count_field": "n",
#         "description": (
#             "Two one-dimensional integer arrays."
#         ),
#     },
# }

# # ============================================================
# # INPUT CONTRACT -> GENERATOR INPUT STRUCTURE
# # ============================================================

# CONTRACT_TO_INPUT_STRUCTURE: dict[str, str] = {
#     # --------------------------------------------------------
#     # Basic / fallback
#     # --------------------------------------------------------
#     "no-input": "no-input",
#     "stdin-present": "stdin-present",

#     # --------------------------------------------------------
#     # Scalars
#     # --------------------------------------------------------
#     "integer-scalar": "integer-scalar",
#     "integer-scalars": "integer-scalars",
#     "float-scalar": "float-scalar",
#     "float-scalars": "float-scalars",
#     "character-scalar": "character-scalar",
#     "mixed-scalars": "mixed-scalars",

#     # --------------------------------------------------------
#     # Strings
#     # --------------------------------------------------------
#     "string-token": "string-token",
#     "string-line": "string-line",
#     "string-array": "string-array",
#     "string-lines": "string-lines",
#     "scalar-plus-line": "scalar-plus-line",
#     "size-plus-string": "size-plus-string",
#     "size-plus-two-strings": "size-plus-two-strings",
#     "size-plus-strings": "size-plus-strings",

#     # --------------------------------------------------------
#     # Character / stream input
#     # --------------------------------------------------------
#     "character-stream": "character-stream",

#     # --------------------------------------------------------
#     # Arrays
#     # --------------------------------------------------------
#     "integer-array": "integer-array",
#     "float-array": "float-array",
#     "character-array": "character-array",
#     "jagged-array": "jagged-array",
#     "array-plus-target": "array-plus-target",
#     "multiple-arrays": "multiple-arrays",
#     "array-with-queries": "array-with-queries",
#     "array-with-range-queries": "array-with-range-queries",

#     # --------------------------------------------------------
#     # Matrix
#     # --------------------------------------------------------
#     "matrix": "matrix",
#     "matrix-plus-target": "matrix-plus-target",
#     "jagged-matrix": "jagged-matrix",
#     "character-grid": "character-grid",
#     "adjacency-matrix": "adjacency-matrix",

#     # --------------------------------------------------------
#     # Graph
#     # --------------------------------------------------------
#     "graph": "graph",
#     "weighted-graph": "weighted-graph",
#     "graph-with-source": "graph-with-source",
#     "weighted-graph-with-source": "weighted-graph-with-source",

#     # --------------------------------------------------------
#     # Tree
#     # --------------------------------------------------------
#     "tree": "tree",
#     "parent-array-tree": "parent-array-tree",
#     "binary-tree-level-order": "binary-tree-level-order",

#     # --------------------------------------------------------
#     # Test cases
#     # --------------------------------------------------------
#     "test-cases": "test-cases",
#     "test-cases-array": "test-cases-array",
#     "test-cases-matrix": "test-cases-matrix",

#     # --------------------------------------------------------
#     # EOF / Sentinel
#     # --------------------------------------------------------
#     "eof-stream": "eof-stream",
#     "eof-records": "eof-records",
#     "eof-lines": "eof-lines",
#     "sentinel-stream": "sentinel-stream",
#     "sentinel-records": "sentinel-records",

#     # --------------------------------------------------------
#     # Records
#     # --------------------------------------------------------
#     "pair-records": "pair-records",
#     "triple-records": "triple-records",
#     "pairs": "pairs",
#     "triples": "triples",
#     "tuple-records": "tuple-records",
#     "structured-records": "structured-records",
#     "key-value-records": "key-value-records",

#     # --------------------------------------------------------
#     # Queries / commands / delimited
#     # --------------------------------------------------------
#     "query-stream": "query-stream",
#     "range-queries": "range-queries",
#     "command-stream": "command-stream",
#     "delimited-lines": "delimited-lines",
#     "scanf-input": "scanf-input",

#     # --------------------------------------------------------
#     # Collection-specific
#     # --------------------------------------------------------
#     "stack-input": "stack-input",
#     "queue-input": "queue-input",
#     "set-input": "set-input",
# }

# def normalize_input_structure_from_contract(
#     input_contract: dict[str, Any] | None,
# ) -> dict[str, Any] | None:
#     """
#     Convert the exact input contract into the normalized
#     generator-facing input structure.

#     Input Contract Analyzer is the authority for contract detection.
#     This function performs mapping only; it does not inspect code.
#     """

#     if not input_contract:
#         return None

#     contract_type = normalize_workload_type(
#         input_contract.get("contract_type")
#     )

#     if not contract_type:
#         return None

#     input_structure_type = CONTRACT_TO_INPUT_STRUCTURE.get(
#         contract_type
#     )

#     if not input_structure_type:
#         return None

#     schema = WORKLOAD_SCHEMAS.get(
#         input_structure_type
#     )

#     return {
#         "status": "known" if schema is not None else "custom",
#         "workload_type": input_structure_type,
#         "schema": schema,
#         "source": "input-contract",
#         "contract_type": contract_type,
#         "contract": input_contract,
#         "detection": {
#             "method": "input-contract-mapping",
#             "confidence": input_contract.get("confidence", 1.0),
#             "reason": (
#                 "Input structure was normalized directly "
#                 "from the exact Input Contract."
#             ),
#         },
#     }
# # ============================================================
# # HELPERS
# # ============================================================

# def normalize_workload_type(
#     workload_type: str | None,
# ) -> str | None:

#     if workload_type is None:
#         return None

#     normalized = (
#         workload_type
#         .strip()
#         .lower()
#     )

#     return normalized or None


# def _combined_text(
#     benchmark_name: str | None,
#     description: str | None,
#     reference_code: str | None,
# ) -> str:

#     return " ".join(
#         [
#             benchmark_name or "",
#             description or "",
#             reference_code or "",
#         ]
#     ).lower()


# def _contains_any(
#     text: str,
#     keywords: list[str],
# ) -> bool:

#     return any(
#         keyword.lower() in text
#         for keyword in keywords
#     )


# # ============================================================
# # CHECK KNOWN WORKLOAD
# # ============================================================

# def is_known_workload(
#     workload_type: str | None,
# ) -> bool:

#     normalized = normalize_workload_type(
#         workload_type
#     )

#     if not normalized:
#         return False

#     return (
#         normalized in WORKLOAD_REGISTRY
#         and normalized in WORKLOAD_SCHEMAS
#     )


# # ============================================================
# # DETERMINISTIC WORKLOAD DETECTION
# # ============================================================

# def detect_input_structure_from_content(
#     benchmark_name: str | None,
#     description: str | None,
#     reference_code: str | None,
# ) -> dict[str, Any] | None:
#     """
#     Detect input/data structure using deterministic rules.

#     This function must NOT identify the algorithmic behavior
#     of the program.
#     """

#     text = _combined_text(
#         benchmark_name,
#         description,
#         reference_code,
#     )

#     # ========================================================
#     # 1. ARRAY + TARGET
#     # ========================================================

#     has_array = _contains_any(
#         text,
#         [
#             "array",
#             "array[",
#             "vector",
#             "list",
#             "integer[]",
#             "arr[",
#         ],
#     )

#     has_target = _contains_any(
#         text,
#         [
#             "target",
#             "target value",
#             "target number",
#             "sum equals",
#         ],
#     )

#     if has_array and has_target:

#         return {
#             "status": "custom",
#             "workload_type": "array-plus-target",
#             "schema": {
#                 "type": "composite",
#                 "fields": [
#                     {
#                         "name": "n",
#                         "type": "integer",
#                     },
#                     {
#                         "name": "array",
#                         "type": "integer[]",
#                     },
#                     {
#                         "name": "target",
#                         "type": "integer",
#                     },
#                 ],
#                 "description": (
#                     "An integer array accompanied "
#                     "by a separate target value."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Benchmark contains both array/list "
#                     "input and a separate target value."
#                 ),
#             },
#         }

#     # ========================================================
#     # 2. MULTIPLE TEST CASES
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "multiple test cases",
#             "multiple test case",
#             "test cases",
#             "test case",
#             "number of test cases",
#             "read t",
#             "cin >> t",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "multiple-test-cases",
#             "schema": {
#                 "type": "multiple-test-cases",
#                 "test_cases_field": "T",
#                 "description": (
#                     "Multiple independent test cases."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Benchmark metadata or reference code "
#                     "contains multiple-test-case input patterns."
#                 ),
#             },
#         }

#     # ========================================================
#     # 3. MATRIX
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "matrix",
#             "matrices",
#             "2d array",
#             "2-d array",
#             "two dimensional array",
#             "two-dimensional array",
#             "rows and columns",
#             "row and column",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "matrix",
#             "schema": WORKLOAD_SCHEMAS["matrix"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Matrix or two-dimensional array "
#                     "input was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 4. GRAPH
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "graph",
#             "vertices",
#             "edges",
#             "edge list",
#             "adjacency list",
#             "adjacency matrix",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "graph",
#             "schema": WORKLOAD_SCHEMAS["graph"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Graph-specific input patterns were detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 5. TREE
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "binary tree",
#             "tree nodes",
#             "parent child",
#             "parent-child",
#             "root node",
#             "tree traversal",
#             "tree input",
#             "tree",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "tree",
#             "schema": WORKLOAD_SCHEMAS["tree"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Tree-specific input patterns were detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 6. LINKED LIST
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "linked list",
#             "linked-list",
#             "node.next",
#             "next pointer",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "linked-list",
#             "schema": {
#                 "type": "linked-list",
#                 "node_value_type": "integer",
#                 "node_count_field": "n",
#                 "description": (
#                     "A linked-list-specific input structure."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Benchmark contains linked-list structure."
#                 ),
#             },
#         }

#     # ========================================================
#     # 7. CHARACTERS
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "character",
#             "characters",
#             "char array",
#             "char[]",
#             "sequence of chars",
#             "string of characters",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "characters",
#             "schema": {
#                 "type": "array",
#                 "item_type": "character",
#                 "count_field": "n",
#                 "description": (
#                     "A sequence or array of characters."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Character-based input patterns were detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 8. BOOLEAN
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "boolean",
#             "bool",
#             "true false",
#             "true/false",
#             "binary flag",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "boolean-array",
#             "schema": {
#                 "type": "array",
#                 "item_type": "boolean",
#                 "count_field": "n",
#                 "description": (
#                     "A sequence of boolean values."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Boolean input patterns were detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 9. FLOAT / DECIMAL
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "floating point",
#             "floating-point",
#             "decimal",
#             "float array",
#             "real numbers",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "float-array",
#             "schema": {
#                 "type": "array",
#                 "item_type": "float",
#                 "count_field": "n",
#                 "description": (
#                     "A one-dimensional array "
#                     "of floating-point values."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Floating-point or decimal "
#                     "input patterns were detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 10. JSON
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "json",
#             "json object",
#             "json data",
#             "json records",
#             "nested json",
#         ],
#     ):

#         return {
#             "status": "known",
#             "workload_type": "json",
#             "schema": WORKLOAD_SCHEMAS["json"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "JSON input structure was explicitly mentioned."
#                 ),
#             },
#         }

#     # ========================================================
#     # 11. CSV / TABULAR
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "csv",
#             "comma separated",
#             "comma-separated",
#             "tabular",
#             "table records",
#             "tabular data",
#         ],
#     ):

#         return {
#             "status": "known",
#             "workload_type": "csv",
#             "schema": WORKLOAD_SCHEMAS["csv"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "CSV or tabular input structure was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 12. URL
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "url",
#             "urls",
#             "web address",
#             "http://",
#             "https://",
#             "endpoint url",
#         ],
#     ):

#         return {
#             "status": "known",
#             "workload_type": "url",
#             "schema": WORKLOAD_SCHEMAS["url"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "URL-based input structure was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 13. HTML / XML
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "html",
#             "html input",
#             "html document",
#             "html fragment",
#             "xml",
#             "xml document",
#             "<div>",
#             "<html>",
#         ],
#     ):

#         return {
#             "status": "known" if "html" in WORKLOAD_REGISTRY else "custom",
#             "workload_type": (
#                 "html"
#                 if "html" in WORKLOAD_REGISTRY
#                 else "html"
#             ),
#             "schema": WORKLOAD_SCHEMAS["html"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "HTML/XML markup input was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 14. PAIRS / TUPLES
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "pair",
#             "pairs",
#             "tuple",
#             "tuples",
#             "(x,y)",
#             "(x, y)",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "pairs",
#             "schema": {
#                 "type": "array",
#                 "item_type": "pair",
#                 "count_field": "n",
#                 "description": (
#                     "A collection of pair or tuple values."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Pair or tuple input structure was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 15. KEY-VALUE
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "key-value",
#             "key value",
#             "key/value",
#             "name=value",
#             "key=value",
#             "dictionary",
#             "map input",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "key-value",
#             "schema": {
#                 "type": "key-value",
#                 "item_type": "record",
#                 "description": (
#                     "Input consists of key-value records."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Key-value input structure was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 16. DATE / TIME
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "date",
#             "dates",
#             "timestamp",
#             "timestamps",
#             "datetime",
#             "date/time",
#             "time series",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "datetime",
#             "schema": {
#                 "type": "array",
#                 "item_type": "datetime",
#                 "count_field": "n",
#                 "description": (
#                     "A collection of date or time values."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Date/time input structure was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 17. MIXED RECORDS
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "mixed datatype",
#             "mixed data type",
#             "mixed records",
#             "mixed fields",
#             "heterogeneous records",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "mixed-records",
#             "schema": {
#                 "type": "records",
#                 "item_type": "mixed",
#                 "count_field": "n",
#                 "description": (
#                     "Records containing multiple data types."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Mixed-type record structure was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # 18. BINARY
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "binary data",
#             "binary input",
#             "bytes",
#             "byte array",
#             "byte[]",
#         ],
#     ):

#         return {
#             "status": "custom",
#             "workload_type": "binary",
#             "schema": {
#                 "type": "bytes",
#                 "item_type": "byte",
#                 "description": (
#                     "Binary or byte-oriented input."
#                 ),
#             },
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Binary or byte input patterns were detected."
#                 ),
#             },
#         }
#         # ========================================================
#     # 19. NUMERIC ARRAY
#     # ========================================================

#     if has_array:

#         return {
#             "status": "known",
#             "workload_type": "numeric-array",
#             "schema": WORKLOAD_SCHEMAS["numeric-array"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "A one-dimensional numeric array "
#                     "input was detected."
#                 ),
#             },
#         }
    
#     # ========================================================
#     #  20. GENERIC TEXT / STRING
#     # ========================================================

#     if _contains_any(
#         text,
#         [
#             "text input",
#             "plain text",
#             "string input",
#             "string data",
#             "text processing",
#             "words",
#             "sentences",
#         ],
#     ):

#         return {
#             "status": "known",
#             "workload_type": "text",
#             "schema": WORKLOAD_SCHEMAS["text"],
#             "detection": {
#                 "method": "deterministic-rule",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Text or string input structure was detected."
#                 ),
#             },
#         }

#     # ========================================================
#     # NO SAFE MATCH
#     # ========================================================

#     return None


# # Backward-compatible alias for existing callers.
# detect_workload_from_content = detect_input_structure_from_content
# # Backward-compatible alias for existing callers.
# detect_reference_input_structure = detect_input_structure_from_content
# detect_reference_input_workload = detect_reference_input_structure


# # ============================================================
# # RESOLVE EXPLICIT WORKLOAD
# # ============================================================

# def resolve_workload(
#     workload_type: str | None,
# ) -> dict[str, Any]:

#     normalized = normalize_workload_type(
#         workload_type
#     )

#     if is_known_workload(normalized):

#         return {
#             "status": "known",
#             "workload_type": normalized,
#             "schema": WORKLOAD_SCHEMAS[normalized],
#             "detection": {
#                 "method": "registry",
#                 "confidence": 1.0,
#                 "reason": (
#                     "Workload type was explicitly "
#                     "provided and is registered."
#                 ),
#             },
#         }

#     return {
#         "status": "custom",
#         "workload_type": (
#             normalized
#             if normalized
#             else "custom"
#         ),
#         "schema": None,
#         "detection": {
#             "method": "unresolved",
#             "confidence": 0.0,
#             "reason": (
#                 "No registered workload type was found."
#             ),
#         },
#     }


# def workload_generation_capability(
#     workload: dict[str, Any],
# ) -> dict[str, Any]:
#     """
#     Determine whether the resolved workload can actually be
#     generated deterministically by the current backend.

#     Registry workloads are generated through WORKLOAD_REGISTRY.

#     Custom workloads are generated through generate_schema_input()
#     in custom_benchmark_engine.py.
#     """

#     workload_type = (
#         workload.get("workload_type")
#     )

#     schema = workload.get("schema")

#     normalized_type = normalize_workload_type(
#         workload_type
#     )

#     # --------------------------------------------------------
#     # No usable workload type/schema
#     # --------------------------------------------------------

#     if (
#         not normalized_type
#         or normalized_type == "custom"
#         or schema is None
#     ):
#         return {
#             "can_generate": False,
#             "reason": (
#                 "No deterministic workload generator "
#                 "is available for this workload."
#             ),
#         }

#     # --------------------------------------------------------
#     # Registry workloads
#     # --------------------------------------------------------

#     if (
#         normalized_type in WORKLOAD_REGISTRY
#         and normalized_type in WORKLOAD_SCHEMAS
#     ):
#         return {
#             "can_generate": True,
#             "reason": (
#                 "A deterministic registry generator "
#                 "is available for this workload."
#             ),
#         }

#     # --------------------------------------------------------
#     # Custom-schema generators currently implemented in
#     # custom_benchmark_engine.generate_schema_input()
#     # --------------------------------------------------------

#     custom_schema_generators = {
#         "characters",
#         "character-array",

#         "float-array",
#         "floating-point",
#         "decimal",
#         "decimal-array",

#         "boolean",
#         "boolean-array",
#         "bool-array",

#         "array-plus-target",
#         "array-target",

#         "multiple-test-cases",
#         "test-cases",

#         "pairs",
#         "tuples",
#         "pairs-tuples",

#         "key-value",
#         "key-value-data",
#         "key-value-records",

#         "mixed-records",
#         "mixed-datatype-records",

#         "date",
#         "datetime",
#         "date-time",
#         "timestamp",
#     }

#     if normalized_type in custom_schema_generators:
#         return {
#             "can_generate": True,
#             "reason": (
#                 "A deterministic custom-schema "
#                 "generator is available for this workload."
#             ),
#         }

#     # --------------------------------------------------------
#     # Generic schema support
#     # --------------------------------------------------------

#     schema_type = schema.get("type")

#     if schema_type == "array":

#         item_type = schema.get(
#             "item_type"
#         )

#         if item_type in {
#             "integer",
#             "float",
#             "character",
#         }:
#             return {
#                 "can_generate": True,
#                 "reason": (
#                     "A deterministic generic array "
#                     "generator is available for this schema."
#                 ),
#             }

#     # --------------------------------------------------------
#     # No actual generator available
#     # --------------------------------------------------------

#     return {
#         "can_generate": False,
#         "reason": (
#             "A workload schema was detected, but the "
#             "backend does not currently have a deterministic "
#             "generator for this workload type."
#         ),
#     }


# def _analyze_algorithm_with_intelligence(
#     reference_code: str | None,
# ) -> dict[str, Any] | None:
#     """
#     Analyze algorithmic behavior using Algorithm Intelligence.

#     Algorithm Intelligence owns computational behavior while
#     input structure remains the responsibility of the input
#     contract analyzer.
#     """

#     if not reference_code or not reference_code.strip():
#         return None

#     try:
#         from app.services.reference_code_analyzer import (
#             detect_reference_language,
#         )

#         language_result = detect_reference_language(
#             reference_code
#         )

#         detected_language = language_result.get(
#             "language"
#         )

#         language_map = {
#             "C": "c",
#             "C++": "cpp",
#             "Java": "java",
#             "Python": "python",
#             "JavaScript": "javascript",
#             "Go": "go",
#             "Rust": "rust",
#             "C#": "csharp",
#             "Kotlin": "kotlin",
#             "PHP": "php",
#         }

#         language = language_map.get(
#             detected_language,
#             detected_language,
#         )

#         if not language:
#             return None

#         analysis = analyze_algorithm(
#             reference_code,
#             language,
#         )

#     except Exception as exc:
#         return {
#             "workload_type": "custom",
#             "algorithm_family": "custom",
#             "algorithm_name": "custom",
#             "specificity": "unknown",
#             "confidence": 0.0,
#             "reason": (
#                 "Algorithm Intelligence could not analyze "
#                 "the reference implementation."
#             ),
#             "evidence": {
#                 "error": str(exc),
#             },
#             "complexity": None,
#             "detection_method": "algorithm-intelligence-error",
#             "parser": None,
#             "parse_success": False,
#             "parse_error_count": None,
#         }

#     if not analysis:
#         return None

#     algorithm = analysis.get(
#         "algorithm",
#         {},
#     )

#     complexity = analysis.get(
#         "complexity"
#     )

#     detection = analysis.get(
#         "detection",
#         {},
#     )

#     algorithm_family = algorithm.get(
#         "family"
#     )

#     if not algorithm_family:
#         return None

#     return {
#         "workload_type": algorithm_family,
#         "algorithm_family": algorithm_family,
#         "algorithm_name": algorithm.get(
#             "name"
#         ),
#         "specificity": algorithm.get(
#             "specificity"
#         ),
#         "confidence": algorithm.get(
#             "confidence",
#             0.0,
#         ),
#         "reason": algorithm.get(
#             "evidence"
#         ),
#         "evidence": algorithm.get(
#             "evidence"
#         ),
#         "complexity": complexity,
#         "detection_method": detection.get(
#             "method",
#             "algorithm-intelligence",
#         ),
#         "parser": detection.get(
#             "parser"
#         ),
#         "parse_success": detection.get(
#             "parse_success"
#         ),
#         "parse_error_count": detection.get(
#             "parse_error_count"
#         ),
#     }


# # def _analyze_algorithm_with_intelligence(
# #     reference_code: str | None,
# # ) -> dict[str, Any] | None:
# #     """
# #     Analyze computational behavior using Algorithm Intelligence.

# #     Algorithm Intelligence owns algorithmic behavior.
# #     Input Contract Analyzer remains authoritative for
# #     input structure and generation schema.
# #     """
# #     if not reference_code or not reference_code.strip():
# #         return None

# #     analysis = analyze_algorithm(reference_code)

# #     if not analysis:
# #         return None

# #     algorithm_family = analysis.get("algorithm_family")

# #     if not algorithm_family:
# #         return None

# #     evidence = analysis.get("evidence")

# #     return {
# #         "workload_type": algorithm_family,
# #         "algorithm_family": algorithm_family,
# #         "algorithm_name": analysis.get("algorithm_name"),
# #         "specificity": analysis.get("specificity"),
# #         "confidence": analysis.get("confidence", 0.0),
# #         "reason": (
# #             evidence.get("summary")
# #             if isinstance(evidence, dict)
# #             else None
# #         ),
# #         "evidence": evidence,
# #         "complexity": analysis.get("complexity"),
# #         "detection_method": analysis.get(
# #             "detection_method",
# #             "algorithm-intelligence",
# #         ),
# #         "parser": analysis.get("parser"),
# #         "parse_success": analysis.get("parse_success"),
# #         "parse_error_count": analysis.get(
# #             "parse_error_count"
# #         ),
# #     }


# def _build_dual_track_workload_result(
#     input_structure_detection: dict[str, Any] | None,
#     algorithm_detection: dict[str, Any] | None,
# ) -> dict[str, Any]:
#     """
#     Build a backward-compatible result that keeps
#     input structure and algorithmic workload separate.
#     """

#     result: dict[str, Any] = {
#         "input_structure": input_structure_detection,
#         "algorithm": algorithm_detection,
#     }

#     if input_structure_detection is not None:
#         result["workload_type"] = input_structure_detection.get(
#             "workload_type"
#         )
#         result["schema"] = input_structure_detection.get(
#             "schema"
#         )
#     else:
#         result["workload_type"] = "custom"
#         result["schema"] = None

#     return result


# def _attach_benchmark_metadata(
#     result: dict[str, Any],
#     input_structure: dict[str, Any] | None,
#     algorithm_detection: dict[str, Any] | None,
# ) -> dict[str, Any]:
#     """Attach presentation metadata without changing workload resolution."""
#     result["benchmark_metadata"] = generate_benchmark_metadata(
#         input_structure=input_structure,
#         algorithm=algorithm_detection,
#     )
#     return result


# def _detect_from_description(
#     description: str | None,
# ) -> dict[str, Any] | None:
#     """
#     Detect workload using ONLY the benchmark description.
#     """

#     if not description or not description.strip():
#         return None

#     return detect_input_structure_from_content(
#         benchmark_name=None,
#         description=description,
#         reference_code=None,
#     )


# def _detect_from_benchmark_name(
#     benchmark_name: str | None,
# ) -> dict[str, Any] | None:
#     """
#     Detect workload using ONLY the benchmark name.
#     """

#     if not benchmark_name or not benchmark_name.strip():
#         return None

#     return detect_input_structure_from_content(
#         benchmark_name=benchmark_name,
#         description=None,
#         reference_code=None,
#     )


# def _detected_type(
#     result: dict[str, Any] | None,
# ) -> str | None:

#     if result is None:
#         return None

#     return normalize_workload_type(
#         result.get("workload_type")
#     )

# # ============================================================
# # RESOLVER INTELLIGENCE / HARDENING
# # ============================================================

# RESOLVER_SCHEMA_VERSION = 2

# CONFIDENCE_HIGH = 0.90
# CONFIDENCE_MEDIUM = 0.70

# _SPECIFICITY_RANK = {
#     "specific": 3,
#     "family": 2,
#     "generic": 1,
#     "unknown": 0,
#     None: 0,
# }

# # ------------------------------------------------------------
# # Algorithm -> compatible input families
# #
# # This layer does NOT identify algorithms.
# # Algorithm Intelligence remains the sole algorithm authority.
# #
# # These rules only detect obvious semantic contradictions.
# # ------------------------------------------------------------

# _ALGORITHM_INPUT_COMPATIBILITY: dict[str, set[str]] = {
#     # Searching
#     "binary-search": {
#         "integer-array",
#         "array-plus-target",
#         "string-array",
#         "string-token",
#         "string-line",
#         "character-array",
#         "characters",
#     },
#     "linear-search": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#         "array-plus-target",
#         "string-token",
#         "string-line",
#     },

#     # Sorting
#     "bubble-sort": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#         "array-plus-target",
#     },
#     "selection-sort": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#     },
#     "insertion-sort": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#     },
#     "merge-sort": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#     },
#     "quick-sort": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#     },
#     "heap-sort": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#     },

#     # Graph algorithms
#     "bfs": {
#         "graph",
#         "weighted-graph",
#         "graph-with-source",
#         "weighted-graph-with-source",
#         "adjacency-matrix",
#     },
#     "dfs": {
#         "graph",
#         "weighted-graph",
#         "graph-with-source",
#         "weighted-graph-with-source",
#         "adjacency-matrix",
#         "tree",
#         "parent-array-tree",
#         "binary-tree-level-order",
#     },
#     "dijkstra": {
#         "weighted-graph",
#         "weighted-graph-with-source",
#         "graph-with-source",
#     },

#     # Tree algorithms
#     "tree-traversal": {
#         "tree",
#         "parent-array-tree",
#         "binary-tree-level-order",
#     },

#     # Array/string techniques
#     "two-pointers": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#         "string-token",
#         "string-line",
#         "array-plus-target",
#     },
#     "sliding-window": {
#         "integer-array",
#         "float-array",
#         "character-array",
#         "string-array",
#         "string-token",
#         "string-line",
#     },
#     "prefix-sum": {
#         "integer-array",
#         "float-array",
#         "matrix",
#         "matrix-plus-target",
#         "array-with-queries",
#         "array-with-range-queries",
#     },

#     # Matrix
#     "matrix-processing": {
#         "matrix",
#         "matrix-plus-target",
#         "jagged-matrix",
#         "character-grid",
#         "adjacency-matrix",
#     },
# }


# def _safe_confidence(value: Any) -> float:
#     """
#     Normalize confidence into [0.0, 1.0].

#     Invalid confidence values never become evidence.
#     """
#     try:
#         value = float(value)
#     except (TypeError, ValueError):
#         return 0.0

#     if value != value:  # NaN
#         return 0.0

#     return max(0.0, min(1.0, value))


# def _confidence_level(score: float) -> str:
#     score = _safe_confidence(score)

#     if score >= CONFIDENCE_HIGH:
#         return "high"

#     if score >= CONFIDENCE_MEDIUM:
#         return "medium"

#     return "low"


# def _normalize_algorithm_name(
#     algorithm_name: str | None,
# ) -> str | None:
#     if not algorithm_name:
#         return None

#     normalized = (
#         str(algorithm_name)
#         .strip()
#         .lower()
#         .replace("_", "-")
#         .replace(" ", "-")
#     )

#     return normalized or None


# def _normalize_specificity(
#     specificity: str | None,
# ) -> str:
#     if not specificity:
#         return "unknown"

#     normalized = (
#         str(specificity)
#         .strip()
#         .lower()
#     )

#     if normalized in _SPECIFICITY_RANK:
#         return normalized

#     return "unknown"


# def _algorithm_is_reliable(
#     algorithm: dict[str, Any] | None,
# ) -> bool:
#     if not isinstance(algorithm, dict):
#         return False

#     name = _normalize_algorithm_name(
#         algorithm.get("algorithm_name")
#     )

#     confidence = _safe_confidence(
#         algorithm.get("confidence", 0.0)
#     )

#     specificity = _normalize_specificity(
#         algorithm.get("specificity")
#     )

#     if not name:
#         return False

#     if name in {"custom", "unknown", "none"}:
#         return False

#     return (
#         confidence >= CONFIDENCE_MEDIUM
#         and specificity != "unknown"
#     )


# def _input_is_reliable(
#     input_structure: dict[str, Any] | None,
#     input_contract: dict[str, Any] | None,
# ) -> bool:
#     if not isinstance(input_structure, dict):
#         return False

#     if not isinstance(input_contract, dict):
#         return False

#     workload_type = normalize_workload_type(
#         input_structure.get("workload_type")
#     )

#     if not workload_type:
#         return False

#     confidence = _safe_confidence(
#         input_contract.get("confidence", 0.0)
#     )

#     return confidence >= CONFIDENCE_MEDIUM


# def _algorithm_compatible_with_input(
#     algorithm: dict[str, Any] | None,
#     input_structure: dict[str, Any] | None,
# ) -> tuple[bool, str, dict[str, Any]]:
#     """
#     Validate only strong semantic contradictions.

#     Unknown combinations are NOT automatically rejected.
#     This is deliberate: the resolver must prefer uncertainty
#     over false negatives.
#     """

#     if not isinstance(algorithm, dict):
#         return (
#             True,
#             "No reliable algorithm evidence is available.",
#             {
#                 "status": "not-applicable",
#             },
#         )

#     if not isinstance(input_structure, dict):
#         return (
#             True,
#             "No verified input structure is available.",
#             {
#                 "status": "not-applicable",
#             },
#         )

#     algorithm_name = _normalize_algorithm_name(
#         algorithm.get("algorithm_name")
#     )

#     input_type = normalize_workload_type(
#         input_structure.get("workload_type")
#     )

#     if not algorithm_name or not input_type:
#         return (
#             True,
#             "Compatibility could not be conclusively evaluated.",
#             {
#                 "status": "insufficient-evidence",
#                 "algorithm": algorithm_name,
#                 "input": input_type,
#             },
#         )

#     allowed_inputs = _ALGORITHM_INPUT_COMPATIBILITY.get(
#         algorithm_name
#     )

#     # No explicit compatibility rule means:
#     # do not invent a contradiction.
#     if not allowed_inputs:
#         return (
#             True,
#             "No restrictive compatibility rule exists for this algorithm.",
#             {
#                 "status": "not-restricted",
#                 "algorithm": algorithm_name,
#                 "input": input_type,
#             },
#         )

#     if input_type in allowed_inputs:
#         return (
#             True,
#             "Algorithm and input structure are semantically compatible.",
#             {
#                 "status": "compatible",
#                 "algorithm": algorithm_name,
#                 "input": input_type,
#             },
#         )

#     return (
#         False,
#         (
#             f"Algorithm '{algorithm_name}' is not compatible "
#             f"with verified input structure '{input_type}'."
#         ),
#         {
#             "status": "contradiction",
#             "algorithm": algorithm_name,
#             "input": input_type,
#             "allowed_inputs": sorted(allowed_inputs),
#         },
#     )


# def _fuse_confidence(
#     input_confidence: float,
#     algorithm_confidence: float,
#     *,
#     algorithm_reliable: bool,
#     input_reliable: bool,
#     compatible: bool,
# ) -> float:
#     """
#     Conservative confidence fusion.

#     We never allow one strong signal to hide another weak signal.
#     """

#     input_score = _safe_confidence(input_confidence)
#     algorithm_score = _safe_confidence(algorithm_confidence)

#     if not input_reliable:
#         return 0.0

#     if not algorithm_reliable:
#         return round(
#             input_score * 0.75,
#             4,
#         )

#     score = min(
#         input_score,
#         algorithm_score,
#     )

#     if not compatible:
#         return 0.0

#     return round(score, 4)


# def _select_algorithm_specificity(
#     algorithm: dict[str, Any] | None,
# ) -> dict[str, Any]:
#     """
#     Enforce the specificity hierarchy:

#         specific > family > generic > unknown

#     No resolver logic is allowed to upgrade specificity.
#     """

#     if not isinstance(algorithm, dict):
#         return {
#             "name": None,
#             "family": None,
#             "specificity": "unknown",
#             "rank": 0,
#         }

#     name = algorithm.get("algorithm_name")
#     family = algorithm.get("algorithm_family")

#     specificity = _normalize_specificity(
#         algorithm.get("specificity")
#     )

#     rank = _SPECIFICITY_RANK.get(
#         specificity,
#         0,
#     )

#     if rank >= 3 and name:
#         return {
#             "name": name,
#             "family": family,
#             "specificity": "specific",
#             "rank": rank,
#         }

#     if rank >= 2 and family:
#         return {
#             "name": None,
#             "family": family,
#             "specificity": "family",
#             "rank": rank,
#         }

#     return {
#         "name": None,
#         "family": family,
#         "specificity": "unknown",
#         "rank": 0,
#     }


# def _build_resolver_evidence(
#     *,
#     input_contract: dict[str, Any] | None,
#     input_structure: dict[str, Any] | None,
#     algorithm: dict[str, Any] | None,
#     description_type: str | None,
#     name_type: str | None,
#     compatibility: dict[str, Any],
#     fused_confidence: float,
# ) -> dict[str, Any]:
#     """
#     Build a stable, auditable evidence object.
#     """

#     return {
#         "input_contract": {
#             "contract_type": (
#                 input_contract.get("contract_type")
#                 if isinstance(input_contract, dict)
#                 else None
#             ),
#             "confidence": _safe_confidence(
#                 input_contract.get("confidence", 0.0)
#                 if isinstance(input_contract, dict)
#                 else 0.0
#             ),
#             "workload_type": (
#                 input_structure.get("workload_type")
#                 if isinstance(input_structure, dict)
#                 else None
#             ),
#         },
#         "algorithm": {
#             "name": (
#                 algorithm.get("algorithm_name")
#                 if isinstance(algorithm, dict)
#                 else None
#             ),
#             "family": (
#                 algorithm.get("algorithm_family")
#                 if isinstance(algorithm, dict)
#                 else None
#             ),
#             "specificity": (
#                 algorithm.get("specificity")
#                 if isinstance(algorithm, dict)
#                 else "unknown"
#             ),
#             "confidence": _safe_confidence(
#                 algorithm.get("confidence", 0.0)
#                 if isinstance(algorithm, dict)
#                 else 0.0
#             ),
#         },
#         "supporting_metadata": {
#             "description_input_structure": description_type,
#             "benchmark_name_input_structure": name_type,
#         },
#         "compatibility": compatibility,
#         "fusion": {
#             "confidence": fused_confidence,
#             "level": _confidence_level(
#                 fused_confidence
#             ),
#         },
#     }


# def _validate_benchmark_metadata(
#     metadata: Any,
# ) -> tuple[bool, list[str]]:
#     """
#     Validate the public metadata contract without making
#     assumptions about future metadata fields.
#     """

#     errors: list[str] = []

#     if not isinstance(metadata, dict):
#         return False, ["benchmark_metadata must be an object"]

#     for key in (
#         "name",
#         "category",
#         "description",
#         "source",
#         "confidence",
#         "provenance",
#         "generation",
#         "schema_version",
#     ):
#         if key not in metadata:
#             errors.append(
#                 f"benchmark_metadata.{key} is missing"
#             )

#     if not isinstance(
#         metadata.get("name"),
#         str,
#     ) or not metadata.get("name", "").strip():
#         errors.append(
#             "benchmark_metadata.name must be a non-empty string"
#         )

#     if not isinstance(
#         metadata.get("category"),
#         str,
#     ) or not metadata.get("category", "").strip():
#         errors.append(
#             "benchmark_metadata.category must be a non-empty string"
#         )

#     if not isinstance(
#         metadata.get("description"),
#         str,
#     ) or not metadata.get("description", "").strip():
#         errors.append(
#             "benchmark_metadata.description must be a non-empty string"
#         )

#     confidence = metadata.get("confidence")

#     if not isinstance(confidence, dict):
#         errors.append(
#             "benchmark_metadata.confidence must be an object"
#         )
#     else:
#         score = _safe_confidence(
#             confidence.get("score")
#         )

#         if score != confidence.get("score"):
#             errors.append(
#                 "benchmark_metadata.confidence.score must be numeric"
#             )

#         if confidence.get("level") not in {
#             "high",
#             "medium",
#             "low",
#         }:
#             errors.append(
#                 "benchmark_metadata.confidence.level is invalid"
#             )

#     return (
#         len(errors) == 0,
#         errors,
#     )


# def _finalize_resolver_result(
#     result: dict[str, Any],
# ) -> dict[str, Any]:
#     """
#     Final safety gate.

#     This does not invent missing values. It only validates and
#     records resolver integrity.
#     """

#     result.setdefault(
#         "resolver",
#         {},
#     )

#     result["resolver"].update(
#         {
#             "schema_version": RESOLVER_SCHEMA_VERSION,
#             "validated": True,
#         }
#     )

#     metadata = result.get(
#         "benchmark_metadata"
#     )

#     valid, errors = _validate_benchmark_metadata(
#         metadata
#     )

#     result["resolver"]["metadata_validation"] = {
#         "valid": valid,
#         "errors": errors,
#     }

#     if not valid:
#         # Metadata is presentation data. A malformed metadata
#         # object must never make an invalid workload executable.
#         result["can_generate"] = False
#         result["resolver"]["validated"] = False

#     return result


# def _build_mismatch_result(
#     code_type: str | None,
#     description_type: str | None,
#     name_type: str | None,
#     reason: str,
# ) -> dict[str, Any]:

#     return {
#         "status": "mismatch",
#         "workload_type": (
#             code_type
#             or description_type
#             or name_type
#             or "custom"
#         ),
#         "schema": None,
#         "detection": {
#             "method": "evidence-conflict",
#             "confidence": 0.0,
#             "reason": reason,
#             "evidence": {
#                 "reference_code": code_type,
#                 "description": description_type,
#                 "benchmark_name": name_type,
#             },
#         },
#         "can_generate": False,
#         "reason": (
#             "Workload mismatch detected. "
#             "Automatic workload generation has been disabled."
#         ),
#     }
# # ============================================================
# # MAIN BENCHMARK WORKLOAD RESOLVER
# # ============================================================

# def resolve_benchmark_workload(
#     benchmark_name: str | None,
#     description: str | None,
#     reference_code: str | None,
#     workload_type: str | None = None,
#     input_contract: dict[str, Any] | None = None,
# ) -> dict[str, Any]:
#     """
#     Production-grade benchmark workload resolver.

#     Responsibilities
#     ----------------
#     1. Obtain algorithm evidence exclusively from Algorithm Intelligence.
#     2. Obtain input structure exclusively from the verified Input Contract.
#     3. Keep supporting metadata non-authoritative.
#     4. Validate algorithm/input compatibility.
#     5. Fuse confidence conservatively.
#     6. Preserve algorithm specificity without upgrading weak evidence.
#     7. Detect contradictions explicitly.
#     8. Never hallucinate an algorithm or input structure.
#     9. Preserve deterministic generation behavior.
#     10. Attach auditable provenance/evidence.
#     11. Validate generated benchmark metadata.
#     12. Preserve backward-compatible resolver fields.

#     Important:
#         The resolver does not attempt to identify algorithms itself.
#         Algorithm Intelligence remains the sole algorithm authority.
#     """

#     normalized = normalize_workload_type(
#         workload_type
#     )

#     # ========================================================
#     # 1. ALGORITHM INTELLIGENCE
#     # ========================================================

#     algorithm_detection = (
#         _analyze_algorithm_with_intelligence(
#             reference_code
#         )
#     )

#     algorithm_reliable = _algorithm_is_reliable(
#         algorithm_detection
#     )

#     algorithm_specificity = (
#         _select_algorithm_specificity(
#             algorithm_detection
#         )
#     )

#     # ========================================================
#     # 2. SUPPORTING LEGACY / EXPLICIT EVIDENCE
#     #
#     # These signals are NEVER authoritative.
#     # ========================================================

#     description_detection = _detect_from_description(
#         description
#     )

#     name_detection = _detect_from_benchmark_name(
#         benchmark_name
#     )

#     description_type = _detected_type(
#         description_detection
#     )

#     name_type = _detected_type(
#         name_detection
#     )

#     # ========================================================
#     # 3. VERIFIED INPUT CONTRACT
#     # ========================================================

#     input_structure_result = (
#         normalize_input_structure_from_contract(
#             input_contract
#         )
#     )

#     input_reliable = _input_is_reliable(
#         input_structure_result,
#         input_contract,
#     )

#     # ========================================================
#     # 4. VERIFIED INPUT PATH
#     # ========================================================

#     if input_structure_result is not None:

#         input_confidence = _safe_confidence(
#             input_contract.get(
#                 "confidence",
#                 0.0,
#             )
#             if isinstance(input_contract, dict)
#             else 0.0
#         )

#         algorithm_confidence = _safe_confidence(
#             algorithm_detection.get(
#                 "confidence",
#                 0.0,
#             )
#             if isinstance(algorithm_detection, dict)
#             else 0.0
#         )

#         compatible, compatibility_reason, compatibility = (
#             _algorithm_compatible_with_input(
#                 algorithm_detection,
#                 input_structure_result,
#             )
#         )

#         fused_confidence = _fuse_confidence(
#             input_confidence,
#             algorithm_confidence,
#             algorithm_reliable=algorithm_reliable,
#             input_reliable=input_reliable,
#             compatible=compatible,
#         )

#         evidence = _build_resolver_evidence(
#             input_contract=input_contract,
#             input_structure=input_structure_result,
#             algorithm=algorithm_detection,
#             description_type=description_type,
#             name_type=name_type,
#             compatibility=compatibility,
#             fused_confidence=fused_confidence,
#         )

#         # ----------------------------------------------------
#         # HARD CONTRADICTION
#         # ----------------------------------------------------

#         if (
#             algorithm_reliable
#             and not compatible
#         ):
#             result = {
#                 "status": "mismatch",
#                 "workload_type": (
#                     input_structure_result.get(
#                         "workload_type"
#                     )
#                     or "custom"
#                 ),
#                 "schema": None,
#                 "input_structure": (
#                     input_structure_result
#                 ),
#                 "input_contract": input_contract,
#                 "algorithm": algorithm_detection,
#                 "can_generate": False,
#                 "reason": (
#                     "Verified input structure conflicts "
#                     "with the reliably identified algorithm."
#                 ),
#                 "detection": {
#                     "method": "resolver-compatibility-validation",
#                     "confidence": 0.0,
#                     "reason": compatibility_reason,
#                     "evidence": evidence,
#                 },
#                 "resolution": {
#                     "algorithm": algorithm_specificity,
#                     "input_structure": (
#                         input_structure_result.get(
#                             "workload_type"
#                         )
#                     ),
#                     "confidence": 0.0,
#                     "confidence_level": "low",
#                     "decision": "reject-conflicting-evidence",
#                 },
#             }

#             result = _attach_benchmark_metadata(
#                 result,
#                 input_structure_result,
#                 algorithm_detection,
#             )

#             return _finalize_resolver_result(
#                 result
#             )

#         # ----------------------------------------------------
#         # VALIDATED INPUT + ALGORITHM
#         # ----------------------------------------------------

#         capability = workload_generation_capability(
#             input_structure_result
#         )

#         result = _build_dual_track_workload_result(
#             input_structure_detection=(
#                 input_structure_result
#             ),
#             algorithm_detection=(
#                 algorithm_detection
#             ),
#         )

#         result.update(
#             capability
#         )

#         result["status"] = (
#             "known"
#             if input_structure_result.get(
#                 "status"
#             ) == "known"
#             else "custom"
#         )

#         result["input_contract"] = input_contract

#         result["detection"] = {
#             "method": "resolver-fusion",
#             "confidence": fused_confidence,
#             "reason": (
#                 "Input structure was obtained from the verified "
#                 "Input Contract and algorithmic behavior was "
#                 "analyzed independently by Algorithm Intelligence."
#             ),
#             "evidence": evidence,
#         }

#         result["resolution"] = {
#             "algorithm": algorithm_specificity,
#             "input_structure": (
#                 input_structure_result.get(
#                     "workload_type"
#                 )
#             ),
#             "confidence": fused_confidence,
#             "confidence_level": _confidence_level(
#                 fused_confidence
#             ),
#             "decision": (
#                 "verified"
#                 if algorithm_reliable
#                 else "verified-input-only"
#             ),
#             "evidence": evidence,
#         }

#         result = _attach_benchmark_metadata(
#             result,
#             input_structure_result,
#             algorithm_detection,
#         )

#         return _finalize_resolver_result(
#             result
#         )

#     # ========================================================
#     # 5. NO VERIFIED INPUT CONTRACT
#     #
#     # Explicit/metadata hints remain non-authoritative.
#     # Generation stays disabled.
#     # ========================================================

#     fallback_structure = None

#     if (
#         normalized
#         and is_known_workload(normalized)
#     ):
#         fallback_structure = resolve_workload(
#             normalized
#         )

#     elif description_detection is not None:
#         fallback_structure = dict(
#             description_detection
#         )

#     elif name_detection is not None:
#         fallback_structure = dict(
#             name_detection
#         )

#     if fallback_structure is not None:

#         result = _build_dual_track_workload_result(
#             input_structure_detection=(
#                 fallback_structure
#             ),
#             algorithm_detection=(
#                 algorithm_detection
#             ),
#         )

#         algorithm_confidence = _safe_confidence(
#             algorithm_detection.get(
#                 "confidence",
#                 0.0,
#             )
#             if isinstance(algorithm_detection, dict)
#             else 0.0
#         )

#         result.update(
#             {
#                 "status": "uncertain",
#                 "can_generate": False,
#                 "detection": {
#                     "method": "unverified-input-contract",
#                     "confidence": 0.0,
#                     "reason": (
#                         "A workload structure was suggested by "
#                         "metadata or explicit configuration, but "
#                         "no verified Input Contract was provided. "
#                         "Automatic workload generation is disabled."
#                     ),
#                     "evidence": {
#                         "input_contract": None,
#                         "description_input_structure": (
#                             description_type
#                         ),
#                         "benchmark_name_input_structure": (
#                             name_type
#                         ),
#                         "explicit_workload_type": normalized,
#                         "algorithm": (
#                             algorithm_detection
#                             if algorithm_detection
#                             else None
#                         ),
#                     },
#                 },
#                 "reason": (
#                     "Automatic workload generation requires "
#                     "a verified Input Contract."
#                 ),
#                 "resolution": {
#                     "algorithm": algorithm_specificity,
#                     "input_structure": (
#                         fallback_structure.get(
#                             "workload_type"
#                         )
#                     ),
#                     "confidence": 0.0,
#                     "confidence_level": "low",
#                     "algorithm_confidence": (
#                         algorithm_confidence
#                     ),
#                     "decision": "unverified-input",
#                 },
#             }
#         )

#         result = _attach_benchmark_metadata(
#             result,
#             fallback_structure,
#             algorithm_detection,
#         )

#         return _finalize_resolver_result(
#             result
#         )

#     # ========================================================
#     # 6. NOTHING VERIFIED
#     # ========================================================

#     result = _build_dual_track_workload_result(
#         input_structure_detection=None,
#         algorithm_detection=algorithm_detection,
#     )

#     result.update(
#         {
#             "status": "custom",
#             "can_generate": False,
#             "detection": {
#                 "method": "no-input-contract",
#                 "confidence": 0.0,
#                 "reason": (
#                     "No verified Input Contract was provided "
#                     "and no reliable fallback input structure "
#                     "was available. Algorithmic behavior was "
#                     "still analyzed independently."
#                 ),
#                 "evidence": {
#                     "input_contract": None,
#                     "description_input_structure": (
#                         description_type
#                     ),
#                     "benchmark_name_input_structure": (
#                         name_type
#                     ),
#                     "explicit_workload_type": normalized,
#                     "algorithm": (
#                         algorithm_detection
#                         if algorithm_detection
#                         else None
#                     ),
#                 },
#             },
#             "reason": (
#                 "No deterministic input structure can be "
#                 "generated without a verified Input Contract."
#             ),
#             "resolution": {
#                 "algorithm": algorithm_specificity,
#                 "input_structure": None,
#                 "confidence": 0.0,
#                 "confidence_level": "low",
#                 "decision": "no-verified-input",
#             },
#         }
#     )

#     result = _attach_benchmark_metadata(
#         result,
#         None,
#         algorithm_detection,
#     )

#     return _finalize_resolver_result(
#         result
#     )








from __future__ import annotations

from typing import Any
# import re

from app.services.custom_workload_generator import (
    WORKLOAD_REGISTRY,
)

from app.services.algorithm_intelligence import (
    analyze_algorithm,
)
from app.services.benchmark_metadata_intelligence import (
    generate_benchmark_metadata,
)
# from app.services.algorithm_intelligence import analyze_algorithm


# ============================================================
# KNOWN WORKLOAD SCHEMAS
# ============================================================

WORKLOAD_SCHEMAS: dict[str, dict[str, Any]] = {

    "numeric-array": {
        "type": "array",
        "item_type": "integer",
        "count_field": "n",
        "description": (
            "A one-dimensional array of integers."
        ),
    },

    "integer-array": {
        "type": "array",
        "item_type": "integer",
        "count_field": "n",
        "description": "A one-dimensional array of integers.",
    },

    "float-array": {
        "type": "array",
        "item_type": "float",
        "count_field": "n",
        "description": "A one-dimensional array of floating-point values.",
    },

    "character-array": {
        "type": "array",
        "item_type": "character",
        "count_field": "n",
        "description": "A one-dimensional array of characters.",
    },

    "text": {
        "type": "text",
        "item_type": "string",
        "count_field": "n",
        "description": (
            "A collection of plain-text strings."
        ),
    },

    "url": {
        "type": "array",
        "item_type": "url",
        "count_field": "n",
        "description": (
            "A collection of URL strings."
        ),
    },

    "html": {
        "type": "array",
        "item_type": "html",
        "count_field": "n",
        "description": (
            "A collection of HTML fragments."
        ),
    },

    "json": {
        "type": "json-array",
        "item_type": "object",
        "count_field": None,
        "description": (
            "A JSON array containing structured records."
        ),
    },

    "csv": {
        "type": "tabular",
        "item_type": "record",
        "count_field": None,
        "description": (
            "Tabular CSV records with a header row."
        ),
    },

    "matrix": {
        "type": "matrix",
        "item_type": "integer",
        "rows_field": "n",
        "columns_field": "n",
        "description": (
            "A square two-dimensional integer matrix."
        ),
    },

    "graph": {
        "type": "graph",
        "representation": "edge-list",
        "node_count_field": "vertices",
        "edge_count_field": "edges",
        "description": (
            "An undirected graph represented using an edge list."
        ),
    },

    "tree": {
        "type": "tree",
        "representation": "parent-child",
        "node_count_field": "n",
        "description": (
            "A rooted tree represented using parent-child edges."
        ),
    },

    "multiple-arrays": {
        "type": "multiple-arrays",
        "arrays": [
            {
                "name": "array_a",
                "item_type": "integer",
            },
            {
                "name": "array_b",
                "item_type": "integer",
            },
        ],
        "count_field": "n",
        "description": (
            "Two one-dimensional integer arrays."
        ),
    },
}

# ============================================================
# INPUT CONTRACT -> GENERATOR INPUT STRUCTURE
# ============================================================

CONTRACT_TO_INPUT_STRUCTURE: dict[str, str] = {
    # --------------------------------------------------------
    # Basic / fallback
    # --------------------------------------------------------
    "no-input": "no-input",
    "stdin-present": "stdin-present",

    # --------------------------------------------------------
    # Scalars
    # --------------------------------------------------------
    "integer-scalar": "integer-scalar",
    "integer-scalars": "integer-scalars",
    "float-scalar": "float-scalar",
    "float-scalars": "float-scalars",
    "character-scalar": "character-scalar",
    "mixed-scalars": "mixed-scalars",

    # --------------------------------------------------------
    # Strings
    # --------------------------------------------------------
    "string-token": "string-token",
    "string-line": "string-line",
    "string-array": "string-array",
    "string-lines": "string-lines",
    "scalar-plus-line": "scalar-plus-line",
    "size-plus-string": "size-plus-string",
    "size-plus-two-strings": "size-plus-two-strings",
    "size-plus-strings": "size-plus-strings",

    # --------------------------------------------------------
    # Character / stream input
    # --------------------------------------------------------
    "character-stream": "character-stream",

    # --------------------------------------------------------
    # Arrays
    # --------------------------------------------------------
    "integer-array": "integer-array",
    "float-array": "float-array",
    "character-array": "character-array",
    "jagged-array": "jagged-array",
    "array-plus-target": "array-plus-target",
    "multiple-arrays": "multiple-arrays",
    "array-with-queries": "array-with-queries",
    "array-with-range-queries": "array-with-range-queries",

    # --------------------------------------------------------
    # Matrix
    # --------------------------------------------------------
    "matrix": "matrix",
    "matrix-plus-target": "matrix-plus-target",
    "jagged-matrix": "jagged-matrix",
    "character-grid": "character-grid",
    "adjacency-matrix": "adjacency-matrix",

    # --------------------------------------------------------
    # Graph
    # --------------------------------------------------------
    "graph": "graph",
    "weighted-graph": "weighted-graph",
    "graph-with-source": "graph-with-source",
    "weighted-graph-with-source": "weighted-graph-with-source",

    # --------------------------------------------------------
    # Tree
    # --------------------------------------------------------
    "tree": "tree",
    "parent-array-tree": "parent-array-tree",
    "binary-tree-level-order": "binary-tree-level-order",

    # --------------------------------------------------------
    # Test cases
    # --------------------------------------------------------
    "test-cases": "test-cases",
    "test-cases-array": "test-cases-array",
    "test-cases-matrix": "test-cases-matrix",

    # --------------------------------------------------------
    # EOF / Sentinel
    # --------------------------------------------------------
    "eof-stream": "eof-stream",
    "eof-records": "eof-records",
    "eof-lines": "eof-lines",
    "sentinel-stream": "sentinel-stream",
    "sentinel-records": "sentinel-records",

    # --------------------------------------------------------
    # Records
    # --------------------------------------------------------
    "pair-records": "pair-records",
    "triple-records": "triple-records",
    "pairs": "pairs",
    "triples": "triples",
    "tuple-records": "tuple-records",
    "structured-records": "structured-records",
    "key-value-records": "key-value-records",

    # --------------------------------------------------------
    # Queries / commands / delimited
    # --------------------------------------------------------
    "query-stream": "query-stream",
    "range-queries": "range-queries",
    "command-stream": "command-stream",
    "delimited-lines": "delimited-lines",
    "scanf-input": "scanf-input",

    # --------------------------------------------------------
    # Collection-specific
    # --------------------------------------------------------
    "stack-input": "stack-input",
    "queue-input": "queue-input",
    "set-input": "set-input",
}

def normalize_input_structure_from_contract(
    input_contract: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """
    Convert the exact input contract into the normalized
    generator-facing input structure.

    Input Contract Analyzer is the authority for contract detection.
    This function performs mapping only; it does not inspect code.
    """

    if not input_contract:
        return None

    contract_type = normalize_workload_type(
        input_contract.get("contract_type")
    )

    if not contract_type:
        return None

    input_structure_type = CONTRACT_TO_INPUT_STRUCTURE.get(
        contract_type
    )

    if not input_structure_type:
        return None

    schema = WORKLOAD_SCHEMAS.get(
        input_structure_type
    )

    return {
        "status": "known" if schema is not None else "custom",
        "workload_type": input_structure_type,
        "schema": schema,
        "source": "input-contract",
        "contract_type": contract_type,
        "contract": input_contract,
        "detection": {
            "method": "input-contract-mapping",
            "confidence": input_contract.get("confidence", 1.0),
            "reason": (
                "Input structure was normalized directly "
                "from the exact Input Contract."
            ),
        },
    }
# ============================================================
# HELPERS
# ============================================================

def normalize_workload_type(
    workload_type: str | None,
) -> str | None:

    if workload_type is None:
        return None

    normalized = (
        workload_type
        .strip()
        .lower()
    )

    return normalized or None


def _combined_text(
    benchmark_name: str | None,
    description: str | None,
    reference_code: str | None,
) -> str:

    return " ".join(
        [
            benchmark_name or "",
            description or "",
            reference_code or "",
        ]
    ).lower()


def _contains_any(
    text: str,
    keywords: list[str],
) -> bool:

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


# ============================================================
# CHECK KNOWN WORKLOAD
# ============================================================

def is_known_workload(
    workload_type: str | None,
) -> bool:

    normalized = normalize_workload_type(
        workload_type
    )

    if not normalized:
        return False

    return (
        normalized in WORKLOAD_REGISTRY
        and normalized in WORKLOAD_SCHEMAS
    )


# ============================================================
# DETERMINISTIC WORKLOAD DETECTION
# ============================================================

def detect_input_structure_from_content(
    benchmark_name: str | None,
    description: str | None,
    reference_code: str | None,
) -> dict[str, Any] | None:
    """
    Detect input/data structure using deterministic rules.

    This function must NOT identify the algorithmic behavior
    of the program.
    """

    text = _combined_text(
        benchmark_name,
        description,
        reference_code,
    )

    # ========================================================
    # 1. ARRAY + TARGET
    # ========================================================

    has_array = _contains_any(
        text,
        [
            "array",
            "array[",
            "vector",
            "list",
            "integer[]",
            "arr[",
        ],
    )

    has_target = _contains_any(
        text,
        [
            "target",
            "target value",
            "target number",
            "sum equals",
        ],
    )

    if has_array and has_target:

        return {
            "status": "custom",
            "workload_type": "array-plus-target",
            "schema": {
                "type": "composite",
                "fields": [
                    {
                        "name": "n",
                        "type": "integer",
                    },
                    {
                        "name": "array",
                        "type": "integer[]",
                    },
                    {
                        "name": "target",
                        "type": "integer",
                    },
                ],
                "description": (
                    "An integer array accompanied "
                    "by a separate target value."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Benchmark contains both array/list "
                    "input and a separate target value."
                ),
            },
        }

    # ========================================================
    # 2. MULTIPLE TEST CASES
    # ========================================================

    if _contains_any(
        text,
        [
            "multiple test cases",
            "multiple test case",
            "test cases",
            "test case",
            "number of test cases",
            "read t",
            "cin >> t",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "multiple-test-cases",
            "schema": {
                "type": "multiple-test-cases",
                "test_cases_field": "T",
                "description": (
                    "Multiple independent test cases."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Benchmark metadata or reference code "
                    "contains multiple-test-case input patterns."
                ),
            },
        }

    # ========================================================
    # 3. MATRIX
    # ========================================================

    if _contains_any(
        text,
        [
            "matrix",
            "matrices",
            "2d array",
            "2-d array",
            "two dimensional array",
            "two-dimensional array",
            "rows and columns",
            "row and column",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "matrix",
            "schema": WORKLOAD_SCHEMAS["matrix"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Matrix or two-dimensional array "
                    "input was detected."
                ),
            },
        }

    # ========================================================
    # 4. GRAPH
    # ========================================================

    if _contains_any(
        text,
        [
            "graph",
            "vertices",
            "edges",
            "edge list",
            "adjacency list",
            "adjacency matrix",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "graph",
            "schema": WORKLOAD_SCHEMAS["graph"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Graph-specific input patterns were detected."
                ),
            },
        }

    # ========================================================
    # 5. TREE
    # ========================================================

    if _contains_any(
        text,
        [
            "binary tree",
            "tree nodes",
            "parent child",
            "parent-child",
            "root node",
            "tree traversal",
            "tree input",
            "tree",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "tree",
            "schema": WORKLOAD_SCHEMAS["tree"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Tree-specific input patterns were detected."
                ),
            },
        }

    # ========================================================
    # 6. LINKED LIST
    # ========================================================

    if _contains_any(
        text,
        [
            "linked list",
            "linked-list",
            "node.next",
            "next pointer",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "linked-list",
            "schema": {
                "type": "linked-list",
                "node_value_type": "integer",
                "node_count_field": "n",
                "description": (
                    "A linked-list-specific input structure."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Benchmark contains linked-list structure."
                ),
            },
        }

    # ========================================================
    # 7. CHARACTERS
    # ========================================================

    if _contains_any(
        text,
        [
            "character",
            "characters",
            "char array",
            "char[]",
            "sequence of chars",
            "string of characters",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "characters",
            "schema": {
                "type": "array",
                "item_type": "character",
                "count_field": "n",
                "description": (
                    "A sequence or array of characters."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Character-based input patterns were detected."
                ),
            },
        }

    # ========================================================
    # 8. BOOLEAN
    # ========================================================

    if _contains_any(
        text,
        [
            "boolean",
            "bool",
            "true false",
            "true/false",
            "binary flag",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "boolean-array",
            "schema": {
                "type": "array",
                "item_type": "boolean",
                "count_field": "n",
                "description": (
                    "A sequence of boolean values."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Boolean input patterns were detected."
                ),
            },
        }

    # ========================================================
    # 9. FLOAT / DECIMAL
    # ========================================================

    if _contains_any(
        text,
        [
            "floating point",
            "floating-point",
            "decimal",
            "float array",
            "real numbers",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "float-array",
            "schema": {
                "type": "array",
                "item_type": "float",
                "count_field": "n",
                "description": (
                    "A one-dimensional array "
                    "of floating-point values."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Floating-point or decimal "
                    "input patterns were detected."
                ),
            },
        }

    # ========================================================
    # 10. JSON
    # ========================================================

    if _contains_any(
        text,
        [
            "json",
            "json object",
            "json data",
            "json records",
            "nested json",
        ],
    ):

        return {
            "status": "known",
            "workload_type": "json",
            "schema": WORKLOAD_SCHEMAS["json"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "JSON input structure was explicitly mentioned."
                ),
            },
        }

    # ========================================================
    # 11. CSV / TABULAR
    # ========================================================

    if _contains_any(
        text,
        [
            "csv",
            "comma separated",
            "comma-separated",
            "tabular",
            "table records",
            "tabular data",
        ],
    ):

        return {
            "status": "known",
            "workload_type": "csv",
            "schema": WORKLOAD_SCHEMAS["csv"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "CSV or tabular input structure was detected."
                ),
            },
        }

    # ========================================================
    # 12. URL
    # ========================================================

    if _contains_any(
        text,
        [
            "url",
            "urls",
            "web address",
            "http://",
            "https://",
            "endpoint url",
        ],
    ):

        return {
            "status": "known",
            "workload_type": "url",
            "schema": WORKLOAD_SCHEMAS["url"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "URL-based input structure was detected."
                ),
            },
        }

    # ========================================================
    # 13. HTML / XML
    # ========================================================

    if _contains_any(
        text,
        [
            "html",
            "html input",
            "html document",
            "html fragment",
            "xml",
            "xml document",
            "<div>",
            "<html>",
        ],
    ):

        return {
            "status": "known" if "html" in WORKLOAD_REGISTRY else "custom",
            "workload_type": (
                "html"
                if "html" in WORKLOAD_REGISTRY
                else "html"
            ),
            "schema": WORKLOAD_SCHEMAS["html"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "HTML/XML markup input was detected."
                ),
            },
        }

    # ========================================================
    # 14. PAIRS / TUPLES
    # ========================================================

    if _contains_any(
        text,
        [
            "pair",
            "pairs",
            "tuple",
            "tuples",
            "(x,y)",
            "(x, y)",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "pairs",
            "schema": {
                "type": "array",
                "item_type": "pair",
                "count_field": "n",
                "description": (
                    "A collection of pair or tuple values."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Pair or tuple input structure was detected."
                ),
            },
        }

    # ========================================================
    # 15. KEY-VALUE
    # ========================================================

    if _contains_any(
        text,
        [
            "key-value",
            "key value",
            "key/value",
            "name=value",
            "key=value",
            "dictionary",
            "map input",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "key-value",
            "schema": {
                "type": "key-value",
                "item_type": "record",
                "description": (
                    "Input consists of key-value records."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Key-value input structure was detected."
                ),
            },
        }

    # ========================================================
    # 16. DATE / TIME
    # ========================================================

    if _contains_any(
        text,
        [
            "date",
            "dates",
            "timestamp",
            "timestamps",
            "datetime",
            "date/time",
            "time series",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "datetime",
            "schema": {
                "type": "array",
                "item_type": "datetime",
                "count_field": "n",
                "description": (
                    "A collection of date or time values."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Date/time input structure was detected."
                ),
            },
        }

    # ========================================================
    # 17. MIXED RECORDS
    # ========================================================

    if _contains_any(
        text,
        [
            "mixed datatype",
            "mixed data type",
            "mixed records",
            "mixed fields",
            "heterogeneous records",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "mixed-records",
            "schema": {
                "type": "records",
                "item_type": "mixed",
                "count_field": "n",
                "description": (
                    "Records containing multiple data types."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Mixed-type record structure was detected."
                ),
            },
        }

    # ========================================================
    # 18. BINARY
    # ========================================================

    if _contains_any(
        text,
        [
            "binary data",
            "binary input",
            "bytes",
            "byte array",
            "byte[]",
        ],
    ):

        return {
            "status": "custom",
            "workload_type": "binary",
            "schema": {
                "type": "bytes",
                "item_type": "byte",
                "description": (
                    "Binary or byte-oriented input."
                ),
            },
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Binary or byte input patterns were detected."
                ),
            },
        }
        # ========================================================
    # 19. NUMERIC ARRAY
    # ========================================================

    if has_array:

        return {
            "status": "known",
            "workload_type": "numeric-array",
            "schema": WORKLOAD_SCHEMAS["numeric-array"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "A one-dimensional numeric array "
                    "input was detected."
                ),
            },
        }
    
    # ========================================================
    #  20. GENERIC TEXT / STRING
    # ========================================================

    if _contains_any(
        text,
        [
            "text input",
            "plain text",
            "string input",
            "string data",
            "text processing",
            "words",
            "sentences",
        ],
    ):

        return {
            "status": "known",
            "workload_type": "text",
            "schema": WORKLOAD_SCHEMAS["text"],
            "detection": {
                "method": "deterministic-rule",
                "confidence": 1.0,
                "reason": (
                    "Text or string input structure was detected."
                ),
            },
        }

    # ========================================================
    # NO SAFE MATCH
    # ========================================================

    return None


# Backward-compatible alias for existing callers.
detect_workload_from_content = detect_input_structure_from_content
# Backward-compatible alias for existing callers.
detect_reference_input_structure = detect_input_structure_from_content
detect_reference_input_workload = detect_reference_input_structure


# ============================================================
# RESOLVE EXPLICIT WORKLOAD
# ============================================================

def resolve_workload(
    workload_type: str | None,
) -> dict[str, Any]:

    normalized = normalize_workload_type(
        workload_type
    )

    if is_known_workload(normalized):

        return {
            "status": "known",
            "workload_type": normalized,
            "schema": WORKLOAD_SCHEMAS[normalized],
            "detection": {
                "method": "registry",
                "confidence": 1.0,
                "reason": (
                    "Workload type was explicitly "
                    "provided and is registered."
                ),
            },
        }

    return {
        "status": "custom",
        "workload_type": (
            normalized
            if normalized
            else "custom"
        ),
        "schema": None,
        "detection": {
            "method": "unresolved",
            "confidence": 0.0,
            "reason": (
                "No registered workload type was found."
            ),
        },
    }


def workload_generation_capability(
    workload: dict[str, Any],
) -> dict[str, Any]:
    """
    Determine whether the resolved workload can actually be
    generated deterministically by the current backend.

    Registry workloads are generated through WORKLOAD_REGISTRY.

    Custom workloads are generated through generate_schema_input()
    in custom_benchmark_engine.py.
    """

    workload_type = (
        workload.get("workload_type")
    )

    schema = workload.get("schema")

    normalized_type = normalize_workload_type(
        workload_type
    )

    # --------------------------------------------------------
    # No usable workload type/schema
    # --------------------------------------------------------

    if (
        not normalized_type
        or normalized_type == "custom"
    ):
        return {
            "can_generate": False,
            "reason": (
                "No deterministic workload generator "
                "is available for this workload."
            ),
        }

    # --------------------------------------------------------
    # Custom-schema generators do not require a WORKLOAD_SCHEMAS
    # entry because generate_schema_input() owns their concrete
    # serialization format.
    # --------------------------------------------------------

    custom_schema_generators = {
        "characters", "character-array",
        "float-array", "floating-point", "decimal", "decimal-array",
        "boolean", "boolean-array", "bool-array",
        "array-plus-target", "array-target",
        "multiple-test-cases", "test-cases",
        "pairs", "tuples", "pairs-tuples",
        "key-value", "key-value-data", "key-value-records",
        "mixed-records", "mixed-datatype-records",
        "date", "datetime", "date-time", "timestamp",
    }

    if normalized_type in custom_schema_generators:
        return {
            "can_generate": True,
            "reason": (
                "A deterministic custom-schema generator "
                "is available for this workload."
            ),
        }

    if schema is None:
        return {
            "can_generate": False,
            "reason": (
                "No deterministic workload generator "
                "is available for this workload."
            ),
        }

    # --------------------------------------------------------
    # Registry workloads
    # --------------------------------------------------------

    if (
        normalized_type in WORKLOAD_REGISTRY
        and normalized_type in WORKLOAD_SCHEMAS
    ):
        return {
            "can_generate": True,
            "reason": (
                "A deterministic registry generator "
                "is available for this workload."
            ),
        }

    # --------------------------------------------------------
    # Generic schema support
    # --------------------------------------------------------

    schema_type = schema.get("type")

    if schema_type == "array":

        item_type = schema.get(
            "item_type"
        )

        if item_type in {
            "integer",
            "float",
            "character",
        }:
            return {
                "can_generate": True,
                "reason": (
                    "A deterministic generic array "
                    "generator is available for this schema."
                ),
            }

    # --------------------------------------------------------
    # No actual generator available
    # --------------------------------------------------------

    return {
        "can_generate": False,
        "reason": (
            "A workload schema was detected, but the "
            "backend does not currently have a deterministic "
            "generator for this workload type."
        ),
    }


def _analyze_algorithm_with_intelligence(
    reference_code: str | None,
) -> dict[str, Any] | None:
    """
    Analyze algorithmic behavior using Algorithm Intelligence.

    Algorithm Intelligence owns computational behavior while
    input structure remains the responsibility of the input
    contract analyzer.
    """

    if not reference_code or not reference_code.strip():
        return None

    try:
        from app.services.reference_code_analyzer import (
            detect_reference_language,
        )

        language_result = detect_reference_language(
            reference_code
        )

        detected_language = language_result.get(
            "language"
        )

        language_map = {
            "C": "c",
            "C++": "cpp",
            "Java": "java",
            "Python": "python",
            "JavaScript": "javascript",
            "Go": "go",
            "Rust": "rust",
            "C#": "csharp",
            "Kotlin": "kotlin",
            "PHP": "php",
        }

        language = language_map.get(
            detected_language,
            detected_language,
        )

        if not language:
            return None

        analysis = analyze_algorithm(
            reference_code,
            language,
        )

    except Exception as exc:
        return {
            "workload_type": "custom",
            "algorithm_family": "custom",
            "algorithm_name": "custom",
            "specificity": "unknown",
            "confidence": 0.0,
            "reason": (
                "Algorithm Intelligence could not analyze "
                "the reference implementation."
            ),
            "evidence": {
                "error": str(exc),
            },
            "complexity": None,
            "detection_method": "algorithm-intelligence-error",
            "parser": None,
            "parse_success": False,
            "parse_error_count": None,
        }

    if not analysis:
        return None

    algorithm = analysis.get(
        "algorithm",
        {},
    )

    complexity = analysis.get(
        "complexity"
    )

    detection = analysis.get(
        "detection",
        {},
    )

    algorithm_family = algorithm.get(
        "family"
    )

    if not algorithm_family:
        return None

    return {
        "workload_type": algorithm_family,
        "algorithm_family": algorithm_family,
        "algorithm_name": algorithm.get(
            "name"
        ),
        "specificity": algorithm.get(
            "specificity"
        ),
        "confidence": algorithm.get(
            "confidence",
            0.0,
        ),
        "reason": algorithm.get(
            "evidence"
        ),
        "evidence": algorithm.get(
            "evidence"
        ),
        "complexity": complexity,
        "detection_method": detection.get(
            "method",
            "algorithm-intelligence",
        ),
        "parser": detection.get(
            "parser"
        ),
        "parse_success": detection.get(
            "parse_success"
        ),
        "parse_error_count": detection.get(
            "parse_error_count"
        ),
    }


# def _analyze_algorithm_with_intelligence(
#     reference_code: str | None,
# ) -> dict[str, Any] | None:
#     """
#     Analyze computational behavior using Algorithm Intelligence.

#     Algorithm Intelligence owns algorithmic behavior.
#     Input Contract Analyzer remains authoritative for
#     input structure and generation schema.
#     """
#     if not reference_code or not reference_code.strip():
#         return None

#     analysis = analyze_algorithm(reference_code)

#     if not analysis:
#         return None

#     algorithm_family = analysis.get("algorithm_family")

#     if not algorithm_family:
#         return None

#     evidence = analysis.get("evidence")

#     return {
#         "workload_type": algorithm_family,
#         "algorithm_family": algorithm_family,
#         "algorithm_name": analysis.get("algorithm_name"),
#         "specificity": analysis.get("specificity"),
#         "confidence": analysis.get("confidence", 0.0),
#         "reason": (
#             evidence.get("summary")
#             if isinstance(evidence, dict)
#             else None
#         ),
#         "evidence": evidence,
#         "complexity": analysis.get("complexity"),
#         "detection_method": analysis.get(
#             "detection_method",
#             "algorithm-intelligence",
#         ),
#         "parser": analysis.get("parser"),
#         "parse_success": analysis.get("parse_success"),
#         "parse_error_count": analysis.get(
#             "parse_error_count"
#         ),
#     }


def _build_dual_track_workload_result(
    input_structure_detection: dict[str, Any] | None,
    algorithm_detection: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Build a backward-compatible result that keeps
    input structure and algorithmic workload separate.
    """

    result: dict[str, Any] = {
        "input_structure": input_structure_detection,
        "algorithm": algorithm_detection,
    }

    # --------------------------------------------------------
    # PUBLIC ALGORITHM FIELD COMPATIBILITY
    # --------------------------------------------------------
    # Algorithm Intelligence internally uses:
    #     algorithm_name
    #     algorithm_family
    #
    # Public consumers may use:
    #     name
    #     family
    #
    # Preserve both representations.
    if isinstance(algorithm_detection, dict):
        algorithm_detection.setdefault(
            "name",
            algorithm_detection.get("algorithm_name"),
        )

        algorithm_detection.setdefault(
            "family",
            algorithm_detection.get("algorithm_family"),
        )

    if input_structure_detection is not None:
        result["workload_type"] = input_structure_detection.get(
            "workload_type"
        )
        result["schema"] = input_structure_detection.get(
            "schema"
        )
    else:
        result["workload_type"] = "custom"
        result["schema"] = None

    return result


def _attach_benchmark_metadata(
    result: dict[str, Any],
    input_structure: dict[str, Any] | None,
    algorithm_detection: dict[str, Any] | None,
) -> dict[str, Any]:
    """Attach presentation metadata without changing workload resolution."""
    result["benchmark_metadata"] = generate_benchmark_metadata(
        input_structure=input_structure,
        algorithm=algorithm_detection,
    )
    return result


def _detect_from_description(
    description: str | None,
) -> dict[str, Any] | None:
    """
    Detect workload using ONLY the benchmark description.
    """

    if not description or not description.strip():
        return None

    return detect_input_structure_from_content(
        benchmark_name=None,
        description=description,
        reference_code=None,
    )


def _detect_from_benchmark_name(
    benchmark_name: str | None,
) -> dict[str, Any] | None:
    """
    Detect workload using ONLY the benchmark name.
    """

    if not benchmark_name or not benchmark_name.strip():
        return None

    return detect_input_structure_from_content(
        benchmark_name=benchmark_name,
        description=None,
        reference_code=None,
    )


def _detected_type(
    result: dict[str, Any] | None,
) -> str | None:

    if result is None:
        return None

    return normalize_workload_type(
        result.get("workload_type")
    )

# ============================================================
# RESOLVER INTELLIGENCE / HARDENING
# ============================================================

RESOLVER_SCHEMA_VERSION = 2

CONFIDENCE_HIGH = 0.90
CONFIDENCE_MEDIUM = 0.70

_SPECIFICITY_RANK = {
    "specific": 3,
    "family": 2,
    "generic": 1,
    "unknown": 0,
    None: 0,
}

# ------------------------------------------------------------
# Algorithm -> compatible input families
#
# This layer does NOT identify algorithms.
# Algorithm Intelligence remains the sole algorithm authority.
#
# These rules only detect obvious semantic contradictions.
# ------------------------------------------------------------

_ALGORITHM_INPUT_COMPATIBILITY: dict[str, set[str]] = {
    # Searching
    "binary-search": {
        "integer-array",
        "array-plus-target",
        "string-array",
        "string-token",
        "string-line",
        "character-array",
        "characters",
    },
    "linear-search": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
        "array-plus-target",
        "string-token",
        "string-line",
    },

    # Sorting
    "bubble-sort": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
        "array-plus-target",
    },
    "selection-sort": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
    },
    "insertion-sort": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
    },
    "merge-sort": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
    },
    "quick-sort": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
    },
    "heap-sort": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
    },

    # Graph algorithms
    "bfs": {
        "graph",
        "weighted-graph",
        "graph-with-source",
        "weighted-graph-with-source",
        "adjacency-matrix",
    },
    "dfs": {
        "graph",
        "weighted-graph",
        "graph-with-source",
        "weighted-graph-with-source",
        "adjacency-matrix",
        "tree",
        "parent-array-tree",
        "binary-tree-level-order",
    },
    "dijkstra": {
        "weighted-graph",
        "weighted-graph-with-source",
        "graph-with-source",
    },

    # Tree algorithms
    "tree-traversal": {
        "tree",
        "parent-array-tree",
        "binary-tree-level-order",
    },

    # Array/string techniques
    "two-pointers": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
        "string-token",
        "string-line",
        "array-plus-target",
    },
    "sliding-window": {
        "integer-array",
        "float-array",
        "character-array",
        "string-array",
        "string-token",
        "string-line",
    },
    "prefix-sum": {
        "integer-array",
        "float-array",
        "matrix",
        "matrix-plus-target",
        "array-with-queries",
        "array-with-range-queries",
    },

    # Matrix
    "matrix-processing": {
        "matrix",
        "matrix-plus-target",
        "jagged-matrix",
        "character-grid",
        "adjacency-matrix",
    },
}


def _safe_confidence(value: Any) -> float:
    """
    Normalize confidence into [0.0, 1.0].

    Invalid confidence values never become evidence.
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.0

    if value != value:  # NaN
        return 0.0

    return max(0.0, min(1.0, value))


def _confidence_level(score: float) -> str:
    score = _safe_confidence(score)

    if score >= CONFIDENCE_HIGH:
        return "high"

    if score >= CONFIDENCE_MEDIUM:
        return "medium"

    return "low"


def _normalize_algorithm_name(
    algorithm_name: str | None,
) -> str | None:
    if not algorithm_name:
        return None

    normalized = (
        str(algorithm_name)
        .strip()
        .lower()
        .replace("_", "-")
        .replace(" ", "-")
    )

    return normalized or None


def _normalize_specificity(
    specificity: str | None,
) -> str:
    if not specificity:
        return "unknown"

    normalized = (
        str(specificity)
        .strip()
        .lower()
    )

    if normalized in _SPECIFICITY_RANK:
        return normalized

    return "unknown"


def _algorithm_is_reliable(
    algorithm: dict[str, Any] | None,
) -> bool:
    if not isinstance(algorithm, dict):
        return False

    name = _normalize_algorithm_name(
        algorithm.get("algorithm_name")
    )

    confidence = _safe_confidence(
        algorithm.get("confidence", 0.0)
    )

    specificity = _normalize_specificity(
        algorithm.get("specificity")
    )

    if not name:
        return False

    if name in {"custom", "unknown", "none"}:
        return False

    return (
        confidence >= CONFIDENCE_MEDIUM
        and specificity != "unknown"
    )


def _input_is_reliable(
    input_structure: dict[str, Any] | None,
    input_contract: dict[str, Any] | None,
) -> bool:
    if not isinstance(input_structure, dict):
        return False

    if not isinstance(input_contract, dict):
        return False

    workload_type = normalize_workload_type(
        input_structure.get("workload_type")
    )

    if not workload_type:
        return False

    confidence = _safe_confidence(
        input_contract.get("confidence", 0.0)
    )

    return confidence >= CONFIDENCE_MEDIUM


def _algorithm_compatible_with_input(
    algorithm: dict[str, Any] | None,
    input_structure: dict[str, Any] | None,
) -> tuple[bool, str, dict[str, Any]]:
    """
    Validate only strong semantic contradictions.

    Unknown combinations are NOT automatically rejected.
    This is deliberate: the resolver must prefer uncertainty
    over false negatives.
    """

    if not isinstance(algorithm, dict):
        return (
            True,
            "No reliable algorithm evidence is available.",
            {
                "status": "not-applicable",
            },
        )

    if not isinstance(input_structure, dict):
        return (
            True,
            "No verified input structure is available.",
            {
                "status": "not-applicable",
            },
        )

    algorithm_name = _normalize_algorithm_name(
        algorithm.get("algorithm_name")
    )

    input_type = normalize_workload_type(
        input_structure.get("workload_type")
    )

    if not algorithm_name or not input_type:
        return (
            True,
            "Compatibility could not be conclusively evaluated.",
            {
                "status": "insufficient-evidence",
                "algorithm": algorithm_name,
                "input": input_type,
            },
        )

    allowed_inputs = _ALGORITHM_INPUT_COMPATIBILITY.get(
        algorithm_name
    )

    # No explicit compatibility rule means:
    # do not invent a contradiction.
    if not allowed_inputs:
        return (
            True,
            "No restrictive compatibility rule exists for this algorithm.",
            {
                "status": "not-restricted",
                "algorithm": algorithm_name,
                "input": input_type,
            },
        )

    if input_type in allowed_inputs:
        return (
            True,
            "Algorithm and input structure are semantically compatible.",
            {
                "status": "compatible",
                "algorithm": algorithm_name,
                "input": input_type,
            },
        )

    return (
        False,
        (
            f"Algorithm '{algorithm_name}' is not compatible "
            f"with verified input structure '{input_type}'."
        ),
        {
            "status": "contradiction",
            "algorithm": algorithm_name,
            "input": input_type,
            "allowed_inputs": sorted(allowed_inputs),
        },
    )


def _fuse_confidence(
    input_confidence: float,
    algorithm_confidence: float,
    *,
    algorithm_reliable: bool,
    input_reliable: bool,
    compatible: bool,
) -> float:
    """
    Conservative confidence fusion.

    We never allow one strong signal to hide another weak signal.
    """

    input_score = _safe_confidence(input_confidence)
    algorithm_score = _safe_confidence(algorithm_confidence)

    if not input_reliable:
        return 0.0

    if not algorithm_reliable:
        return round(
            input_score * 0.75,
            4,
        )

    score = min(
        input_score,
        algorithm_score,
    )

    if not compatible:
        return 0.0

    return round(score, 4)


def _select_algorithm_specificity(
    algorithm: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Enforce the specificity hierarchy:

        specific > family > generic > unknown

    No resolver logic is allowed to upgrade specificity.
    """

    if not isinstance(algorithm, dict):
        return {
            "name": None,
            "family": None,
            "specificity": "unknown",
            "rank": 0,
        }

    name = algorithm.get("algorithm_name")
    family = algorithm.get("algorithm_family")

    specificity = _normalize_specificity(
        algorithm.get("specificity")
    )

    rank = _SPECIFICITY_RANK.get(
        specificity,
        0,
    )

    if rank >= 3 and name:
        return {
            "name": name,
            "family": family,
            "specificity": "specific",
            "rank": rank,
        }

    if rank >= 2 and family:
        return {
            "name": None,
            "family": family,
            "specificity": "family",
            "rank": rank,
        }

    return {
        "name": None,
        "family": family,
        "specificity": "unknown",
        "rank": 0,
    }


def _build_resolver_evidence(
    *,
    input_contract: dict[str, Any] | None,
    input_structure: dict[str, Any] | None,
    algorithm: dict[str, Any] | None,
    description_type: str | None,
    name_type: str | None,
    compatibility: dict[str, Any],
    fused_confidence: float,
) -> dict[str, Any]:
    """
    Build a stable, auditable evidence object.
    """

    return {
        "input_contract": {
            "contract_type": (
                input_contract.get("contract_type")
                if isinstance(input_contract, dict)
                else None
            ),
            "confidence": _safe_confidence(
                input_contract.get("confidence", 0.0)
                if isinstance(input_contract, dict)
                else 0.0
            ),
            "workload_type": (
                input_structure.get("workload_type")
                if isinstance(input_structure, dict)
                else None
            ),
        },
        "algorithm": {
            "name": (
                algorithm.get("algorithm_name")
                if isinstance(algorithm, dict)
                else None
            ),
            "family": (
                algorithm.get("algorithm_family")
                if isinstance(algorithm, dict)
                else None
            ),
            "specificity": (
                algorithm.get("specificity")
                if isinstance(algorithm, dict)
                else "unknown"
            ),
            "confidence": _safe_confidence(
                algorithm.get("confidence", 0.0)
                if isinstance(algorithm, dict)
                else 0.0
            ),
        },
        "supporting_metadata": {
            "description_input_structure": description_type,
            "benchmark_name_input_structure": name_type,
        },
        "compatibility": compatibility,
        "fusion": {
            "confidence": fused_confidence,
            "level": _confidence_level(
                fused_confidence
            ),
        },
    }


def _validate_benchmark_metadata(
    metadata: Any,
) -> tuple[bool, list[str]]:
    """
    Validate the public metadata contract without making
    assumptions about future metadata fields.
    """

    errors: list[str] = []

    if not isinstance(metadata, dict):
        return False, ["benchmark_metadata must be an object"]

    for key in (
        "name",
        "category",
        "description",
        "source",
        "confidence",
        "provenance",
        "generation",
        "schema_version",
    ):
        if key not in metadata:
            errors.append(
                f"benchmark_metadata.{key} is missing"
            )

    if not isinstance(
        metadata.get("name"),
        str,
    ) or not metadata.get("name", "").strip():
        errors.append(
            "benchmark_metadata.name must be a non-empty string"
        )

    if not isinstance(
        metadata.get("category"),
        str,
    ) or not metadata.get("category", "").strip():
        errors.append(
            "benchmark_metadata.category must be a non-empty string"
        )

    if not isinstance(
        metadata.get("description"),
        str,
    ) or not metadata.get("description", "").strip():
        errors.append(
            "benchmark_metadata.description must be a non-empty string"
        )

    confidence = metadata.get("confidence")

    if not isinstance(confidence, dict):
        errors.append(
            "benchmark_metadata.confidence must be an object"
        )
    else:
        score = _safe_confidence(
            confidence.get("score")
        )

        if score != confidence.get("score"):
            errors.append(
                "benchmark_metadata.confidence.score must be numeric"
            )

        if confidence.get("level") not in {
            "high",
            "medium",
            "low",
        }:
            errors.append(
                "benchmark_metadata.confidence.level is invalid"
            )

    return (
        len(errors) == 0,
        errors,
    )


def _finalize_resolver_result(
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Final safety gate.

    This does not invent missing values. It only validates and
    records resolver integrity.
    """

    result.setdefault(
        "resolver",
        {},
    )

    result["resolver"].update(
        {
            "schema_version": RESOLVER_SCHEMA_VERSION,
            "validated": True,
        }
    )

    metadata = result.get(
        "benchmark_metadata"
    )

    valid, errors = _validate_benchmark_metadata(
        metadata
    )

    result["resolver"]["metadata_validation"] = {
        "valid": valid,
        "errors": errors,
    }

    if not valid:
        # Metadata is presentation data. A malformed metadata
        # object must never make an invalid workload executable.
        result["can_generate"] = False
        result["resolver"]["validated"] = False

    return result

    
def _build_mismatch_result(
    code_type: str | None,
    description_type: str | None,
    name_type: str | None,
    reason: str,
) -> dict[str, Any]:

    return {
        "status": "mismatch",
        "workload_type": (
            code_type
            or description_type
            or name_type
            or "custom"
        ),
        "schema": None,
        "detection": {
            "method": "evidence-conflict",
            "confidence": 0.0,
            "reason": reason,
            "evidence": {
                "reference_code": code_type,
                "description": description_type,
                "benchmark_name": name_type,
            },
        },
        "can_generate": False,
        "reason": (
            "Workload mismatch detected. "
            "Automatic workload generation has been disabled."
        ),
    }
# ============================================================
# MAIN BENCHMARK WORKLOAD RESOLVER
# ============================================================

def resolve_benchmark_workload(
    benchmark_name: str | None,
    description: str | None,
    reference_code: str | None,
    workload_type: str | None = None,
    input_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Production-grade benchmark workload resolver.

    Responsibilities
    ----------------
    1. Obtain algorithm evidence exclusively from Algorithm Intelligence.
    2. Obtain input structure exclusively from the verified Input Contract.
    3. Keep supporting metadata non-authoritative.
    4. Validate algorithm/input compatibility.
    5. Fuse confidence conservatively.
    6. Preserve algorithm specificity without upgrading weak evidence.
    7. Detect contradictions explicitly.
    8. Never hallucinate an algorithm or input structure.
    9. Preserve deterministic generation behavior.
    10. Attach auditable provenance/evidence.
    11. Validate generated benchmark metadata.
    12. Preserve backward-compatible resolver fields.

    Important:
        The resolver does not attempt to identify algorithms itself.
        Algorithm Intelligence remains the sole algorithm authority.
    """

    normalized = normalize_workload_type(
        workload_type
    )

    # ========================================================
    # 1. ALGORITHM INTELLIGENCE
    # ========================================================

    algorithm_detection = (
        _analyze_algorithm_with_intelligence(
            reference_code
        )
    )

    algorithm_reliable = _algorithm_is_reliable(
        algorithm_detection
    )

    algorithm_specificity = (
        _select_algorithm_specificity(
            algorithm_detection
        )
    )

    # ========================================================
    # 2. SUPPORTING LEGACY / EXPLICIT EVIDENCE
    #
    # These signals are NEVER authoritative.
    # ========================================================

    description_detection = _detect_from_description(
        description
    )

    name_detection = _detect_from_benchmark_name(
        benchmark_name
    )

    description_type = _detected_type(
        description_detection
    )

    name_type = _detected_type(
        name_detection
    )

    # ========================================================
    # 3. VERIFIED INPUT CONTRACT
    # ========================================================

    input_structure_result = (
        normalize_input_structure_from_contract(
            input_contract
        )
    )

    input_reliable = _input_is_reliable(
        input_structure_result,
        input_contract,
    )

    # ========================================================
    # 4. VERIFIED INPUT PATH
    # ========================================================

    if input_structure_result is not None:

        input_confidence = _safe_confidence(
            input_contract.get(
                "confidence",
                0.0,
            )
            if isinstance(input_contract, dict)
            else 0.0
        )

        algorithm_confidence = _safe_confidence(
            algorithm_detection.get(
                "confidence",
                0.0,
            )
            if isinstance(algorithm_detection, dict)
            else 0.0
        )

        compatible, compatibility_reason, compatibility = (
            _algorithm_compatible_with_input(
                algorithm_detection,
                input_structure_result,
            )
        )

        fused_confidence = _fuse_confidence(
            input_confidence,
            algorithm_confidence,
            algorithm_reliable=algorithm_reliable,
            input_reliable=input_reliable,
            compatible=compatible,
        )

        evidence = _build_resolver_evidence(
            input_contract=input_contract,
            input_structure=input_structure_result,
            algorithm=algorithm_detection,
            description_type=description_type,
            name_type=name_type,
            compatibility=compatibility,
            fused_confidence=fused_confidence,
        )

        # ----------------------------------------------------
        # HARD CONTRADICTION
        # ----------------------------------------------------

        if (
            algorithm_reliable
            and not compatible
        ):
            result = {
                "status": "mismatch",
                "workload_type": (
                    input_structure_result.get(
                        "workload_type"
                    )
                    or "custom"
                ),
                "schema": None,
                "input_structure": (
                    input_structure_result
                ),
                "input_contract": input_contract,
                "algorithm": algorithm_detection,
                "can_generate": False,
                "reason": (
                    "Verified input structure conflicts "
                    "with the reliably identified algorithm."
                ),
                "detection": {
                    "method": "resolver-compatibility-validation",
                    "confidence": 0.0,
                    "reason": compatibility_reason,
                    "evidence": evidence,
                },
                "resolution": {
                    "algorithm": algorithm_specificity,
                    "input_structure": (
                        input_structure_result.get(
                            "workload_type"
                        )
                    ),
                    "confidence": 0.0,
                    "confidence_level": "low",
                    "decision": "reject-conflicting-evidence",
                },
            }

            result = _attach_benchmark_metadata(
                result,
                input_structure_result,
                algorithm_detection,
            )

            return _finalize_resolver_result(
                result
            )

        # ----------------------------------------------------
        # VALIDATED INPUT + ALGORITHM
        # ----------------------------------------------------

        capability = workload_generation_capability(
            input_structure_result
        )

        result = _build_dual_track_workload_result(
            input_structure_detection=(
                input_structure_result
            ),
            algorithm_detection=(
                algorithm_detection
            ),
        )

        result.update(
            capability
        )

        result["status"] = (
            "known"
            if input_structure_result.get(
                "status"
            ) == "known"
            else "custom"
        )

        result["input_contract"] = input_contract

        result["detection"] = {
            "method": "resolver-fusion",
            "confidence": fused_confidence,
            "reason": (
                "Input structure was obtained from the verified "
                "Input Contract and algorithmic behavior was "
                "analyzed independently by Algorithm Intelligence."
            ),
            "evidence": evidence,
        }

        result["resolution"] = {
            "algorithm": algorithm_specificity,
            "input_structure": (
                input_structure_result.get(
                    "workload_type"
                )
            ),
            "confidence": fused_confidence,
            "confidence_level": _confidence_level(
                fused_confidence
            ),
            "decision": (
                "verified"
                if algorithm_reliable
                else "verified-input-only"
            ),
            "evidence": evidence,
        }

        result = _attach_benchmark_metadata(
            result,
            input_structure_result,
            algorithm_detection,
        )

        return _finalize_resolver_result(
            result
        )

    # ========================================================
    # 5. NO VERIFIED INPUT CONTRACT
    #
    # Explicit/metadata hints remain non-authoritative.
    # Generation stays disabled.
    # ========================================================

    fallback_structure = None

    if (
        normalized
        and is_known_workload(normalized)
    ):
        fallback_structure = resolve_workload(
            normalized
        )

    elif description_detection is not None:
        fallback_structure = dict(
            description_detection
        )

    elif name_detection is not None:
        fallback_structure = dict(
            name_detection
        )

    if fallback_structure is not None:

        result = _build_dual_track_workload_result(
            input_structure_detection=(
                fallback_structure
            ),
            algorithm_detection=(
                algorithm_detection
            ),
        )

        algorithm_confidence = _safe_confidence(
            algorithm_detection.get(
                "confidence",
                0.0,
            )
            if isinstance(algorithm_detection, dict)
            else 0.0
        )

        result.update(
            {
                "status": "uncertain",
                "can_generate": False,
                "detection": {
                    "method": "unverified-input-contract",
                    "confidence": 0.0,
                    "reason": (
                        "A workload structure was suggested by "
                        "metadata or explicit configuration, but "
                        "no verified Input Contract was provided. "
                        "Automatic workload generation is disabled."
                    ),
                    "evidence": {
                        "input_contract": None,
                        "description_input_structure": (
                            description_type
                        ),
                        "benchmark_name_input_structure": (
                            name_type
                        ),
                        "explicit_workload_type": normalized,
                        "algorithm": (
                            algorithm_detection
                            if algorithm_detection
                            else None
                        ),
                    },
                },
                "reason": (
                    "Automatic workload generation requires "
                    "a verified Input Contract."
                ),
                "resolution": {
                    "algorithm": algorithm_specificity,
                    "input_structure": (
                        fallback_structure.get(
                            "workload_type"
                        )
                    ),
                    "confidence": 0.0,
                    "confidence_level": "low",
                    "algorithm_confidence": (
                        algorithm_confidence
                    ),
                    "decision": "unverified-input",
                },
            }
        )

        result = _attach_benchmark_metadata(
            result,
            fallback_structure,
            algorithm_detection,
        )

        return _finalize_resolver_result(
            result
        )

    # ========================================================
    # 6. NOTHING VERIFIED
    # ========================================================

    result = _build_dual_track_workload_result(
        input_structure_detection=None,
        algorithm_detection=algorithm_detection,
    )

    result.update(
        {
            "status": "custom",
            "can_generate": False,
            "detection": {
                "method": "no-input-contract",
                "confidence": 0.0,
                "reason": (
                    "No verified Input Contract was provided "
                    "and no reliable fallback input structure "
                    "was available. Algorithmic behavior was "
                    "still analyzed independently."
                ),
                "evidence": {
                    "input_contract": None,
                    "description_input_structure": (
                        description_type
                    ),
                    "benchmark_name_input_structure": (
                        name_type
                    ),
                    "explicit_workload_type": normalized,
                    "algorithm": (
                        algorithm_detection
                        if algorithm_detection
                        else None
                    ),
                },
            },
            "reason": (
                "No deterministic input structure can be "
                "generated without a verified Input Contract."
            ),
            "resolution": {
                "algorithm": algorithm_specificity,
                "input_structure": None,
                "confidence": 0.0,
                "confidence_level": "low",
                "decision": "no-verified-input",
            },
        }
    )

    result = _attach_benchmark_metadata(
        result,
        None,
        algorithm_detection,
    )

    return _finalize_resolver_result(
        result
    )