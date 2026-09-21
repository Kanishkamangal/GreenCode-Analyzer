// Benchmark: 0/1 Knapsack
// Category: Dynamic Programming
// Algorithm: 0/1 Knapsack - O(n * capacity)

use std::io::{self, Read};

fn main() {
    let mut input = String::new();

    io::stdin()
        .read_to_string(&mut input)
        .unwrap();

    let mut it =
        input.split_whitespace();

    let n: usize = match it
        .next()
        .and_then(|x| x.parse().ok())
    {
        Some(value) => value,
        None => return,
    };

    let capacity: usize = match it
        .next()
        .and_then(|x| x.parse().ok())
    {
        Some(value) => value,
        None => return,
    };

    let mut weights =
        Vec::with_capacity(n);

    for _ in 0..n {
        match it
            .next()
            .and_then(|x| x.parse::<usize>().ok())
        {
            Some(value) => weights.push(value),
            None => return,
        }
    }

    let mut values =
        Vec::with_capacity(n);

    for _ in 0..n {
        match it
            .next()
            .and_then(|x| x.parse::<i64>().ok())
        {
            Some(value) => values.push(value),
            None => return,
        }
    }

    let mut dp =
        vec![0_i64; capacity + 1];

    for i in 0..n {
        let weight = weights[i];
        let value = values[i];

        if weight == 0 {
            continue;
        }

        for c in (weight..=capacity).rev() {
            let candidate =
                dp[c - weight] + value;

            if candidate > dp[c] {
                dp[c] = candidate;
            }
        }
    }

    println!("{}", dp[capacity]);
}
