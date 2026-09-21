import sys

a = [
    int(x)
    for x in sys.stdin.buffer.read().split()
]

n = len(a)

for i in range(1, n):
    key = a[i]
    j = i - 1

    while j >= 0 and a[j] > key:
        a[j + 1] = a[j]
        j -= 1

    a[j + 1] = key

print(
    a[-1] if a else 0,
    end=""
)
