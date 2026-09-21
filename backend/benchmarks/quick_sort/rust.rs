// Benchmark: Quick Sort
// Category: Sorting
// Algorithm: Quick Sort - O(n log n) average

use std::io::{
    self,
    Read
};

fn partition(
    a: &mut Vec<i64>,
    low: usize,
    high: usize,
) -> usize {
    let pivot = a[high];
    let mut i = low;

    for j in low..high {
        if a[j] <= pivot {
            a.swap(i, j);
            i += 1;
        }
    }

    a.swap(i, high);

    i
}

fn quick_sort(
    a: &mut Vec<i64>,
    low: usize,
    high: usize,
) {
    if low >= high {
        return;
    }

    let pivot_index = partition(
        a,
        low,
        high,
    );

    if pivot_index > 0 {
        quick_sort(
            a,
            low,
            pivot_index - 1,
        );
    }

    quick_sort(
        a,
        pivot_index + 1,
        high,
    );
}

fn main() {
    let mut input = String::new();

    io::stdin()
        .read_to_string(&mut input)
        .unwrap();

    let mut a: Vec<i64> = input
        .split_whitespace()
        .map(|x| {
            x.parse::<i64>().unwrap()
        })
        .collect();

    if !a.is_empty() {
        let high = a.len() - 1;

        quick_sort(
            &mut a,
            0,
            high,
        );
    }

    if a.is_empty() {
        println!("0");
    } else {
        println!("{}", a[a.len() - 1]);
    }
}
