def fib(num):
    if num<=1 :
        return num
    else:
        return fib(num-1)+fib(num-2)

# 피보나치 외워둘 것!

N=int(input())
print(fib(N))