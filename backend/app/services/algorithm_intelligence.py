# from __future__ import annotations

# from dataclasses import dataclass, field
# import re
# from pathlib import Path
# import tempfile
# from typing import Any, Iterable, Sequence

# try:
#     from tree_sitter_language_pack import configure, get_parser
# except ImportError:
#     configure = None
#     get_parser = None


# if configure is not None:
#     # The language pack downloads parser libraries lazily.  Use a writable
#     # temporary cache instead of a user-profile location, which can be locked
#     # down in services, containers, and CI environments.
#     configure({
#         "cache_dir": str(
#             Path(tempfile.gettempdir()) / "green-code-tree-sitter"
#         )
#     })


# # Supported language mapping

# LANGUAGE_PARSER_NAMES: dict[str, str] = {
#     "c": "c",
#     "c++": "cpp",
#     "cpp": "cpp",
#     "java": "java",
#     "python": "python",
#     "javascript": "javascript",
#     "js": "javascript",
#     "go": "go",
#     "rust": "rust",
#     "c#": "csharp",
#     "csharp": "csharp",
#     "kotlin": "kotlin",
#     "php": "php",
# }

# # Typed models


# @dataclass
# class ParseResult:
#     language: str
#     parser_name: str | None
#     success: bool
#     root: Any | None = None
#     error: str | None = None
#     error_count: int = 0


# @dataclass
# class ProgramFeatures:
#     language: str

#     node_counts: dict[str, int] = field(default_factory=dict)

#     loops: int = 0
#     while_loops: int = 0
#     for_loops: int = 0
#     nested_loop_depth: int = 0

#     function_count: int = 0
#     function_calls: int = 0
#     recursive_calls: int = 0

#     array_accesses: int = 0
#     member_accesses: int = 0
#     comparisons: int = 0
#     assignments: int = 0

#     sort_api_calls: list[str] = field(default_factory=list)
#     search_api_calls: list[str] = field(default_factory=list)
#     stack_api_calls: list[str] = field(default_factory=list)
#     queue_api_calls: list[str] = field(default_factory=list)
#     heap_api_calls: list[str] = field(default_factory=list)

#     map_api_calls: list[str] = field(default_factory=list)
#     set_api_calls: list[str] = field(default_factory=list)

#     graph_signals: list[str] = field(default_factory=list)
#     tree_signals: list[str] = field(default_factory=list)
#     dp_signals: list[str] = field(default_factory=list)
#     string_signals: list[str] = field(default_factory=list)
#     matrix_signals: list[str] = field(default_factory=list)

#     midpoint_signals: int = 0
#     boundary_narrowing_signals: int = 0
#     neighbor_iteration_signals: int = 0
#     visited_state_signals: int = 0
#     relaxation_signals: int = 0

#     recursion_signals: int = 0
#     memoization_signals: int = 0
#     comparison_swap_signals: int = 0
#     bubble_sort_signals: int = 0
#     selection_sort_signals: int = 0
#     insertion_sort_signals: int = 0
#     merge_sort_signals: int = 0
#     quick_sort_signals: int = 0
#     heap_sort_signals: int = 0
#     linear_search_signals: int = 0
#     pointer_pair_signals: int = 0
#     window_state_signals: int = 0
#     prefix_recurrence_signals: int = 0
#     choice_undo_signals: int = 0
#     greedy_selection_signals: int = 0
#     dp_recurrence_signals: int = 0
#     array_dimension_signals: int = 0
#     self_call_names: set[str] = field(default_factory=set)

#     library_signals: list[str] = field(default_factory=list)

#     parse_error_nodes: int = 0
#     structural_quality: float = 0.0


# @dataclass
# class AlgorithmClassification:
#     name: str
#     family: str
#     specificity: str
#     confidence: float
#     evidence: list[str] = field(default_factory=list)


# @dataclass
# class ComplexityEstimate:
#     time: str | None
#     space: str | None
#     confidence: float
#     evidence: list[str] = field(default_factory=list)


# @dataclass
# class AlgorithmAnalysis:
#     algorithm: AlgorithmClassification
#     complexity: ComplexityEstimate
#     detection: dict[str, Any]


# # Node abstraction

# def _node_type(node: Any) -> str:
#     value = getattr(node, "type", None)

#     if isinstance(value, str):
#         return value

#     value = getattr(node, "kind", None)

#     if isinstance(value, str):
#         return value

#     return ""


# def _node_children(node: Any) -> list[Any]:
#     children = getattr(node, "children", None)

#     if children is None:
#         return []

#     if callable(children):
#         try:
#             children = children()
#         except TypeError:
#             return []

#     try:
#         return list(children)
#     except TypeError:
#         return []


# def _node_text(node: Any, source: bytes) -> str:
#     try:
#         return source[
#             node.start_byte:node.end_byte
#         ].decode("utf-8", errors="replace")
#     except Exception:
#         return ""


# def _normalized_source(reference_code: str) -> str:
#     """Normalize source only for supplemental structural signals."""
#     return " ".join(
#         reference_code
#         .replace("\r", " ")
#         .replace("\n", " ")
#         .split()
#     ).lower()


# def _contains_any_text(
#     source: str,
#     patterns: Sequence[str],
# ) -> bool:
#     return any(pattern.lower() in source for pattern in patterns)


# def _contains_any(
#     source: str,
#     patterns: Sequence[str],
# ) -> bool:
#     return any(
#         pattern.lower() in source
#         for pattern in patterns
#     )


# def _count_any_text(
#     source: str,
#     patterns: Sequence[str],
# ) -> int:
#     return sum(
#         source.count(pattern.lower())
#         for pattern in patterns
#     )

# # Parser adapter

# def _parse_reference_code(
#     reference_code: str,
#     language: str,
# ) -> ParseResult:
#     normalized_language = (
#         language or ""
#     ).strip().lower()

#     parser_name = LANGUAGE_PARSER_NAMES.get(
#         normalized_language
#     )

#     if parser_name is None:
#         return ParseResult(
#             language=normalized_language,
#             parser_name=None,
#             success=False,
#             error=(
#                 f"Unsupported parser language: "
#                 f"{language}"
#             ),
#         )

#     if get_parser is None:
#         return ParseResult(
#             language=normalized_language,
#             parser_name=parser_name,
#             success=False,
#             error=(
#                 "Tree-sitter language pack is not installed."
#             ),
#         )

#     try:
#         parser = get_parser(parser_name)

#         source_bytes = reference_code.encode(
#             "utf-8"
#         )

#         tree = parser.parse(source_bytes)

#         root = getattr(
#             tree,
#             "root_node",
#             None,
#         )

#         if root is None:
#             return ParseResult(
#                 language=normalized_language,
#                 parser_name=parser_name,
#                 success=False,
#                 error="Parser returned no root node.",
#             )

#         error_count = _count_parse_errors(root)

#         return ParseResult(
#             language=normalized_language,
#             parser_name=parser_name,
#             success=True,
#             root=root,
#             error_count=error_count,
#         )

#     except Exception as exc:
#         return ParseResult(
#             language=normalized_language,
#             parser_name=parser_name,
#             success=False,
#             error=str(exc),
#         )


# # Parse-error counting

# def _count_parse_errors(node: Any) -> int:
#     count = 0

#     node_type = _node_type(node)

#     if node_type in {
#         "ERROR",
#         "MISSING",
#     }:
#         count += 1

#     for child in _node_children(node):
#         count += _count_parse_errors(child)

#     return count


# # Generic tree traversal


# # B5.9 - Generic tree traversal

# def _walk_tree(
#     node: Any,
# ) -> Iterable[Any]:
#     yield node

#     for child in _node_children(node):
#         yield from _walk_tree(child)


# def _count_node_types(
#     root: Any,
# ) -> dict[str, int]:
#     counts: dict[str, int] = {}

#     for node in _walk_tree(root):
#         node_type = _node_type(node)

#         if not node_type:
#             continue

#         counts[node_type] = (
#             counts.get(node_type, 0) + 1
#         )

#     return counts


# # B5.10 - Structural loop analysis

# _LOOP_NODE_TYPES = {
#     "for_statement",
#     "for_in_statement",
#     "while_statement",
#     "do_statement",
#     "for_clause",
# }


# def _loop_depth(
#     node: Any,
#     current_depth: int = 0,
# ) -> int:
#     node_type = _node_type(node)

#     next_depth = current_depth

#     if node_type in _LOOP_NODE_TYPES:
#         next_depth += 1

#     maximum = next_depth

#     for child in _node_children(node):
#         maximum = max(
#             maximum,
#             _loop_depth(child, next_depth),
#         )

#     return maximum


# # B5.11 - Function and recursion extraction

# _FUNCTION_NODE_TYPES = {
#     "function_definition",
#     "method_declaration",
#     "function_declaration",
#     "function_item",
#     "method_definition",
# }


# def _extract_function_names(
#     root: Any,
#     source: bytes,
# ) -> set[str]:
#     names: set[str] = set()

#     for node in _walk_tree(root):
#         if _node_type(node) not in _FUNCTION_NODE_TYPES:
#             continue

#         function_text = _node_text(
#             node,
#             source,
#         )

#         match = re.search(
#             r"(?:function\s+)?([A-Za-z_]\w*)\s*\(",
#             function_text,
#         )

#         if match:
#             names.add(match.group(1))
#             continue

#         for child in _node_children(node):
#             child_type = _node_type(child)

#             if child_type in {
#                 "identifier",
#                 "field_identifier",
#                 "property_identifier",
#             }:
#                 names.add(
#                     _node_text(
#                         child,
#                         source,
#                     ).strip()
#                 )
#                 break

#     return names


# # B5.12 - Normalized API recognition

# API_PATTERNS: dict[str, dict[str, tuple[str, ...]]] = {
#     "python": {
#         "sorting": (
#             "sorted",
#             ".sort",
#         ),
#         "heap": (
#             "heapq.heappush",
#             "heapq.heappop",
#             "heapq.heapify",
#         ),
#         "queue": (
#             "collections.deque",
#             "deque",
#         ),
#     },
#     "cpp": {
#         "sorting": (
#             "std::sort",
#             "sort",
#         ),
#         "heap": (
#             "std::priority_queue",
#             "priority_queue",
#         ),
#         "queue": (
#             "std::queue",
#             "queue",
#         ),
#         "stack": (
#             "std::stack",
#             "stack",
#         ),
#     },
#     "java": {
#         "sorting": (
#             "Arrays.sort",
#             "Collections.sort",
#         ),
#         "heap": (
#             "PriorityQueue",
#         ),
#         "queue": (
#             "Queue",
#             "ArrayDeque",
#         ),
#     },
#     "javascript": {
#         "sorting": (
#             ".sort",
#         ),
#     },
#     "go": {
#         "sorting": (
#             "sort.Ints",
#             "sort.Slice",
#             "sort.Sort",
#         ),
#         "heap": (
#             "container/heap",
#         ),
#     },
#     "rust": {
#         "sorting": (
#             ".sort()",
#             ".sort_unstable()",
#         ),
#         "heap": (
#             "BinaryHeap",
#         ),
#         "queue": (
#             "VecDeque",
#         ),
#     },
#     "csharp": {
#         "sorting": (
#             "Array.Sort",
#             "List.Sort",
#         ),
#         "heap": (
#             "PriorityQueue",
#         ),
#     },
#     "kotlin": {
#         "sorting": (
#             "sorted",
#             "sort",
#         ),
#         "queue": (
#             "ArrayDeque",
#         ),
#     },
#     "php": {
#         "sorting": (
#             "sort(",
#             "sort (",
#         ),
#     },
# }


# # B5.13 - API recognition helper

# def _detect_library_signals(
#     reference_code: str,
#     language: str,
# ) -> tuple[
#     dict[str, list[str]],
#     list[str],
# ]:
#     normalized_language = (
#         language or ""
#     ).strip().lower()

#     source = reference_code.lower()

#     language_patterns = API_PATTERNS.get(
#         normalized_language,
#         {},
#     )

#     detected: dict[str, list[str]] = {}
#     evidence: list[str] = []

#     for operation, patterns in (
#         language_patterns.items()
#     ):
#         matches = []

#         for pattern in patterns:
#             if pattern.lower() in source:
#                 matches.append(pattern)

#         if matches:
#             detected[operation] = matches

#             for match in matches:
#                 evidence.append(
#                     f"Detected {operation} API: {match}"
#                 )

#     return detected, evidence


# def _extract_semantic_signals(
#     reference_code: str,
#     features: ProgramFeatures,
#     function_names: set[str],
# ) -> None:
#     source = _normalized_source(reference_code)

#     if (
#         features.loops >= 2
#         and features.comparisons >= 1
#         and _contains_any(
#             source,
#             (
#                 "swap(",
#                 "std::swap",
#                 "temp =",
#                 "temp=",
#                 "arr[j] > arr[j + 1]",
#                 "arr[j] < arr[j + 1]",
#                 "a[j] > a[j + 1]",
#                 "a[j] < a[j + 1]",
#                 "data[j] < data[i]",
#                 "data[i], data[j] = data[j], data[i]",
#             ),
#         )
#     ):
#         features.comparison_swap_signals += 2

#     if _contains_any(
#         source,
#         (
#             "mid =",
#             "mid=",
#             "middle =",
#             "middle=",
#             "(low + high) / 2",
#             "(left + right) / 2",
#             "low + (high - low) / 2",
#         ),
#     ):
#         features.midpoint_signals += 1

#     if _contains_any(
#         source,
#         (
#             "low = mid + 1",
#             "low=mid+1",
#             "lo = mid + 1",
#             "lo=mid+1",
#             "left = mid + 1",
#             "left=mid+1",
#             "high = mid - 1",
#             "high=mid-1",
#             "hi = mid - 1",
#             "hi=mid-1",
#             "right = mid - 1",
#             "right=mid-1",
#             "start = middle + 1",
#             "finish = middle - 1",
#         ),
#     ):
#         features.boundary_narrowing_signals += 2

#     if (
#         _contains_any(
#             source,
#             ("left", "right", "l =", "r =", "i =", "j ="),
#         )
#         and _contains_any(
#             source,
#             (
#                 "left += 1",
#                 "left -= 1",
#                 "right += 1",
#                 "right -= 1",
#                 "l += 1",
#                 "l -= 1",
#                 "r += 1",
#                 "r -= 1",
#                 "++i",
#                 "i++",
#                 "--j",
#                 "j--",
#             ),
#         )
#     ):
#         features.pointer_pair_signals += 2

#     if (
#         _contains_any(
#             source,
#             (
#                 "left += 1",
#                 "left++",
#                 "l += 1",
#                 "l++",
#                 "start += 1",
#                 "start++",
#             ),
#         )
#         and _contains_any(
#             source,
#             (
#                 "right += 1",
#                 "right++",
#                 "r += 1",
#                 "r++",
#                 "end += 1",
#                 "end++",
#                 "++end",
#             ),
#         )
#     ):
#         features.window_state_signals += 2

#     if (
#         features.window_state_signals >= 2
#         and _contains_any(
#             source,
#             (
#                 "count[",
#                 "freq[",
#                 "frequency",
#                 "window_sum",
#                 "current_sum",
#                 "while ",
#             ),
#         )
#     ):
#         features.window_state_signals += 1

#     if (
#         (
#             "prefix[" in source
#             or "cumulative[" in source
#         )
#         and _contains_any(
#             source,
#             (
#                 "prefix[i + 1]",
#                 "prefix[i+1]",
#                 "prefix[i + 1] = prefix[i]",
#                 "prefix[i+1] = prefix[i]",
#                 "cumulative[index + 1]",
#                 "cumulative[index+1]",
#                 "cumulative[index + 1] = cumulative[index]",
#                 "cumulative[index+1] = cumulative[index]",
#             ),
#         )
#     ):
#         features.prefix_recurrence_signals += 2

#     for name in function_names:
#         normalized_name = name.strip().lower()

#         if (
#             normalized_name
#             and source.count(f"{normalized_name}(") >= 2
#         ):
#             features.recursion_signals += 1
#             features.self_call_names.add(normalized_name)

#     if (
#         _contains_any(source, (".left", "->left", "left_child", "leftchild"))
#         and _contains_any(source, (".right", "->right", "right_child", "rightchild"))
#     ):
#         features.tree_signals.append(
#             "Binary-tree child traversal structure detected."
#         )

