<?php
// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

$input = trim(stream_get_contents(STDIN));
$tokens = preg_split('/\s+/', $input, -1, PREG_SPLIT_NO_EMPTY);

if (count($tokens) < 2) {
    echo "0\n";
    exit;
}

$s1 = $tokens[0];
$s2 = $tokens[1];

if (strlen($s1) !== strlen($s2)) {
    echo "0\n";
    exit;
}

$count = [];

for ($i = 0; $i < strlen($s1); $i++) {
    $c = $s1[$i];
    $count[$c] = ($count[$c] ?? 0) + 1;
}

for ($i = 0; $i < strlen($s2); $i++) {
    $c = $s2[$i];
    $count[$c] = ($count[$c] ?? 0) - 1;
}

foreach ($count as $value) {
    if ($value !== 0) {
        echo "0\n";
        exit;
    }
}

echo "1\n";
?>
