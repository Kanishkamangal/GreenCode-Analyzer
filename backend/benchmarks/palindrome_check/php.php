<?php

// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

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

$palindrome = true;

while ($left < $right) {
    if ($s[$left] !== $s[$right]) {
        $palindrome = false;
        break;
    }

    $left++;
    $right--;
}

echo (
    $palindrome ? 1 : 0
) . PHP_EOL;

?>
