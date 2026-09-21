// Benchmark: Counting Sort
// Category: Sorting
// Algorithm: Counting Sort - O(n + k)

use std::io::{
    self,
    Read
};

fn counting_sort(
    a: &mut Vec<i64>
) {
    if a.len() <= 1 {
        return;
    }

    let mut min_value = a[0];
    let mut max_value = a[0];

    for &value in a.iter() {
        if value < min_value {
            min_value = value;
        }

        if value > max_value {
            max_value = value;
        }
    }

    let range =
        (max_value - min_value + 1)
            as usize;

    let mut count =
        vec![0usize; range];

    for &value in a.iter() {
        count[
            (value - min_value)
                as usize
        ] += 1;
    }

    let mut index = 0usize;

    for i in 0..range {
        while count[i] > 0 {
            a[index] =
                i as i64 + min_value;

            index += 1;
            count[i] -= 1;
        }
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
        counting_sort(
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
