// Benchmark: Radix Sort
// Category: Sorting
// Algorithm: LSD Radix Sort - O(d * (n + b))

use std::io::{
    self,
    Read
};

fn radix_sort_non_negative(
    a: &mut Vec<u64>
) {
    if a.len() <= 1 {
        return;
    }

    let mut max_value = a[0];

    for &value in a.iter() {
        if value > max_value {
            max_value = value;
        }
    }

    let mut output =
        vec![0u64; a.len()];

    let mut exp = 1u64;

    while max_value / exp > 0 {
        let mut count =
            [0usize; 10];

        for &value in a.iter() {
            let digit =
                ((value / exp) % 10)
                    as usize;

            count[digit] += 1;
        }

        for i in 1..10 {
            count[i] += count[i - 1];
        }

        for i in (
            0..a.len()
        ).rev() {
            let digit =
                ((a[i] / exp) % 10)
                    as usize;

            count[digit] -= 1;

            output[
                count[digit]
            ] = a[i];
        }

        a.copy_from_slice(
            &output
        );

        if exp > max_value / 10 {
            break;
        }

        exp *= 10;
    }
}

fn radix_sort(
    a: &mut Vec<i64>
) {
    let mut negative:
        Vec<u64> = Vec::new();

    let mut positive:
        Vec<u64> = Vec::new();

    for &value in a.iter() {
        if value < 0 {
            negative.push(
                value.unsigned_abs()
            );
        } else {
            positive.push(
                value as u64
            );
        }
    }

    radix_sort_non_negative(
        &mut negative
    );

    radix_sort_non_negative(
        &mut positive
    );

    let mut index = 0usize;

    for i in (
        0..negative.len()
    ).rev() {
        a[index] =
            -(negative[i] as i64);

        index += 1;
    }

    for value in positive {
        a[index] = value as i64;
        index += 1;
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
        radix_sort(
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
