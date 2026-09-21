<?php

// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

function substringSearch(
    $text,
    $pattern
) {
    $n = strlen($text);
    $m = strlen($pattern);

    if ($m === 0) {
        return 0;
    }

    if ($m > $n) {
        return -1;
    }

    for (
        $i = 0;
        $i <= $n - $m;
        $i++
    ) {
        $j = 0;

        while (
            $j < $m &&
            $text[$i + $j] ===
            $pattern[$j]
        ) {
            $j++;
        }

        if ($j === $m) {
            return $i;
        }
    }

    return -1;
}

$input = trim(
    stream_get_contents(STDIN)
);

if ($input === '') {
    exit;
}

$parts = preg_split(
    '/\s+/',
    $input
);

if (count($parts) < 2) {
    exit;
}

$text = $parts[0];
$pattern = $parts[1];

echo substringSearch(
    $text,
    $pattern
) . PHP_EOL;

?>
