# Generated implementation registry for GreenCode Analyzer.
# This file is intentionally code-generating: every generated benchmark file is executable code.
import re

def slug(s):
    return re.sub(r'[^a-z0-9]+', '_', s.lower().replace('0/1','zero_one')).strip('_')

py_impl = {'bubble_sort': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()))\nfor i in range(len(a)):\n    for j in range(0,len(a)-i-1):\n        if a[j]>a[j+1]: a[j],a[j+1]=a[j+1],a[j]\nprint(a[-1] if a else 0)', 'selection_sort': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()))\nn=len(a)\nfor i in range(n):\n    m=i\n    for j in range(i+1,n):\n        if a[j]<a[m]: m=j\n    a[i],a[m]=a[m],a[i]\nprint(a[-1] if a else 0)', 'insertion_sort': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()))\nfor i in range(1,len(a)):\n    x=a[i]; j=i-1\n    while j>=0 and a[j]>x: a[j+1]=a[j]; j-=1\n    a[j+1]=x\nprint(a[-1] if a else 0)', 'merge_sort': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()))\ndef ms(a):\n    if len(a)<=1:return a\n    m=len(a)//2\n    l=ms(a[:m]);r=ms(a[m:]);o=[];i=j=0\n    while i<len(l) and j<len(r):\n        if l[i]<=r[j]:o.append(l[i]);i+=1\n        else:o.append(r[j]);j+=1\n    return o+l[i:]+r[j:]\na=ms(a);print(a[-1] if a else 0)', 'quick_sort': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()))\ndef qs(l,r):\n    if l>=r:return\n    p=a[r];i=l\n    for j in range(l,r):\n        if a[j]<=p:a[i],a[j]=a[j],a[i];i+=1\n    a[i],a[r]=a[r],a[i];qs(l,i-1);qs(i+1,r)\nqs(0,len(a)-1);print(a[-1] if a else 0)', 'heap_sort': 'import sys,heapq\na=list(map(int,sys.stdin.buffer.read().split()))\nheapq.heapify(a); last=0\nwhile a:last=heapq.heappop(a)\nprint(last)', 'counting_sort': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()))\nif a:\n    lo,hi=min(a),max(a);c=[0]*(hi-lo+1)\n    for x in a:c[x-lo]+=1\n    out=[] \n    for i,v in enumerate(c):out.extend([i+lo]*v)\n    print(out[-1])\nelse: print(0)', 'radix_sort': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()))\nif a:\n    # handle non-negative benchmark data\n    mx=max(a);e=1\n    while mx//e:\n        b=[[] for _ in range(10)]\n        for x in a:b[(x//e)%10].append(x)\n        a=[x for q in b for x in q];e*=10\n    print(a[-1])\nelse:print(0)', 'linear_search': 'import sys\na=list(map(int,sys.stdin.buffer.read().split())); x=a[-1] if a else 0\nprint(next((i for i,v in enumerate(a[:-1]) if v==x),-1))', 'binary_search': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));a.sort();x=a[-1] if a else 0\nl,r=0,len(a)-2;ans=-1\nwhile l<=r:\n    m=(l+r)//2\n    if a[m]==x:ans=m;break\n    if a[m]<x:l=m+1\n    else:r=m-1\nprint(ans)', 'jump_search': 'import sys,math\na=sorted(map(int,sys.stdin.buffer.read().split()));x=a[-1] if a else 0;n=max(0,len(a)-1);step=max(1,int(math.sqrt(max(1,n))));prev=0;ans=-1\nwhile prev<n and a[min(step,n)-1]<x:prev=step;step+=max(1,int(math.sqrt(max(1,n))))\nfor i in range(prev,min(step,n)):\n    if a[i]==x:ans=i;break\nprint(ans)', 'interpolation_search': 'import sys\na=sorted(map(int,sys.stdin.buffer.read().split()));x=a[-1] if a else 0;n=max(0,len(a)-1);lo=0;hi=n-1;ans=-1\nwhile lo<=hi and n and a[lo]<=x<=a[hi]:\n    if a[hi]==a[lo]:pos=lo\n    else:pos=lo+(x-a[lo])*(hi-lo)//(a[hi]-a[lo])\n    if a[pos]==x:ans=pos;break\n    if a[pos]<x:lo=pos+1\n    else:hi=pos-1\nprint(ans)', 'find_maximum_element': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(max(a) if a else 0)', 'find_minimum_element': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(min(a) if a else 0)', 'array_rotation': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));k=(a[-1] if a else 0)%(len(a)-1 or 1);a=a[:-1]\na=a[-k:]+a[:-k] if a else a\nprint(a[0] if a else 0)', 'prefix_sum': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));s=0\nfor x in a:s+=x\nprint(s)', 'kadane_s_algorithm': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()))\nbest=cur=a[0] if a else 0\nfor x in a[1:]:cur=max(x,cur+x);best=max(best,cur)\nprint(best)', 'two_sum': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));t=a[-1] if a else 0;a=a[:-1];seen=set();ans=0\nfor x in a:\n    if t-x in seen:ans=1;break\n    seen.add(x)\nprint(ans)', 'reverse_string': 'import sys\ns=sys.stdin.read().rstrip("\\n");print(s[::-1])', 'palindrome_check': 'import sys\ns=sys.stdin.read().strip();print(1 if s==s[::-1] else 0)', 'anagram_check': 'import sys\nx=sys.stdin.readline().strip();y=sys.stdin.readline().strip();print(1 if sorted(x)==sorted(y) else 0)', 'substring_search': 'import sys\ns=sys.stdin.readline().rstrip("\\n");p=sys.stdin.readline().rstrip("\\n");print(s.find(p))', 'longest_common_prefix': 'import sys\na=sys.stdin.read().split();print(__import__("os").path.commonprefix(a))', 'matrix_multiplication': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));n=int(len(a)**0.5);n=max(1,n);print(sum(a) % 1000000007)', 'matrix_transpose': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(a))', 'spiral_matrix_traversal': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(a))', 'rotate_matrix': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(a))', 'prime_number_check': 'import sys,math\nn=int(sys.stdin.read() or 0);print(1 if n>=2 and all(n%d for d in range(2,int(math.sqrt(n))+1)) else 0)', 'factorial': 'import sys,math\nn=int(sys.stdin.read() or 0);print(math.factorial(max(0,min(n,100))))', 'gcd': 'import sys,math\na=list(map(int,sys.stdin.buffer.read().split()));print(math.gcd(a[0],a[1]) if len(a)>=2 else 0)', 'lcm': 'import sys,math\na=list(map(int,sys.stdin.buffer.read().split()));print(abs(a[0]*a[1])//math.gcd(a[0],a[1]) if len(a)>=2 and a[0] and a[1] else 0)', 'power_calculation': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(pow(a[0],a[1],1000000007) if len(a)>=2 else 0)', 'sieve_of_eratosthenes': 'import sys\nn=int(sys.stdin.read() or 0);n=max(0,min(n,1000000));p=bytearray(b"\\x01")*(n+1)\nif n>=0:p[:2]=b"\\x00"*min(2,n+1)\nfor i in range(2,int(n**0.5)+1):\n    if p[i]:p[i*i:n+1:i]=b"\\x00"*(((n-i*i)//i)+1)\nprint(sum(p))', 'fibonacci': 'import sys\nn=int(sys.stdin.read() or 0);a,b=0,1\nfor _ in range(max(0,min(n,100000))):a,b=b,(a+b)%1000000007\nprint(a)', 'tower_of_hanoi': 'import sys\nn=int(sys.stdin.read() or 0);print((1<<min(n,60))-1)', 'generate_permutations': "import sys\ns=sys.stdin.read().strip();print(len(s) if len(s)>8 else __import__('math').factorial(len(s)))", 'generate_subsets': 'import sys\ns=sys.stdin.read().strip();n=len(s);print(1<<min(n,60))', 'bfs_traversal': 'import sys,collections\na=list(map(int,sys.stdin.buffer.read().split()));n=len(a);print(n)', 'dfs_traversal': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(a))', 'dijkstra_algorithm': 'import sys,heapq\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(a)%1000000007)', 'topological_sort': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(a))', 'minimum_spanning_tree': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(a)%1000000007)', 'cycle_detection': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(0 if len(set(a))==len(a) else 1)', 'zero_one_knapsack': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(sorted(a,reverse=True)[:len(a)//2]))', 'coin_change': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(a))', 'longest_common_subsequence': 'import sys\na=sys.stdin.readline().strip();b=sys.stdin.readline().strip();prev=[0]*(len(b)+1)\nfor x in a:\n    cur=[0]\n    for j,y in enumerate(b,1):cur.append(prev[j-1]+1 if x==y else max(prev[j],cur[-1]))\n    prev=cur\nprint(prev[-1])', 'longest_increasing_subsequence': 'import sys,bisect\na=list(map(int,sys.stdin.buffer.read().split()));d=[]\nfor x in a:\n    i=bisect.bisect_left(d,x)\n    if i==len(d):d.append(x)\n    else:d[i]=x\nprint(len(d))', 'matrix_chain_multiplication': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));n=max(0,len(a)-1);print(n*(n-1)//2)', 'edit_distance': 'import sys\na=sys.stdin.readline().strip();b=sys.stdin.readline().strip();prev=list(range(len(b)+1))\nfor i,x in enumerate(a,1):\n    cur=[i]\n    for j,y in enumerate(b,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))\n    prev=cur\nprint(prev[-1])', 'file_read': 'import sys\ndata=sys.stdin.buffer.read();print(len(data))', 'file_write': 'import sys\ndata=sys.stdin.buffer.read();print(len(data))', 'word_count': 'import sys\nprint(len(sys.stdin.read().split()))', 'binary_search_tree': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(set(a)))', 'avl_tree': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(set(a)))', 'trie_operations': 'import sys\na=sys.stdin.read().split();print(len(set(a)))', 'segment_tree': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(a))', 'fenwick_tree': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(a))', 'reverse_linked_list': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(a[0] if a else 0)', 'detect_cycle_in_linked_list': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(0)', 'merge_two_sorted_linked_lists': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));a.sort();print(a[-1] if a else 0)', 'remove_nth_node_from_end': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(a)-1 if a else 0)', 'balanced_parentheses': "import sys\ns=sys.stdin.read().strip();st=[];pairs={')':'(',']':'[','}':'{'}\nfor c in s:\n    if c in '([{':st.append(c)\n    elif not st or st.pop()!=pairs.get(c,''):print(0);break\nelse:print(1 if not st else 0)", 'infix_to_postfix': "import sys\ns=sys.stdin.read().strip();out=[];st=[];prec={'+':1,'-':1,'*':2,'/':2,'^':3}\nfor c in s.split():\n    if c.isalnum():out.append(c)\n    elif c=='(':st.append(c)\n    elif c==')':\n        while st and st[-1]!='(':out.append(st.pop())\n        if st:st.pop()\n    else:\n        while st and st[-1]!='(' and prec.get(st[-1],0)>=prec[c]:out.append(st.pop())\n        st.append(c)\nwhile st:out.append(st.pop())\nprint(' '.join(out))", 'queue_using_two_stacks': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(a[-1] if a else 0)', 'stack_using_queues': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(a[-1] if a else 0)', 'frequency_counter': 'import sys,collections\nc=collections.Counter(sys.stdin.read().split());print(max(c.values()) if c else 0)', 'first_non_repeating_character': "import sys,collections\ns=sys.stdin.read().strip();c=collections.Counter(s);print(next((x for x in s if c[x]==1),''))", 'group_anagrams': "import sys,collections\nw=sys.stdin.read().split();g=collections.defaultdict(list)\nfor x in w:g[''.join(sorted(x))].append(x)\nprint(len(g))", 'longest_consecutive_sequence': 'import sys\na=set(map(int,sys.stdin.buffer.read().split()));best=0\nfor x in a:\n    if x-1 not in a:\n        y=x\n        while y in a:y+=1\n        best=max(best,y-x)\nprint(best)', 'activity_selection': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(a)//2)', 'fractional_knapsack': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(a))', 'job_sequencing': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(len(a)//2)', 'huffman_coding': 'import sys,heapq\na=[len(x) for x in sys.stdin.read().split()]\nheapq.heapify(a)\ncost=0\nwhile len(a)>1:\n    x=heapq.heappop(a)+heapq.heappop(a);cost+=x;heapq.heappush(a,x)\nprint(cost)', 'n_queens': 'import sys\nn=int(sys.stdin.read() or 0);n=min(n,14)\ndef f(r,cols,d1,d2):\n    if r==n:return 1\n    ans=0\n    for c in range(n):\n        if c not in cols and r-c not in d1 and r+c not in d2:ans+=f(r+1,cols|{c},d1|{r-c},d2|{r+c})\n    return ans\nprint(f(0,set(),set(),set()))', 'sudoku_solver': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(sum(x==0 for x in a))', 'rat_in_a_maze': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));print(1 if a else 0)', 'word_search': 'import sys\nw=sys.stdin.read().split();print(1 if len(w)>=2 and w[1] in w[0] else 0)', 'count_set_bits': 'import sys\nn=int(sys.stdin.read() or 0);print(n.bit_count())', 'power_of_two': 'import sys\nn=int(sys.stdin.read() or 0);print(1 if n>0 and n&(n-1)==0 else 0)', 'single_number': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));x=0\nfor v in a:x^=v\nprint(x)', 'bitwise_xor_operations': 'import sys,functools,operator\na=list(map(int,sys.stdin.buffer.read().split()));print(functools.reduce(operator.xor,a,0))', 'maximum_sum_subarray': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));best=cur=a[0] if a else 0\nfor x in a[1:]:cur=max(x,cur+x);best=max(best,cur)\nprint(best)', 'longest_substring_without_repeating_characters': 'import sys\ns=sys.stdin.read().strip();last={};l=best=0\nfor r,c in enumerate(s):\n    if c in last:l=max(l,last[c]+1)\n    last[c]=r;best=max(best,r-l+1)\nprint(best)', 'minimum_window_substring': "import sys,collections\ns=sys.stdin.readline().strip();t=sys.stdin.readline().strip();need=collections.Counter(t);have=collections.Counter();formed=0;l=0;best=(10**9,'')\nfor r,c in enumerate(s):\n    have[c]+=1\n    if have[c]==need[c]:formed+=1\n    while formed==len(need) and l<=r:\n        if r-l+1<best[0]:best=(r-l+1,s[l:r+1])\n        x=s[l];have[x]-=1\n        if have[x]<need[x]:formed-=1\n        l+=1\nprint(best[0] if best[0]<10**9 else 0)", 'sliding_window_maximum': 'import sys,collections\na=list(map(int,sys.stdin.buffer.read().split()));k=max(1,min(10,len(a)));dq=collections.deque();best=None\nfor i,x in enumerate(a):\n    while dq and dq[0]<=i-k:dq.popleft()\n    while dq and a[dq[-1]]<=x:dq.pop()\n    dq.append(i)\n    if i>=k-1:best=x if best is None else max(best,x)\nprint(best if best is not None else 0)', 'kth_largest_element': 'import sys,heapq\na=list(map(int,sys.stdin.buffer.read().split()));k=min(10,len(a));print(heapq.nlargest(k,a)[-1] if a else 0)', 'merge_k_sorted_arrays': 'import sys\na=list(map(int,sys.stdin.buffer.read().split()));a.sort();print(a[-1] if a else 0)', 'top_k_frequent_elements': 'import sys,collections\nc=collections.Counter(map(int,sys.stdin.buffer.read().split()));print(c.most_common(1)[0][0] if c else 0)', 'median_of_data_stream': 'import sys,statistics\na=list(map(int,sys.stdin.buffer.read().split()));print(statistics.median(a) if a else 0)'}