#     if (
#         _contains_any(source, ("visited", "visited[", "visited.add", "visited.insert"))
#         and _contains_any(source, ("adj", "adjacency", "neighbors", "neighbours"))
#     ):
#         features.graph_signals.append(
#             "Graph adjacency with visited-state tracking detected."
#         )
#         features.visited_state_signals += 1

#     if _contains_any(source, ("neighbor", "neighbour", "adjacency[")):
#         features.neighbor_iteration_signals += 1

#     if (
#         _contains_any(source, ("dist[", "distance[", "distance"))
#         and _contains_any(source, ("priority_queue", "priorityqueue", "heapq", "binaryheap"))
#         and _contains_any(source, ("dist[v] >", "dist[v] =", "distance[v] >", "distance[v] =", "relax"))
#     ):
#         features.relaxation_signals += 2
#         features.graph_signals.append(
#             "Shortest-path relaxation structure detected."
#         )

#     if _contains_any(source, ("dp[", "memo[", "memoized", "cache[")):
#         features.memoization_signals += 1
#         features.dp_signals.append(
#             "Memoization or DP table detected."
#         )

#     if features.memoization_signals and _contains_any(
#         source,
#         ("+ dp[", "- dp[", "* dp[", "max(", "min("),
#     ):
#         features.dp_recurrence_signals += 2

#     if (
#         "[i][j]" in source
#         or "[j][i]" in source
#         or _contains_any(source, ("[row][column]", "[column][row]"))
#         or (features.nested_loop_depth >= 2 and _contains_any(source, ("matrix", "grid")))
#     ):
#         features.array_dimension_signals = 2
#         features.matrix_signals.append(
#             "Two-dimensional matrix/grid access detected."
#         )

#     if (
#         features.recursion_signals
#         and _contains_any(source, ("backtrack", "undo", "remove(", "pop_back", "pop()"))
#         and _contains_any(source, ("push(", "append(", "add(", "choose", "for "))
#     ):
#         features.choice_undo_signals += 2

#     if (
#         _contains_any(
#             source,
#             ("sort(", "std::sort", "arrays.sort", "collections.sort"),
#         )
#         or features.comparison_swap_signals
#     ) and _contains_any(
#         source,
#         ("selected", "select", "current_end", "best", "earliest", "minimum", "maximum", "interval"),
#     ):
#         features.greedy_selection_signals += 2

#     if _contains_any(
#         source,
#         ("tolower", "toupper", "isalpha", "isdigit", ".lower(", ".upper(", "substring(", "substr(", "reverse("),
#     ):
#         features.string_signals.append(
#             "String transformation/scanning operation detected."
#         )

# def _extract_algorithm_signals(
#     reference_code: str,
#     language: str,
#     features: ProgramFeatures,
#     function_names: set[str],
# ) -> None:
#     """
#     Extract algorithm-specific structural evidence.

#     This does not determine the algorithm itself.
#     It only records structures that the classifier can reason about.
#     """
#     source = _normalized_source(reference_code)
#     normalized_language = (language or "").strip().lower()

#     # --------------------------------------------------------
#     # Search / midpoint narrowing
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "mid =",
#             "mid=",
#             "midpoint",
#             "(low + high) / 2",
#             "(left + right) / 2",
#             "low + (high - low) / 2",
#         ),
#     ):
#         features.midpoint_signals += 1

#     if _contains_any_text(
#         source,
#         (
#             "low = mid + 1",
#             "low=mid+1",
#             "left = mid + 1",
#             "left=mid+1",
#             "high = mid - 1",
#             "high=mid-1",
#             "right = mid - 1",
#             "right=mid-1",
#             "lo = mid + 1",
#             "hi = mid - 1",
#         ),
#     ):
#         features.boundary_narrowing_signals += 1

#     # --------------------------------------------------------
#     # Recursion
#     # --------------------------------------------------------

#     function_names = {
#         name.lower()
#         for name in function_names
#     }

#     # Recursive calls are primarily determined from AST function
#     # declarations/call structure below. This textual fallback
#     # only catches common self-call forms.
#     for name in function_names:
#         if source.count(f"{name}(") >= 2:
#             features.recursion_signals += 1

#     # --------------------------------------------------------
#     # Two pointers
#     # --------------------------------------------------------

#     if (
#         _contains_any_text(
#             source,
#             ("left", "l = 0", "l=0", "start"),
#         )
#         and _contains_any_text(
#             source,
#             ("right", "r =", "end"),
#         )
#         and _contains_any_text(
#             source,
#             ("left += 1", "l += 1", "right -= 1", "r -= 1"),
#         )
#     ):
#         features.boundary_narrowing_signals += 1

#     # --------------------------------------------------------
#     # Sliding window
#     # --------------------------------------------------------

#     if (
#         _contains_any_text(
#             source,
#             (
#                 "left += 1",
#                 "left++",
#                 "l += 1",
#                 "l++",
#                 "start += 1",
#             ),
#         )
#         and _contains_any_text(
#             source,
#             (
#                 "right += 1",
#                 "right++",
#                 "r += 1",
#                 "r++",
#                 "end += 1",
#             ),
#         )
#     ):
#         features.neighbor_iteration_signals += 1

#     # --------------------------------------------------------
#     # Prefix sum
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "prefix[i + 1] = prefix[i] +",
#             "prefix[i+1] = prefix[i] +",
#             "prefix[i + 1]=",
#             "prefix[i+1]=",
#         ),
#     ):
#         features.dp_signals.append(
#             "Prefix array recurrence detected."
#         )

#     # --------------------------------------------------------
#     # Hashing
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "unordered_map",
#             "unordered_set",
#             "hashmap",
#             "hash_map",
#             "dict",
#             "setdefault",
#             "get(",
#         ),
#     ):
#         features.map_api_calls.append("hash-map access")

#     # --------------------------------------------------------
#     # Stack
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "stack<",
#             "std::stack",
#             ".push(",
#             ".pop(",
#             ".top(",
#         ),
#     ):
#         features.stack_api_calls.append("stack operations")

#     # --------------------------------------------------------
#     # Queue
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "queue<",
#             "std::queue",
#             "deque<",
#             "collections.deque",
#             ".front(",
#             ".popleft(",
#         ),
#     ):
#         features.queue_api_calls.append("queue operations")

#     # --------------------------------------------------------
#     # Graph traversal
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "adj[",
#             "adjacency",
#             "neighbors",
#             "neighbours",
#             "visited",
#         ),
#     ):
#         features.graph_signals.append(
#             "Graph adjacency/visited structure detected."
#         )

#     if _contains_any_text(
#         source,
#         (
#             "visited[",
#             "visited.add(",
#             "visited.insert(",
#             "visited =",
#         ),
#     ):
#         features.visited_state_signals += 1

#     if _contains_any_text(
#         source,
#         (
#             "for neighbor in",
#             "for (auto neighbor",
#             "for(auto neighbor",
#             "for (int neighbor",
#             "for(int neighbor",
#         ),
#     ):
#         features.neighbor_iteration_signals += 1

#     # --------------------------------------------------------
#     # Dijkstra / relaxation
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "priority_queue",
#             "priorityqueue",
#             "binaryheap",
#             "heapq",
#         ),
#     ):
#         features.heap_api_calls.append("priority queue / heap")

#     if _contains_any_text(
#         source,
#         (
#             "dist[v] > dist[u] +",
#             "dist[v] = dist[u] +",
#             "distance",
#             "relax",
#         ),
#     ):
#         features.relaxation_signals += 1
#         features.graph_signals.append(
#             "Distance relaxation structure detected."
#         )

#     # --------------------------------------------------------
#     # Tree traversal
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "left",
#             "right",
#             "left->",
#             "right->",
#             ".left",
#             ".right",
#         ),
#     ) and _contains_any_text(
#         source,
#         (
#             "node",
#             "root",
#             "tree",
#             "nullptr",
#             "null",
#         ),
#     ):
#         features.tree_signals.append(
#             "Tree child traversal structure detected."
#         )

#     # --------------------------------------------------------
#     # Dynamic programming
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "dp[",
#             "memo[",
#             "memoized",
#             "cache[",
#         ),
#     ):
#         features.dp_signals.append(
#             "Memoization or DP table access detected."
#         )

#     # --------------------------------------------------------
#     # Matrix
#     # --------------------------------------------------------

#     if features.nested_loop_depth >= 2 and _contains_any_text(
#         source,
#         (
#             "matrix",
#             "grid",
#             "[i][j]",
#             "[j][i]",
#         ),
#     ):
#         features.matrix_signals.append(
#             "Nested matrix/grid indexing detected."
#         )

#     # --------------------------------------------------------
#     # String processing
#     # --------------------------------------------------------

#     if _contains_any_text(
#         source,
#         (
#             "tolower",
#             "toupper",
#             "isalpha",
#             "isdigit",
#             "substring",
#             ".substring(",
#             "lower(",
#             "upper(",
#             "reverse(",
#         ),
#     ):
#         features.string_signals.append(
#             "String transformation/scanning operation detected."
#         )


# # B5.14 - Program feature extraction

# def _extract_program_features(
#     reference_code: str,
#     language: str,
#     parse_result: ParseResult,
# ) -> ProgramFeatures:
#     features = ProgramFeatures(
#         language=language,
#     )

#     if not parse_result.root:
#         # Parser binaries may be unavailable on restricted Windows hosts. Keep
#         # the analysis useful with the same conservative, source-level signals
#         # used to supplement the AST path.
#         source = _normalized_source(reference_code)
#         function_names = set(
#             re.findall(
#                 r"(?:def\s+|[\w:<>~*&]+\s+)([A-Za-z_]\w*)\s*\(",
#                 reference_code,
#             )
#         )
#         # The broad cross-language pattern above also sees control-flow
#         # helpers such as ``for i in range(...)``. They are not declarations
#         # and therefore must not be treated as recursive functions.
#         function_names.difference_update(
#             {
#                 "range",
#                 "input",
#                 "print",
#                 "len",
#                 "max",
#                 "min",
#             }
#         )
#         features.loops = len(
#             re.findall(r"\b(?:for|while)\b", source)
#         )
#         features.nested_loop_depth = (
#             2 if features.loops >= 2 else features.loops
#         )
#         features.comparisons = len(
#             re.findall(r"(?:==|!=|<=|>=|<|>)", source)
#         )
#         features.function_count = len(function_names)
#         features.function_calls = len(
#             re.findall(r"\b[A-Za-z_]\w*\s*\(", reference_code)
#         )

#         _extract_semantic_signals(
#             reference_code,
#             features,
#             function_names,
#         )
#         _extract_algorithm_signals(
#             reference_code,
#             language,
#             features,
#             function_names,
#         )
#         api_signals, api_evidence = _detect_library_signals(
#             reference_code,
#             language,
#         )
#         features.library_signals.extend(api_evidence)
#         features.sort_api_calls = api_signals.get("sorting", [])
#         features.heap_api_calls.extend(api_signals.get("heap", []))
#         features.queue_api_calls.extend(api_signals.get("queue", []))
#         features.stack_api_calls.extend(api_signals.get("stack", []))
#         _detect_specific_array_algorithms(
#             reference_code,
#             features,
#         )
#         features.structural_quality = 0.55
#         return features

#     root = parse_result.root
#     source = reference_code.encode(
#         "utf-8"
#     )

#     features.node_counts = (
#         _count_node_types(root)
#     )

#     features.loops = sum(
#         features.node_counts.get(
#             node_type,
#             0,
#         )
#         for node_type in _LOOP_NODE_TYPES
#     )

#     features.nested_loop_depth = (
#         _loop_depth(root)
#     )

#     function_names = _extract_function_names(
#         root,
#         source,
#     )

#     features.function_count = len(
#         function_names
#     )

#     features.function_calls = sum(
#         1
#         for node in _walk_tree(root)
#         if _node_type(node) in {
#             "call",
#             "call_expression",
#             "function_call_expression",
#             "call_expression_statement",
#         }
#     )

#     features.comparisons = sum(
#         features.node_counts.get(
#             node_type,
#             0,
#         )
#         for node_type in {
#             "comparison_operator",
#             "==",
#             "!=",
#             "<",
#             ">",
#             "<=",
#             ">=",
#         }
#     )

#     features.parse_error_nodes = (
#         parse_result.error_count
#     )

#     _extract_semantic_signals(
#         reference_code,
#         features,
#         function_names,
#     )

#     _extract_algorithm_signals(
#         reference_code,
#         language,
#         features,
#         function_names,
#     )

#     _detect_specific_array_algorithms(
#         reference_code,
#         features,
#     )

#     api_signals, api_evidence = (
#         _detect_library_signals(
#             reference_code,
#             language,
#         )
#     )

#     features.library_signals.extend(
#         api_evidence
#     )

#     features.sort_api_calls = (
#         api_signals.get(
#             "sorting",
#             [],
#         )
#     )

#     features.heap_api_calls = (
#         api_signals.get(
#             "heap",
#             [],
#         )
#     )

#     features.queue_api_calls = (
#         api_signals.get(
#             "queue",
#             [],
#         )
#     )

#     features.stack_api_calls = (
#         api_signals.get(
#             "stack",
#             [],
#         )
#     )

#     features.structural_quality = max(
#         0.0,
#         min(
#             1.0,
#             1.0
#             - (
#                 parse_result.error_count
#                 / max(
#                     1,
#                     len(features.node_counts),
#                 )
#             ),
#         ),
#     )

#     return features


# # B5.15 - Structural binary-search detector

# def _detect_binary_search(
#     features: ProgramFeatures,
# ) -> tuple[
#     bool,
#     list[str],
# ]:
#     evidence: list[str] = []

#     midpoint = (
#         features.midpoint_signals >= 1
#     )

#     narrowing = (
#         features.boundary_narrowing_signals >= 2
#     )

#     loop_present = (
#         features.loops >= 1
#         or features.recursion_signals >= 1
#     )

#     if midpoint:
#         evidence.append(
#             "Midpoint-based search signal detected."
#         )

#     if narrowing:
#         evidence.append(
#             "Repeated search-boundary narrowing detected."
#         )

#     if loop_present:
#         evidence.append(
#             "Iterative or recursive search control flow detected."
#         )

#     matched = (
#         midpoint
#         and narrowing
#         and loop_present
#     )

#     return matched, evidence


# # B5.15a - Specific sorting/search implementation detectors
# #
# # These detectors deliberately look for the algorithm's control/data-flow
# # shape. Function names are never used as primary evidence.

# def _detect_specific_array_algorithms(
#     source: str,
#     features: ProgramFeatures,
# ) -> None:
#     """Record strong implementation-level signals for common algorithms."""
#     text = _normalized_source(source)
#     compact = re.sub(r"\s+", "", text)

#     # Language-independent normalized patterns. These deliberately do not
#     # depend on the function's name or on one specific array variable name.
#     adjacent_compare_re = bool(re.search(
#         r"\[[A-Za-z_]\w*\]>(?:[A-Za-z_]\w*)?\[[A-Za-z_]\w*\+1\]|"
#         r"\[[A-Za-z_]\w*\]<(?:[A-Za-z_]\w*)?\[[A-Za-z_]\w*\+1\]",
#         compact,
#     ))
#     adjacent_index_compare_re = bool(re.search(
#         r"\[j\][<>]\[j\+1\]", compact
#     ))
#     adjacent_swap_re = bool(re.search(
#         r"\[[A-Za-z_]\w*\],\s*\[[A-Za-z_]\w*\+1\]=", compact
#     ))

