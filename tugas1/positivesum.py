# Calculate sum
def positive_sum(N, sequence):
    total_sum = 0
    for num in sequence:
        if num > 0:
            total_sum += num
            
    return total_sum

N = int(input())
sequence = [int(input()) for _ in range(N)]

print(positive_sum(N, sequence))