// Benchmark: Anagram Check
// Category: String
// Algorithm: Anagram Check - O(n)

use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    let mut it = input.split_whitespace();

    let s1 = match it.next() {
        Some(value) => value,
        None => {
            println!("0");
            return;
        }
    };

    let s2 = match it.next() {
        Some(value) => value,
        None => {
            println!("0");
            return;
        }
    };

    if s1.len() != s2.len() {
        println!("0");
        return;
    }

    let mut count = [0i64; 256];

    for b in s1.bytes() {
        count[b as usize] += 1;
    }

    for b in s2.bytes() {
        count[b as usize] -= 1;
    }

    println!(
        "{}",
        if count.iter().all(|&x| x == 0) { 1 } else { 0 }
    );
}