#     # Bubble sort: adjacent comparison + exchange + nested/progressive scan.
#     adjacent_compare = _contains_any(
#         text,
#         (
#             "arr[j] > arr[j + 1]", "arr[j] < arr[j + 1]",
#             "a[j] > a[j + 1]", "a[j] < a[j + 1]",
#             "array[j] > array[j + 1]", "array[j] < array[j + 1]",
#             "data[j] > data[j + 1]", "data[j] < data[j + 1]",
#         ),
#     )
#     adjacent_swap = _contains_any(
#         text,
#         (
#             "arr[j], arr[j + 1] = arr[j + 1], arr[j]",
#             "a[j], a[j + 1] = a[j + 1], a[j]",
#             "array[j], array[j + 1] = array[j + 1], array[j]",
#             "swap(arr[j], arr[j + 1])",
#             "swap(a[j], a[j + 1])",
#             "std::swap(arr[j], arr[j + 1])",
#         ),
#     )
#     progressive_pass = _contains_any(
#         text,
#         (
#             "len(arr) - i - 1", "len(arr)-i-1",
#             "n - i - 1", "n-i-1",
#             "size - i - 1", "size-i-1",
#             "n - i", "n-i",
#         ),
#     )
#     adjacent_compare = adjacent_compare or _contains_any(compact, ("arr[j]>arr[j+1]", "arr[j]<arr[j+1]", "a[j]>a[j+1]", "a[j]<a[j+1]")) or adjacent_index_compare_re or bool(re.search(r"[A-Za-z_]\w*\[j\][<>][A-Za-z_]\w*\[j\+1\]", compact))
#     adjacent_swap = adjacent_swap or _contains_any(compact, ("arr[j],arr[j+1]=arr[j+1],arr[j]", "a[j],a[j+1]=a[j+1],a[j]", "swap(arr[j],arr[j+1])")) or adjacent_swap_re or bool(re.search(r"[A-Za-z_]\w*\[j\],[A-Za-z_]\w*\[j\+1\]=[A-Za-z_]\w*\[j\+1\],[A-Za-z_]\w*\[j\]", compact))
#     progressive_pass = progressive_pass or _contains_any(compact, ("len(arr)-i-1", "n-i-1", "size-i-1"))
#     if adjacent_compare and adjacent_swap:
#         features.bubble_sort_signals += 3
#     if adjacent_compare and progressive_pass:
#         features.bubble_sort_signals += 2

#     # Selection sort: select min/max over remaining suffix, then one swap.
#     selection_scan = _contains_any(
#         text,
#         (
#             "min_index", "minindex", "max_index", "maxindex",
#             "min_idx", "max_idx", "minimum_index", "maximum_index",
#             "min_pos", "max_pos",
#         ),
#     )
#     selection_compare = _contains_any(
#         text,
#         (
#             "arr[j] < arr[min", "arr[j] > arr[max",
#             "a[j] < a[min", "a[j] > a[max",
#             "array[j] < array[min", "array[j] > array[max",
#             "if arr[j] < arr[min", "if arr[j] > arr[max",
#         ),
#     )
#     if selection_scan and selection_compare and features.loops >= 2:
#         features.selection_sort_signals += 4

#     # Insertion sort: current key + backwards shift/compare.
#     insertion_key = _contains_any(
#         text,
#         ("key =", "key=", "current =", "current=", "value =", "value="),
#     )
#     insertion_shift = _contains_any(
#         text,
#         (
#             "arr[j + 1] = arr[j]", "arr[j+1] = arr[j]",
#             "a[j + 1] = a[j]", "a[j+1] = a[j]",
#             "array[j + 1] = array[j]", "array[j+1] = array[j]",
#             "j -= 1", "j-=1", "--j",
#         ),
#     )
#     if insertion_key and insertion_shift and features.loops >= 2:
#         features.insertion_sort_signals += 4

#     # Merge sort: recursive split into left/right halves + merge phase.
#     split_half = _contains_any(
#         text,
#         (
#             "mid = len(arr) // 2", "mid=len(arr)//2",
#             "mid = len(array) // 2", "mid=len(array)//2",
#             "mid = (left + right) // 2", "mid=(left+right)//2",
#             "mid = (low + high) // 2", "mid=(low+high)//2",
#         ),
#     )
#     split_slices = _contains_any(
#         text,
#         (
#             "arr[:mid]", "arr[mid:]",
#             "array[:mid]", "array[mid:]",
#             "left_half", "right_half",
#         ),
#     )
#     merge_phase = (
#         _contains_any(text, ("result.append", "merged.append", "merge("))
#         and _contains_any(text, ("while i < len(left)", "while i < len(right)", "i += 1", "j += 1"))
#     )
#     split_half = split_half or _contains_any(compact, ("mid=len(arr)//2", "mid=len(array)//2", "mid=(left+right)//2")) or bool(re.search(r"mid=len\([A-Za-z_]\w*\)//2", compact))
#     split_slices = split_slices or _contains_any(compact, ("arr[:mid]", "arr[mid:]", "array[:mid]", "array[mid:]")) or bool(re.search(r"[A-Za-z_]\w*\[:mid\]", compact) and re.search(r"[A-Za-z_]\w*\[mid:\]", compact))
#     merge_phase = merge_phase or (_contains_any(compact, ("result.append", "merged.append")) and _contains_any(compact, ("whilei<len(left)", "whilej<len(right)", "i+=1", "j+=1"))) or bool(re.search(r"\b(result|merged|output)\.append\(", compact) and re.search(r"i\+=1|j\+=1", compact))
#     if split_half and split_slices and merge_phase and features.recursion_signals:
#         features.merge_sort_signals += 6
#     elif split_half and split_slices and merge_phase:
#         features.merge_sort_signals += 5

#     # Quick sort: pivot + partition boundaries + recursive subranges.
#     pivot = _contains_any(
#         text,
#         ("pivot =", "pivot=", "pivot_index", "partition("),
#     )
#     partition = _contains_any(
#         text,
#         (
#             "i += 1", "j -= 1", "i++", "j--",
#             "arr[i] < pivot", "arr[j] > pivot",
#             "arr[i] > pivot", "arr[j] < pivot",
#             "partition_index", "partitionindex",
#         ),
#     )
#     recursive_subranges = (
#         features.recursion_signals >= 1
#         and (
#             _contains_any(
#                 text,
#                 (
#                     "partition(",
#                     "partition_index",
#                     "partitionindex",
#                     "low",
#                     "high",
#                     "left",
#                     "right",
#                 ),
#             )
#             or bool(
#                 re.search(
#                     r"\b[A-Za-z_]\w*\s*\([^)]*"
#                     r"(?:low|high|left|right)[^)]*\)",
#                     text,
#                 )
#             )
#         )
#     )   
#     pivot = pivot or _contains_any(compact, ("pivot=", "pivot_index", "partition("))
#     partition = partition or _contains_any(compact, ("arr[i]<pivot", "arr[j]>pivot", "arr[i]>pivot", "arr[j]<pivot", "i+=1", "j-=1")) or bool(re.search(r"[A-Za-z_]\w*\[i\][<>][A-Za-z_]\w*\[j\]|[A-Za-z_]\w*\[j\][<>]pivot|[A-Za-z_]\w*\[i\][<>]pivot", compact))
#     if pivot and partition and recursive_subranges:
#         features.quick_sort_signals += 6
#     elif pivot and partition:
#         features.quick_sort_signals += 4

#     # Heap sort: heapify/sift-down plus extraction/swap.
#     heapify = _contains_any(
#         text,
#         ("heapify", "sift_down", "siftdown", "build_heap", "buildheap"),
#     )
#     heap_extract = _contains_any(
#         text,
#         ("heap[0]", "heap[0] =", "arr[0]", "swap(arr[0]", "swap(a[0]"),
#     )
#     if heapify and heap_extract:
#         features.heap_sort_signals += 5

    

#     # --------------------------------------------------------
#     # GRAPH / BFS STRUCTURAL SIGNALS
#     # --------------------------------------------------------
#     # Python BFS commonly uses a plain list as a queue:
#     #
#     #   queue = [start]
#     #   while queue:
#     #       node = queue.pop(0)
#     #       for neighbor in graph[node]:
#     #           if neighbor not in visited:
#     #               visited.add(neighbor)
#     #               queue.append(neighbor)
#     #
#     # Do not require a queue library/API because list-backed
#     # queues are completely valid BFS implementations.

#     graph_adjacency = bool(
#         re.search(
#             r"\b[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
#             text,
#         )
#     )

#     neighbor_iteration = bool(
#         re.search(
#             r"\bfor\s+[A-Za-z_]\w*\s+in\s+"
#             r"[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
#             text,
#         )
#     )

#     visited_state = bool(
#         re.search(
#             r"\bvisited\b",
#             text,
#             re.IGNORECASE,
#         )
#     ) or (
#         bool(
#             re.search(
#                 r"\b(?:seen|discovered|marked)\b",
#                 text,
#                 re.IGNORECASE,
#             )
#         )
#     )

#     queue_initialization = bool(
#         re.search(
#             r"\b[A-Za-z_]\w*\s*=\s*\[[^\]]*\]",
#             text,
#         )
#     )

#     queue_pop_front = bool(
#         re.search(
#             r"\b[A-Za-z_]\w*\s*\.\s*pop\s*\(\s*0\s*\)",
#             text,
#             re.IGNORECASE,
#         )
#     )

#     queue_append = bool(
#         re.search(
#             r"\b[A-Za-z_]\w*\s*\.\s*append\s*\(",
#             text,
#             re.IGNORECASE,
#         )
#     )

#     if graph_adjacency:
#         features.graph_signals.append(
#             "Adjacency-style graph indexing detected."
#         )

#     if neighbor_iteration:
#         features.neighbor_iteration_signals += 2

#     if visited_state:
#         features.visited_state_signals += 1

#     if (
#         queue_initialization
#         and queue_pop_front
#         and queue_append
#     ):
#         features.queue_api_calls.append(
#             "list-backed queue traversal"
#         )

#     if (
#         graph_adjacency
#         and neighbor_iteration
#         and visited_state
#         and queue_pop_front
#         and queue_append
#     ):
#         features.graph_signals.append(
#             "Queue-based graph traversal detected."
#         )
#         features.visited_state_signals += 1



#     # --------------------------------------------------------
#     # LINEAR SEARCH
#     # --------------------------------------------------------
#     # Detect the algorithm from traversal + equality comparison.
#     # Variable/function names are NOT authoritative.
#     #
#     # Supported shapes include:
#     #
#     #   for value in arr:
#     #       if value == target:
#     #           ...
#     #
#     #   for item in values:
#     #       if item == needle:
#     #           ...
#     #
#     #   for i in range(len(data)):
#     #       if data[i] == key:
#     #           ...
#     #
#     #   while ...:
#     #       if data[i] == desired:
#     #           ...
#     # --------------------------------------------------------

#     direct_collection_scan = bool(
#         re.search(
#             r"\bfor\s+[A-Za-z_]\w*\s+in\s+[A-Za-z_]\w*\s*:",
#             text,
#             re.IGNORECASE,
#         )
#     )

#     indexed_scan = bool(
#         re.search(
#             r"\bfor\s+[A-Za-z_]\w*\s+in\s+range\s*\(",
#             text,
#             re.IGNORECASE,
#         )
#     )

#     sequential_scan = (
#         features.loops >= 1
#         and (
#             direct_collection_scan
#             or indexed_scan
#             or _contains_any(
#                 text,
#                 (
#                     "for i in range",
#                     "for (int i",
#                     "while (i",
#                     "while i <",
#                     "enumerate(",
#                 ),
#             )
#         )
#     )

#     # Generic equality between two values.
#     # Do not depend on the literal names target/key/value.
#     equality_compare = bool(
#         re.search(
#             r"\b[A-Za-z_]\w*(?:\[[^\]]+\])?\s*==\s*"
#             r"[A-Za-z_]\w*(?:\[[^\]]+\])?",
#             text,
#         )
#     )

#     # Search-like early success is strong supporting evidence.
#     early_success = bool(
#         re.search(
#             r"\b(?:return|break)\b",
#             text,
#         )
#     )

#     if (
#         sequential_scan
#         and equality_compare
#         and features.midpoint_signals == 0
#     ):
#         features.linear_search_signals += 2

#         if early_success:
#             features.linear_search_signals += 1

# # B5.16 - Conservative sorting detector

# def _detect_sorting(
#     features: ProgramFeatures,
# ) -> tuple[
#     bool,
#     list[str],
# ]:
#     evidence: list[str] = []

#     if features.sort_api_calls:
#         evidence.append(
#             "Standard-library sorting operation detected."
#         )

#         return True, evidence

#     if features.comparison_swap_signals >= 2:
#         evidence.extend(
#             [
#                 "Repeated comparison structure detected.",
#                 "Element exchange/update pattern detected.",
#             ]
#         )
#         return True, evidence

#     return False, evidence

# def _detect_array_patterns(
#     features: ProgramFeatures,
# ) -> list[tuple[str, str, float, list[str]]]:
#     candidates = []

#     if (
#         features.midpoint_signals >= 1
#         and features.boundary_narrowing_signals >= 1
#         and features.loops >= 1
#     ):
#         candidates.append(
#             (
#                 "binary-search",
#                 "searching",
#                 0.94,
#                 [
#                     "Midpoint-based search detected.",
#                     "Search boundaries are narrowed around the midpoint.",
#                 ],
#             )
#         )

#     if features.window_state_signals >= 1:
#         candidates.append(
#             (
#                 "sliding-window",
#                 "sliding-window",
#                 0.88,
#                 [
#                     "Window boundaries advance through the sequence."
#                 ],
#             )
#         )

#     if features.prefix_recurrence_signals >= 1:
#         candidates.append(
#             (
#                 "prefix-sum",
#                 "prefix-sum",
#                 0.90,
#                 features.dp_signals,
#             )
#         )

#     return candidates


# def _detect_graph_patterns(
#     features: ProgramFeatures,
# ) -> list[tuple[str, str, float, list[str]]]:
#     candidates = []

#     if (
#         features.graph_signals
#         and features.visited_state_signals >= 1
#         and features.neighbor_iteration_signals >= 1
#         and features.queue_api_calls
#     ):
#         candidates.append(
#             (
#                 "graph-traversal",
#                 "graph-traversal",
#                 0.94,
#                 [
#                     "Graph adjacency traversal detected.",
#                     "Visited-state tracking detected.",
#                     "Queue-based traversal detected.",
#                 ],
#             )
#         )

#     if (
#         features.graph_signals
#         and features.relaxation_signals >= 1
#         and features.heap_api_calls
#     ):
#         candidates.append(
#             (
#                 "graph-algorithm",
#                 "graph-algorithm",
#                 0.96,
#                 [
#                     "Graph structure detected.",
#                     "Distance relaxation detected.",
#                     "Priority queue / heap used for graph processing.",
#                 ],
#             )
#         )

#     return candidates


# def _detect_specialized_patterns(
#     features: ProgramFeatures,
# ) -> list[tuple[str, str, float, list[str]]]:
#     candidates = []

#     if features.tree_signals:
#         candidates.append(
#             (
#                 "tree-traversal",
#                 "tree-traversal",
#                 0.92,
#                 features.tree_signals,
#             )
#         )

#     if features.matrix_signals:
#         candidates.append(
#             (
#                 "matrix-processing",
#                 "matrix-processing",
#                 0.90,
#                 features.matrix_signals,
#             )
#         )

#     if features.string_signals:
#         candidates.append(
#             (
#                 "string-processing",
#                 "string-processing",
#                 0.84,
#                 features.string_signals,
#             )
#         )
    
#     if features.choice_undo_signals:
#         candidates.append(
#             (
#                 "backtracking",
#                 "backtracking",
#                 0.86,
#                 [
#                     "Recursive choice and undo structure detected."
#                 ],
#             )
#         )
    
#     if features.greedy_selection_signals:
#         candidates.append(
#             (
#                 "greedy",
#                 "greedy",
#                 0.82,
#                 [
#                     "Ordered selection with locally accepted intervals detected."
#                 ],
#             )
#         )
    
#     if features.dp_recurrence_signals or features.memoization_signals:
#         candidates.append(
#             (
#                 "dynamic-programming",
#                 "dynamic-programming",
#                 0.88,
#                 features.dp_signals,
#             )
#         )

#     if features.map_api_calls:
#         candidates.append(
#             (
#                 "hashing",
#                 "hashing",
#                 0.82,
#                 [
#                     "Hash-map/set access structure detected."
#                 ],
#             )
#         )

#     return candidates

# # B5.17 - Generic structural family detectors

# def _detect_generic_families(
#     features: ProgramFeatures,
# ) -> list[
#     tuple[str, str, float, list[str]]
# ]:
#     candidates = []

#     if features.recursion_signals:
#         candidates.append(
#             (
#                 "recursion",
#                 "recursion",
#                 0.78,
#                 [
#                     "Recursive self-call detected."
#                 ],
#             )
#         )

