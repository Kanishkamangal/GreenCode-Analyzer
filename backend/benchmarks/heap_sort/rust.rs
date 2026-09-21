// Benchmark: Heap Sort
// Category: Sorting
// Algorithm: Heap Sort - O(n log n)

use std::io::{
    self,
    Read
};

fn heapify(
    a: &mut Vec<i64>,
    n: usize,
    i: usize,
) {
    let mut largest = i;
    let left = 2 * i + 1;
    let right = 2 * i + 2;

    if (
        left < n &&
        a[left] > a[largest]
    ) {
        largest = left;
    }

    if (
        right < n &&
        a[right] > a[largest]
    ) {
        largest = right;
    }

    if largest != i {
        a.swap(
            i,
            largest
        );

        heapify(
            a,
            n,
            largest
        );
    }
}

fn heap_sort(
    a: &mut Vec<i64>
) {
    let n = a.len();

    if n < 2 {
        return;
    }

    for i in (
        0..=(n / 2 - 1)
    ).rev() {
        heapify(
            a,
            n,
            i
        );
    }

    for i in (
        1..n
    ).rev() {
        a.swap(
            0,
            i
        );

        heapify(
            a,
            i,
            0
        );
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
        heap_sort(
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
