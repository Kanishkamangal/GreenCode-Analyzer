<?php
// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

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
$capacity = intval($tokens[$index++]);

if (
    $n < 0 ||
    $capacity < 0 ||
    count($tokens) < 2 + 2 * $n
) {
    exit;
}

$weights = [];

for ($i = 0; $i < $n; $i++) {
    $weights[] =
        intval($tokens[$index++]);
}

$values = [];

for ($i = 0; $i < $n; $i++) {
    $values[] =
        intval($tokens[$index++]);
}

$dp =
    array_fill(
        0,
        $capacity + 1,
        0
    );

for ($i = 0; $i < $n; $i++) {
    $weight = $weights[$i];
    $value = $values[$i];

    if ($weight <= 0) {
        continue;
    }

    for (
        $c = $capacity;
        $c >= $weight;
        $c--
    ) {
        $candidate =
            $dp[$c - $weight] + $value;

        if ($candidate > $dp[$c]) {
            $dp[$c] = $candidate;
        }
    }
}

echo $dp[$capacity] . PHP_EOL;
?>
