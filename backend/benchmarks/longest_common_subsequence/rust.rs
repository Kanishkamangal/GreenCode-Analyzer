// Benchmark: Longest Common Subsequence
// Category: Strings
// Algorithm: Dynamic Programming LCS - O(n * m)

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

    let first =
        values[0].as_bytes();

    let second =
        values[1].as_bytes();

    let n = first.len();
    let m = second.len();

    let mut previous =
        vec![0usize; m + 1];

    let mut current =
        vec![0usize; m + 1];

    for i in 1..=n {
        current[0] = 0;

        for j in 1..=m {
            if (
                first[i - 1] ==
                second[j - 1]
            ) {
                current[j] =
                    previous[j - 1] + 1;
            } else {
                current[j] =
                    previous[j]
                        .max(
                            current[j - 1]
                        );
            }
        }

        std::mem::swap(
            &mut previous,
            &mut current
        );
    }

    println!(
        "{}",
        previous[m]
    );
}
