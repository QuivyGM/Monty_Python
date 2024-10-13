# input

N = int(input())    # 받는 좌표 갯수 입력 받기
x=[]                # x 좌표
y=[]                # y 좌표

for i in range(N):        # i 가 N에 있는 동안 좌표 입력 받기
    xi, yi = map(int, input().split())    # 좌표를 입력 받은 뒤 split해서 xi, yi 에 저장
    x.append(xi)
    y.append(yi)

# Sorting
for i in range(N):
    for j in range(i, N):
        if(x[i]==x[j]):    # x 좌표 같으면 y 좌표 빅교해서 더 작으면 바꾸기
            if(y[i] > y[j]):
                x[i], x[j], y[i], y[j] = x[j], x[i], y[j], y[i]
        else:                # x 좌표가 더 큰 작은 것이랑 바꾸기
            if(x[i] > x[j]):
                x[i], x[j], y[i], y[j] = x[j], x[i], y[j], y[i]

# output

for i in range(N):        # 출력
    print(x[i], y[i])
