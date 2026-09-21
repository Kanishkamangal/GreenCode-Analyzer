<?php

// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

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

$s = $values[0];

$n = strlen($s);
$bestStart = 0;
$bestLength = 1;

for (
    $center = 0;
    $center < $n;
    $center++
) {
    $left = $center;
    $right = $center;

    while (
        $left >= 0 &&
        $right < $n &&
        $s[$left] === $s[$right]
    ) {
        $length =
            $right - $left + 1;

        if ($length > $bestLength) {
            $bestStart = $left;
            $bestLength = $length;
        }

        $left--;
        $right++;
    }

    $left = $center;
    $right = $center + 1;

    while (
        $left >= 0 &&
        $right < $n &&
        $s[$left] === $s[$right]
    ) {
        $length =
            $right - $left + 1;

        if ($length > $bestLength) {
            $bestStart = $left;
            $bestLength = $length;
        }

        $left--;
        $right++;
    }
}

$result = '';

for (
    $i = $bestStart;
    $i < $bestStart + $bestLength;
    $i++
) {
    $result .= $s[$i];
}

echo $result . PHP_EOL;

?>
