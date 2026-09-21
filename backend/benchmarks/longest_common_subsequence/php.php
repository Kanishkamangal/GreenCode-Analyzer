<?php

// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

$input = trim(
    stream_get_contents(STDIN)
);

if ($input === '') {
    exit;
}

$values = preg_split(
    '/\s+/',
    $input
);

if (count($values) < 2) {
    exit;
}

$first = $values[0];
$second = $values[1];

$n = strlen($first);
$m = strlen($second);

$previous =
    array_fill(
        0,
        $m + 1,
        0
    );

$current =
    array_fill(
        0,
        $m + 1,
        0
    );

for ($i = 1; $i <= $n; $i++) {
    $current[0] = 0;

    for ($j = 1; $j <= $m; $j++) {
        if (
            $first[$i - 1] ===
            $second[$j - 1]
        ) {
            $current[$j] =
                $previous[$j - 1] + 1;
        } else {
            $current[$j] =
                max(
                    $previous[$j],
                    $current[$j - 1]
                );
        }
    }

    $temp = $previous;
    $previous = $current;
    $current = $temp;
}

echo $previous[$m] . PHP_EOL;

?>
