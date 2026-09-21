// Benchmark: Palindrome Check
// Category: Strings
// Algorithm: Two-Pointer Palindrome Check - O(n)

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

    let s = match input
        .split_whitespace()
        .next()
    {
        Some(value) => value.as_bytes(),
        None => return,
    };

    let mut left = 0usize;
    let mut right = s.len();

    let mut palindrome = true;

    while left < right {
        if s[left] != s[right - 1] {
            palindrome = false;
            break;
        }

        left += 1;
        right -= 1;
    }

    println!(
        "{}",
        if palindrome { 1 } else { 0 }
    );
}