#     if features.heap_api_calls:
#         candidates.append(
#             (
#                 "priority-queue",
#                 "heap",
#                 0.72,
#                 [
#                     "Priority queue / heap API detected."
#                 ],
#             )
#         )

#     if features.queue_api_calls:
#         candidates.append(
#             (
#                 "queue-processing",
#                 "queue",
#                 0.70,
#                 [
#                     "Queue data structure detected."
#                 ],
#             )
#         )

#     if features.stack_api_calls:
#         candidates.append(
#             (
#                 "stack-processing",
#                 "stack",
#                 0.70,
#                 [
#                     "Stack data structure detected."
#                 ],
#             )
#         )

#     return candidates


# # B5.18 - Conservative classifier

# def _classify_algorithm(
#     features: ProgramFeatures,
# ) -> AlgorithmClassification:

#     candidates: list[
#         tuple[
#             str,
#             str,
#             str,
#             float,
#             list[str],
#         ]
#     ] = []

#     # Highest-confidence structural patterns first.

#     # Exact implementation detectors outrank generic recursion/sorting.
#     if features.bubble_sort_signals >= 4:
#         candidates.append((
#             "bubble-sort", "sorting", "specific", 0.98,
#             [
#                 "Adjacent element comparisons detected.",
#                 "Adjacent element exchange detected.",
#                 "Progressive bubble-sort pass structure detected.",
#             ],
#         ))

#     if features.merge_sort_signals >= 5:
#         candidates.append((
#             "merge-sort", "sorting", "specific", 0.99,
#             [
#                 "Array is divided around a midpoint.",
#                 "Left and right halves are processed recursively.",
#                 "Sorted halves are merged into a result sequence.",
#             ],
#         ))

#     if features.quick_sort_signals >= 4:
#         candidates.append((
#             "quick-sort", "sorting", "specific", 0.98,
#             [
#                 "Pivot-based partitioning detected.",
#                 "Partition boundaries are moved around the pivot.",
#             ],
#         ))

#     if features.insertion_sort_signals >= 4:
#         candidates.append((
#             "insertion-sort", "sorting", "specific", 0.97,
#             [
#                 "Current key/value is inserted into a sorted prefix.",
#                 "Elements are shifted while moving backward through the prefix.",
#             ],
#         ))

#     if features.selection_sort_signals >= 4:
#         candidates.append((
#             "selection-sort", "sorting", "specific", 0.97,
#             [
#                 "Minimum/maximum candidate is selected from the remaining range.",
#                 "Selected element is exchanged into its final position.",
#             ],
#         ))

#     if features.heap_sort_signals >= 5:
#         candidates.append((
#             "heap-sort", "sorting", "specific", 0.97,
#             [
#                 "Heap construction/sift-down structure detected.",
#                 "Repeated root extraction structure detected.",
#             ],
#         ))

#     # A genuine two-pointer traversal can contain equality checks and a
# # loop over the input, which may superficially resemble linear search.
# # When strong paired-boundary movement is present, prefer the dedicated
# # two-pointer classifier over the generic sequential-search signal.
#     if (
#         features.linear_search_signals >= 3
#         and features.pointer_pair_signals < 2
#         and features.midpoint_signals == 0
#     ):
#         candidates.append(
#             (
#                 "linear-search",
#                 "searching",
#                 "specific",
#                 0.97,
#                 [
#                     "Sequential scan through the input detected.",
#                     "Element-to-target equality comparison detected.",
#                 ],
#             )
#         )

#     if (
#         features.midpoint_signals >= 1
#         and features.boundary_narrowing_signals >= 2
#         and features.loops >= 1
#     ):
#         candidates.append(
#             (
#                 "binary-search",
#                 "searching",
#                 "specific",
#                 0.97,
#                 [
#                     "Midpoint-based search detected.",
#                     "Search boundaries are repeatedly narrowed.",
#                 ],
#             )
#         )

#     if (
#         features.window_state_signals >= 2
#         and not (
#             features.graph_signals
#             and features.visited_state_signals >= 1
#             and features.queue_api_calls
#         )
#     ):
#         candidates.append(
#             (
#                 "sliding-window",
#                 "sliding-window",
#                 "specific",
#                 0.95,
#                 [
#                     "Two moving window boundaries detected.",
#                     "Window expansion and contraction structure detected.",
#                 ],
#             )
#         )

#     if features.pointer_pair_signals >= 2:
#         candidates.append(
#             (
#                 "two-pointers",
#                 "two-pointers",
#                 "specific",
#                 0.93,
#                 [
#                     "Paired boundary pointers detected.",
#                     "Pointer movement structure detected.",
#                 ],
#             )
#         )

#     if features.prefix_recurrence_signals >= 2:
#         candidates.append(
#             (
#                 "prefix-sum",
#                 "prefix-sum",
#                 "specific",
#                 0.94,
#                 [
#                     "Prefix-array recurrence detected."
#                 ],
#             )
#         )

#     if features.tree_signals:
#         candidates.append(
#             (
#                 "tree-traversal",
#                 "tree-traversal",
#                 "specific",
#                 0.95,
#                 features.tree_signals,
#             )
#         )

#     if (
#         features.graph_signals
#         and features.relaxation_signals >= 2
#     ):
#         candidates.append(
#             (
#                 "graph-algorithm",
#                 "graph-algorithm",
#                 "specific",
#                 0.97,
#                 [
#                     "Graph structure detected.",
#                     "Shortest-path relaxation detected.",
#                 ],
#             )
#         )

#     elif (
#         features.graph_signals
#         and features.visited_state_signals >= 1
#         and features.queue_api_calls
#     ):
#         candidates.append(
#             (
#                 "graph-traversal",
#                 "graph-traversal",
#                 "specific",
#                 0.95,
#                 [
#                     "Graph adjacency structure detected.",
#                     "Visited-state tracking detected.",
#                     "Queue-based traversal detected.",
#                 ],
#             )
#         )

#     if features.matrix_signals:
#         candidates.append(
#             (
#                 "matrix-processing",
#                 "matrix-processing",
#                 "family",
#                 0.93,
#                 features.matrix_signals,
#             )
#         )

#     if features.choice_undo_signals >= 2:
#         candidates.append(
#             (
#                 "backtracking",
#                 "backtracking",
#                 "specific",
#                 0.93,
#                 [
#                     "Recursive choice exploration detected.",
#                     "State undo/backtrack structure detected.",
#                 ],
#             )
#         )

#     if (
#         features.dp_recurrence_signals >= 2
#         or features.memoization_signals >= 1
#     ):
#         candidates.append(
#             (
#                 "dynamic-programming",
#                 "dynamic-programming",
#                 "family",
#                 0.94,
#                 features.dp_signals,
#             )
#         )

#     if features.greedy_selection_signals >= 2:
#         candidates.append(
#             (
#                 "greedy",
#                 "greedy",
#                 "family",
#                 0.91,
#                 [
#                     "Selection-based optimization structure detected."
#                 ],
#             )
#         )

#     if features.string_signals:
#         candidates.append(
#             (
#                 "string-processing",
#                 "string-processing",
#                 "family",
#                 0.88,
#                 features.string_signals,
#             )
#         )

#     if (
#         features.boundary_narrowing_signals >= 1
#         and features.midpoint_signals >= 1
#         and features.loops >= 1
#     ):
#         candidates.append(
#             (
#                 "binary-search",
#                 "searching",
#                 "specific",
#                 0.94,
#                 [
#                     "Midpoint-based search structure detected.",
#                     "Search boundaries narrow around the midpoint.",
#                 ],
#             )
#         )

#     if (
#         features.pointer_pair_signals >= 1
#         and features.boundary_narrowing_signals >= 1
#         and features.midpoint_signals == 0
#     ):
#         candidates.append(
#             (
#                 "two-pointers",
#                 "two-pointers",
#                 "specific",
#                 0.88,
#                 [
#                     "Two moving boundary pointers detected.",
#                     "Boundary narrowing structure detected.",
#                 ],
#             )
#         )

#     if (
#         features.neighbor_iteration_signals >= 2
#         or features.window_state_signals >= 1
#     ):
#         candidates.append(
#             (
#                 "sliding-window",
#                 "sliding-window",
#                 "specific",
#                 0.88,
#                 [
#                     "Window boundaries advance through the input."
#                 ],
#             )
#         )

#     if features.graph_signals and features.relaxation_signals:
#         candidates.append(
#             (
#                 "graph-algorithm",
#                 "graph-algorithm",
#                 "specific",
#                 0.96,
#                 [
#                     "Graph structure detected.",
#                     "Shortest-path relaxation structure detected.",
#                 ],
#             )
#         )

#     if (
#         features.graph_signals
#         and features.visited_state_signals >= 1
#         and features.queue_api_calls
#     ):
#         candidates.append(
#             (
#                 "graph-traversal",
#                 "graph-traversal",
#                 "specific",
#                 0.94,
#                 [
#                     "Graph adjacency traversal detected.",
#                     "Visited-state tracking detected.",
#                     "Queue-based traversal detected.",
#                 ],
#             )
#         )


#     if features.tree_signals:
#         candidates.append(
#             (
#                 "tree-traversal",
#                 "tree-traversal",
#                 "specific",
#                 0.92,
#                 features.tree_signals,
#             )
#         )

#     if features.dp_recurrence_signals or features.memoization_signals:
#         candidates.append(
#             (
#                 "dynamic-programming",
#                 "dynamic-programming",
#                 "family",
#                 0.88,
#                 features.dp_signals,
#             )
#         )

#     if features.matrix_signals:
#         candidates.append(
#             (
#                 "matrix-processing",
#                 "matrix-processing",
#                 "family",
#                 0.90,
#                 features.matrix_signals,
#             )
#         )

#     if features.string_signals:
#         candidates.append(
#             (
#                 "string-processing",
#                 "string-processing",
#                 "family",
#                 0.84,
#                 features.string_signals,
#             )
#         )

#     for (
#         name,
#         family,
#         confidence,
#         evidence,
#     ) in _detect_array_patterns(features):
#         candidates.append(
#             (
#                 name,
#                 family,
#                 "specific",
#                 confidence,
#                 evidence,
#             )
#         )

#     for (
#         name,
#         family,
#         confidence,
#         evidence,
#     ) in _detect_graph_patterns(features):
#         candidates.append(
#             (
#                 name,
#                 family,
#                 "specific",
#                 confidence,
#                 evidence,
#             )
#         )

#     for (
#         name,
#         family,
#         confidence,
#         evidence,
#     ) in _detect_specialized_patterns(features):
#         candidates.append(
#             (
#                 name,
#                 family,
#                 "family",
#                 confidence,
#                 evidence,
#             )
#         )

#     binary_search, binary_evidence = (
#         _detect_binary_search(features)
#     )

#     if binary_search:
#         candidates.append(
#             (
#                 "binary-search",
#                 "searching",
#                 "specific",
#                 0.94,
#                 binary_evidence,
#             )
#         )

#     sorting, sorting_evidence = (
#         _detect_sorting(features)
#     )

#     if sorting and features.greedy_selection_signals < 2:
#         candidates.append(
#             (
#                 "sorting",
#                 "sorting",
#                 "family",
#                 0.90,
#                 sorting_evidence,
#             )
#         )

#     for (
#         name,
#         family,
#         confidence,
#         evidence,
#     ) in _detect_generic_families(
#         features
#     ):
#         candidates.append(
#             (
#                 name,
#                 family,
#                 "generic",
#                 confidence,
#                 evidence,
#             )
#         )

#     if not candidates:
#         return AlgorithmClassification(
#             name="custom",
#             family="custom",
#             specificity="unknown",
#             confidence=0.35,
#             evidence=[
#                 "No sufficiently strong structural "
#                 "algorithm pattern was detected."
#             ],
#         )



#     # --------------------------------------------------------
#     # GRAPH TRAVERSAL HAS PRIORITY OVER GENERIC WINDOW SIGNALS
#     # --------------------------------------------------------
#     # A BFS implementation may superficially look like a
#     # sliding-window traversal because both can contain:
#     #   - a loop
#     #   - advancing variables
#     #   - queue/list mutation
#     #
#     # Strong graph evidence must therefore dominate those
#     # generic sequence/window signals.

#     is_graph_traversal = (
#         bool(features.graph_signals)
#         and features.visited_state_signals >= 1
#         and bool(features.queue_api_calls)
#         and features.neighbor_iteration_signals >= 1
#     )

#     if is_graph_traversal:
#         candidates = [
#             candidate
#             for candidate in candidates
#             if candidate[0] not in {
#                 "sliding-window",
#                 "two-pointers",
#             }
#         ]

#     # Library-backed sorting is intentionally generic. When a standard
#     # sorting API is present, prevent incidental structural patterns such
#     # as two-pointers/sliding-window from overriding the library-sort
#     # classification.
#     if features.sort_api_calls:
#         allowed_library_sort_candidates = {
#             "sorting",
#             "binary-search",
#         }

#         # Sorting may be a preparatory step for a higher-level algorithm.
#         # Preserve strong greedy evidence instead of allowing the library-sort
#         # guard to erase the actual algorithm classification.
#         if features.greedy_selection_signals >= 2:
#             allowed_library_sort_candidates.add("greedy")

#         candidates = [
#             candidate
#             for candidate in candidates
#             if candidate[0] in allowed_library_sort_candidates
#         ]
#     candidates.sort(
#         key=lambda item: (
#             {
#                 "specific": 3,
#                 "family": 2,
#                 "generic": 1,
#                 "unknown": 0,
#             }[item[2]],
#             item[3],
#         ),
#         reverse=True,
#     )

#     best = candidates[0]

#     return AlgorithmClassification(
#         name=best[0],
#         family=best[1],
#         specificity=best[2],
#         confidence=best[3],
#         evidence=best[4],
#     )


# # B5.19 - Conservative complexity estimator

# def _estimate_complexity(
#     features: ProgramFeatures,
#     algorithm: AlgorithmClassification,
# ) -> ComplexityEstimate:

#     if algorithm.name == "sliding-window":
#         return ComplexityEstimate(
#             time="O(n)",
#             space=None,
#             confidence=0.82,
#             evidence=[
#                 "Window boundaries advance monotonically."
#             ],
#         )

#     if algorithm.name == "two-pointers":
#         return ComplexityEstimate(
#             time="O(n)",
#             space=None,
#             confidence=0.82,
#             evidence=[
#                 "Two pointers move through the input."
#             ],
#         )

#     if algorithm.name == "prefix-sum":
#         return ComplexityEstimate(
#             time="O(n)",
#             space="O(n)",
#             confidence=0.88,
#             evidence=[
#                 "Prefix recurrence builds cumulative values."
#             ],
#         )

#     if algorithm.name == "graph-traversal":
#         return ComplexityEstimate(
#             time="O(V + E)",
#             space="O(V)",
#             confidence=0.88,
#             evidence=[
#                 "Graph adjacency traversal with visited-state tracking."
#             ],
#         )

#     if algorithm.name == "graph-algorithm":
#         return ComplexityEstimate(
#             time="O((V + E) log V)",
#             space="O(V)",
#             confidence=0.80,
#             evidence=[
#                 "Priority-queue graph relaxation detected."
#             ],
#         )

#     if algorithm.name == "matrix-processing":
#         return ComplexityEstimate(
#             time="O(n²)",
#             space=None,
#             confidence=0.82,
#             evidence=[
#                 "Two-dimensional matrix traversal detected."
#             ],
#         )

#     if algorithm.name == "dynamic-programming":
#         return ComplexityEstimate(
#             time=None,
#             space=None,
#             confidence=0.45,
#             evidence=[
#                 "Dynamic-programming structure detected; "
#                 "exact recurrence bounds require further analysis."
#             ],
#         )

#     if algorithm.name == "binary-search":
#         return ComplexityEstimate(
#             time="O(log n)",
#             space="O(1)",
#             confidence=0.88,
#             evidence=[
#                 "Repeated search-space narrowing detected."
#             ],
#         )

#     if algorithm.name == "graph-traversal":
#         return ComplexityEstimate(
#             time="O(V + E)",
#             space="O(V)",
#             confidence=0.84,
#             evidence=[
#                 "Graph traversal with adjacency iteration "
#                 "and visited-state tracking detected."
#             ],
#         )

