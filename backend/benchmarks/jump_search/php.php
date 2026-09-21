<?php

// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

function jumpSearch(
    $a,
    $target
) {
    $n = count($a);

    if ($n === 0) {
        return -1;
    }

    $step = max(
        1,
        (int)floor(
            sqrt($n)
        )
    );

    $previous = 0;
    $current = $step;

    while (
        $previous < $n &&
        $a[min($current, $n) - 1]
            < $target
    ) {
        $previous = $current;
        $current += $step;

        if ($previous >= $n) {
            return -1;
        }
    }

    $end =
        min($current, $n);

    for (
        $i = $previous;
        $i < $end;
        $i++
    ) {
        if ($a[$i] === $target) {
            return $i;
        }

        if ($a[$i] > $target) {
            break;
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

echo jumpSearch(
    $a,
    $target
) . PHP_EOL;

?>
