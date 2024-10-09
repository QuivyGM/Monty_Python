def fib(num):
    if num<=1 :
        return num
    a, b = 0, 1
    for _ in range(2, num+1):
        a, b = b, a+b
    return b

# 피보나치 함수는 중복 계산이 많아서 느림 -> 기억하면서 작동할수 있는 방법으로 코딩!!!

N=int(input())
print(fib(N))