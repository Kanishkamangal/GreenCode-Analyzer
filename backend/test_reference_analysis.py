from app.services.reference_code_analyzer import (
    analyze_reference_code,
)


tests = {
    "C++": r"""
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    cout << n;
    return 0;
}
""",

    "C": r"""
#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);
    printf("%d", n);
    return 0;
}
""",

    "Java": r"""
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(n);
    }
}
""",

    "Python": r"""
n = int(input())
print(n)
""",

    "JavaScript": r"""
const fs = require("fs");

const input = fs.readFileSync(0, "utf8").trim();
const n = Number(input);

console.log(n);
""",

    "Go": r"""
package main

import "fmt"

func main() {
    var n int
    fmt.Scan(&n)
    fmt.Println(n)
}
""",

    "Rust": r"""
use std::io;

fn main() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();

    let n: i32 = input.trim().parse().unwrap();
    println!("{}", n);
}
""",

    "C#": r"""
using System;

class Program
{
    static void Main()
    {
        int n = int.Parse(Console.ReadLine());
        Console.WriteLine(n);
    }
}
""",

    "Kotlin": r"""
fun main() {
    val n = readLine()!!.toInt()
    println(n)
}
""",

    "PHP": r"""
<?php

$n = intval(trim(fgets(STDIN)));
echo $n;
?>
""",
}


for expected_language, code in tests.items():

    result = analyze_reference_code(code)

    detected_language = result["language"]
    syntax_valid = result["syntax_valid"]

    passed = (
        detected_language == expected_language
        and syntax_valid is True
    )

    print(
        f"{expected_language:<12} -> "
        f"{str(detected_language):<12} "
        f"{'PASS' if passed else 'FAIL'} "
        f"(confidence={result['confidence']})"
    )

    if not syntax_valid:
        print(
            "  syntax_errors:",
            result["syntax_errors"]
        )