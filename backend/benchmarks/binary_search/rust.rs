// Benchmark: Binary Search
// Category: Searching
// Algorithm: Binary Search - O(log n)

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

    let mut left = 0usize;
    let mut right = n;
    let mut result: i64 = -1;

    while left < right {
        let mid =
            left + (right - left) / 2;

        if a[mid] == target {
            result = mid as i64;
            break;
        }

        if a[mid] < target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    println!("{}", result);
}
