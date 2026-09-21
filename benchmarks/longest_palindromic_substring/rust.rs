// Benchmark: Longest Palindromic Substring
// Category: Strings
// Algorithm: Expand Around Center - O(n^2)

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

    let value = match input
        .split_whitespace()
        .next()
    {
        Some(value) => value,
        None => return,
    };

    let s = value.as_bytes();
    let n = s.len();

    if n == 0 {
        println!();
        return;
    }

    let mut best_start = 0usize;
    let mut best_length = 1usize;

    for center in 0..n {
        let mut left =
            center as isize;

        let mut right =
            center as isize;

        while (
            left >= 0 &&
            right < n as isize &&
            s[left as usize] ==
            s[right as usize]
        ) {
            let length =
                (right - left + 1)
                    as usize;

            if length > best_length {
                best_start =
                    left as usize;

                best_length =
                    length;
            }

            left -= 1;
            right += 1;
        }

        left = center as isize;
        right =
            center as isize + 1;

        while (
            left >= 0 &&
            right < n as isize &&
            s[left as usize] ==
            s[right as usize]
        ) {
            let length =
                (right - left + 1)
                    as usize;

            if length > best_length {
                best_start =
                    left as usize;

                best_length =
                    length;
            }

            left -= 1;
            right += 1;
        }
    }

    let result =
        std::str::from_utf8(
            &s[
                best_start..
                best_start + best_length
            ]
        )
        .unwrap();

    println!("{}", result);
}
