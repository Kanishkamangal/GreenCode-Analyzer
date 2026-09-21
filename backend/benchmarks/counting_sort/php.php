<?php

// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

function countingSort(&$a) {
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

    $range =
        $maxValue - $minValue + 1;

    $count = array_fill(
        0,
        $range,
        0
    );

    foreach ($a as $value) {
        $count[
            $value - $minValue
        ]++;
    }

    $index = 0;

    for (
        $i = 0;
        $i < $range;
        $i++
    ) {
        while ($count[$i] > 0) {
            $a[$index++] =
                $i + $minValue;

            $count[$i]--;
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
    countingSort($a);
}

echo (
    count($a) === 0
        ? 0
        : $a[count($a) - 1]
) . PHP_EOL;

?>