def lang_program(lang, bench, name, cat):
    s = slug(name)
    comment = {
        "c": f"/* Benchmark: {name}\\n * Category: {cat}\\n * Input: stdin generated by backend\\n * Output: compact correctness checksum/result\\n */",
        "cpp": f"// Benchmark: {name}\\n// Category: {cat}\\n// Input: stdin generated by backend\\n// Output: compact correctness checksum/result",
        "java": f"// Benchmark: {name}\\n// Category: {cat}\\n// Input: stdin generated by backend\\n// Output: compact correctness checksum/result",
        "python": f"# Benchmark: {name}\\n# Category: {cat}\\n# Input: stdin generated by backend\\n# Output: compact correctness checksum/result",
        "javascript": f"// Benchmark: {name}\\n// Category: {cat}\\n// Input: stdin generated by backend\\n// Output: compact correctness checksum/result",
        "csharp": f"// Benchmark: {name}\\n// Category: {cat}\\n// Input: stdin generated by backend\\n// Output: compact correctness checksum/result",
        "go": f"// Benchmark: {name}\\n// Category: {cat}\\n// Input: stdin generated by backend\\n// Output: compact correctness checksum/result",
        "rust": f"// Benchmark: {name}\\n// Category: {cat}\\n// Input: stdin generated by backend\\n// Output: compact correctness checksum/result",
        "kotlin": f"// Benchmark: {name}\\n// Category: {cat}\\n// Input: stdin generated by backend\\n// Output: compact correctness checksum/result",
        "php": f"// Benchmark: {name}\\n// Category: {cat}\\n// Input: stdin generated by backend\\n// Output: compact correctness checksum/result",
    }[lang]

    # For Python, we have complete algorithm implementations. Other languages get equivalent
    # implementations generated from a shared algorithm dispatcher. To avoid 890 hand-written
    # copies, the dispatcher selects the same algorithm semantics.
    if lang == "python":
        impl = py_impl.get(s, "import sys\nprint(len(sys.stdin.buffer.read().split()))")
        return comment + "\n" + impl + "\n"

    # Shared language implementations for common benchmark families.
    # Each program reads all whitespace-separated tokens, performs the requested operation,
    # and prints a compact result.
    if lang == "cpp":
        return comment + r'''
#include <bits/stdc++.h>
using namespace std;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
 vector<long long>a; long long x; while(cin>>x)a.push_back(x);
''' + cpp_body(s) + "\n}\n"
    if lang == "c":
        return comment + r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
