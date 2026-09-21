// Benchmark: Character Frequency in String
// Category: Strings
// Algorithm: Linear Character Frequency Count - O(n)

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

    let values:
        Vec<&str> =
        input
            .split_whitespace()
            .collect();

    if values.len() < 2 {
        return;
    }

    let s =
        values[0].as_bytes();

    let target_values =
        values[1].as_bytes();

    if target_values.is_empty() {
        return;
    }

    let target =
        target_values[0];

    let mut frequency:
        u64 = 0;

    for &ch in s {
        if ch == target {
            frequency += 1;
        }
    }

    println!(
        "{}",
        frequency
    );
}
