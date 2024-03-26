a = int(input())
result = 0

if a > 0:
    for i in range(1,a+1):
        result += i
else:
    for i in range(a,1):
        result += i

print(result)