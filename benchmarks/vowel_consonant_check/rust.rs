// Benchmark: Vowel or Consonant Check
// Category: Character
// Algorithm: Direct Character Check - O(1)

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

    let value = input.trim();

    if value.is_empty() {
        return;
    }

    let ch =
        value.as_bytes()[0];

    let vowel =
        ch == b'a' ||
        ch == b'e' ||
        ch == b'i' ||
        ch == b'o' ||
        ch == b'u' ||
        ch == b'A' ||
        ch == b'E' ||
        ch == b'I' ||
        ch == b'O' ||
        ch == b'U';

    println!(
        "{}",
        if vowel { 1 } else { 0 }
    );
}
