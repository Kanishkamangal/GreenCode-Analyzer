import pytest

from app.services.algorithm_intelligence import analyze_algorithm


def analyze(code: str, language: str = "cpp"):
    return analyze_algorithm(code, language)


def algorithm_family(result):
    return result["algorithm"]["family"]


def algorithm_name(result):
    return result["algorithm"]["name"]


# ============================================================
# SORTING
# ============================================================


def test_sorting_cpp_library_api():
    code = """
    #include <algorithm>
    #include <vector>

    int main() {
        std::vector<int> values = {4, 2, 7, 1};
        std::sort(values.begin(), values.end());
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "sorting"


def test_sorting_python_builtin():
    code = """
    values = [4, 2, 7, 1]
    values = sorted(values)
    print(values)
    """

    result = analyze(code, "python")

    assert algorithm_family(result) == "sorting"


def test_sorting_renamed_variables():
    code = """
    data = [5, 1, 4, 2, 3]

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[j] < data[i]:
                data[i], data[j] = data[j], data[i]
    """

    result = analyze(code, "python")

    assert algorithm_family(result) == "sorting"


# ============================================================
# SEARCHING
# ============================================================


def test_binary_search_with_nonstandard_variable_names():
    code = """
    int locate(vector<int>& values, int target) {
        int start = 0;
        int finish = values.size() - 1;

        while (start <= finish) {
            int middle = (start + finish) / 2;

            if (values[middle] == target)
                return middle;

            if (values[middle] < target)
                start = middle + 1;
            else
                finish = middle - 1;
        }

        return -1;
    }
    """

    result = analyze(code)

    assert algorithm_name(result) == "binary-search"


# ============================================================
# TWO POINTERS
# ============================================================


def test_two_pointers_with_renamed_variables():
    code = """
    int solve(vector<int>& values, int target) {
        int i = 0;
        int j = values.size() - 1;

        while (i < j) {
            int sum = values[i] + values[j];

            if (sum == target)
                return 1;

            if (sum < target)
                ++i;
            else
                --j;
        }

        return 0;
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "two-pointers"


# ============================================================
# SLIDING WINDOW
# ============================================================


def test_sliding_window_is_not_plain_two_pointers():
    code = """
    int longest(vector<int>& values) {
        int start = 0;
        int best = 0;

        unordered_map<int, int> frequency;

        for (int end = 0; end < values.size(); ++end) {
            frequency[values[end]]++;

            while (frequency[values[end]] > 1) {
                frequency[values[start]]--;
                start++;
            }

            best = max(best, end - start + 1);
        }

        return best;
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "sliding-window"


# ============================================================
# PREFIX SUM
# ============================================================


def test_prefix_sum_structural_pattern():
    code = """
    vector<long long> cumulative(n + 1, 0);

    for (int index = 0; index < n; ++index) {
        cumulative[index + 1] =
            cumulative[index] + values[index];
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "prefix-sum"


# ============================================================
# HASHING
# ============================================================


def test_hashing_frequency_map():
    code = """
    unordered_map<int, int> counts;

    for (int value : values) {
        counts[value]++;
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "hashing"


# ============================================================
# STACK
# ============================================================


def test_stack_operations():
    code = """
    stack<char> items;

    for (char ch : text) {
        if (ch == '(') {
            items.push(ch);
        } else if (!items.empty()) {
            items.pop();
        }
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "stack"


# ============================================================
# QUEUE
# ============================================================


def test_queue_is_not_stack():
    code = """
    queue<int> pending;

    pending.push(0);

    while (!pending.empty()) {
        int current = pending.front();
        pending.pop();

        process(current);
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "queue"


# ============================================================
# RECURSION
# ============================================================


def test_simple_recursion():
    code = """
    int factorial(int value) {
        if (value <= 1)
            return 1;

        return value * factorial(value - 1);
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "recursion"


# ============================================================
# TREE TRAVERSAL
# ============================================================


def test_tree_traversal_is_more_specific_than_recursion():
    code = """
    void inorder(Node* node) {
        if (node == nullptr)
            return;

        inorder(node->left);
        visit(node);
        inorder(node->right);
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "tree-traversal"


# ============================================================
# GRAPH TRAVERSAL
# ============================================================


def test_graph_bfs():
    code = """
    vector<vector<int>> adjacency(n);
    vector<int> visited(n, 0);
    queue<int> pending;

    visited[source] = 1;
    pending.push(source);

    while (!pending.empty()) {
        int node = pending.front();
        pending.pop();

        for (int next : adjacency[node]) {
            if (!visited[next]) {
                visited[next] = 1;
                pending.push(next);
            }
        }
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "graph-traversal"


# ============================================================
# GRAPH ALGORITHM
# ============================================================


def test_dijkstra_is_graph_algorithm():
    code = """
    priority_queue<
        pair<int, int>,
        vector<pair<int, int>>,
        greater<pair<int, int>>
    > pending;

    pending.push({0, source});

    while (!pending.empty()) {
        auto [distance, node] = pending.top();
        pending.pop();

        for (auto edge : adjacency[node]) {
            int next = edge.first;
            int weight = edge.second;

            if (distance + weight < dist[next]) {
                dist[next] = distance + weight;
                pending.push({dist[next], next});
            }
        }
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "graph-algorithm"


# ============================================================
# MATRIX
# ============================================================


def test_nested_loops_matrix_processing():
    code = """
    for (int row = 0; row < n; ++row) {
        for (int column = 0; column < n; ++column) {
            result[row][column] =
                first[row][column] + second[row][column];
        }
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "matrix-processing"


# ============================================================
# DYNAMIC PROGRAMMING
# ============================================================


def test_dynamic_programming_table():
    code = """
    vector<int> dp(n + 1, 0);

    for (int index = 1; index <= n; ++index) {
        dp[index] = max(
            dp[index - 1],
            dp[index - 2] + value[index]
        );
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "dynamic-programming"


# ============================================================
# BACKTRACKING
# ============================================================


def test_backtracking_pattern():
    code = """
    void generate(int position) {
        if (position == limit) {
            output();
            return;
        }

        choose(position);
        generate(position + 1);
        undo(position);

        skip(position);
        generate(position + 1);
        undo(position);
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "backtracking"


# ============================================================
# GREEDY
# ============================================================


def test_greedy_selection():
    code = """
    sort(intervals.begin(), intervals.end(), byEnd);

    int selected = 0;

    for (auto interval : intervals) {
        if (interval.start >= currentEnd) {
            selected++;
            currentEnd = interval.end;
        }
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "greedy"


# ============================================================
# STRING PROCESSING
# ============================================================


def test_string_processing():
    code = """
    string value;
    cin >> value;

    reverse(value.begin(), value.end());

    for (char ch : value) {
        if (isalpha(ch)) {
            output(tolower(ch));
        }
    }
    """

    result = analyze(code)

    assert algorithm_family(result) == "string-processing"


# ============================================================
# ADVERSARIAL CASES
# ============================================================


def test_algorithm_keyword_inside_string_is_ignored():
    code = """
    text = "sort this later"
    print(text)
    """

    result = analyze(code, "python")

    assert algorithm_name(result) == "custom"



def test_algorithm_keyword_inside_comment_is_ignored():
    code = """
    # binary search algorithm
    value = int(input())
    print(value)
    """

    result = analyze(code, "python")

    assert algorithm_name(result) != "binary-search"



def test_mid_variable_alone_is_not_binary_search():
    code = """
    mid = 10
    print(mid)
    """

    result = analyze(code, "python")

    assert algorithm_name(result) != "binary-search"



def test_graph_variable_name_alone_is_not_graph_algorithm():
    code = """
    graph = [1, 2, 3, 4]

    for value in graph:
        print(value)
    """

    result = analyze(code, "python")

    assert algorithm_family(result) not in {
        "graph-traversal",
        "graph-algorithm",
    }



def test_generic_nested_loop_does_not_fake_specific_algorithm():
    code = """
    total = 0

    for i in range(n):
        for j in range(n):
            total += i + j

    print(total)
    """

    result = analyze(code, "python")

    assert algorithm_name(result) == "custom"
