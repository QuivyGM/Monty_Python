# input

N = int(input())
x=[]
y=[]

for i in range(N):
    xi, yi = map(int, input().split())
    x.append(xi)
    y.append(yi)

# Sorting
for i in range(N):
    for j in range(i, N):
        if(x[i]==x[j]):
            if(y[i] > y[j]):
                x[i], x[j], y[i], y[j] = x[j], x[i], y[j], y[i]
        else:
            if(x[i] > x[j]):
                x[i], x[j], y[i], y[j] = x[j], x[i], y[j], y[i]

# output

for i in range(N):
    print(x[i], y[i])