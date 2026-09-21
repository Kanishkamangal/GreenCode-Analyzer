// Benchmark: Jump Search
// Category: Searching
// Algorithm: Jump Search - O(sqrt(n))

use std::io::{
    self,
    Read
};

fn integer_sqrt(
    n: usize
) -> usize {
    if n == 0 {
        return 0;
    }

    let mut x =
        (n as f64).sqrt() as usize;

    while (
        (x + 1) <= n / (x + 1)
    ) {
        x += 1;
    }

    while x > n / x {
        x -= 1;
    }

    x
}

fn jump_search(
    a: &[i64],
    target: i64
) -> i64 {
    let n = a.len();

    if n == 0 {
        return -1;
    }

    let step =
        integer_sqrt(n).max(1);

    let mut previous = 0usize;
    let mut current = step;

    while (
        previous < n &&
        a[current.min(n) - 1]
            < target
    ) {
        previous = current;
        current += step;

        if previous >= n {
            return -1;
        }
    }

    let end =
        current.min(n);

    for i in previous..end {
        if a[i] == target {
            return i as i64;
        }

        if a[i] > target {
            break;
        }
    }

    -1
}

fn main() {
    let mut input =
        String::new();

    io::stdin()
        .read_to_string(
            &mut input
        )
        .unwrap();

    let values: Vec<i64> =
        input
            .split_whitespace()
            .map(|x| {
                x.parse::<i64>()
                    .unwrap()
            })
            .collect();

    if values.is_empty() {
        return;
    }

    let mut position = 0usize;

    let n =
        values[position] as usize;

    position += 1;

    let mut a =
        Vec::with_capacity(n);

    for _ in 0..n {
        a.push(
            values[position]
        );

        position += 1;
    }

    let target =
        values[position];

    println!(
        "{}",
        jump_search(
            &a,
            target
        )
    );
}
