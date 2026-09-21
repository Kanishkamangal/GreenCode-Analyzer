// Benchmark: Merge Sort
// Category: Sorting
// Algorithm: Merge Sort - O(n log n)

use std::io::{
    self,
    Read
};

fn merge(
    a: &mut Vec<i64>,
    temp: &mut Vec<i64>,
    left: usize,
    mid: usize,
    right: usize,
) {
    let mut i = left;
    let mut j = mid + 1;
    let mut k = left;

    while i <= mid && j <= right {
        if a[i] <= a[j] {
            temp[k] = a[i];
            i += 1;
        } else {
            temp[k] = a[j];
            j += 1;
        }

        k += 1;
    }

    while i <= mid {
        temp[k] = a[i];
        i += 1;
        k += 1;
    }

    while j <= right {
        temp[k] = a[j];
        j += 1;
        k += 1;
    }

    for index in left..=right {
        a[index] = temp[index];
    }
}

fn merge_sort(
    a: &mut Vec<i64>,
    temp: &mut Vec<i64>,
    left: usize,
    right: usize,
) {
    if left >= right {
        return;
    }

    let mid = left + (right - left) / 2;

    merge_sort(
        a,
        temp,
        left,
        mid
    );

    merge_sort(
        a,
        temp,
        mid + 1,
        right
    );

    merge(
        a,
        temp,
        left,
        mid,
        right
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
        let mut temp = vec![0; a.len()];
        let right = a.len() - 1;

        merge_sort(
            &mut a,
            &mut temp,
            0,
            right
        );
    }

    if a.is_empty() {
        println!("0");
    } else {
        println!("{}", a[a.len() - 1]);
    }
}