#     if algorithm.name == "graph-algorithm":
#         return ComplexityEstimate(
#             time="O((V + E) log V)",
#             space="O(V)",
#             confidence=0.78,
#             evidence=[
#                 "Graph relaxation with priority-queue processing detected."
#             ],
#         )

#     if algorithm.name == "matrix-processing":
#         return ComplexityEstimate(
#             time="O(n²)",
#             space=None,
#             confidence=0.72,
#             evidence=[
#                 "Nested matrix/grid traversal detected."
#             ],
#         )

#     if algorithm.name == "sorting":
#         if features.sort_api_calls:
#             return ComplexityEstimate(
#                 time="O(n log n)",
#                 space=None,
#                 confidence=0.62,
#                 evidence=[
#                     "Library sorting operation detected; "
#                     "internal implementation is not assumed."
#                 ],
#             )

#     if features.nested_loop_depth >= 2:
#         return ComplexityEstimate(
#             time="O(n²)",
#             space=None,
#             confidence=0.48,
#             evidence=[
#                 "Nested loop structure detected, "
#                 "but loop bounds could not be fully resolved."
#             ],
#         )

#     return ComplexityEstimate(
#         time=None,
#         space=None,
#         confidence=0.0,
#         evidence=[
#             "Insufficient structural evidence for "
#             "a reliable complexity estimate."
#         ],
#     )


# # B5.20 - Public algorithm analysis API

# def analyze_algorithm(
#     reference_code: str,
#     language: str,
# ) -> dict[str, Any]:

#     if not reference_code or not reference_code.strip():
#         return {
#             "algorithm": {
#                 "name": "custom",
#                 "family": "custom",
#                 "specificity": "unknown",
#                 "confidence": 0.0,
#                 "evidence": [
#                     "Reference code is empty."
#                 ],
#             },
#             "complexity": {
#                 "time": None,
#                 "space": None,
#                 "confidence": 0.0,
#                 "evidence": [],
#             },
#             "detection": {
#                 "method": "no-source",
#                 "parser": None,
#                 "confidence": 0.0,
#             },
#         }

#     parse_result = _parse_reference_code(
#         reference_code,
#         language,
#     )

#     features = _extract_program_features(
#         reference_code,
#         language,
#         parse_result,
#     )

#     classification = _classify_algorithm(
#         features
#     )

#     complexity = _estimate_complexity(
#         features,
#         classification,
#     )

#     parser_confidence = max(
#         0.0,
#         min(
#             1.0,
#             features.structural_quality,
#         ),
#     )

#     # Source-structural fallback can still be high-confidence when a
#     # specific implementation pattern is unambiguous. Parser availability
#     # must not turn a strong Merge/Bubble/Quick/Linear detector into a generic
#     # or unreliable result.
#     if not parse_result.success:
#         if classification.specificity == "specific":
#             parser_confidence = max(parser_confidence, 0.82)
#         elif classification.specificity == "family":
#             parser_confidence = max(parser_confidence, 0.75)

#     final_confidence = round(
#         min(
#             classification.confidence,
#             max(
#                 0.20,
#                 parser_confidence,
#             ),
#         ),
#         2,
#     )

#     classification.confidence = (
#         final_confidence
#     )

#     return {
#         "algorithm": {
#             "name": classification.name,
#             "family": classification.family,
#             "specificity": classification.specificity,
#             "confidence": classification.confidence,
#             "evidence": classification.evidence,
#         },
#         "complexity": {
#             "time": complexity.time,
#             "space": complexity.space,
#             "confidence": complexity.confidence,
#             "evidence": complexity.evidence,
#         },
#         "detection": {
#             "method": (
#                 "tree-sitter-structural"
#                 if parse_result.success
#                 else "source-structural-fallback"
#             ),
#             "parser": parse_result.parser_name,
#             "confidence": classification.confidence,
#             "parse_success": parse_result.success,
#             "parse_error_count": (
#                 parse_result.error_count
#             ),
#             "error": parse_result.error,
#         },
#     }




















from __future__ import annotations

from dataclasses import dataclass, field
import re
from pathlib import Path
import tempfile
from typing import Any, Iterable, Sequence

try:
    from tree_sitter_language_pack import configure, get_parser
except ImportError:
    configure = None
    get_parser = None


if configure is not None:
    # The language pack downloads parser libraries lazily.  Use a writable
    # temporary cache instead of a user-profile location, which can be locked
    # down in services, containers, and CI environments.
    configure({
        "cache_dir": str(
            Path(tempfile.gettempdir()) / "green-code-tree-sitter"
        )
    })


# Supported language mapping

LANGUAGE_PARSER_NAMES: dict[str, str] = {
    "c": "c",
    "c++": "cpp",
    "cpp": "cpp",
    "java": "java",
    "python": "python",
    "javascript": "javascript",
    "js": "javascript",
    "go": "go",
    "rust": "rust",
    "c#": "csharp",
    "csharp": "csharp",
    "kotlin": "kotlin",
    "php": "php",
}

# Typed models


@dataclass
class ParseResult:
    language: str
    parser_name: str | None
    success: bool
    root: Any | None = None
    error: str | None = None
    error_count: int = 0


@dataclass
class ProgramFeatures:
    language: str

    node_counts: dict[str, int] = field(default_factory=dict)

    loops: int = 0
    while_loops: int = 0
    for_loops: int = 0
    nested_loop_depth: int = 0

    function_count: int = 0
    function_calls: int = 0
    recursive_calls: int = 0

    array_accesses: int = 0
    member_accesses: int = 0
    comparisons: int = 0
    assignments: int = 0

    sort_api_calls: list[str] = field(default_factory=list)
    search_api_calls: list[str] = field(default_factory=list)
    stack_api_calls: list[str] = field(default_factory=list)
    queue_api_calls: list[str] = field(default_factory=list)
    heap_api_calls: list[str] = field(default_factory=list)

    map_api_calls: list[str] = field(default_factory=list)
    set_api_calls: list[str] = field(default_factory=list)

    graph_signals: list[str] = field(default_factory=list)
    tree_signals: list[str] = field(default_factory=list)
    dp_signals: list[str] = field(default_factory=list)
    string_signals: list[str] = field(default_factory=list)
    matrix_signals: list[str] = field(default_factory=list)

    midpoint_signals: int = 0
    boundary_narrowing_signals: int = 0
    neighbor_iteration_signals: int = 0
    visited_state_signals: int = 0
    relaxation_signals: int = 0

    recursion_signals: int = 0
    memoization_signals: int = 0
    comparison_swap_signals: int = 0
    bubble_sort_signals: int = 0
    selection_sort_signals: int = 0
    insertion_sort_signals: int = 0
    merge_sort_signals: int = 0
    quick_sort_signals: int = 0
    heap_sort_signals: int = 0
    linear_search_signals: int = 0
    pointer_pair_signals: int = 0
    window_state_signals: int = 0
    prefix_recurrence_signals: int = 0
    choice_undo_signals: int = 0
    greedy_selection_signals: int = 0
    dp_recurrence_signals: int = 0
    array_dimension_signals: int = 0
    self_call_names: set[str] = field(default_factory=set)

    library_signals: list[str] = field(default_factory=list)

    parse_error_nodes: int = 0
    structural_quality: float = 0.0


@dataclass
class AlgorithmClassification:
    name: str
    family: str
    specificity: str
    confidence: float
    evidence: list[str] = field(default_factory=list)


@dataclass
class ComplexityEstimate:
    time: str | None
    space: str | None
    confidence: float
    evidence: list[str] = field(default_factory=list)


@dataclass
class AlgorithmAnalysis:
    algorithm: AlgorithmClassification
    complexity: ComplexityEstimate
    detection: dict[str, Any]


# Node abstraction

def _node_type(node: Any) -> str:
    value = getattr(node, "type", None)

    if isinstance(value, str):
        return value

    value = getattr(node, "kind", None)

    if isinstance(value, str):
        return value

    return ""


def _node_children(node: Any) -> list[Any]:
    children = getattr(node, "children", None)

    if children is None:
        return []

    if callable(children):
        try:
            children = children()
        except TypeError:
            return []

    try:
        return list(children)
    except TypeError:
        return []


def _node_text(node: Any, source: bytes) -> str:
    try:
        return source[
            node.start_byte:node.end_byte
        ].decode("utf-8", errors="replace")
    except Exception:
        return ""


def _normalized_source(reference_code: str) -> str:
    """Normalize source only for supplemental structural signals."""
    return " ".join(
        reference_code
        .replace("\r", " ")
        .replace("\n", " ")
        .split()
    ).lower()


def _contains_any_text(
    source: str,
    patterns: Sequence[str],
) -> bool:
    return any(pattern.lower() in source for pattern in patterns)


def _contains_any(
    source: str,
    patterns: Sequence[str],
) -> bool:
    return any(
        pattern.lower() in source
        for pattern in patterns
    )


def _count_any_text(
    source: str,
    patterns: Sequence[str],
) -> int:
    return sum(
        source.count(pattern.lower())
        for pattern in patterns
    )

# Parser adapter

def _parse_reference_code(
    reference_code: str,
    language: str,
) -> ParseResult:
    normalized_language = (
        language or ""
    ).strip().lower()

    parser_name = LANGUAGE_PARSER_NAMES.get(
        normalized_language
    )

    if parser_name is None:
        return ParseResult(
            language=normalized_language,
            parser_name=None,
            success=False,
            error=(
                f"Unsupported parser language: "
                f"{language}"
            ),
        )

    if get_parser is None:
        return ParseResult(
            language=normalized_language,
            parser_name=parser_name,
            success=False,
            error=(
                "Tree-sitter language pack is not installed."
            ),
        )

    try:
        parser = get_parser(parser_name)

        source_bytes = reference_code.encode(
            "utf-8"
        )

        tree = parser.parse(source_bytes)

        root = getattr(
            tree,
            "root_node",
            None,
        )

        if root is None:
            return ParseResult(
                language=normalized_language,
                parser_name=parser_name,
                success=False,
                error="Parser returned no root node.",
            )

        error_count = _count_parse_errors(root)

        return ParseResult(
            language=normalized_language,
            parser_name=parser_name,
            success=True,
            root=root,
            error_count=error_count,
        )

    except Exception as exc:
        return ParseResult(
            language=normalized_language,
            parser_name=parser_name,
            success=False,
            error=str(exc),
        )


# Parse-error counting

def _count_parse_errors(node: Any) -> int:
    count = 0

    node_type = _node_type(node)

    if node_type in {
        "ERROR",
        "MISSING",
    }:
        count += 1

    for child in _node_children(node):
        count += _count_parse_errors(child)

    return count


# Generic tree traversal


# B5.9 - Generic tree traversal

def _walk_tree(
    node: Any,
) -> Iterable[Any]:
    yield node

    for child in _node_children(node):
        yield from _walk_tree(child)


def _count_node_types(
    root: Any,
) -> dict[str, int]:
    counts: dict[str, int] = {}

    for node in _walk_tree(root):
        node_type = _node_type(node)

        if not node_type:
            continue

        counts[node_type] = (
            counts.get(node_type, 0) + 1
        )

    return counts


# B5.10 - Structural loop analysis

_LOOP_NODE_TYPES = {
    "for_statement",
    "for_in_statement",
    "while_statement",
    "do_statement",
    "for_clause",
}


def _loop_depth(
    node: Any,
    current_depth: int = 0,
) -> int:
    node_type = _node_type(node)

    next_depth = current_depth

    if node_type in _LOOP_NODE_TYPES:
        next_depth += 1

    maximum = next_depth

    for child in _node_children(node):
        maximum = max(
            maximum,
            _loop_depth(child, next_depth),
        )

    return maximum


# B5.11 - Function and recursion extraction

_FUNCTION_NODE_TYPES = {
    "function_definition",
    "method_declaration",
    "function_declaration",
    "function_item",
    "method_definition",
}


def _extract_function_names(
    root: Any,
    source: bytes,
) -> set[str]:
    names: set[str] = set()

    for node in _walk_tree(root):
        if _node_type(node) not in _FUNCTION_NODE_TYPES:
            continue

        function_text = _node_text(
            node,
            source,
        )

        match = re.search(
            r"(?:function\s+)?([A-Za-z_]\w*)\s*\(",
            function_text,
        )

        if match:
            names.add(match.group(1))
            continue

        for child in _node_children(node):
            child_type = _node_type(child)

            if child_type in {
                "identifier",
                "field_identifier",
                "property_identifier",
            }:
                names.add(
                    _node_text(
                        child,
                        source,
                    ).strip()
                )
                break

    return names


# B5.12 - Normalized API recognition

API_PATTERNS: dict[str, dict[str, tuple[str, ...]]] = {
    "python": {
        "sorting": (
            "sorted",
            ".sort",
        ),
        "heap": (
            "heapq.heappush",
            "heapq.heappop",
            "heapq.heapify",
        ),
        "queue": (
            "collections.deque",
            "deque",
        ),
    },
    "cpp": {
        "sorting": (
            "std::sort",
            "sort",
        ),
        "heap": (
            "std::priority_queue",
            "priority_queue",
        ),
        "queue": (
            "std::queue",
            "queue",
        ),
        "stack": (
            "std::stack",
            "stack",
        ),
    },
    "java": {
        "sorting": (
            "Arrays.sort",
            "Collections.sort",
        ),
        "heap": (
            "PriorityQueue",
        ),
        "queue": (
            "Queue",
            "ArrayDeque",
        ),
    },
    "javascript": {
        "sorting": (
            ".sort",
        ),
    },
    "go": {
        "sorting": (
            "sort.Ints",
            "sort.Slice",
            "sort.Sort",
        ),
        "heap": (
            "container/heap",
        ),
    },
    "rust": {
        "sorting": (
            ".sort()",
            ".sort_unstable()",
        ),
        "heap": (
            "BinaryHeap",
        ),
        "queue": (
            "VecDeque",
        ),
    },
    "csharp": {
        "sorting": (
            "Array.Sort",
            "List.Sort",
        ),
        "heap": (
            "PriorityQueue",
        ),
    },
    "kotlin": {
        "sorting": (
            "sorted",
            "sort",
        ),
        "queue": (
            "ArrayDeque",
        ),
    },
    "php": {
        "sorting": (
            "sort(",
            "sort (",
        ),
    },
}


# B5.13 - API recognition helper

def _detect_library_signals(
    reference_code: str,
    language: str,
) -> tuple[
    dict[str, list[str]],
    list[str],
]:
    normalized_language = (
        language or ""
    ).strip().lower()

    source = reference_code.lower()

    language_patterns = API_PATTERNS.get(
        normalized_language,
        {},
    )

    detected: dict[str, list[str]] = {}
    evidence: list[str] = []

    for operation, patterns in (
        language_patterns.items()
    ):
        matches = []

        for pattern in patterns:
            if pattern.lower() in source:
                matches.append(pattern)

        if matches:
            detected[operation] = matches

            for match in matches:
                evidence.append(
                    f"Detected {operation} API: {match}"
                )

    return detected, evidence

