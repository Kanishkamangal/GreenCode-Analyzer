// Benchmark: Bubble Sort
// Category: Sorting
// Algorithm: Bubble Sort - O(n^2)

use std::io::{self, Read};

fn main() {

    let mut input = String::new();

    io::stdin()
        .read_to_string(&mut input)
        .unwrap();

    let mut a: Vec<i64> = input
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .collect();

    let n = a.len();

    for i in 0..n.saturating_sub(1) {

        let mut swapped = false;

        for j in 0..n - i - 1 {

            if a[j] > a[j + 1] {

                a.swap(j, j + 1);

                swapped = true;
            }
        }

        if !swapped {
            break;
        }
    }

    if n == 0 {
        println!("0");
    } else {
        println!("{}", a[n - 1]);
    }
}