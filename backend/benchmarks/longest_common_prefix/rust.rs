// Benchmark: Longest Common Prefix
// Category: Strings
// Algorithm: Vertical Scanning - O(total characters)

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

    let values: Vec<&str> =
        input
            .split_whitespace()
            .collect();

    if values.is_empty() {
        return;
    }

    let mut input_position =
        0usize;

    let n: usize =
        values[input_position]
            .parse()
            .unwrap();

    input_position += 1;

    if n == 0 {
        println!();
        return;
    }

    let mut strings:
        Vec<&[u8]> =
        Vec::with_capacity(n);

    for _ in 0..n {
        strings.push(
            values[input_position]
                .as_bytes()
        );

        input_position += 1;
    }

    let mut prefix_length =
        0usize;

    for position in 0..strings[0].len() {
        let current =
            strings[0][position];

        let mut matches = true;

        for i in 1..n {
            if (
                position >= strings[i].len() ||
                strings[i][position] != current
            ) {
                matches = false;
                break;
            }
        }

        if !matches {
            break;
        }

        prefix_length += 1;
    }

    let result =
        std::str::from_utf8(
            &strings[0][..prefix_length]
        )
        .unwrap();

    println!("{}", result);
}
