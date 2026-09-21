<?php

// Benchmark: Character Frequency in String
// Category: Strings
// Algorithm: Linear Character Frequency Count - O(n)

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

$s =
    $values[0];

$target =
    $values[1][0];

$frequency = 0;

$length =
    strlen($s);

for (
    $i = 0;
    $i < $length;
    $i++
) {
    if ($s[$i] === $target) {
        $frequency++;
    }
}

echo $frequency . PHP_EOL;

?>
