def hanoi(n, source, auxiliary, target):
    if n == 1:
        print(f"{source} > {target}")
        return
    hanoi(n-1, source, target, auxiliary)
    print(f"{source} > {target}")
    hanoi(n-1, auxiliary, source, target)

n = int(input())
hanoi(n, 'A', 'B', 'C')