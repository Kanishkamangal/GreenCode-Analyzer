<?php
// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

$tokens = preg_split(
    '/\s+/',
    trim(stream_get_contents(STDIN)),
    -1,
    PREG_SPLIT_NO_EMPTY
);

if (count($tokens) < 2) {
    exit;
}

$index = 0;

$n = intval($tokens[$index++]);
$m = intval($tokens[$index++]);

if ($n <= 0 || $m < 0) {
    exit;
}

$adj = array_fill(0, $n, []);

for ($i = 0; $i < $m; $i++) {
    if ($index + 1 >= count($tokens)) {
        exit;
    }

    $u = intval($tokens[$index++]);
    $v = intval($tokens[$index++]);

    if (
        $u >= 0 && $u < $n &&
        $v >= 0 && $v < $n
    ) {
        $adj[$u][] = $v;
        $adj[$v][] = $u;
    }
}

if ($index >= count($tokens)) {
    exit;
}

$source = intval($tokens[$index]);

if ($source < 0 || $source >= $n) {
    exit;
}

$visited = array_fill(0, $n, false);
$queue = [];
$front = 0;

$queue[] = $source;
$visited[$source] = true;

$result = [];

while ($front < count($queue)) {
    $node = $queue[$front++];

    $result[] = $node;

    foreach ($adj[$node] as $next) {
        if (!$visited[$next]) {
            $visited[$next] = true;
            $queue[] = $next;
        }
    }
}

echo implode(" ", $result) . PHP_EOL;
?>
