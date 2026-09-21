// Benchmark: Shell Sort
// Category: Sorting
// Algorithm: Shell Sort - Gap-based

use std::io::{
    self,
    Read
};

fn shell_sort(
    a: &mut Vec<i64>
) {
    let n = a.len();
    let mut gap = n / 2;

    while gap > 0 {
        for i in gap..n {
            let temp = a[i];
            let mut j = i;

            while (
                j >= gap &&
                a[j - gap] > temp
            ) {
                a[j] = a[j - gap];
                j -= gap;
            }

            a[j] = temp;
        }

        gap /= 2;
    }
}

fn main() {
    let mut input =
        String::new();

    io::stdin()
        .read_to_string(
            &mut input
        )
        .unwrap();

    let mut a: Vec<i64> =
        input
            .split_whitespace()
            .map(|x| {
                x.parse::<i64>()
                    .unwrap()
            })
            .collect();

    if !a.is_empty() {
        shell_sort(
            &mut a
        );
    }

    if a.is_empty() {
        println!("0");
    } else {
        println!(
            "{}",
            a[a.len() - 1]
        );
    }
}
