<?php

// Benchmark: Linear Search
// Category: Searching
// Algorithm: Linear Search - O(n)

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

$position = 0;

$n = intval(
    $values[$position++]
);

$a = [];

for ($i = 0; $i < $n; $i++) {
    $a[] = intval(
        $values[$position++]
    );
}

$target = intval(
    $values[$position]
);

$result = -1;

for ($i = 0; $i < $n; $i++) {
    if ($a[$i] === $target) {
        $result = $i;
        break;
    }
}

echo $result . PHP_EOL;

?>
