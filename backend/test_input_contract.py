from app.services.input_contract_analyzer import detect_input_contract

def run_test(
    test_name,
    code,
    expected_type,
    language="C++",
):
    result = detect_input_contract(
        code,
        language,
    )

    actual_type = result.get("contract_type")

    if actual_type == expected_type:
        print(
            f"[PASS] [{language}] {test_name}"
        )
    else:
        print(
            f"[FAIL] [{language}] {test_name}"
        )
        print(
            f"       Expected : {expected_type}"
        )
        print(
            f"       Actual   : {actual_type}"
        )
        print(
            f"       Full     : {result}"
        )

    return actual_type == expected_type

tests = [

    # ========================================================
    # 1. NO INPUT
    # ========================================================
    (
        "No Input",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            cout << "Hello World";
            return 0;
        }
        ''',
        "no-input",
    ),

    # ========================================================
    # 2. INTEGER SCALAR
    # ========================================================
    (
        "Integer Scalar",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n;
            cin >> n;
        }
        ''',
        "integer-scalar",
    ),

    # ========================================================
    # 3. MULTIPLE INTEGER SCALARS
    # ========================================================
    (
        "Integer Scalars",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int a, b, c;
            cin >> a >> b >> c;
        }
        ''',
        "integer-scalars",
    ),

    # ========================================================
    # 4. FLOAT SCALAR
    # ========================================================
    (
        "Float Scalar",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            double x;
            cin >> x;
        }
        ''',
        "float-scalar",
    ),

    # ========================================================
    # 5. FLOAT SCALARS
    # ========================================================
    (
        "Float Scalars",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            double x, y;
            cin >> x >> y;
        }
        ''',
        "float-scalars",
    ),

    # ========================================================
    # 6. CHARACTER SCALAR
    # ========================================================
    (
        "Character Scalar",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            char ch;
            cin >> ch;
        }
        ''',
        "character-scalar",
    ),

    # ========================================================
    # 7. STRING TOKEN
    # ========================================================
    (
        "String Token",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            string s;
            cin >> s;
        }
        ''',
        "string-token",
    ),

    # ========================================================
    # 8. STRING LINE
    # ========================================================
    (
        "String Line",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            string line;
            getline(cin, line);
        }
        ''',
        "string-line",
    ),

    # ========================================================
    # 9. SCALAR + LINE
    # ========================================================
    (
        "Scalar Plus Line",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            int n;
            string line;

            cin >> n;
            cin.ignore();
            getline(cin, line);
        }
        ''',
        "scalar-plus-line",
    ),

    # ========================================================
    # 10. INTEGER VECTOR ARRAY
    # ========================================================
    (
        "Integer Vector Array",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> a(n);

            for (int i = 0; i < n; i++) {
                cin >> a[i];
            }
        }
        ''',
        "integer-array",
    ),

    # ========================================================
    # 11. FLOAT VECTOR ARRAY
    # ========================================================
    (
        "Float Vector Array",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<double> a(n);

            for (int i = 0; i < n; i++) {
                cin >> a[i];
            }
        }
        ''',
        "float-array",
    ),

    # ========================================================
    # 12. C-STYLE ARRAY
    # ========================================================
    (
        "C Style Array",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            int a[100];

            for (int i = 0; i < n; i++) {
                cin >> a[i];
            }
        }
        ''',
        "integer-array",
    ),

    # ========================================================
    # 13. DYNAMIC ARRAY
    # ========================================================
    (
        "Dynamic Array",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            int* a = new int[n];

            for (int i = 0; i < n; i++) {
                cin >> a[i];
            }

            delete[] a;
        }
        ''',
        "integer-array",
    ),

    # ========================================================
    # 14. STD ARRAY
    # ========================================================
    (
        "STD Array",
        r'''
        #include <iostream>
        #include <array>
        using namespace std;

        int main() {
            array<int, 5> a;

            for (int i = 0; i < 5; i++) {
                cin >> a[i];
            }
        }
        ''',
        "integer-array",
    ),

    # ========================================================
    # 15. ARRAY + TARGET
    # ========================================================
    (
        "Array Plus Target",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> a(n);

            for (int i = 0; i < n; i++) {
                cin >> a[i];
            }

            int target;
            cin >> target;
        }
        ''',
        "array-plus-target",
    ),

    # ========================================================
    # 16. MULTIPLE ARRAYS
    # ========================================================
    (
        "Multiple Arrays",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> a(n);
            vector<int> b(n);

            for (int i = 0; i < n; i++)
                cin >> a[i];

            for (int i = 0; i < n; i++)
                cin >> b[i];
        }
        ''',
        "multiple-arrays",
    ),

    # ========================================================
    # 17. MATRIX
    # ========================================================
    (
        "Matrix",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int r, c;
            cin >> r >> c;

            vector<vector<int>> a(
                r,
                vector<int>(c)
            );

            for (int i = 0; i < r; i++) {
                for (int j = 0; j < c; j++) {
                    cin >> a[i][j];
                }
            }
        }
        ''',
        "matrix",
    ),

    # ========================================================
    # 18. C STYLE 2D MATRIX
    # ========================================================
    (
        "C Style 2D Matrix",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int r, c;
            cin >> r >> c;

            int a[100][100];

            for (int i = 0; i < r; i++) {
                for (int j = 0; j < c; j++) {
                    cin >> a[i][j];
                }
            }
        }
        ''',
        "matrix",
    ),

    # ========================================================
    # 19. MATRIX + TARGET
    # ========================================================
    (
        "Matrix Plus Target",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int r, c;
            cin >> r >> c;

            vector<vector<int>> a(
                r,
                vector<int>(c)
            );

            for (int i = 0; i < r; i++) {
                for (int j = 0; j < c; j++) {
                    cin >> a[i][j];
                }
            }

            int target;
            cin >> target;
        }
        ''',
        "matrix-plus-target",
    ),

    # ========================================================
    # 20. CHARACTER GRID
    # ========================================================
    (
        "Character Grid",
        r'''
        #include <iostream>
        #include <vector>
        #include <string>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            vector<string> grid(n);

            for (int i = 0; i < n; i++) {
                cin >> grid[i];
            }
        }
        ''',
        "character-grid",
    ),

    # ========================================================
    # 21. TREE
    # ========================================================
    (
        "Tree Edge List",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            for (int i = 0; i < n - 1; i++) {
                int u, v;
                cin >> u >> v;
            }
        }
        ''',
        "tree",
    ),

    # ========================================================
    # 22. GRAPH
    # ========================================================
    (
        "Graph Edge List",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            for (int i = 0; i < m; i++) {
                int u, v;
                cin >> u >> v;
            }
        }
        ''',
        "graph",
    ),

    # ========================================================
    # 23. WEIGHTED GRAPH
    # ========================================================
    (
        "Weighted Graph",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            for (int i = 0; i < m; i++) {
                int u, v, w;
                cin >> u >> v >> w;
            }
        }
        ''',
        "weighted-graph",
    ),

    # ========================================================
    # 24. GRAPH + SOURCE
    # ========================================================
    (
        "Graph With Source",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            for (int i = 0; i < m; i++) {
                int u, v;
                cin >> u >> v;
            }

            int source;
            cin >> source;
        }
        ''',
        "graph-with-source",
    ),

    # ========================================================
    # 25. WEIGHTED GRAPH + SOURCE
    # ========================================================
    (
        "Weighted Graph With Source",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            for (int i = 0; i < m; i++) {
                int u, v, w;
                cin >> u >> v >> w;
            }

            int source;
            cin >> source;
        }
        ''',
        "weighted-graph-with-source",
    ),

    # ========================================================
    # 26. TEST CASES
    # ========================================================
    (
        "Test Cases",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int t;
            cin >> t;

            while (t--) {
                int x;
                cin >> x;
            }
        }
        ''',
        "test-cases",
    ),

    # ========================================================
    # 27. TEST CASES + ARRAY
    # ========================================================
    (
        "Test Cases Array",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int t;
            cin >> t;

            while (t--) {
                int n;
                cin >> n;

                vector<int> a(n);

                for (int i = 0; i < n; i++) {
                    cin >> a[i];
                }
            }
        }
        ''',
        "test-cases-array",
    ),

    # ========================================================
    # 28. TEST CASES + MATRIX
    # ========================================================
    (
        "Test Cases Matrix",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int t;
            cin >> t;

            while (t--) {
                int r, c;
                cin >> r >> c;

                vector<vector<int>> a(
                    r,
                    vector<int>(c)
                );

                for (int i = 0; i < r; i++) {
                    for (int j = 0; j < c; j++) {
                        cin >> a[i][j];
                    }
                }
            }
        }
        ''',
        "test-cases-matrix",
    ),

    # ========================================================
    # 29. EOF SINGLE VALUE
    # ========================================================
    (
        "EOF Stream",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int x;

            while (cin >> x) {
                cout << x;
            }
        }
        ''',
        "eof-stream",
    ),

    # ========================================================
    # 30. EOF MULTIPLE VALUES
    # ========================================================
    (
        "EOF Records",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int a, b;

            while (cin >> a >> b) {
                cout << a + b;
            }
        }
        ''',
        "eof-records",
    ),

    # ========================================================
    # 31. GETLINE UNTIL EOF
    # ========================================================
    (
        "Lines Until EOF",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            string line;

            while (getline(cin, line)) {
                cout << line;
            }
        }
        ''',
        "eof-lines",
    ),

    # ========================================================
    # 32. SENTINEL
    # ========================================================
    (
        "Sentinel Stream",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int x;

            while (cin >> x && x != -1) {
                cout << x;
            }
        }
        ''',
        "sentinel-stream",
    ),

    # ========================================================
    # 33. MULTI FIELD SENTINEL
    # ========================================================
    (
        "Multi Field Sentinel",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int a, b;

            while (
                cin >> a >> b &&
                !(a == -1 && b == -1)
            ) {
                cout << a + b;
            }
        }
        ''',
        "sentinel-records",
    ),

    # ========================================================
    # 34. SCANF INTEGER
    # ========================================================
    (
        "Scanf Integer",
        r'''
        #include <cstdio>

        int main() {
            int n;
            scanf("%d", &n);
        }
        ''',
        "integer-scalar",
    ),

    # ========================================================
    # 35. SCANF MIXED
    # ========================================================
    (
        "Scanf Mixed",
        r'''
        #include <cstdio>

        int main() {
            int n;
            double x;

            scanf("%d %lf", &n, &x);
        }
        ''',
        "mixed-scalars",
    ),

    # ========================================================
    # 36. SIZE + STRING
    # ========================================================
    (
        "Size Plus String",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            int n;
            string s;

            cin >> n >> s;
        }
        ''',
        "size-plus-string",
    ),

    # ========================================================
    # 37. SIZE + TWO STRINGS
    # ========================================================
    (
        "Size Plus Two Strings",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            int n;
            string a, b;

            cin >> n >> a >> b;
        }
        ''',
        "size-plus-two-strings",
    ),

    # ========================================================
    # 38. JAGGED MATRIX
    # ========================================================
    (
        "Jagged Matrix",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<vector<int>> a(n);

            for (int i = 0; i < n; i++) {
                int m;
                cin >> m;

                a[i].resize(m);

                for (int j = 0; j < m; j++) {
                    cin >> a[i][j];
                }
            }
        }
        ''',
        "jagged-matrix",
    ),

    # ========================================================
    # 39. ADJACENCY MATRIX GRAPH
    # ========================================================
    (
        "Adjacency Matrix Graph",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<vector<int>> adj(
                n,
                vector<int>(n)
            );

            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    cin >> adj[i][j];
                }
            }

            vector<int> visited(n, 0);
        }
        ''',
        "adjacency-matrix",
    ),

    # ========================================================
    # 40. BINARY TREE LEVEL ORDER
    # ========================================================
    (
        "Binary Tree Level Order",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        struct TreeNode {
            int value;
            TreeNode* left;
            TreeNode* right;
        };

        int main() {
            int n;
            cin >> n;

            vector<int> values(n);

            for (int i = 0; i < n; i++) {
                cin >> values[i];
            }

            TreeNode* root = nullptr;
        }
        ''',
        "binary-tree-level-order",
    ),

    # ========================================================
    # 41. PARENT ARRAY TREE
    # ========================================================
    (
        "Parent Array Tree",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> parent(n);

            for (int i = 0; i < n; i++) {
                cin >> parent[i];
            }

            int root = -1;
        }
        ''',
        "parent-array-tree",
    ),

    # ========================================================
    # 42. RANGE QUERIES
    # ========================================================
    (
        "Array Range Queries",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> a(n);

            for (int i = 0; i < n; i++) {
                cin >> a[i];
            }

            int q;
            cin >> q;

            while (q--) {
                int l, r;
                cin >> l >> r;
            }
        }
        ''',
        "array-with-range-queries",
    ),

    # ========================================================
    # 43. GENERIC QUERY STREAM
    # ========================================================
    (
        "Array Query Stream",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> a(n);

            for (int i = 0; i < n; i++) {
                cin >> a[i];
            }

            int q;
            cin >> q;

            for (int i = 0; i < q; i++) {
                int index;
                cin >> index;
            }
        }
        ''',
        "array-with-queries",
    ),

    # ========================================================
    # 44. COMMAND STREAM
    # ========================================================
    (
        "Command Stream",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            int q;
            cin >> q;

            while (q--) {
                string command;
                cin >> command;

                if (command == "push") {
                    int x;
                    cin >> x;
                }
            }
        }
        ''',
        "command-stream",
    ),

    # ========================================================
    # 45. VECTOR OF PAIRS
    # ========================================================
    (
        "Vector Pair Records",
        r'''
        #include <iostream>
        #include <vector>
        #include <utility>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<pair<int, int>> edges;

            for (int i = 0; i < n; i++) {
                int u, v;
                cin >> u >> v;
                edges.push_back({u, v});
            }
        }
        ''',
        "pair-records",
    ),

    # ========================================================
    # 46. VECTOR OF TUPLES
    # ========================================================
    (
        "Vector Tuple Records",
        r'''
        #include <iostream>
        #include <vector>
        #include <tuple>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<tuple<int, int, int>> records;

            for (int i = 0; i < n; i++) {
                int a, b, c;
                cin >> a >> b >> c;
                records.push_back({a, b, c});
            }
        }
        ''',
        "tuple-records",
    ),

    # ========================================================
    # 47. MAP INPUT
    # ========================================================
    (
        "Map Key Value",
        r'''
        #include <iostream>
        #include <map>
        #include <string>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            map<string, int> mp;

            for (int i = 0; i < n; i++) {
                string key;
                int value;

                cin >> key >> value;
                mp[key] = value;
            }
        }
        ''',
        "key-value-records",
    ),

    # ========================================================
    # 48. UNORDERED MAP INPUT
    # ========================================================
    (
        "Unordered Map Key Value",
        r'''
        #include <iostream>
        #include <unordered_map>
        #include <string>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            unordered_map<string, int> mp;

            for (int i = 0; i < n; i++) {
                string key;
                int value;

                cin >> key >> value;
                mp[key] = value;
            }
        }
        ''',
        "key-value-records",
    ),

    # ========================================================
    # 49. TRIPLE RECORDS
    # ========================================================
    (
        "Triple Records",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            for (int i = 0; i < n; i++) {
                int a, b, c;
                cin >> a >> b >> c;
            }
        }
        ''',
        "triples",
    ),

    # ========================================================
    # 50. PAIR RECORDS
    # ========================================================
    (
        "Pair Records",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            for (int i = 0; i < n; i++) {
                int a, b;
                cin >> a >> b;
            }
        }
        ''',
        "pair-records",
    ),

    # ========================================================
    # 51. QUEUE INPUT
    # ========================================================
    (
        "Queue Input",
        r'''
        #include <iostream>
        #include <queue>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            queue<int> q;

            for (int i = 0; i < n; i++) {
                int x;
                cin >> x;
                q.push(x);
            }
        }
        ''',
        "integer-collection",
    ),

    # ========================================================
    # 52. STACK INPUT
    # ========================================================
    (
        "Stack Input",
        r'''
        #include <iostream>
        #include <stack>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            stack<int> st;

            for (int i = 0; i < n; i++) {
                int x;
                cin >> x;
                st.push(x);
            }
        }
        ''',
        "integer-collection",
    ),

    # ========================================================
    # 53. PRIORITY QUEUE INPUT
    # ========================================================
    (
        "Priority Queue Input",
        r'''
        #include <iostream>
        #include <queue>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            priority_queue<int> pq;

            for (int i = 0; i < n; i++) {
                int x;
                cin >> x;
                pq.push(x);
            }
        }
        ''',
        "integer-collection",
    ),

    # ========================================================
    # 54. DEQUE INPUT
    # ========================================================
    (
        "Deque Input",
        r'''
        #include <iostream>
        #include <deque>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            deque<int> d;

            for (int i = 0; i < n; i++) {
                int x;
                cin >> x;
                d.push_back(x);
            }
        }
        ''',
        "integer-collection",
    ),

    # ========================================================
    # 55. SET INPUT
    # ========================================================
    (
        "Set Input",
        r'''
        #include <iostream>
        #include <set>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            set<int> values;

            for (int i = 0; i < n; i++) {
                int x;
                cin >> x;
                values.insert(x);
            }
        }
        ''',
        "integer-collection",
    ),

    # ========================================================
    # 56. STRUCT RECORD INPUT
    # ========================================================
    (
        "Struct Record Input",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        struct Student {
            int id;
            string name;
            double score;
        };

        int main() {
            int n;
            cin >> n;

            Student student;

            for (int i = 0; i < n; i++) {
                cin
                    >> student.id
                    >> student.name
                    >> student.score;
            }
        }
        ''',
        "structured-records",
    ),

    # ========================================================
    # 57. MULTIPLE GETLINE STRINGS
    # ========================================================
    (
        "String Array Getline",
        r'''
        #include <iostream>
        #include <vector>
        #include <string>
        using namespace std;

        int main() {
            int n;
            cin >> n;
            cin.ignore();

            vector<string> lines(n);

            for (int i = 0; i < n; i++) {
                getline(cin, lines[i]);
            }
        }
        ''',
        "string-array",
    ),

    # ========================================================
    # 58. CSV / DELIMITED LINE
    # ========================================================
    (
        "Delimited CSV Line",
        r'''
        #include <iostream>
        #include <sstream>
        #include <string>
        using namespace std;

        int main() {
            string line;
            getline(cin, line);

            stringstream ss(line);

            string token;

            while (
                getline(ss, token, ',')
            ) {
                cout << token;
            }
        }
        ''',
        "delimited-lines",
    ),
        # ========================================================
    # 59. NORMAL MATRIX MUST NOT BECOME ADJACENCY MATRIX
    # ========================================================
    (
        "Collision Matrix Not Adjacency",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int r, c;
            cin >> r >> c;

            vector<vector<int>> matrix(
                r,
                vector<int>(c)
            );

            for (int i = 0; i < r; i++) {
                for (int j = 0; j < c; j++) {
                    cin >> matrix[i][j];
                }
            }

            int visitedCount = 0;
            cout << visitedCount;
        }
        ''',
        "matrix",
    ),

    # ========================================================
    # 60. GRAPH MUST NOT BECOME TREE
    # ========================================================
    (
        "Collision Graph Not Tree",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            for (int i = 0; i < m; i++) {
                int u, v;
                cin >> u >> v;
            }
        }
        ''',
        "graph",
    ),

    # ========================================================
    # 61. TREE MUST NOT BECOME GRAPH
    # ========================================================
    (
        "Collision Tree Not Graph",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            for (int i = 0; i < n - 1; i++) {
                int u, v;
                cin >> u >> v;
            }
        }
        ''',
        "tree",
    ),

    # ========================================================
    # 62. WEIGHTED GRAPH MUST NOT BECOME TRIPLES
    # ========================================================
    (
        "Collision Weighted Graph Not Triples",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            for (int i = 0; i < m; i++) {
                int u, v, w;
                cin >> u >> v >> w;
            }
        }
        ''',
        "weighted-graph",
    ),

    # ========================================================
    # 63. GRAPH + SOURCE MUST NOT BECOME NORMAL GRAPH
    # ========================================================
    (
        "Collision Graph Source Priority",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            for (int i = 0; i < m; i++) {
                int u, v;
                cin >> u >> v;
            }

            int source;
            cin >> source;
        }
        ''',
        "graph-with-source",
    ),

    # ========================================================
    # 64. WEIGHTED GRAPH + SOURCE PRIORITY
    # ========================================================
    (
        "Collision Weighted Graph Source Priority",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n, m;
            cin >> n >> m;

            for (int i = 0; i < m; i++) {
                int u, v, weight;
                cin >> u >> v >> weight;
            }

            int source;
            cin >> source;
        }
        ''',
        "weighted-graph-with-source",
    ),

    # ========================================================
    # 65. ARRAY + TARGET MUST NOT BECOME INTEGER ARRAY
    # ========================================================
    (
        "Collision Array Target Priority",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> arr(n);

            for (int i = 0; i < n; i++) {
                cin >> arr[i];
            }

            int target;
            cin >> target;
        }
        ''',
        "array-plus-target",
    ),

    # ========================================================
    # 66. MATRIX + TARGET MUST NOT BECOME MATRIX
    # ========================================================
    (
        "Collision Matrix Target Priority",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int rows, cols;
            cin >> rows >> cols;

            vector<vector<int>> matrix(
                rows,
                vector<int>(cols)
            );

            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    cin >> matrix[i][j];
                }
            }

            int value;
            cin >> value;
        }
        ''',
        "matrix-plus-target",
    ),

    # ========================================================
    # 67. RANGE QUERY MUST NOT BECOME TEST CASES
    # ========================================================
    (
        "Collision Range Query Not Test Cases",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> a(n);

            for (int i = 0; i < n; i++) {
                cin >> a[i];
            }

            int q;
            cin >> q;

            while (q--) {
                int left, right;
                cin >> left >> right;
            }
        }
        ''',
        "array-with-range-queries",
    ),

    # ========================================================
    # 68. MAP MUST NOT BECOME COMMAND STREAM
    # ========================================================
    (
        "Collision Map Not Command",
        r'''
        #include <iostream>
        #include <map>
        #include <string>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            map<string, int> data;

            for (int i = 0; i < n; i++) {
                string operation;
                int value;

                cin >> operation >> value;
                data[operation] = value;
            }
        }
        ''',
        "key-value-records",
    ),

    # ========================================================
    # 69. REAL COMMAND STREAM MUST STAY COMMAND STREAM
    # ========================================================
    (
        "Collision Real Command Stream",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            int q;
            cin >> q;

            while (q--) {
                string command;
                cin >> command;

                if (command == "ADD") {
                    int x;
                    cin >> x;
                }
                else if (command == "REMOVE") {
                    int x;
                    cin >> x;
                }
            }
        }
        ''',
        "command-stream",
    ),

    # ========================================================
    # 70. TRIPLES MUST NOT BECOME PAIRS
    # ========================================================
    (
        "Collision Triples Not Pairs",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            for (int i = 0; i < n; i++) {
                int a, b, c;
                cin >> a >> b >> c;
            }
        }
        ''',
        "triples",
    ),

    # ========================================================
    # 71. SIZE + TWO STRINGS MUST NOT BECOME SIZE + STRING
    # ========================================================
    (
        "Collision Two Strings Priority",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            int n;
            string first, second;

            cin >> n >> first >> second;
        }
        ''',
        "size-plus-two-strings",
    ),

    # ========================================================
    # 72. SIZE + STRING MUST NOT BECOME MIXED SCALARS
    # ========================================================
    (
        "Collision Size String Not Mixed",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            int length;
            string text;

            cin >> length;
            cin >> text;
        }
        ''',
        "size-plus-string",
    ),

    # ========================================================
    # 73. DECLARED VECTOR BUT NOT READ
    # ========================================================
    (
        "False Positive Unread Vector",
        r'''
        #include <iostream>
        #include <vector>
        using namespace std;

        int main() {
            int n;
            cin >> n;

            vector<int> arr(n);

            for (int i = 0; i < n; i++) {
                arr[i] = i;
            }
        }
        ''',
        "integer-scalar",
    ),

    # ========================================================
    # 74. CIN ONLY INSIDE COMMENT
    # ========================================================
    (
        "False Positive Cin In Comment",
        r'''
        #include <iostream>
        using namespace std;

        int main() {
            // int n;
            // cin >> n;

            cout << "No input";
        }
        ''',
        "no-input",
    ),

    # ========================================================
    # 75. STRING CONTAINING CIN TEXT
    # ========================================================
    (
        "False Positive Cin Inside String",
        r'''
        #include <iostream>
        #include <string>
        using namespace std;

        int main() {
            string example = "cin >> n";
            cout << example;
        }
        ''',
        "no-input",
    ),

        # ============================================================
    # FINAL C++ REGRESSION / EDGE-CASE BATCH
    # Tests 76-105
    # ============================================================

    (
        "Boolean Scalar",
        r'''
#include <iostream>
using namespace std;

int main() {
    bool flag;
    cin >> flag;
}
''',
        "boolean-scalar",
    ),

    (
        "Boolean Vector Array",
        r'''
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<bool> flags(n);

    for (int i = 0; i < n; i++) {
        cin >> flags[i];
    }
}
''',
        "boolean-array",
    ),

    (
        "Character Vector Array",
        r'''
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<char> a(n);

    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
}
''',
        "character-array",
    ),

    (
        "String Vector Array",
        r'''
#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<string> words(n);

    for (int i = 0; i < n; i++) {
        cin >> words[i];
    }
}
''',
        "string-array",
    ),

    (
        "Multiple String Tokens",
        r'''
#include <iostream>
#include <string>
using namespace std;

int main() {
    string first, second;
    cin >> first >> second;
}
''',
        "string-tokens",
    ),

    (
        "Long Long Scalar",
        r'''
#include <iostream>
using namespace std;

int main() {
    long long n;
    cin >> n;
}
''',
        "integer-scalar",
    ),

    (
        "Unsigned Integer Scalar",
        r'''
#include <iostream>
using namespace std;

int main() {
    unsigned int n;
    cin >> n;
}
''',
        "integer-scalar",
    ),

    (
        "STD Cin Scalar",
        r'''
#include <iostream>

int main() {
    int n;
    std::cin >> n;
}
''',
        "integer-scalar",
    ),

    (
        "STD Cin Whitespace Variant",
        r'''
#include <iostream>

int main() {
    int n;

    std::cin
        >> n;
}
''',
        "integer-scalar",
    ),

    (
        "Real Cin With Fake Cin String",
        r'''
#include <iostream>
#include <string>
using namespace std;

int main() {
    string example = "cin >> fake";

    int n;
    cin >> n;

    cout << example;
}
''',
        "integer-scalar",
    ),

    (
        "False Positive Scanf Inside String",
        r'''
#include <iostream>
#include <string>
using namespace std;

int main() {
    string example = "scanf(\"%d\", &n)";
    cout << example;
}
''',
        "no-input",
    ),

    (
        "False Positive Getline Inside String",
        r'''
#include <iostream>
#include <string>
using namespace std;

int main() {
    string example = "getline(cin, line)";
    cout << example;
}
''',
        "no-input",
    ),

    (
        "False Positive Input In Block Comment",
        r'''
#include <iostream>
using namespace std;

int main() {
    /*
        int n;
        cin >> n;

        double x;
        scanf("%lf", &x);
    */

    cout << "Hello";
}
''',
        "no-input",
    ),

    (
        "False Positive Cin Inside Raw String",
        r'''
#include <iostream>
#include <string>
using namespace std;

int main() {
    string example = R"(cin >> n)";
    cout << example;
}
''',
        "no-input",
    ),

    (
        "Unread C Style Array",
        r'''
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    int a[100];

    for (int i = 0; i < n; i++) {
        a[i] = i;
    }
}
''',
        "integer-scalar",
    ),

    (
        "Unread Dynamic Array",
        r'''
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    int* a = new int[n];

    for (int i = 0; i < n; i++) {
        a[i] = i;
    }

    delete[] a;
}
''',
        "integer-scalar",
    ),

    (
        "Unread STD Array",
        r'''
#include <iostream>
#include <array>
using namespace std;

int main() {
    int n;
    cin >> n;

    array<int, 10> a{};

    for (int i = 0; i < 10; i++) {
        a[i] = i;
    }
}
''',
        "integer-scalar",
    ),

    (
        "Unread Queue",
        r'''
#include <iostream>
#include <queue>
using namespace std;

int main() {
    int n;
    cin >> n;

    queue<int> q;

    for (int i = 0; i < n; i++) {
        q.push(i);
    }
}
''',
        "integer-scalar",
    ),

    (
        "Unread Set",
        r'''
#include <iostream>
#include <set>
using namespace std;

int main() {
    int n;
    cin >> n;

    set<int> values;

    for (int i = 0; i < n; i++) {
        values.insert(i);
    }
}
''',
        "integer-scalar",
    ),

    (
        "False Positive Unread Matrix",
        r'''
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int r, c;
    cin >> r >> c;

    vector<vector<int>> matrix(
        r,
        vector<int>(c)
    );

    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            matrix[i][j] = i + j;
        }
    }
}
''',
        "integer-scalars",
    ),

    (
        "False Positive Unread Character Grid",
        r'''
#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;

    vector<string> grid(n, string(m, '.'));

    cout << grid[0];
}
''',
        "integer-scalars",
    ),

    (
        "False Positive Test Cases Unread Array",
        r'''
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<int> a(n);

        for (int i = 0; i < n; i++) {
            a[i] = i;
        }
    }
}
''',
        "test-cases",
    ),

    (
        "False Positive Test Cases Unread Matrix",
        r'''
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int t;
    cin >> t;

    while (t--) {
        int r, c;
        cin >> r >> c;

        vector<vector<int>> matrix(
            r,
            vector<int>(c)
        );

        for (int i = 0; i < r; i++) {
            for (int j = 0; j < c; j++) {
                matrix[i][j] = i + j;
            }
        }
    }
}
''',
        "test-cases",
    ),

    (
        "Range Based Vector Input",
        r'''
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> a(n);

    for (int &x : a) {
        cin >> x;
    }
}
''',
        "integer-array",
    ),

    (
        "False Positive Multiple Unread Vectors",
        r'''
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> a(n);
    vector<int> b(n);

    for (int i = 0; i < n; i++) {
        a[i] = i;
        b[i] = n - i;
    }
}
''',
        "integer-scalar",
    ),

    (
        "Only First Of Two Vectors Is Input",
        r'''
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> a(n);
    vector<int> b(n);

    for (int i = 0; i < n; i++) {
        cin >> a[i];
        b[i] = i;
    }
}
''',
        "integer-array",
    ),

    (
        "Cin Get Character Stream",
        r'''
#include <iostream>
using namespace std;

int main() {
    char ch;
    cin.get(ch);
}
''',
        "character-stream",
    ),

    (
        "Getchar Character Stream",
        r'''
#include <cstdio>

int main() {
    char ch;
    ch = getchar();
}
''',
        "character-stream",
    ),

    (
        "Unknown Cin Structure Fallback",
        r'''
#include <iostream>
using namespace std;

struct CustomValue {
    int x;
};

istream& operator>>(istream& in, CustomValue& value);

int main() {
    CustomValue value;
    cin >> value;
}
''',
        "stdin-present",
    ),

    (
        "Map Declaration Does Not Mean Key Value Input",
        r'''
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;

    map<string, int> unused;

    for (int i = 0; i < n; i++) {
        string name;
        int age;

        cin >> name >> age;

        cout << name << age;
    }
}
''',
        "pair-records",
    ),

]


