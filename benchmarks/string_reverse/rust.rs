// Benchmark: String Reverse
// Category: Strings
// Algorithm: Two-Pointer String Reverse - O(n)

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

    let mut chars =
        value.as_bytes().to_vec();

    if !chars.is_empty() {
        let mut left = 0usize;
        let mut right =
            chars.len() - 1;

        while left < right {
            chars.swap(
                left,
                right
            );

            left += 1;
            right -= 1;
        }
    }

    let result =
        String::from_utf8(chars)
            .unwrap();

    println!("{}", result);
}
