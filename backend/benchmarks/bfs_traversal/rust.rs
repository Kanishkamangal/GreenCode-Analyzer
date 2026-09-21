// Benchmark: BFS Traversal
// Category: Graph
// Algorithm: Breadth First Search - O(V + E)

use std::collections::VecDeque;
use std::io::{self, Read};

fn main() {
    let mut input = String::new();

    io::stdin()
        .read_to_string(&mut input)
        .unwrap();

    let mut it = input.split_whitespace();

    let n: usize = match it.next() {
        Some(value) => match value.parse() {
            Ok(value) => value,
            Err(_) => return,
        },
        None => return,
    };

    let m: usize = match it.next() {
        Some(value) => match value.parse() {
            Ok(value) => value,
            Err(_) => return,
        },
        None => return,
    };

    if n == 0 {
        return;
    }

    let mut adj =
        vec![Vec::<usize>::new(); n];

    for _ in 0..m {
        let u: usize = match it
            .next()
            .and_then(|x| x.parse().ok())
        {
            Some(value) => value,
            None => return,
        };

        let v: usize = match it
            .next()
            .and_then(|x| x.parse().ok())
        {
            Some(value) => value,
            None => return,
        };

        if u < n && v < n {
            adj[u].push(v);
            adj[v].push(u);
        }
    }

    let source: usize = match it
        .next()
        .and_then(|x| x.parse().ok())
    {
        Some(value) => value,
        None => return,
    };

    if source >= n {
        return;
    }

    let mut visited = vec![false; n];
    let mut queue = VecDeque::new();
    let mut result = Vec::new();

    visited[source] = true;
    queue.push_back(source);

    while let Some(node) = queue.pop_front() {
        result.push(node);

        for &next in &adj[node] {
            if !visited[next] {
                visited[next] = true;
                queue.push_back(next);
            }
        }
    }

    for (i, node) in result.iter().enumerate() {
        if i > 0 {
            print!(" ");
        }

        print!("{}", node);
    }

    println!();
}
