<?php

// Benchmark: Heap Sort
// Category: Sorting
// Algorithm: Heap Sort - O(n log n)

function heapify(
    &$a,
    $n,
    $i
) {
    $largest = $i;
    $left = 2 * $i + 1;
    $right = 2 * $i + 2;

    if (
        $left < $n &&
        $a[$left] > $a[$largest]
    ) {
        $largest = $left;
    }

    if (
        $right < $n &&
        $a[$right] > $a[$largest]
    ) {
        $largest = $right;
    }

    if ($largest != $i) {
        $temp = $a[$i];
        $a[$i] = $a[$largest];
        $a[$largest] = $temp;

        heapify(
            $a,
            $n,
            $largest
        );
    }
}

function heapSort(&$a) {
    $n = count($a);

    for (
        $i = intdiv($n, 2) - 1;
        $i >= 0;
        $i--
    ) {
        heapify(
            $a,
            $n,
            $i
        );
    }

    for (
        $i = $n - 1;
        $i > 0;
        $i--
    ) {
        $temp = $a[0];
        $a[0] = $a[$i];
        $a[$i] = $temp;

        heapify(
            $a,
            $i,
            0
        );
    }
}

$input = trim(
    stream_get_contents(STDIN)
);

$a = $input === ''
    ? []
    : preg_split(
        '/\s+/',
        $input
    );

$a = array_map(
    'intval',
    $a
);

if (count($a) > 0) {
    heapSort($a);
}

echo (
    count($a) === 0
        ? 0
        : $a[count($a) - 1]
) . PHP_EOL;

?>
