from app.services.reference_code_analyzer import (
    detect_reference_language,
)


tests = {
    "C++": """
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    cout << n;
    return 0;
}
""",

    "C": """
#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);
    printf("%d", n);
    return 0;
}
""",

    "Java": """
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(n);
    }
}
""",

    "Python": """
n = int(input())
print(n)
""",

    "JavaScript": """
const fs = require('fs');
const input = fs.readFileSync(0, 'utf8');
console.log(input);
""",

    "Go": """
package main

import "fmt"

func main() {
    var n int
    fmt.Scan(&n)
    fmt.Println(n)
}
""",

    "Rust": """
use std::io;

fn main() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    println!("{}", input);
}
""",

    "C#": """
using System;

class Program {
    static void Main() {
        string input = Console.ReadLine();
        Console.WriteLine(input);
    }
}
""",

    "Kotlin": """
fun main() {
    val n = readLine()!!.toInt()
    println(n)
}
""",

    "PHP": """
<?php
$n = trim(fgets(STDIN));
echo $n;
?>
""",
}


for expected, code in tests.items():

    result = detect_reference_language(code)

    detected = result["language"]

    status = (
        "PASS"
        if detected == expected
        else "FAIL"
    )

    print(
        f"{expected:12} -> "
        f"{str(detected):12} "
        f"{status} "
        f"(confidence={result['confidence']})"
    )