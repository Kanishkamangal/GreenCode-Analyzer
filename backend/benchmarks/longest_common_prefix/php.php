<?php

// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

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

$inputPosition = 0;

$n = intval(
    $values[$inputPosition++]
);

if ($n <= 0) {
    echo PHP_EOL;
    exit;
}

$strings = [];

for ($i = 0; $i < $n; $i++) {
    $strings[] =
        $values[$inputPosition++];
}

$prefixLength = 0;
$firstLength =
    strlen($strings[0]);

for (
    $position = 0;
    $position < $firstLength;
    $position++
) {
    $current =
        $strings[0][$position];

    $matches = true;

    for ($i = 1; $i < $n; $i++) {
        if (
            $position >= strlen($strings[$i]) ||
            $strings[$i][$position] !== $current
        ) {
            $matches = false;
            break;
        }
    }

    if (!$matches) {
        break;
    }

    $prefixLength++;
}

$result = '';

for (
    $i = 0;
    $i < $prefixLength;
    $i++
) {
    $result .= $strings[0][$i];
}

echo $result . PHP_EOL;

?>