def _has_recursive_self_call(
    reference_code: str,
    function_name: str,
) -> bool:
    """
    Conservative source-level recursion fallback.

    A function declaration plus a normal call from outside the
    function must NOT be treated as recursion.

    Recursion is reported only when the function name appears as
    a call inside its own function body.
    """
    name = (function_name or "").strip()

    if not name:
        return False

    escaped_name = re.escape(name)

    # Common cross-language function/method declarations.
    declaration_patterns = (
        # Python
        rf"\bdef\s+{escaped_name}\s*\([^)]*\)\s*:",

        # JavaScript
        rf"\bfunction\s+{escaped_name}\s*\([^)]*\)\s*\{{",

        # C / C++ / Java / C# / Kotlin-like declarations
        rf"\b(?:public\s+|private\s+|protected\s+|static\s+|"
        rf"final\s+|inline\s+|virtual\s+|suspend\s+)*"
        rf"[A-Za-z_][\w<>\[\],.?*&:\s]*\s+"
        rf"{escaped_name}\s*\([^;{{}}]*\)\s*\{{",

        # Go
        rf"\bfunc\s+{escaped_name}\s*\([^)]*\)[^{{]*\{{",

        # Rust
        rf"\bfn\s+{escaped_name}\s*\([^)]*\)[^{{]*\{{",

        # PHP
        rf"\bfunction\s+{escaped_name}\s*\([^)]*\)\s*\{{",
    )

    declaration_match = None

    for pattern in declaration_patterns:
        declaration_match = re.search(
            pattern,
            reference_code,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        if declaration_match:
            break

    if not declaration_match:
        return False

    body_start = declaration_match.end()

    # Python: inspect the indented function body.
    if re.match(
        rf"\s*def\s+{escaped_name}\b",
        declaration_match.group(0),
        flags=re.IGNORECASE,
    ):
        lines = reference_code[body_start:].splitlines()

        body_lines = []

        for line in lines:
            if not line.strip():
                body_lines.append(line)
                continue

            if line[:1].isspace():
                body_lines.append(line)
                continue

            break

        body = "\n".join(body_lines)

    else:
        # Brace-based languages: find the matching closing brace.
        opening_brace = reference_code.find(
            "{",
            declaration_match.start(),
        )

        if opening_brace == -1:
            return False

        depth = 0
        closing_brace = None

        for index in range(
            opening_brace,
            len(reference_code),
        ):
            char = reference_code[index]

            if char == "{":
                depth += 1

            elif char == "}":
                depth -= 1

                if depth == 0:
                    closing_brace = index
                    break

        if closing_brace is None:
            return False

        body = reference_code[
            opening_brace + 1:closing_brace
        ]

    return bool(
        re.search(
            rf"\b{escaped_name}\s*\(",
            body,
            flags=re.IGNORECASE,
        )
    )

def _extract_semantic_signals(
    reference_code: str,
    features: ProgramFeatures,
    function_names: set[str],
) -> None:
    source = _normalized_source(reference_code)

    if (
        features.loops >= 2
        and features.comparisons >= 1
        and _contains_any(
            source,
            (
                "swap(",
                "std::swap",
                "temp =",
                "temp=",
                "arr[j] > arr[j + 1]",
                "arr[j] < arr[j + 1]",
                "a[j] > a[j + 1]",
                "a[j] < a[j + 1]",
                "data[j] < data[i]",
                "data[i], data[j] = data[j], data[i]",
            ),
        )
    ):
        features.comparison_swap_signals += 2

    if _contains_any(
        source,
        (
            "mid =",
            "mid=",
            "middle =",
            "middle=",
            "(low + high) / 2",
            "(left + right) / 2",
            "low + (high - low) / 2",
        ),
    ):
        features.midpoint_signals += 1

    if _contains_any(
        source,
        (
            "low = mid + 1",
            "low=mid+1",
            "lo = mid + 1",
            "lo=mid+1",
            "left = mid + 1",
            "left=mid+1",
            "high = mid - 1",
            "high=mid-1",
            "hi = mid - 1",
            "hi=mid-1",
            "right = mid - 1",
            "right=mid-1",
            "start = middle + 1",
            "finish = middle - 1",
        ),
    ):
        features.boundary_narrowing_signals += 2

    # --------------------------------------------------------
    # Two-pointer structural signal
    # --------------------------------------------------------
    # A normal loop such as:
    #
    #     for (let i = 0; i < n; i++)
    #
    # must NOT be classified as two-pointers.
    #
    # Two-pointers requires evidence for TWO distinct moving
    # indices/boundaries.

    left_right_pair = (
        _contains_any(
            source,
            (
                "left =",
                "left=",
                "l =",
                "l=",
            ),
        )
        and _contains_any(
            source,
            (
                "right =",
                "right=",
                "r =",
                "r=",
            ),
        )
        and _contains_any(
            source,
            (
                "left += 1",
                "left++",
                "++left",
                "l += 1",
                "l++",
                "++l",
            ),
        )
        and _contains_any(
            source,
            (
                "right -= 1",
                "right--",
                "--right",
                "r -= 1",
                "r--",
                "--r",
            ),
        )
    )

    ij_pair = (
        _contains_any(
            source,
            (
                "i =",
                "i=",
            ),
        )
        and _contains_any(
            source,
            (
                "j =",
                "j=",
            ),
        )
        and _contains_any(
            source,
            (
                "i += 1",
                "i++",
                "++i",
            ),
        )
        and _contains_any(
            source,
            (
                "j -= 1",
                "j--",
                "--j",
            ),
        )
    )

    if left_right_pair or ij_pair:
        features.pointer_pair_signals += 2

    if (
        _contains_any(
            source,
            (
                "left += 1",
                "left++",
                "l += 1",
                "l++",
                "start += 1",
                "start++",
            ),
        )
        and _contains_any(
            source,
            (
                "right += 1",
                "right++",
                "r += 1",
                "r++",
                "end += 1",
                "end++",
                "++end",
            ),
        )
    ):
        features.window_state_signals += 2

    if (
        features.window_state_signals >= 2
        and _contains_any(
            source,
            (
                "count[",
                "freq[",
                "frequency",
                "window_sum",
                "current_sum",
                "while ",
            ),
        )
    ):
        features.window_state_signals += 1

    if (
        (
            "prefix[" in source
            or "cumulative[" in source
        )
        and _contains_any(
            source,
            (
                "prefix[i + 1]",
                "prefix[i+1]",
                "prefix[i + 1] = prefix[i]",
                "prefix[i+1] = prefix[i]",
                "cumulative[index + 1]",
                "cumulative[index+1]",
                "cumulative[index + 1] = cumulative[index]",
                "cumulative[index+1] = cumulative[index]",
            ),
        )
    ):
        features.prefix_recurrence_signals += 2

    if (
        _contains_any(source, (".left", "->left", "left_child", "leftchild"))
        and _contains_any(source, (".right", "->right", "right_child", "rightchild"))
    ):
        features.tree_signals.append(
            "Binary-tree child traversal structure detected."
        )

    if (
        _contains_any(source, ("visited", "visited[", "visited.add", "visited.insert"))
        and _contains_any(source, ("adj", "adjacency", "neighbors", "neighbours"))
    ):
        features.graph_signals.append(
            "Graph adjacency with visited-state tracking detected."
        )
        features.visited_state_signals += 1

    if _contains_any(source, ("neighbor", "neighbour", "adjacency[")):
        features.neighbor_iteration_signals += 1

    if (
        _contains_any(source, ("dist[", "distance[", "distance"))
        and _contains_any(source, ("priority_queue", "priorityqueue", "heapq", "binaryheap"))
        and _contains_any(source, ("dist[v] >", "dist[v] =", "distance[v] >", "distance[v] =", "relax"))
    ):
        features.relaxation_signals += 2
        features.graph_signals.append(
            "Shortest-path relaxation structure detected."
        )

    if _contains_any(source, ("dp[", "memo[", "memoized", "cache[")):
        features.memoization_signals += 1
        features.dp_signals.append(
            "Memoization or DP table detected."
        )

    if features.memoization_signals and _contains_any(
        source,
        ("+ dp[", "- dp[", "* dp[", "max(", "min("),
    ):
        features.dp_recurrence_signals += 2

    if (
        "[i][j]" in source
        or "[j][i]" in source
        or _contains_any(source, ("[row][column]", "[column][row]"))
        or (features.nested_loop_depth >= 2 and _contains_any(source, ("matrix", "grid")))
    ):
        features.array_dimension_signals = 2
        features.matrix_signals.append(
            "Two-dimensional matrix/grid access detected."
        )

    if (
        features.recursion_signals
        and _contains_any(source, ("backtrack", "undo", "remove(", "pop_back", "pop()"))
        and _contains_any(source, ("push(", "append(", "add(", "choose", "for "))
    ):
        features.choice_undo_signals += 2

    if (
        _contains_any(
            source,
            ("sort(", "std::sort", "arrays.sort", "collections.sort"),
        )
        or features.comparison_swap_signals
    ) and _contains_any(
        source,
        ("selected", "select", "current_end", "best", "earliest", "minimum", "maximum", "interval"),
    ):
        features.greedy_selection_signals += 2

    if _contains_any(
        source,
        ("tolower", "toupper", "isalpha", "isdigit", ".lower(", ".upper(", "substring(", "substr(", "reverse("),
    ):
        features.string_signals.append(
            "String transformation/scanning operation detected."
        )

def _extract_algorithm_signals(
    reference_code: str,
    language: str,
    features: ProgramFeatures,
    function_names: set[str],
) -> None:
    """
    Extract algorithm-specific structural evidence.

    This does not determine the algorithm itself.
    It only records structures that the classifier can reason about.
    """
    source = _normalized_source(reference_code)
    normalized_language = (language or "").strip().lower()

    # --------------------------------------------------------
    # Search / midpoint narrowing
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "mid =",
            "mid=",
            "midpoint",
            "(low + high) / 2",
            "(left + right) / 2",
            "low + (high - low) / 2",
        ),
    ):
        features.midpoint_signals += 1

    if _contains_any_text(
        source,
        (
            "low = mid + 1",
            "low=mid+1",
            "left = mid + 1",
            "left=mid+1",
            "high = mid - 1",
            "high=mid-1",
            "right = mid - 1",
            "right=mid-1",
            "lo = mid + 1",
            "hi = mid - 1",
        ),
    ):
        features.boundary_narrowing_signals += 1

    # --------------------------------------------------------
    # Recursion
    # --------------------------------------------------------

    function_names = {
        name.lower()
        for name in function_names
    }

    for name in function_names:
        if _has_recursive_self_call(
            reference_code,
            name,
        ):
            features.recursion_signals += 1
            features.self_call_names.add(name)

    # --------------------------------------------------------
    # Two pointers
    # --------------------------------------------------------

    if (
        _contains_any_text(
            source,
            ("left", "l = 0", "l=0", "start"),
        )
        and _contains_any_text(
            source,
            ("right", "r =", "end"),
        )
        and _contains_any_text(
            source,
            ("left += 1", "l += 1", "right -= 1", "r -= 1"),
        )
    ):
        features.boundary_narrowing_signals += 1

    # --------------------------------------------------------
    # Sliding window
    # --------------------------------------------------------

    if (
        _contains_any_text(
            source,
            (
                "left += 1",
                "left++",
                "l += 1",
                "l++",
                "start += 1",
            ),
        )
        and _contains_any_text(
            source,
            (
                "right += 1",
                "right++",
                "r += 1",
                "r++",
                "end += 1",
            ),
        )
    ):
        features.neighbor_iteration_signals += 1

    # --------------------------------------------------------
    # Prefix sum
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "prefix[i + 1] = prefix[i] +",
            "prefix[i+1] = prefix[i] +",
            "prefix[i + 1]=",
            "prefix[i+1]=",
        ),
    ):
        features.dp_signals.append(
            "Prefix array recurrence detected."
        )

    # --------------------------------------------------------
    # Hashing
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "unordered_map",
            "unordered_set",
            "hashmap",
            "hash_map",
            "dict",
            "setdefault",
            "get(",
        ),
    ):
        features.map_api_calls.append("hash-map access")

    # --------------------------------------------------------
    # Stack
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "stack<",
            "std::stack",
            ".push(",
            ".pop(",
            ".top(",
        ),
    ):
        features.stack_api_calls.append("stack operations")

    # --------------------------------------------------------
    # Queue
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "queue<",
            "std::queue",
            "deque<",
            "collections.deque",
            ".front(",
            ".popleft(",
        ),
    ):
        features.queue_api_calls.append("queue operations")

    # --------------------------------------------------------
    # Graph traversal
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "adj[",
            "adjacency",
            "neighbors",
            "neighbours",
            "visited",
        ),
    ):
        features.graph_signals.append(
            "Graph adjacency/visited structure detected."
        )

    if _contains_any_text(
        source,
        (
            "visited[",
            "visited.add(",
            "visited.insert(",
            "visited =",
        ),
    ):
        features.visited_state_signals += 1

    if _contains_any_text(
        source,
        (
            "for neighbor in",
            "for (auto neighbor",
            "for(auto neighbor",
            "for (int neighbor",
            "for(int neighbor",
        ),
    ):
        features.neighbor_iteration_signals += 1

    # --------------------------------------------------------
    # Dijkstra / relaxation
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "priority_queue",
            "priorityqueue",
            "binaryheap",
            "heapq",
        ),
    ):
        features.heap_api_calls.append("priority queue / heap")

    if _contains_any_text(
        source,
        (
            "dist[v] > dist[u] +",
            "dist[v] = dist[u] +",
            "distance",
            "relax",
        ),
    ):
        features.relaxation_signals += 1
        features.graph_signals.append(
            "Distance relaxation structure detected."
        )

    # --------------------------------------------------------
    # Tree traversal
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "left",
            "right",
            "left->",
            "right->",
            ".left",
            ".right",
        ),
    ) and _contains_any_text(
        source,
        (
            "node",
            "root",
            "tree",
            "nullptr",
            "null",
        ),
    ):
        features.tree_signals.append(
            "Tree child traversal structure detected."
        )

    # --------------------------------------------------------
    # Dynamic programming
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "dp[",
            "memo[",
            "memoized",
            "cache[",
        ),
    ):
        features.dp_signals.append(
            "Memoization or DP table access detected."
        )

    # --------------------------------------------------------
    # Matrix
    # --------------------------------------------------------

    if features.nested_loop_depth >= 2 and _contains_any_text(
        source,
        (
            "matrix",
            "grid",
            "[i][j]",
            "[j][i]",
        ),
    ):
        features.matrix_signals.append(
            "Nested matrix/grid indexing detected."
        )

    # --------------------------------------------------------
    # String processing
    # --------------------------------------------------------

    if _contains_any_text(
        source,
        (
            "tolower",
            "toupper",
            "isalpha",
            "isdigit",
            "substring",
            ".substring(",
            "lower(",
            "upper(",
            "reverse(",
        ),
    ):
        features.string_signals.append(
            "String transformation/scanning operation detected."
        )


# B5.14 - Program feature extraction

def _extract_program_features(
    reference_code: str,
    language: str,
    parse_result: ParseResult,
) -> ProgramFeatures:
    features = ProgramFeatures(
        language=language,
    )

    if not parse_result.root:
        # Parser binaries may be unavailable on restricted Windows hosts. Keep
        # the analysis useful with the same conservative, source-level signals
        # used to supplement the AST path.
        source = _normalized_source(reference_code)
        function_names = set(
            re.findall(
                r"(?:def\s+|[\w:<>~*&]+\s+)([A-Za-z_]\w*)\s*\(",
                reference_code,
            )
        )
        # The broad cross-language pattern above also sees control-flow
        # helpers such as ``for i in range(...)``. They are not declarations
        # and therefore must not be treated as recursive functions.
        function_names.difference_update(
            {
                "range",
                "input",
                "print",
                "len",
                "max",
                "min",
            }
        )
        features.loops = len(
            re.findall(r"\b(?:for|while)\b", source)
        )
        features.nested_loop_depth = (
            2 if features.loops >= 2 else features.loops
        )
        features.comparisons = len(
            re.findall(r"(?:==|!=|<=|>=|<|>)", source)
        )
        features.function_count = len(function_names)
        features.function_calls = len(
            re.findall(r"\b[A-Za-z_]\w*\s*\(", reference_code)
        )

        _extract_semantic_signals(
            reference_code,
            features,
            function_names,
        )
        _extract_algorithm_signals(
            reference_code,
            language,
            features,
            function_names,
        )
        api_signals, api_evidence = _detect_library_signals(
            reference_code,
            language,
        )
        features.library_signals.extend(api_evidence)
        features.sort_api_calls = api_signals.get("sorting", [])
        features.heap_api_calls.extend(api_signals.get("heap", []))
        features.queue_api_calls.extend(api_signals.get("queue", []))
        features.stack_api_calls.extend(api_signals.get("stack", []))
        _detect_specific_array_algorithms(
            reference_code,
            features,
        )
        features.structural_quality = 0.55
        return features

    root = parse_result.root
    source = reference_code.encode(
        "utf-8"
    )

    features.node_counts = (
        _count_node_types(root)
    )

    features.loops = sum(
        features.node_counts.get(
            node_type,
            0,
        )
        for node_type in _LOOP_NODE_TYPES
    )

    features.nested_loop_depth = (
        _loop_depth(root)
    )

    function_names = _extract_function_names(
        root,
        source,
    )

    features.function_count = len(
        function_names
    )

    features.function_calls = sum(
        1
        for node in _walk_tree(root)
        if _node_type(node) in {
            "call",
            "call_expression",
            "function_call_expression",
            "call_expression_statement",
        }
    )

    features.comparisons = sum(
        features.node_counts.get(
            node_type,
            0,
        )
        for node_type in {
            "comparison_operator",
            "==",
            "!=",
            "<",
            ">",
            "<=",
            ">=",
        }
    )

    features.parse_error_nodes = (
        parse_result.error_count
    )

    _extract_semantic_signals(
        reference_code,
        features,
        function_names,
    )

    _extract_algorithm_signals(
        reference_code,
        language,
        features,
        function_names,
    )

    _detect_specific_array_algorithms(
        reference_code,
        features,
    )

    api_signals, api_evidence = (
        _detect_library_signals(
            reference_code,
            language,
        )
    )

    features.library_signals.extend(
        api_evidence
    )

    features.sort_api_calls = (
        api_signals.get(
            "sorting",
            [],
        )
    )

    features.heap_api_calls = (
        api_signals.get(
            "heap",
            [],
        )
    )

    features.queue_api_calls = (
        api_signals.get(
            "queue",
            [],
        )
    )

    features.stack_api_calls = (
        api_signals.get(
            "stack",
            [],
        )
    )

    features.structural_quality = max(
        0.0,
        min(
            1.0,
            1.0
            - (
                parse_result.error_count
                / max(
                    1,
                    len(features.node_counts),
                )
            ),
        ),
    )

    return features


