// Benchmark: Substring Search
// Category: Strings
// Algorithm: Naive Substring Search - O(n * m)

use std::io::{
    self,
    Read
};

fn substring_search(
    text: &[u8],
    pattern: &[u8]
) -> i64 {
    let n = text.len();
    let m = pattern.len();

    if m == 0 {
        return 0;
    }

    if m > n {
        return -1;
    }

    for i in 0..=n - m {
        let mut j = 0usize;

        while (
            j < m &&
            text[i + j] ==
            pattern[j]
        ) {
            j += 1;
        }

        if j == m {
            return i as i64;
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

    let values: Vec<&str> =
        input
            .split_whitespace()
            .collect();

    if values.len() < 2 {
        return;
    }

    let text =
        values[0].as_bytes();

    let pattern =
        values[1].as_bytes();

    println!(
        "{}",
        substring_search(
            text,
            pattern
        )
    );
}
