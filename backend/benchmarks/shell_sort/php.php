<?php

// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

function shellSort(&$a) {
    $n = count($a);

    for (
        $gap = intdiv($n, 2);
        $gap > 0;
        $gap = intdiv($gap, 2)
    ) {
        for (
            $i = $gap;
            $i < $n;
            $i++
        ) {
            $temp = $a[$i];
            $j = $i;

            while (
                $j >= $gap &&
                $a[$j - $gap] > $temp
            ) {
                $a[$j] =
                    $a[$j - $gap];

                $j -= $gap;
            }

            $a[$j] = $temp;
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
    shellSort($a);
}

echo (
    count($a) === 0
        ? 0
        : $a[count($a) - 1]
) . PHP_EOL;

?>
