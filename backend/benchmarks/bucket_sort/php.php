<?php

// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

function insertionSort(&$bucket) {
    $n = count($bucket);

    for ($i = 1; $i < $n; $i++) {
        $key = $bucket[$i];
        $j = $i - 1;

        while (
            $j >= 0 &&
            $bucket[$j] > $key
        ) {
            $bucket[$j + 1] =
                $bucket[$j];

            $j--;
        }

        $bucket[$j + 1] = $key;
    }
}

function bucketSort(&$a) {
    $n = count($a);

    if ($n <= 1) {
        return;
    }

    $minValue = $a[0];
    $maxValue = $a[0];

    foreach ($a as $value) {
        if ($value < $minValue) {
            $minValue = $value;
        }

        if ($value > $maxValue) {
            $maxValue = $value;
        }
    }

    if ($minValue == $maxValue) {
        return;
    }

    $bucketCount = max(
        1,
        (int)sqrt($n)
    );

    $buckets = array_fill(
        0,
        $bucketCount,
        null
    );

    for (
        $i = 0;
        $i < $bucketCount;
        $i++
    ) {
        $buckets[$i] = [];
    }

    $range =
        $maxValue -
        $minValue + 1;

    foreach ($a as $value) {
        $index = (int)floor(
            (($value - $minValue) *
            $bucketCount) /
            $range
        );

        if ($index >= $bucketCount) {
            $index =
                $bucketCount - 1;
        }

        $buckets[$index][] = $value;
    }

    $position = 0;

    for (
        $i = 0;
        $i < $bucketCount;
        $i++
    ) {
        insertionSort(
            $buckets[$i]
        );

        foreach (
            $buckets[$i] as $value
        ) {
            $a[$position++] = $value;
        }
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
    bucketSort($a);
}

echo (
    count($a) === 0
        ? 0
        : $a[count($a) - 1]
) . PHP_EOL;

?>
