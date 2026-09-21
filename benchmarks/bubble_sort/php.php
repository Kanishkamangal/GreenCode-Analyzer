<?php

// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

$input = trim(stream_get_contents(STDIN));

if ($input === '') {
    echo "0\n";
    exit;
}

$tokens = preg_split('/\s+/', $input);

$a = [];

foreach ($tokens as $token) {
    $a[] = (int)$token;
}

$n = count($a);

for ($i = 0; $i < $n - 1; $i++) {

    $swapped = false;

    for ($j = 0; $j < $n - $i - 1; $j++) {

        if ($a[$j] > $a[$j + 1]) {

            $temp = $a[$j];
            $a[$j] = $a[$j + 1];
            $a[$j + 1] = $temp;

            $swapped = true;
        }
    }

    if (!$swapped) {
        break;
    }
}

echo ($n > 0 ? $a[$n - 1] : 0) . PHP_EOL;