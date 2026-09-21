from app.services.custom_benchmark_engine import run_custom_code

tests = {
    "C": '#include <stdio.h>\nint main(){int n;scanf("%d",&n);printf("%d",n*2);}',
    "C++": '#include <iostream>\nint main(){int n;std::cin>>n;std::cout<<n*2;}',
    "Java": 'import java.util.*;class Main{public static void main(String[]a){Scanner s=new Scanner(System.in);int n=s.nextInt();System.out.print(n*2);}}',
    "JavaScript": 'const fs=require("fs");let n=parseInt(fs.readFileSync(0,"utf8"));console.log(n*2);',
    "Go": 'package main\nimport "fmt"\nfunc main(){var n int;fmt.Scan(&n);fmt.Print(n*2)}',
    "Rust": 'use std::io::{self,Read};fn main(){let mut s=String::new();io::stdin().read_to_string(&mut s).unwrap();let n:i32=s.trim().parse().unwrap();print!("{}",n*2);}',
    "C#": 'using System;class Program{static void Main(){int n=int.Parse(Console.ReadLine());Console.Write(n*2);}}',
    "Kotlin": 'fun main(){val n=readLine()!!.trim().toInt();print(n*2)}',
    "PHP": '<?php $n=(int)trim(fgets(STDIN));echo $n*2; ?>'
}

for language, code in tests.items():
    print(f"\n=== {language} ===")
    try:
        result = run_custom_code(language, code, "5\n")
        print({
            "stdout": result["stdout"],
            "return_code": result["return_code"],
            "execution_time": result["execution_time"],
            "cpu_usage": result["cpu_usage"],
            "memory_usage": result["memory_usage"],
            "energy_consumption": result["energy_consumption"],
        })
    except Exception as e:
        print("FAILED:", type(e).__name__, str(e))