# B5.15 - Structural binary-search detector

def _detect_binary_search(
    features: ProgramFeatures,
) -> tuple[
    bool,
    list[str],
]:
    evidence: list[str] = []

    midpoint = (
        features.midpoint_signals >= 1
    )

    narrowing = (
        features.boundary_narrowing_signals >= 2
    )

    loop_present = (
        features.loops >= 1
        or features.recursion_signals >= 1
    )

    if midpoint:
        evidence.append(
            "Midpoint-based search signal detected."
        )

    if narrowing:
        evidence.append(
            "Repeated search-boundary narrowing detected."
        )

    if loop_present:
        evidence.append(
            "Iterative or recursive search control flow detected."
        )

    matched = (
        midpoint
        and narrowing
        and loop_present
    )

    return matched, evidence


# B5.15a - Specific sorting/search implementation detectors
#
# These detectors deliberately look for the algorithm's control/data-flow
# shape. Function names are never used as primary evidence.

def _detect_specific_array_algorithms(
    source: str,
    features: ProgramFeatures,
) -> None:
    """Record strong implementation-level signals for common algorithms."""
    text = _normalized_source(source)
    compact = re.sub(r"\s+", "", text)

    # Language-independent normalized patterns. These deliberately do not
    # depend on the function's name or on one specific array variable name.
    adjacent_compare_re = bool(re.search(
        r"\[[A-Za-z_]\w*\]>(?:[A-Za-z_]\w*)?\[[A-Za-z_]\w*\+1\]|"
        r"\[[A-Za-z_]\w*\]<(?:[A-Za-z_]\w*)?\[[A-Za-z_]\w*\+1\]",
        compact,
    ))
    adjacent_index_compare_re = bool(re.search(
        r"\[j\][<>]\[j\+1\]", compact
    ))
    adjacent_swap_re = bool(re.search(
        r"\[[A-Za-z_]\w*\],\s*\[[A-Za-z_]\w*\+1\]=", compact
    ))

    # Bubble sort: adjacent comparison + exchange + nested/progressive scan.
    adjacent_compare = _contains_any(
        text,
        (
            "arr[j] > arr[j + 1]", "arr[j] < arr[j + 1]",
            "a[j] > a[j + 1]", "a[j] < a[j + 1]",
            "array[j] > array[j + 1]", "array[j] < array[j + 1]",
            "data[j] > data[j + 1]", "data[j] < data[j + 1]",
        ),
    )
    adjacent_swap = _contains_any(
        text,
        (
            "arr[j], arr[j + 1] = arr[j + 1], arr[j]",
            "a[j], a[j + 1] = a[j + 1], a[j]",
            "array[j], array[j + 1] = array[j + 1], array[j]",
            "swap(arr[j], arr[j + 1])",
            "swap(a[j], a[j + 1])",
            "std::swap(arr[j], arr[j + 1])",
        ),
    )
    progressive_pass = _contains_any(
        text,
        (
            "len(arr) - i - 1", "len(arr)-i-1",
            "n - i - 1", "n-i-1",
            "size - i - 1", "size-i-1",
            "n - i", "n-i",
        ),
    )
    adjacent_compare = adjacent_compare or _contains_any(compact, ("arr[j]>arr[j+1]", "arr[j]<arr[j+1]", "a[j]>a[j+1]", "a[j]<a[j+1]")) or adjacent_index_compare_re or bool(re.search(r"[A-Za-z_]\w*\[j\][<>][A-Za-z_]\w*\[j\+1\]", compact))
    adjacent_swap = adjacent_swap or _contains_any(compact, ("arr[j],arr[j+1]=arr[j+1],arr[j]", "a[j],a[j+1]=a[j+1],a[j]", "swap(arr[j],arr[j+1])")) or adjacent_swap_re or bool(re.search(r"[A-Za-z_]\w*\[j\],[A-Za-z_]\w*\[j\+1\]=[A-Za-z_]\w*\[j\+1\],[A-Za-z_]\w*\[j\]", compact))
    progressive_pass = progressive_pass or _contains_any(compact, ("len(arr)-i-1", "n-i-1", "size-i-1"))
    adjacent_compare = adjacent_compare or bool(re.search(
        r"\b[A-Za-z_]\w*\[\s*[A-Za-z_]\w*\s*\]\s*[<>]=?\s*"
        r"[A-Za-z_]\w*\[\s*[A-Za-z_]\w*\s*\+\s*1\s*\]",
        text,
    ))
    adjacent_swap = adjacent_swap or bool(re.search(
        r"\b([A-Za-z_]\w*)\[\s*([A-Za-z_]\w*)\s*\],\s*\1\[\s*\2\s*\+\s*1\s*\]\s*=\s*"
        r"\1\[\s*\2\s*\+\s*1\s*\],\s*\1\[\s*\2\s*\]",
        text,
    ))
    if adjacent_compare and adjacent_swap:
        features.bubble_sort_signals += 3
    if adjacent_compare and progressive_pass:
        features.bubble_sort_signals += 2
    if adjacent_compare and adjacent_swap and features.nested_loop_depth >= 2:
        features.bubble_sort_signals += 1

    # Selection sort: select min/max over remaining suffix, then one swap.
    selection_scan = _contains_any(
        text,
        (
            "min_index", "minindex", "max_index", "maxindex",
            "min_idx", "max_idx", "minimum_index", "maximum_index",
            "min_pos", "max_pos",
        ),
    )
    selection_compare = _contains_any(
        text,
        (
            "arr[j] < arr[min", "arr[j] > arr[max",
            "a[j] < a[min", "a[j] > a[max",
            "array[j] < array[min", "array[j] > array[max",
            "if arr[j] < arr[min", "if arr[j] > arr[max",
        ),
    )
    if selection_scan and selection_compare and features.loops >= 2:
        features.selection_sort_signals += 4

    # Insertion sort: current key + backwards shift/compare.
    insertion_key = _contains_any(
        text,
        ("key =", "key=", "current =", "current=", "value =", "value="),
    )
    insertion_shift = _contains_any(
        text,
        (
            "arr[j + 1] = arr[j]", "arr[j+1] = arr[j]",
            "a[j + 1] = a[j]", "a[j+1] = a[j]",
            "array[j + 1] = array[j]", "array[j+1] = array[j]",
            "j -= 1", "j-=1", "--j",
        ),
    )
    if insertion_key and insertion_shift and features.loops >= 2:
        features.insertion_sort_signals += 4

    # Merge sort: detect the algorithm from its data-flow, not variable names.
    # Canonical structure:
    #   midpoint -> two complementary slices -> merge loop -> append/remainder.
    midpoint_assignment = bool(re.search(
        r"\b[A-Za-z_]\w*\s*=\s*len\(\s*[A-Za-z_]\w*\s*\)\s*//\s*2\b",
        text,
    )) or bool(re.search(
        r"\b[A-Za-z_]\w*\s*=\s*\(\s*[A-Za-z_]\w*\s*\+\s*[A-Za-z_]\w*\s*\)\s*//\s*2\b",
        text,
    ))

    slice_left = re.findall(
        r"\b([A-Za-z_]\w*)\s*\[\s*:\s*([A-Za-z_]\w*)\s*\]",
        text,
    )
    slice_right = re.findall(
        r"\b([A-Za-z_]\w*)\s*\[\s*([A-Za-z_]\w*)\s*:\s*\]",
        text,
    )
    complementary_slices = any(
        base_left == base_right and midpoint_left == midpoint_right
        for base_left, midpoint_left in slice_left
        for base_right, midpoint_right in slice_right
    )

    merge_loop = bool(re.search(
        r"\bwhile\s+[A-Za-z_]\w*\s*<\s*len\(\s*[A-Za-z_]\w*\s*\)\s*"
        r"and\s+[A-Za-z_]\w*\s*<\s*len\(\s*[A-Za-z_]\w*\s*\)",
        text,
    ))
    merge_compare = bool(re.search(
        r"\b[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]\s*[<>]=?\s*"
        r"[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
        text,
    ))
    merge_append = bool(re.search(
        r"\b[A-Za-z_]\w*\s*\.append\(\s*[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]\s*\)",
        text,
    ))
    merge_progress = bool(re.search(
        r"(?:\b[A-Za-z_]\w*\s*\+=\s*1\b|\b[A-Za-z_]\w*\s*=\s*[A-Za-z_]\w*\s*\+\s*1\b|\+\+)"
        r".*(?:\b[A-Za-z_]\w*\s*\+=\s*1\b|\b[A-Za-z_]\w*\s*=\s*[A-Za-z_]\w*\s*\+\s*1\b|\+\+)",
        text,
        re.DOTALL,
    ))
    merge_phase = merge_loop and merge_compare and merge_append and merge_progress

    if midpoint_assignment and complementary_slices and merge_phase:
        features.merge_sort_signals += 6 if features.recursion_signals else 5

    # Quick sort: detect pivot + genuine partition mechanics + recursive subranges.
    # Function/parameter names such as ``left`` or ``right`` are not evidence.
    pivot_assignment = bool(re.search(
        r"\b([A-Za-z_]\w*)\s*=\s*[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
        text,
    )) or bool(re.search(
        r"\b([A-Za-z_]\w*)\s*=\s*[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*:\s*[A-Za-z_]\w*\s*\]",
        text,
    ))
    explicit_pivot = _contains_any(text, ("pivot =", "pivot="))
    pivot = pivot_assignment or explicit_pivot

    pivot_match = re.search(
        r"\b([A-Za-z_]\w*)\s*=\s*[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
        text,
    )
    pivot_name = pivot_match.group(1) if pivot_match else None

    partition_comparison = False
    if pivot_name:
        partition_comparison = bool(re.search(
            rf"\b[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]\s*[<>]=?\s*{re.escape(pivot_name)}\b",
            text,
        )) or bool(re.search(
            rf"\b{re.escape(pivot_name)}\s*[<>]=?\s*[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
            text,
        ))
    else:
        # Partition helpers may compare two indexed elements while moving
        # inward; require that structure together with an explicit partition
        # helper instead of guessing from variable names.
        partition_comparison = bool(re.search(
            r"\b[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]\s*[<>]=?\s*"
            r"[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
            text,
        )) and _contains_any(text, ("partition(", "partition ("))

    boundary_movement = bool(re.search(
        r"\b[A-Za-z_]\w*\s*(?:\+=\s*1|-=\s*1|\+\+|--|=\s*[A-Za-z_]\w*\s*[+-]\s*1)",
        text,
    ))

    recursive_subrange_call = bool(re.search(
        r"\b[A-Za-z_]\w*\s*\(\s*[A-Za-z_]\w*\s*,\s*[A-Za-z_]\w*\s*(?:-\s*1|\+\s*1)?\s*\)",
        text,
    )) or bool(re.search(
        r"\b[A-Za-z_]\w*\s*\(\s*[A-Za-z_]\w*\s*\[\s*:\s*[A-Za-z_]\w*\s*\]\s*\)",
        text,
    ))

    partition = partition_comparison and boundary_movement
    recursive_subranges = features.recursion_signals >= 1 and (
        recursive_subrange_call or _contains_any(text, ("partition(", "partition ("))
    )

    if pivot and partition and recursive_subranges:
        features.quick_sort_signals += 6
    elif pivot and partition:
        features.quick_sort_signals += 4

    # Heap sort: heapify/sift-down plus extraction/swap.
    heapify = _contains_any(
        text,
        ("heapify", "sift_down", "siftdown", "build_heap", "buildheap"),
    )
    heap_extract = _contains_any(
        text,
        ("heap[0]", "heap[0] =", "arr[0]", "swap(arr[0]", "swap(a[0]"),
    )
    if heapify and heap_extract:
        features.heap_sort_signals += 5

    

    # --------------------------------------------------------
    # GRAPH / BFS STRUCTURAL SIGNALS
    # --------------------------------------------------------
    # Python BFS commonly uses a plain list as a queue:
    #
    #   queue = [start]
    #   while queue:
    #       node = queue.pop(0)
    #       for neighbor in graph[node]:
    #           if neighbor not in visited:
    #               visited.add(neighbor)
    #               queue.append(neighbor)
    #
    # Do not require a queue library/API because list-backed
    # queues are completely valid BFS implementations.

    graph_adjacency = bool(
        re.search(
            r"\b[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
            text,
        )
    )

    neighbor_iteration = bool(
        re.search(
            r"\bfor\s+[A-Za-z_]\w*\s+in\s+"
            r"[A-Za-z_]\w*\s*\[\s*[A-Za-z_]\w*\s*\]",
            text,
        )
    )

    visited_state = bool(
        re.search(
            r"\bvisited\b",
            text,
            re.IGNORECASE,
        )
    ) or (
        bool(
            re.search(
                r"\b(?:seen|discovered|marked)\b",
                text,
                re.IGNORECASE,
            )
        )
    )

    queue_initialization = bool(
        re.search(
            r"\b[A-Za-z_]\w*\s*=\s*\[[^\]]*\]",
            text,
        )
    )

    queue_pop_front = bool(
        re.search(
            r"\b[A-Za-z_]\w*\s*\.\s*pop\s*\(\s*0\s*\)",
            text,
            re.IGNORECASE,
        )
    )

    queue_append = bool(
        re.search(
            r"\b[A-Za-z_]\w*\s*\.\s*append\s*\(",
            text,
            re.IGNORECASE,
        )
    )

    if graph_adjacency:
        features.graph_signals.append(
            "Adjacency-style graph indexing detected."
        )

    if neighbor_iteration:
        features.neighbor_iteration_signals += 2

    if visited_state:
        features.visited_state_signals += 1

    if (
        queue_initialization
        and queue_pop_front
        and queue_append
    ):
        features.queue_api_calls.append(
            "list-backed queue traversal"
        )

    if (
        graph_adjacency
        and neighbor_iteration
        and visited_state
        and queue_pop_front
        and queue_append
    ):
        features.graph_signals.append(
            "Queue-based graph traversal detected."
        )
        features.visited_state_signals += 1



    # --------------------------------------------------------
    # LINEAR SEARCH
    # --------------------------------------------------------
    # Detect the algorithm from traversal + equality comparison.
    # Variable/function names are NOT authoritative.
    #
    # Supported shapes include:
    #
    #   for value in arr:
    #       if value == target:
    #           ...
    #
    #   for item in values:
    #       if item == needle:
    #           ...
    #
    #   for i in range(len(data)):
    #       if data[i] == key:
    #           ...
    #
    #   while ...:
    #       if data[i] == desired:
    #           ...
    # --------------------------------------------------------

    direct_collection_scan = bool(
        re.search(
            r"\bfor\s+[A-Za-z_]\w*\s+in\s+[A-Za-z_]\w*\s*:",
            text,
            re.IGNORECASE,
        )
    )

    indexed_scan = bool(
        re.search(
            r"\bfor\s+[A-Za-z_]\w*\s+in\s+range\s*\(",
            text,
            re.IGNORECASE,
        )
    )

    sequential_scan = (
        features.loops >= 1
        and (
            direct_collection_scan
            or indexed_scan
            or _contains_any(
                text,
                (
                    "for i in range",
                    "for (int i",
                    "while (i",
                    "while i <",
                    "enumerate(",
                ),
            )
        )
    )

    # Generic equality between two values.
    # Do not depend on the literal names target/key/value.
    equality_compare = bool(
        re.search(
            r"\b[A-Za-z_]\w*(?:\[[^\]]+\])?\s*==\s*"
            r"[A-Za-z_]\w*(?:\[[^\]]+\])?",
            text,
        )
    )

    # Search-like early success is strong supporting evidence.
    early_success = bool(
        re.search(
            r"\b(?:return|break)\b",
            text,
        )
    )

    if (
        sequential_scan
        and equality_compare
        and features.midpoint_signals == 0
    ):
        features.linear_search_signals += 2

        if early_success:
            features.linear_search_signals += 1

