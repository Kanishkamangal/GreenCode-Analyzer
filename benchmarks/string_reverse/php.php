<?php

// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

$input = trim(
    stream_get_contents(STDIN)
);

if ($input === '') {
    exit;
}

$parts = preg_split(
    '/\s+/',
    $input
);

$s = $parts[0];

$left = 0;
$right = strlen($s) - 1;

while ($left < $right) {
    $temp = $s[$left];

    $s[$left] =
        $s[$right];

    $s[$right] =
        $temp;

    $left++;
    $right--;
}

echo $s . PHP_EOL;

?>
