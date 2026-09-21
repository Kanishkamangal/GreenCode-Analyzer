<?php

// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

function radixSortNonNegative(&$a) {
    $n = count($a);

    if ($n <= 1) {
        return;
    }

    $maxValue = $a[0];

    foreach ($a as $value) {
        if ($value > $maxValue) {
            $maxValue = $value;
        }
    }

    $output = array_fill(
        0,
        $n,
        0
    );

    for (
        $exp = 1;
        intdiv($maxValue, $exp) > 0;
        $exp *= 10
    ) {
        $count = array_fill(
            0,
            10,
            0
        );

        foreach ($a as $value) {
            $digit =
                intdiv($value, $exp) % 10;

            $count[$digit]++;
        }

        for ($i = 1; $i < 10; $i++) {
            $count[$i] +=
                $count[$i - 1];
        }

        for (
            $i = $n - 1;
            $i >= 0;
            $i--
        ) {
            $digit =
                intdiv($a[$i], $exp) % 10;

            $count[$digit]--;

            $output[
                $count[$digit]
            ] = $a[$i];
        }

        for ($i = 0; $i < $n; $i++) {
            $a[$i] = $output[$i];
        }

        if ($exp > intdiv($maxValue, 10)) {
            break;
        }
    }
}

function radixSort(&$a) {
    $negative = [];
    $positive = [];

    foreach ($a as $value) {
        if ($value < 0) {
            $negative[] = -$value;
        } else {
            $positive[] = $value;
        }
    }

    radixSortNonNegative($negative);
    radixSortNonNegative($positive);

    $index = 0;

    for (
        $i = count($negative) - 1;
        $i >= 0;
        $i--
    ) {
        $a[$index++] =
            -$negative[$i];
    }

    foreach ($positive as $value) {
        $a[$index++] = $value;
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
    radixSort($a);
}

echo (
    count($a) === 0
        ? 0
        : $a[count($a) - 1]
) . PHP_EOL;

?>