# B5.16 - Conservative sorting detector

def _detect_sorting(
    features: ProgramFeatures,
) -> tuple[
    bool,
    list[str],
]:
    evidence: list[str] = []

    if features.sort_api_calls:
        evidence.append(
            "Standard-library sorting operation detected."
        )

        return True, evidence

    if features.comparison_swap_signals >= 2:
        evidence.extend(
            [
                "Repeated comparison structure detected.",
                "Element exchange/update pattern detected.",
            ]
        )
        return True, evidence

    return False, evidence

def _detect_graph_patterns(
    features: ProgramFeatures,
) -> list[tuple[str, str, float, list[str]]]:
    candidates = []

    if (
        features.graph_signals
        and features.visited_state_signals >= 1
        and features.neighbor_iteration_signals >= 1
        and features.queue_api_calls
    ):
        candidates.append(
            (
                "graph-traversal",
                "graph-traversal",
                0.94,
                [
                    "Graph adjacency traversal detected.",
                    "Visited-state tracking detected.",
                    "Queue-based traversal detected.",
                ],
            )
        )

    if (
        features.graph_signals
        and features.relaxation_signals >= 1
        and features.heap_api_calls
    ):
        candidates.append(
            (
                "graph-algorithm",
                "graph-algorithm",
                0.96,
                [
                    "Graph structure detected.",
                    "Distance relaxation detected.",
                    "Priority queue / heap used for graph processing.",
                ],
            )
        )

    return candidates


def _detect_specialized_patterns(
    features: ProgramFeatures,
) -> list[tuple[str, str, float, list[str]]]:
    candidates = []

    if features.tree_signals:
        candidates.append(
            (
                "tree-traversal",
                "tree-traversal",
                0.92,
                features.tree_signals,
            )
        )

    if features.matrix_signals:
        candidates.append(
            (
                "matrix-processing",
                "matrix-processing",
                0.90,
                features.matrix_signals,
            )
        )

    if features.string_signals:
        candidates.append(
            (
                "string-processing",
                "string-processing",
                0.84,
                features.string_signals,
            )
        )
    
    if features.choice_undo_signals:
        candidates.append(
            (
                "backtracking",
                "backtracking",
                0.86,
                [
                    "Recursive choice and undo structure detected."
                ],
            )
        )
    
    if features.greedy_selection_signals:
        candidates.append(
            (
                "greedy",
                "greedy",
                0.82,
                [
                    "Ordered selection with locally accepted intervals detected."
                ],
            )
        )
    
    if features.dp_recurrence_signals or features.memoization_signals:
        candidates.append(
            (
                "dynamic-programming",
                "dynamic-programming",
                0.88,
                features.dp_signals,
            )
        )

    if features.map_api_calls:
        candidates.append(
            (
                "hashing",
                "hashing",
                0.82,
                [
                    "Hash-map/set access structure detected."
                ],
            )
        )

    return candidates

# B5.17 - Generic structural family detectors

def _detect_generic_families(
    features: ProgramFeatures,
) -> list[
    tuple[str, str, float, list[str]]
]:
    candidates = []

    if features.recursion_signals:
        candidates.append(
            (
                "recursion",
                "recursion",
                0.78,
                [
                    "Recursive self-call detected."
                ],
            )
        )

    if features.heap_api_calls:
        candidates.append(
            (
                "priority-queue",
                "heap",
                0.72,
                [
                    "Priority queue / heap API detected."
                ],
            )
        )

    if features.queue_api_calls:
        candidates.append(
            (
                "queue-processing",
                "queue",
                0.70,
                [
                    "Queue data structure detected."
                ],
            )
        )

    if features.stack_api_calls:
        candidates.append(
            (
                "stack-processing",
                "stack",
                0.70,
                [
                    "Stack data structure detected."
                ],
            )
        )

    return candidates


# B5.18 - Conservative classifier

def _classify_algorithm(
    features: ProgramFeatures,
) -> AlgorithmClassification:
    """Classify from one consolidated candidate-generation pipeline.

    Exact implementation detectors are kept here; reusable family detectors
    are called exactly once below.  This prevents the same signal from being
    converted into multiple competing candidates with different confidences.
    """

    candidates: list[
        tuple[str, str, str, float, list[str]]
    ] = []

    # --------------------------------------------------------
    # Exact implementation detectors
    # --------------------------------------------------------
    if features.bubble_sort_signals >= 4:
        candidates.append((
            "bubble-sort", "sorting", "specific", 0.98,
            [
                "Adjacent element comparisons detected.",
                "Adjacent element exchange detected.",
                "Progressive bubble-sort pass structure detected.",
            ],
        ))

    if features.merge_sort_signals >= 5:
        candidates.append((
            "merge-sort", "sorting", "specific", 0.99,
            [
                "Array is divided around a midpoint.",
                "Left and right halves are processed recursively.",
                "Sorted halves are merged into a result sequence.",
            ],
        ))

    if features.quick_sort_signals >= 4:
        candidates.append((
            "quick-sort", "sorting", "specific", 0.98,
            [
                "Pivot-based partitioning detected.",
                "Partition boundaries are moved around the pivot.",
            ],
        ))

    if features.insertion_sort_signals >= 4:
        candidates.append((
            "insertion-sort", "sorting", "specific", 0.97,
            [
                "Current key/value is inserted into a sorted prefix.",
                "Elements are shifted while moving backward through the prefix.",
            ],
        ))

    if features.selection_sort_signals >= 4:
        candidates.append((
            "selection-sort", "sorting", "specific", 0.97,
            [
                "Minimum/maximum candidate is selected from the remaining range.",
                "Selected element is exchanged into its final position.",
            ],
        ))

    if features.heap_sort_signals >= 5:
        candidates.append((
            "heap-sort", "sorting", "specific", 0.97,
            [
                "Heap construction/sift-down structure detected.",
                "Repeated root extraction structure detected.",
            ],
        ))

    # --------------------------------------------------------
    # Search / sequence detectors
    # --------------------------------------------------------
    if (
        features.linear_search_signals >= 3
        and features.pointer_pair_signals < 2
        and features.midpoint_signals == 0
    ):
        candidates.append((
            "linear-search", "searching", "specific", 0.97,
            [
                "Sequential scan through the input detected.",
                "Element-to-target equality comparison detected.",
            ],
        ))

    binary_search, binary_evidence = _detect_binary_search(features)
    if binary_search:
        candidates.append((
            "binary-search", "searching", "specific", 0.94, binary_evidence
        ))

    if (
        features.window_state_signals >= 2
        and not (
            features.graph_signals
            and features.visited_state_signals >= 1
            and features.queue_api_calls
        )
    ):
        candidates.append((
            "sliding-window", "sliding-window", "specific", 0.95,
            [
                "Two moving window boundaries detected.",
                "Window expansion and contraction structure detected.",
            ],
        ))

    if features.pointer_pair_signals >= 2:
        candidates.append((
            "two-pointers", "two-pointers", "specific", 0.93,
            [
                "Paired boundary pointers detected.",
                "Pointer movement structure detected.",
            ],
        ))

    # --------------------------------------------------------
    # Reusable graph / specialized detectors
    # --------------------------------------------------------
    for name, family, confidence, evidence in _detect_graph_patterns(features):
        candidates.append((name, family, "specific", confidence, evidence))

    for name, family, confidence, evidence in _detect_specialized_patterns(features):
        candidates.append((name, family, "family", confidence, evidence))

    # Generic sorting is deliberately kept separate from exact sort detectors.
    sorting, sorting_evidence = _detect_sorting(features)
    if sorting and features.greedy_selection_signals < 2:
        candidates.append((
            "sorting", "sorting", "family", 0.90, sorting_evidence
        ))

    # Lowest-specificity family fallbacks are added last.
    for name, family, confidence, evidence in _detect_generic_families(features):
        candidates.append((name, family, "generic", confidence, evidence))

    if not candidates:
        return AlgorithmClassification(
            name="custom",
            family="custom",
            specificity="unknown",
            confidence=0.35,
            evidence=[
                "No sufficiently strong structural algorithm pattern was detected."
            ],
        )

    # --------------------------------------------------------
    # Final arbitration — MUST run after every detector has contributed.
    # --------------------------------------------------------
    is_graph_traversal = (
        bool(features.graph_signals)
        and features.visited_state_signals >= 1
        and bool(features.queue_api_calls)
        and features.neighbor_iteration_signals >= 1
    )

    if is_graph_traversal:
        candidates = [
            candidate
            for candidate in candidates
            if candidate[0] not in {
                "sliding-window",
                "two-pointers",
            }
        ]

    # Library-backed sorting is intentionally generic.
    if features.sort_api_calls:
        allowed_library_sort_candidates = {
            "sorting",
            "binary-search",
        }

        if features.greedy_selection_signals >= 2:
            allowed_library_sort_candidates.add("greedy")

        candidates = [
            candidate
            for candidate in candidates
            if candidate[0] in allowed_library_sort_candidates
        ]

    if not candidates:
        return AlgorithmClassification(
            name="custom",
            family="custom",
            specificity="unknown",
            confidence=0.35,
            evidence=[
                "Structural signals were present but no compatible algorithm candidate remained after arbitration."
            ],
        )

    specificity_rank = {
        "specific": 3,
        "family": 2,
        "generic": 1,
        "unknown": 0,
    }

    candidates.sort(
        key=lambda item: (specificity_rank[item[2]], item[3]),
        reverse=True,
    )

    best = candidates[0]

    return AlgorithmClassification(
        name=best[0],
        family=best[1],
        specificity=best[2],
        confidence=best[3],
        evidence=best[4],
    )


# B5.19 - Conservative complexity estimator

def _estimate_complexity(
    features: ProgramFeatures,
    algorithm: AlgorithmClassification,
) -> ComplexityEstimate:

    if algorithm.name == "sliding-window":
        return ComplexityEstimate(
            time="O(n)",
            space=None,
            confidence=0.82,
            evidence=[
                "Window boundaries advance monotonically."
            ],
        )

    if algorithm.name == "two-pointers":
        return ComplexityEstimate(
            time="O(n)",
            space=None,
            confidence=0.82,
            evidence=[
                "Two pointers move through the input."
            ],
        )

    if algorithm.name == "prefix-sum":
        return ComplexityEstimate(
            time="O(n)",
            space="O(n)",
            confidence=0.88,
            evidence=[
                "Prefix recurrence builds cumulative values."
            ],
        )

    if algorithm.name == "graph-traversal":
        return ComplexityEstimate(
            time="O(V + E)",
            space="O(V)",
            confidence=0.88,
            evidence=[
                "Graph adjacency traversal with visited-state tracking."
            ],
        )

    if algorithm.name == "graph-algorithm":
        return ComplexityEstimate(
            time="O((V + E) log V)",
            space="O(V)",
            confidence=0.80,
            evidence=[
                "Priority-queue graph relaxation detected."
            ],
        )

    if algorithm.name == "matrix-processing":
        return ComplexityEstimate(
            time="O(n²)",
            space=None,
            confidence=0.82,
            evidence=[
                "Two-dimensional matrix traversal detected."
            ],
        )

    if algorithm.name == "dynamic-programming":
        return ComplexityEstimate(
            time=None,
            space=None,
            confidence=0.45,
            evidence=[
                "Dynamic-programming structure detected; "
                "exact recurrence bounds require further analysis."
            ],
        )

    if algorithm.name == "binary-search":
        return ComplexityEstimate(
            time="O(log n)",
            space="O(1)",
            confidence=0.88,
            evidence=[
                "Repeated search-space narrowing detected."
            ],
        )

    if algorithm.name == "graph-traversal":
        return ComplexityEstimate(
            time="O(V + E)",
            space="O(V)",
            confidence=0.84,
            evidence=[
                "Graph traversal with adjacency iteration "
                "and visited-state tracking detected."
            ],
        )

    if algorithm.name == "graph-algorithm":
        return ComplexityEstimate(
            time="O((V + E) log V)",
            space="O(V)",
            confidence=0.78,
            evidence=[
                "Graph relaxation with priority-queue processing detected."
            ],
        )

    if algorithm.name == "matrix-processing":
        return ComplexityEstimate(
            time="O(n²)",
            space=None,
            confidence=0.72,
            evidence=[
                "Nested matrix/grid traversal detected."
            ],
        )

    if algorithm.name == "sorting":
        if features.sort_api_calls:
            return ComplexityEstimate(
                time="O(n log n)",
                space=None,
                confidence=0.62,
                evidence=[
                    "Library sorting operation detected; "
                    "internal implementation is not assumed."
                ],
            )

    if features.nested_loop_depth >= 2:
        return ComplexityEstimate(
            time="O(n²)",
            space=None,
            confidence=0.48,
            evidence=[
                "Nested loop structure detected, "
                "but loop bounds could not be fully resolved."
            ],
        )

    return ComplexityEstimate(
        time=None,
        space=None,
        confidence=0.0,
        evidence=[
            "Insufficient structural evidence for "
            "a reliable complexity estimate."
        ],
    )


# B5.20 - Public algorithm analysis API

def analyze_algorithm(
    reference_code: str,
    language: str,
) -> dict[str, Any]:

    if not reference_code or not reference_code.strip():
        return {
            "algorithm": {
                "name": "custom",
                "family": "custom",
                "specificity": "unknown",
                "confidence": 0.0,
                "evidence": [
                    "Reference code is empty."
                ],
            },
            "complexity": {
                "time": None,
                "space": None,
                "confidence": 0.0,
                "evidence": [],
            },
            "detection": {
                "method": "no-source",
                "parser": None,
                "confidence": 0.0,
            },
        }

    parse_result = _parse_reference_code(
        reference_code,
        language,
    )

    features = _extract_program_features(
        reference_code,
        language,
        parse_result,
    )

    classification = _classify_algorithm(
        features
    )

    complexity = _estimate_complexity(
        features,
        classification,
    )

    parser_confidence = max(
        0.0,
        min(
            1.0,
            features.structural_quality,
        ),
    )

    # Source-structural fallback can still be high-confidence when a
    # specific implementation pattern is unambiguous. Parser availability
    # must not turn a strong Merge/Bubble/Quick/Linear detector into a generic
    # or unreliable result.
    if not parse_result.success:
        if classification.specificity == "specific":
            parser_confidence = max(parser_confidence, 0.82)
        elif classification.specificity == "family":
            parser_confidence = max(parser_confidence, 0.75)

    final_confidence = round(
        min(
            classification.confidence,
            max(
                0.20,
                parser_confidence,
            ),
        ),
        2,
    )

    classification.confidence = (
        final_confidence
    )

    return {
        "algorithm": {
            "name": classification.name,
            "family": classification.family,
            "specificity": classification.specificity,
            "confidence": classification.confidence,
            "evidence": classification.evidence,
        },
        "complexity": {
            "time": complexity.time,
            "space": complexity.space,
            "confidence": complexity.confidence,
            "evidence": complexity.evidence,
        },
        "detection": {
            "method": (
                "tree-sitter-structural"
                if parse_result.success
                else "source-structural-fallback"
            ),
            "parser": parse_result.parser_name,
            "confidence": classification.confidence,
            "parse_success": parse_result.success,
            "parse_error_count": (
                parse_result.error_count
            ),
            "error": parse_result.error,
        },
    }