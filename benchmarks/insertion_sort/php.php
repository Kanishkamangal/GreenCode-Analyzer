<?php

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

$n = count($a);

for ($i = 1; $i < $n; $i++) {
    $key = $a[$i];
    $j = $i - 1;

    while (
        $j >= 0 &&
        $a[$j] > $key
    ) {
        $a[$j + 1] = $a[$j];
        $j--;
    }

    $a[$j + 1] = $key;
}

echo $n === 0
    ? 0
    : $a[$n - 1];

?>
