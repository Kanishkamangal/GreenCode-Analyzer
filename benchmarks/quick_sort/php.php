<?php

// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

function partitionArray(&$a, $low, $high) {
    $pivot = $a[$high];
    $i = $low - 1;

    for ($j = $low; $j < $high; $j++) {
        if ($a[$j] <= $pivot) {
            $i++;

            $temp = $a[$i];
            $a[$i] = $a[$j];
            $a[$j] = $temp;
        }
    }

    $temp = $a[$i + 1];
    $a[$i + 1] = $a[$high];
    $a[$high] = $temp;

    return $i + 1;
}

function quickSort(&$a, $low, $high) {
    if ($low < $high) {
        $pivotIndex = partitionArray(
            $a,
            $low,
            $high
        );

        quickSort(
            $a,
            $low,
            $pivotIndex - 1
        );

        quickSort(
            $a,
            $pivotIndex + 1,
            $high
        );
    }
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
    quickSort(
        $a,
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
