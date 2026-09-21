// Benchmark: Bucket Sort
// Category: Sorting
// Algorithm: Bucket Sort - O(n + k) average

use std::io::{
    self,
    Read
};

fn insertion_sort(
    bucket: &mut Vec<i64>
) {
    for i in 1..bucket.len() {
        let key = bucket[i];
        let mut j = i;

        while (
            j > 0 &&
            bucket[j - 1] > key
        ) {
            bucket[j] =
                bucket[j - 1];

            j -= 1;
        }

        bucket[j] = key;
    }
}

fn bucket_sort(
    a: &mut Vec<i64>
) {
    let n = a.len();

    if n <= 1 {
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

    if min_value == max_value {
        return;
    }

    let bucket_count =
        ((n as f64).sqrt() as usize)
            .max(1);

    let mut buckets:
        Vec<Vec<i64>> =
        vec![
            Vec::new();
            bucket_count
        ];

    let range =
        max_value as f64 -
        min_value as f64 +
        1.0;

    for &value in a.iter() {
        let offset =
            value as f64 -
            min_value as f64;

        let mut index = (
            offset *
            bucket_count as f64 /
            range
        ) as usize;

        if index >= bucket_count {
            index =
                bucket_count - 1;
        }

        buckets[index].push(value);
    }

    let mut position = 0usize;

    for bucket in buckets.iter_mut() {
        insertion_sort(bucket);

        for &value in bucket.iter() {
            a[position] = value;
            position += 1;
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
        bucket_sort(
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