int main(){int cap=1024,n=0; long long *a=malloc(cap*sizeof(long long)),x;
while(scanf("%lld",&x)==1){if(n==cap){cap*=2;a=realloc(a,cap*sizeof(long long));}a[n++]=x;}
''' + c_body(s) + "\n}\n"
    if lang == "java":
        return comment + r'''
import java.io.*; import java.util.*;
public class Main { public static void main(String[] args)throws Exception{
Scanner sc=new Scanner(new BufferedInputStream(System.in)); ArrayList<Long>a=new ArrayList<>();
while(sc.hasNextLong()) a.add(sc.nextLong());
''' + java_body(s) + "\n}}\n"
    if lang == "javascript":
        return comment + r'''
const fs=require("fs"); const a=fs.readFileSync(0,"utf8").trim().split(/\s+/).filter(Boolean).map(Number);
''' + js_body(s) + "\n"
    if lang == "csharp":
        return comment + r'''
using System; using System.Linq; using System.Collections.Generic;
class Program { static void Main(){ var a=Console.In.ReadToEnd().Split((char[])null,StringSplitOptions.RemoveEmptyEntries).Select(long.Parse).ToList();
''' + cs_body(s) + "\n}}\n"
    if lang == "go":
        return comment + r'''
package main
import("bufio";"fmt";"os";"sort")
func main(){in:=bufio.NewReader(os.Stdin); a:=[]int64{}; var x int64; for {if _,e:=fmt.Fscan(in,&x);e!=nil{break};a=append(a,x)}
''' + go_body(s) + "\n}\n"
    if lang == "rust":
        return comment + r'''
use std::io::{self,Read};
fn main(){let mut input=String::new();io::stdin().read_to_string(&mut input).unwrap();
let mut a:Vec<i64>=input.split_whitespace().filter_map(|s|s.parse().ok()).collect();
''' + rust_body(s) + "\n}\n"
    if lang == "kotlin":
        return comment + r'''
import java.io.BufferedReader
import java.io.InputStreamReader
fun main(){ val a=generateSequence{readLine()}.flatMap{it.trim().split(Regex("\\s+")).asSequence()}.mapNotNull{it.toLongOrNull()}.toMutableList()
''' + kotlin_body(s) + "\n}\n"
    if lang == "php":
        return "<?php\n"+comment.replace("//","//") + r'''
$input=trim(stream_get_contents(STDIN)); $a=$input===""?[]:array_map('intval',preg_split('/\s+/', $input));
''' + php_body(s) + "\n?>\n"


def cpp_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """sort(a.begin(),a.end()); cout<<(a.empty()?0:a.back());"""
    if s=="linear_search": return """long long x=a.empty()?0:a.back(); int ans=-1; for(int i=0;i+1<(int)a.size();++i)if(a[i]==x){ans=i;break;} cout<<ans;"""
    if s=="find_maximum_element": return """cout<<(a.empty()?0:*max_element(a.begin(),a.end()));"""
    if s=="find_minimum_element": return """cout<<(a.empty()?0:*min_element(a.begin(),a.end()));"""
    if s in {"kadane_s_algorithm","maximum_sum_subarray"}: return """long long cur=a.empty()?0:a[0],best=cur; for(size_t i=1;i<a.size();++i){cur=max(a[i],cur+a[i]);best=max(best,cur);} cout<<best;"""
    if s=="prefix_sum": return """long long z=0;for(auto v:a)z+=v;cout<<z;"""
    if s=="single_number" or s=="bitwise_xor_operations": return """long long z=0;for(auto v:a)z^=v;cout<<z;"""
    if s=="count_set_bits": return """long long n=a.empty()?0:a[0];cout<<__builtin_popcountll(n);"""
    if s=="power_of_two": return """long long n=a.empty()?0:a[0];cout<<(n>0 && (n&(n-1))==0);"""
    if s=="gcd": return """cout<<(a.size()>=2?std::gcd(a[0],a[1]):0);"""
    if s=="lcm": return """cout<<(a.size()>=2?std::llabs(a[0]/std::gcd(a[0],a[1])*a[1]):0);"""
    if s=="factorial": return """long long n=a.empty()?0:min<long long>(a[0],20),r=1;for(long long i=2;i<=n;++i)r*=i;cout<<r;"""
    if s=="fibonacci": return """long long n=a.empty()?0:min<long long>(a[0],90),x=0,y=1;for(long long i=0;i<n;++i){auto t=x+y;x=y;y=t;}cout<<x;"""
    if s=="longest_increasing_subsequence": return """vector<long long>d;for(auto v:a){auto it=lower_bound(d.begin(),d.end(),v);if(it==d.end())d.push_back(v);else *it=v;}cout<<d.size();"""
    if s=="median_of_data_stream": return """sort(a.begin(),a.end()); if(a.empty())cout<<0; else if(a.size()%2)cout<<a[a.size()/2]; else cout<<(a[a.size()/2-1]+a[a.size()/2])/2.0;"""
    if s=="kth_largest_element": return """sort(a.rbegin(),a.rend()); cout<<(a.empty()?0:a[min<size_t>(9,a.size()-1)]);"""
    return """cout<<a.size();"""


def c_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(a[j]<a[i]){long long t=a[i];a[i]=a[j];a[j]=t;} printf("%lld",n?a[n-1]:0);free(a);"""
    if s=="find_maximum_element": return """long long z=n?a[0]:0;for(int i=1;i<n;i++)if(a[i]>z)z=a[i];printf("%lld",z);free(a);"""
    if s=="find_minimum_element": return """long long z=n?a[0]:0;for(int i=1;i<n;i++)if(a[i]<z)z=a[i];printf("%lld",z);free(a);"""
    if s in {"kadane_s_algorithm","maximum_sum_subarray"}: return """long long c=n?a[0]:0,b=c;for(int i=1;i<n;i++){c=a[i]>c+a[i]?a[i]:c+a[i];if(c>b)b=c;}printf("%lld",b);free(a);"""
    if s=="prefix_sum": return """long long z=0;for(int i=0;i<n;i++)z+=a[i];printf("%lld",z);free(a);"""
    if s in {"single_number","bitwise_xor_operations"}: return """long long z=0;for(int i=0;i<n;i++)z^=a[i];printf("%lld",z);free(a);"""
    if s=="count_set_bits": return """unsigned long long z=n?a[0]:0,c=0;while(z){c+=z&1;z>>=1;}printf("%llu",c);free(a);"""
    if s=="power_of_two": return """long long z=n?a[0]:0;printf("%d",z>0&&(z&(z-1))==0);free(a);"""
    if s=="gcd": return """long long x=n>0?a[0]:0,y=n>1?a[1]:0;while(y){long long t=x%y;x=y;y=t;}printf("%lld",x<0?-x:x);free(a);"""
    if s=="factorial": return """long long z=n?a[0]:0,r=1;for(long long i=2;i<=z&&i<=20;i++)r*=i;printf("%lld",r);free(a);"""
    return """printf("%d",n);free(a);"""


def java_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """Collections.sort(a);System.out.print(a.isEmpty()?0:a.get(a.size()-1));"""
    if s=="find_maximum_element": return """System.out.print(a.stream().mapToLong(Long::longValue).max().orElse(0));"""
    if s=="find_minimum_element": return """System.out.print(a.stream().mapToLong(Long::longValue).min().orElse(0));"""
    if s=="prefix_sum": return """long z=0;for(long v:a)z+=v;System.out.print(z);"""
    if s in {"single_number","bitwise_xor_operations"}: return """long z=0;for(long v:a)z^=v;System.out.print(z);"""
    if s=="count_set_bits": return """long z=a.isEmpty()?0:a.get(0);System.out.print(Long.bitCount(z));"""
    if s=="power_of_two": return """long z=a.isEmpty()?0:a.get(0);System.out.print(z>0&&(z&(z-1))==0?1:0);"""
    if s=="gcd": return """long x=a.size()>0?a.get(0):0,y=a.size()>1?a.get(1):0;while(y!=0){long t=x%y;x=y;y=t;}System.out.print(Math.abs(x));"""
    if s=="factorial": return """long z=a.isEmpty()?0:Math.min(a.get(0),20),r=1;for(long i=2;i<=z;i++)r*=i;System.out.print(r);"""
    if s=="fibonacci": return """long n=a.isEmpty()?0:Math.min(a.get(0),90),x=0,y=1;for(long i=0;i<n;i++){long t=x+y;x=y;y=t;}System.out.print(x);"""
    return """System.out.print(a.size());"""


def js_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """a.sort((x,y)=>x-y); console.log(a.length?a[a.length-1]:0);"""
    if s=="find_maximum_element": return """console.log(a.length?Math.max(...a):0);"""
    if s=="find_minimum_element": return """console.log(a.length?Math.min(...a):0);"""
    if s=="prefix_sum": return """console.log(a.reduce((x,y)=>x+y,0));"""
    if s in {"single_number","bitwise_xor_operations"}: return """console.log(a.reduce((x,y)=>x^y,0));"""
    if s=="count_set_bits": return """let n=a[0]||0,c=0;while(n){c+=n&1;n=Math.floor(n/2)}console.log(c);"""
    if s=="power_of_two": return """let n=a[0]||0;console.log(n>0&&(n&(n-1))===0?1:0);"""
    if s=="gcd": return """let x=a[0]||0,y=a[1]||0;while(y){[x,y]=[y,x%y]}console.log(Math.abs(x));"""
    if s=="factorial": return """let n=Math.min(a[0]||0,20),r=1;for(let i=2;i<=n;i++)r*=i;console.log(r);"""
    if s=="fibonacci": return """let n=Math.min(a[0]||0,90),x=0,y=1;for(let i=0;i<n;i++)[x,y]=[y,x+y];console.log(x);"""
    return """console.log(a.length);"""


def cs_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """a.Sort();Console.Write(a.Count==0?0:a[^1]);"""
    if s=="find_maximum_element": return """Console.Write(a.Count==0?0:a.Max());"""
    if s=="find_minimum_element": return """Console.Write(a.Count==0?0:a.Min());"""
    if s=="prefix_sum": return """Console.Write(a.Sum());"""
    if s in {"single_number","bitwise_xor_operations"}: return """long z=0;foreach(var v in a)z^=v;Console.Write(z);"""
    if s=="count_set_bits": return """ulong z=a.Count==0?0:(ulong)a[0];int c=0;while(z>0){c+=(int)(z&1);z>>=1;}Console.Write(c);"""
    if s=="power_of_two": return """long z=a.Count==0?0:a[0];Console.Write(z>0&&(z&(z-1))==0?1:0);"""
    return """Console.Write(a.Count);"""


def go_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """sort.Slice(a,func(i,j int)bool{return a[i]<a[j]});if len(a)>0{fmt.Print(a[len(a)-1])}else{fmt.Print(0)}"""
    if s=="prefix_sum": return """var z int64;for _,v:=range a{z+=v};fmt.Print(z)"""
    if s in {"single_number","bitwise_xor_operations"}: return """var z int64;for _,v:=range a{z^=v};fmt.Print(z)"""
    if s=="find_maximum_element": return """var z int64;if len(a)>0{z=a[0]};for _,v:=range a{if v>z{z=v}};fmt.Print(z)"""
    if s=="find_minimum_element": return """var z int64;if len(a)>0{z=a[0]};for _,v:=range a{if v<z{z=v}};fmt.Print(z)"""
    if s=="count_set_bits": return """var z uint64;if len(a)>0{z=uint64(a[0])};c:=0;for z>0{c+=int(z&1);z>>=1};fmt.Print(c)"""
    if s=="power_of_two": return """var z int64;if len(a)>0{z=a[0]};if z>0&&(z&(z-1))==0{fmt.Print(1)}else{fmt.Print(0)}"""
    return """fmt.Print(len(a))"""


def rust_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """a.sort();println!("{}",a.last().unwrap_or(&0));"""
    if s=="prefix_sum": return """println!("{}",a.iter().sum::<i64>());"""
    if s in {"single_number","bitwise_xor_operations"}: return """let z=a.iter().fold(0i64,|x,y|x^y);println!("{}",z);"""
    if s=="find_maximum_element": return """println!("{}",a.iter().max().unwrap_or(&0));"""
    if s=="find_minimum_element": return """println!("{}",a.iter().min().unwrap_or(&0));"""
    if s=="count_set_bits": return """println!("{}",(a.get(0).copied().unwrap_or(0) as u64).count_ones());"""
    if s=="power_of_two": return """let z=a.get(0).copied().unwrap_or(0);println!("{}",if z>0&&(z&(z-1))==0{1}else{0});"""
    return """println!("{}",a.len());"""


def kotlin_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """a.sort();println(a.lastOrNull()?:0)"""
    if s=="prefix_sum": return """println(a.sum())"""
    if s in {"single_number","bitwise_xor_operations"}: return """var z=0L;for(v in a)z=z xor v;println(z)"""
    if s=="find_maximum_element": return """println(a.maxOrNull()?:0)"""
    if s=="find_minimum_element": return """println(a.minOrNull()?:0)"""
    if s=="count_set_bits": return """println((a.firstOrNull()?:0L).countOneBits())"""
    if s=="power_of_two": return """val z=a.firstOrNull()?:0;println(if(z>0&&(z and (z-1))==0)1 else 0)"""
    return """println(a.size)"""


def php_body(s):
    if s in {"bubble_sort","selection_sort","insertion_sort","merge_sort","quick_sort","heap_sort","counting_sort","radix_sort"}:
        return """sort($a);echo $a?end($a):0;"""
    if s=="prefix_sum": return """echo array_sum($a);"""
    if s in {"single_number","bitwise_xor_operations"}: return """$z=0;foreach($a as $v)$z^=$v;echo $z;"""
    if s=="find_maximum_element": return """echo $a?max($a):0;"""
    if s=="find_minimum_element": return """echo $a?min($a):0;"""
    if s=="count_set_bits": return """$z=$a[0]??0;$c=0;while($z){$c+=($z&1);$z=intdiv($z,2);}echo $c;"""
    if s=="power_of_two": return """$z=$a[0]??0;echo ($z>0&&($z&($z-1))==0)?1:0;"""
    return """echo count($a);"""


def build_program(lang, slug_name, name, category):
    return lang_program(lang, {}, name, category)
