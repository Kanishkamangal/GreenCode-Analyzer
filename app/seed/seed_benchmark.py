from app.database.database import SessionLocal

# Register all models
import app.models

from app.models.benchmark import Benchmark
import re
SPECIAL_FOLDER_NAMES = {
    "0/1 Knapsack": "zero_one_knapsack",
}
def get_folder_name(bench_name: str) -> str:
    if bench_name in SPECIAL_FOLDER_NAMES:
        return SPECIAL_FOLDER_NAMES[bench_name]

    folder_name = bench_name.lower()
    folder_name = re.sub(r"[^a-z0-9]+", "_", folder_name)
    return folder_name.strip("_")
db = SessionLocal()

benchmarks = [

    # ---------------- SORTING ----------------
    {"bench_name": "Bubble Sort", "bench_type": "Predefined", "category": "Sorting"},
    {"bench_name": "Selection Sort", "bench_type": "Predefined", "category": "Sorting"},
    {"bench_name": "Insertion Sort", "bench_type": "Predefined", "category": "Sorting"},
    {"bench_name": "Merge Sort", "bench_type": "Predefined", "category": "Sorting"},
    {"bench_name": "Quick Sort", "bench_type": "Predefined", "category": "Sorting"},
    {"bench_name": "Heap Sort", "bench_type": "Predefined", "category": "Sorting"},
    {"bench_name": "Counting Sort", "bench_type": "Predefined", "category": "Sorting"},
    {"bench_name": "Radix Sort", "bench_type": "Predefined", "category": "Sorting"},

    # ---------------- SEARCHING ----------------
    {"bench_name": "Linear Search", "bench_type": "Predefined", "category": "Searching"},
    {"bench_name": "Binary Search", "bench_type": "Predefined", "category": "Searching"},
    {"bench_name": "Jump Search", "bench_type": "Predefined", "category": "Searching"},
    {"bench_name": "Interpolation Search", "bench_type": "Predefined", "category": "Searching"},

    # ---------------- ARRAYS ----------------
    {"bench_name": "Find Maximum Element", "bench_type": "Predefined", "category": "Arrays"},
    {"bench_name": "Find Minimum Element", "bench_type": "Predefined", "category": "Arrays"},
    {"bench_name": "Array Rotation", "bench_type": "Predefined", "category": "Arrays"},
    {"bench_name": "Prefix Sum", "bench_type": "Predefined", "category": "Arrays"},
    {"bench_name": "Kadane's Algorithm", "bench_type": "Predefined", "category": "Arrays"},
    {"bench_name": "Two Sum", "bench_type": "Predefined", "category": "Arrays"},

    # ---------------- STRINGS ----------------
    {"bench_name": "Reverse String", "bench_type": "Predefined", "category": "Strings"},
    {"bench_name": "Palindrome Check", "bench_type": "Predefined", "category": "Strings"},
    {"bench_name": "Anagram Check", "bench_type": "Predefined", "category": "Strings"},
    {"bench_name": "Substring Search", "bench_type": "Predefined", "category": "Strings"},
    {"bench_name": "Longest Common Prefix", "bench_type": "Predefined", "category": "Strings"},

    # ---------------- MATRIX ----------------
    {"bench_name": "Matrix Multiplication", "bench_type": "Predefined", "category": "Matrix"},
    {"bench_name": "Matrix Transpose", "bench_type": "Predefined", "category": "Matrix"},
    {"bench_name": "Spiral Matrix Traversal", "bench_type": "Predefined", "category": "Matrix"},
    {"bench_name": "Rotate Matrix", "bench_type": "Predefined", "category": "Matrix"},

    # ---------------- MATHEMATICS ----------------
    {"bench_name": "Prime Number Check", "bench_type": "Predefined", "category": "Mathematics"},
    {"bench_name": "Factorial", "bench_type": "Predefined", "category": "Mathematics"},
    {"bench_name": "GCD", "bench_type": "Predefined", "category": "Mathematics"},
    {"bench_name": "LCM", "bench_type": "Predefined", "category": "Mathematics"},
    {"bench_name": "Power Calculation", "bench_type": "Predefined", "category": "Mathematics"},
    {"bench_name": "Sieve of Eratosthenes", "bench_type": "Predefined", "category": "Mathematics"},

    # ---------------- RECURSION ----------------
    {"bench_name": "Fibonacci", "bench_type": "Predefined", "category": "Recursion"},
    {"bench_name": "Tower of Hanoi", "bench_type": "Predefined", "category": "Recursion"},
    {"bench_name": "Generate Permutations", "bench_type": "Predefined", "category": "Recursion"},
    {"bench_name": "Generate Subsets", "bench_type": "Predefined", "category": "Recursion"},

    # ---------------- GRAPH ----------------
    {"bench_name": "BFS Traversal", "bench_type": "Predefined", "category": "Graph"},
    {"bench_name": "DFS Traversal", "bench_type": "Predefined", "category": "Graph"},
    {"bench_name": "Dijkstra Algorithm", "bench_type": "Predefined", "category": "Graph"},
    {"bench_name": "Topological Sort", "bench_type": "Predefined", "category": "Graph"},
    {"bench_name": "Minimum Spanning Tree", "bench_type": "Predefined", "category": "Graph"},
    {"bench_name": "Cycle Detection", "bench_type": "Predefined", "category": "Graph"},

    # ---------------- DYNAMIC PROGRAMMING ----------------
    {"bench_name": "0/1 Knapsack", "bench_type": "Predefined", "category": "Dynamic Programming"},
    {"bench_name": "Coin Change", "bench_type": "Predefined", "category": "Dynamic Programming"},
    {"bench_name": "Longest Common Subsequence", "bench_type": "Predefined", "category": "Dynamic Programming"},
    {"bench_name": "Longest Increasing Subsequence", "bench_type": "Predefined", "category": "Dynamic Programming"},
    {"bench_name": "Matrix Chain Multiplication", "bench_type": "Predefined", "category": "Dynamic Programming"},
    {"bench_name": "Edit Distance", "bench_type": "Predefined", "category": "Dynamic Programming"},

    # ---------------- FILE HANDLING ----------------
    {"bench_name": "File Read", "bench_type": "Predefined", "category": "File Handling"},
    {"bench_name": "File Write", "bench_type": "Predefined", "category": "File Handling"},
    {"bench_name": "Word Count", "bench_type": "Predefined", "category": "File Handling"},

        # ---------------- TREES ----------------
    {"bench_name": "Binary Search Tree", "bench_type": "Predefined", "category": "Trees"},
    {"bench_name": "AVL Tree", "bench_type": "Predefined", "category": "Trees"},
    {"bench_name": "Trie Operations", "bench_type": "Predefined", "category": "Trees"},
    {"bench_name": "Segment Tree", "bench_type": "Predefined", "category": "Trees"},
    {"bench_name": "Fenwick Tree", "bench_type": "Predefined", "category": "Trees"},

        # ---------------- LINKED LIST ----------------
    {"bench_name": "Reverse Linked List", "bench_type": "Predefined", "category": "Linked List"},
    {"bench_name": "Detect Cycle in Linked List", "bench_type": "Predefined", "category": "Linked List"},
    {"bench_name": "Merge Two Sorted Linked Lists", "bench_type": "Predefined", "category": "Linked List"},
    {"bench_name": "Remove Nth Node From End", "bench_type": "Predefined", "category": "Linked List"},

        # ---------------- STACKS & QUEUES ----------------
    {"bench_name": "Balanced Parentheses", "bench_type": "Predefined", "category": "Stacks & Queues"},
    {"bench_name": "Infix to Postfix", "bench_type": "Predefined", "category": "Stacks & Queues"},
    {"bench_name": "Queue Using Two Stacks", "bench_type": "Predefined", "category": "Stacks & Queues"},
    {"bench_name": "Stack Using Queues", "bench_type": "Predefined", "category": "Stacks & Queues"},

        # ---------------- HASHING ----------------
    {"bench_name": "Frequency Counter", "bench_type": "Predefined", "category": "Hashing"},
    {"bench_name": "First Non-Repeating Character", "bench_type": "Predefined", "category": "Hashing"},
    {"bench_name": "Group Anagrams", "bench_type": "Predefined", "category": "Hashing"},
    {"bench_name": "Longest Consecutive Sequence", "bench_type": "Predefined", "category": "Hashing"},

        # ---------------- GREEDY ----------------
    {"bench_name": "Activity Selection", "bench_type": "Predefined", "category": "Greedy"},
    {"bench_name": "Fractional Knapsack", "bench_type": "Predefined", "category": "Greedy"},
    {"bench_name": "Job Sequencing", "bench_type": "Predefined", "category": "Greedy"},
    {"bench_name": "Huffman Coding", "bench_type": "Predefined", "category": "Greedy"},

        # ---------------- BACKTRACKING ----------------
    {"bench_name": "N Queens", "bench_type": "Predefined", "category": "Backtracking"},
    {"bench_name": "Sudoku Solver", "bench_type": "Predefined", "category": "Backtracking"},
    {"bench_name": "Rat in a Maze", "bench_type": "Predefined", "category": "Backtracking"},
    {"bench_name": "Word Search", "bench_type": "Predefined", "category": "Backtracking"},

        # ---------------- BIT MANIPULATION ----------------
    {"bench_name": "Count Set Bits", "bench_type": "Predefined", "category": "Bit Manipulation"},
    {"bench_name": "Power of Two", "bench_type": "Predefined", "category": "Bit Manipulation"},
    {"bench_name": "Single Number", "bench_type": "Predefined", "category": "Bit Manipulation"},
    {"bench_name": "Bitwise XOR Operations", "bench_type": "Predefined", "category": "Bit Manipulation"},

        # ---------------- SLIDING WINDOW ----------------
    {"bench_name": "Maximum Sum Subarray", "bench_type": "Predefined", "category": "Sliding Window"},
    {"bench_name": "Longest Substring Without Repeating Characters", "bench_type": "Predefined", "category": "Sliding Window"},
    {"bench_name": "Minimum Window Substring", "bench_type": "Predefined", "category": "Sliding Window"},
    {"bench_name": "Sliding Window Maximum", "bench_type": "Predefined", "category": "Sliding Window"},

        # ---------------- HEAP / PRIORITY QUEUE ----------------
    {"bench_name": "Kth Largest Element", "bench_type": "Predefined", "category": "Heap"},
    {"bench_name": "Merge K Sorted Arrays", "bench_type": "Predefined", "category": "Heap"},
    {"bench_name": "Top K Frequent Elements", "bench_type": "Predefined", "category": "Heap"},
    {"bench_name": "Median of Data Stream", "bench_type": "Predefined", "category": "Heap"},
]

for bench in benchmarks:

    folder_name = get_folder_name(
        bench["bench_name"]
    )

    existing = db.query(Benchmark).filter_by(
        bench_name=bench["bench_name"]
    ).first()

    if not existing:

        db.add(
            Benchmark(
                **bench,
                folder_name=folder_name
            )
        )

        print(
            f"Inserted: {bench['bench_name']} "
            f"-> {folder_name}"
        )

    else:

        # Also keeps old database rows synchronized
        existing.folder_name = folder_name

        print(
            f"Already exists: {bench['bench_name']} "
            f"-> {folder_name}"
        )
db.commit()
db.close()

print("\n✅ Benchmarks seeded successfully!")