use std::io::{
    self,
    Read
};

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

    let n = a.len();

    for i in 1..n {
        let key = a[i];
        let mut j = i;

        while (
            j > 0 &&
            a[j - 1] > key
        ) {
            a[j] = a[j - 1];
            j -= 1;
        }

        a[j] = key;
    }

    if a.is_empty() {
        print!("0");
    } else {
        print!(
            "{}",
            a[a.len() - 1]
        );
    }
}
