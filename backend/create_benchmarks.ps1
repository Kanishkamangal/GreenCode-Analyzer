$benchmarks = @(
"bubble_sort",
"selection_sort",
"insertion_sort",
"merge_sort",
"quick_sort",
"heap_sort",
"counting_sort",
"radix_sort",
"linear_search",
"binary_search",
"jump_search",
"interpolation_search",
"find_maximum_element",
"find_minimum_element",
"array_rotation",
"prefix_sum",
"kadanes_algorithm",
"two_sum",
"reverse_string",
"palindrome_check",
"anagram_check",
"substring_search",
"longest_common_prefix",
"matrix_multiplication",
"matrix_transpose",
"spiral_matrix_traversal",
"rotate_matrix",
"prime_number_check",
"factorial",
"gcd",
"lcm",
"power_calculation",
"sieve_of_eratosthenes",
"fibonacci",
"tower_of_hanoi",
"generate_permutations",
"generate_subsets",
"bfs_traversal",
"dfs_traversal",
"dijkstra_algorithm",
"topological_sort",
"minimum_spanning_tree",
"cycle_detection",
"zero_one_knapsack",
"coin_change",
"longest_common_subsequence",
"longest_increasing_subsequence",
"matrix_chain_multiplication",
"edit_distance",
"file_read",
"file_write",
"word_count",
"binary_search_tree",
"avl_tree",
"trie_operations",
"segment_tree",
"fenwick_tree",
"reverse_linked_list",
"detect_cycle_in_linked_list",
"merge_two_sorted_linked_lists",
"remove_nth_node_from_end",
"balanced_parentheses",
"infix_to_postfix",
"queue_using_two_stacks",
"stack_using_queues",
"frequency_counter",
"first_non_repeating_character",
"group_anagrams",
"longest_consecutive_sequence",
"activity_selection",
"fractional_knapsack",
"job_sequencing",
"huffman_coding",
"n_queens",
"sudoku_solver",
"rat_in_a_maze",
"word_search",
"count_set_bits",
"power_of_two",
"single_number",
"bitwise_xor_operations",
"maximum_sum_subarray",
"longest_substring_without_repeating_characters",
"minimum_window_substring",
"sliding_window_maximum",
"kth_largest_element",
"merge_k_sorted_arrays",
"top_k_frequent_elements",
"median_of_data_stream"
)

$languages = @(
"c.c",
"cpp.cpp",
"java.java",
"python.py",
"javascript.js",
"csharp.cs",
"go.go",
"rust.rs",
"kotlin.kt",
"php.php"
)

New-Item -ItemType Directory -Force -Path "benchmarks" | Out-Null

foreach($benchmark in $benchmarks)
{
    $folder = "benchmarks\$benchmark"

    New-Item -ItemType Directory -Force -Path $folder | Out-Null

    foreach($lang in $languages)
    {
        New-Item -ItemType File -Force -Path "$folder\$lang" | Out-Null
    }
}

Write-Host ""
Write-Host "Done!"
Write-Host "$($benchmarks.Count) benchmark folders created."
Write-Host "$($benchmarks.Count * $languages.Count) language files created."