c_tests = [

    # ========================================================
    # C-1. INTEGER SCALAR
    # ========================================================
    (
        "C Integer Scalar",
        r'''
#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    return 0;
}
''',
        "integer-scalar",
    ),

    # ========================================================
    # C-2. FLOAT SCALAR
    # ========================================================
    (
        "C Float Scalar",
        r'''
#include <stdio.h>

int main() {
    double x;
    scanf("%lf", &x);

    return 0;
}
''',
        "float-scalar",
    ),

    # ========================================================
    # C-3. CHARACTER SCALAR
    # ========================================================
    (
        "C Character Scalar",
        r'''
#include <stdio.h>

int main() {
    char ch;
    scanf(" %c", &ch);

    return 0;
}
''',
        "character-scalar",
    ),

    # ========================================================
    # C-4. STRING TOKEN
    # ========================================================
    (
        "C String Token",
        r'''
#include <stdio.h>

int main() {
    char name[100];
    scanf("%99s", name);

    return 0;
}
''',
        "string-token",
    ),

    # ========================================================
    # C-5. INTEGER SCALARS
    # ========================================================
    (
        "C Integer Scalars",
        r'''
#include <stdio.h>

int main() {
    int a, b, c;

    scanf("%d %d %d", &a, &b, &c);

    return 0;
}
''',
        "integer-scalars",
    ),

    # ========================================================
    # C-6. FLOAT SCALARS
    # ========================================================
    (
        "C Float Scalars",
        r'''
#include <stdio.h>

int main() {
    double a, b;

    scanf("%lf %lf", &a, &b);

    return 0;
}
''',
        "float-scalars",
    ),

    # ========================================================
    # C-7. MIXED SCALARS
    # ========================================================
    (
        "C Mixed Scalars",
        r'''
#include <stdio.h>

int main() {
    int n;
    double x;
    char ch;

    scanf("%d %lf %c", &n, &x, &ch);

    return 0;
}
''',
        "mixed-scalars",
    ),

    # ========================================================
    # C-8. NO INPUT
    # ========================================================
    (
        "C No Input",
        r'''
#include <stdio.h>

int main() {
    printf("Hello");
    return 0;
}
''',
        "no-input",
    ),

    # ========================================================
    # C-9. SCANF INSIDE COMMENT
    # ========================================================
    (
        "C Scanf In Comment",
        r'''
#include <stdio.h>

int main() {
    /*
        int n;
        scanf("%d", &n);
    */

    printf("Hello");
    return 0;
}
''',
        "no-input",
    ),

    # ========================================================
    # C-10. ARRAY DECLARED BUT NOT READ
    # ========================================================
    (
        "C Unread Array",
        r'''
#include <stdio.h>

int main() {
    int n;
    int a[100];

    scanf("%d", &n);

    for (int i = 0; i < 100; i++) {
        a[i] = i;
    }

    return 0;
}
''',
        "integer-scalar",
    ),

    

        (
        "C Fixed Integer Array",
        r'''
#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    int a[100];

    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }

    return 0;
}
''',
        "integer-array",
    ),

        (
        "C Fixed Float Array",
        r'''
#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    double a[100];

    for (int i = 0; i < n; i++) {
        scanf("%lf", &a[i]);
    }

    return 0;
}
''',
        "float-array",
    ),

        (
        "C Dynamic Malloc Array",
        r'''
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    scanf("%d", &n);

    int *a = malloc(n * sizeof(int));

    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }

    free(a);

    return 0;
}
''',
        "integer-array",
    ),

        (
        "C Unread Fixed Array",
        r'''
#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    int a[100];

    for (int i = 0; i < 100; i++) {
        a[i] = i;
    }

    return 0;
}
''',
        "integer-scalar",
    ),

        (
        "C Unread Malloc Array",
        r'''
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    scanf("%d", &n);

    int *a = malloc(n * sizeof(int));

    for (int i = 0; i < n; i++) {
        a[i] = i;
    }

    free(a);

    return 0;
}
''',
        "integer-scalar",
    ),

]



cpp_passed = 0

print("=" * 70)
print("C++ INPUT CONTRACT ANALYZER TESTS")
print("=" * 70)

for test_name, code, expected_type in tests:
    if run_test(
        test_name,
        code,
        expected_type,
        "C++",
    ):
        cpp_passed += 1


c_passed = 0

print("\n" + "=" * 70)
print("C INPUT CONTRACT ANALYZER TESTS")
print("=" * 70)

for test_name, code, expected_type in c_tests:
    if run_test(
        test_name,
        code,
        expected_type,
        "C",
    ):
        c_passed += 1


print("=" * 70)
print(
    f"C++ RESULT: {cpp_passed}/{len(tests)}"
)
print(
    f"C RESULT:   {c_passed}/{len(c_tests)}"
)
print("=" * 70)