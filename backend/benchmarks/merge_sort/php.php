<?php

// Benchmark: Merge Sort
// Category: Sorting
// Algorithm: Merge Sort - O(n log n)

function mergeArrays(&$a, &$temp, $left, $mid, $right) {
    $i = $left;
    $j = $mid + 1;
    $k = $left;

    while ($i <= $mid && $j <= $right) {
        if ($a[$i] <= $a[$j]) {
            $temp[$k++] = $a[$i++];
        } else {
            $temp[$k++] = $a[$j++];
        }
    }

    while ($i <= $mid) {
        $temp[$k++] = $a[$i++];
    }

    while ($j <= $right) {
        $temp[$k++] = $a[$j++];
    }

    for ($i = $left; $i <= $right; $i++) {
        $a[$i] = $temp[$i];
    }
}

function mergeSort(&$a, &$temp, $left, $right) {
    if ($left >= $right) {
        return;
    }

    $mid = intdiv(
        $left + $right,
        2
    );

    mergeSort(
        $a,
        $temp,
        $left,
        $mid
    );

    mergeSort(
        $a,
        $temp,
        $mid + 1,
        $right
    );

    mergeArrays(
        $a,
        $temp,
        $left,
        $mid,
        $right
    );
}

$input = trim(
    stream_get_contents(STDIN)
);

$a = $input === ''
    ? []
    : preg_split('/\s+/', $input);

$a = array_map(
    'intval',
    $a
);

if (count($a) > 0) {
    $temp = array_fill(
        0,
        count($a),
        0
    );

    mergeSort(
        $a,
        $temp,
        0,
        count($a) - 1
    );
}

echo (
    count($a) === 0
        ? 0
        : $a[count($a) - 1]
) . PHP_EOL;

?>
