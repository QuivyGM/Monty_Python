def count_trailing_zeros(n):
    count = 0
    while n >= 5:
        n //= 5
        count += n
    return count

# 사용자로부터 N 입력받기
N = int(input("N을 입력하세요: "))
print(count_trailing_zeros(N))
