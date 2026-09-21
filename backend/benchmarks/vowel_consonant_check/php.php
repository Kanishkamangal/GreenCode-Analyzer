<?php

// Benchmark: Vowel or Consonant Check
// Category: Character
// Algorithm: Direct Character Check - O(1)

$input = trim(
    stream_get_contents(STDIN)
);

if ($input === '') {
    exit;
}

$ch = $input[0];

$vowel =
    $ch === 'a' ||
    $ch === 'e' ||
    $ch === 'i' ||
    $ch === 'o' ||
    $ch === 'u' ||
    $ch === 'A' ||
    $ch === 'E' ||
    $ch === 'I' ||
    $ch === 'O' ||
    $ch === 'U';

echo (
    $vowel ? 1 : 0
) . PHP_EOL;

?>
