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
        let mut min_index = i;

        for j in (i + 1)..n {
            if a[j] < a[min_index] {
                min_index = j;
            }
        }

        if min_index != i {
            a.swap(i, min_index);
        }
    }

    if a.is_empty() {
        print!("0");
    } else {
        print!("{}", a[a.len() - 1]);
    }
}
