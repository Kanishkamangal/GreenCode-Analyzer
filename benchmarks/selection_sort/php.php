<?php

$input = trim(stream_get_contents(STDIN));

$a = $input === ""
    ? []
    : preg_split('/\s+/', $input);

$a = array_map('intval', $a);
$n = count($a);

for ($i = 0; $i < $n - 1; $i++) {
    $minIndex = $i;

    for ($j = $i + 1; $j < $n; $j++) {
        if ($a[$j] < $a[$minIndex])
            $minIndex = $j;
    }

    if ($minIndex != $i) {
        $temp = $a[$i];
        $a[$i] = $a[$minIndex];
        $a[$minIndex] = $temp;
    }
}

echo $n === 0 ? 0 : $a[$n - 1];
?>
