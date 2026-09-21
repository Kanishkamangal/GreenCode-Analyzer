<?php

// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

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

$left = 0;
$right = $n - 1;
$result = -1;

while ($left <= $right) {
    $mid =
        $left +
        intdiv(
            $right - $left,
            2
        );

    if ($a[$mid] === $target) {
        $result = $mid;
        break;
    }

    if ($a[$mid] < $target) {
        $left = $mid + 1;
    } else {
        $right = $mid - 1;
    }
}

echo $result . PHP_EOL;

?>
