// Benchmark: Linear Search
// Category: Searching
// Algorithm: Linear Search - O(n)

use std::io::{
    self,
    Read
};

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

    let mut result: i64 = -1;

    for i in 0..n {
        if a[i] == target {
            result = i as i64;
            break;
        }
    }

    println!("{}", result);
}
