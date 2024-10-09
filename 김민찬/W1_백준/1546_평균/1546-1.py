clss = int(input())
score=[]
top=0
score.extend(map(int, input().split()))
for i in range(clss):
    #score.append(int(input()))
    if(top<score[i]):
        top=score[i]
# 입력을 받을때 입력 타입은 기본 string 임
avg=0
for i in range(clss):
    score[i] = score[i]*100/top
    #print(score[i])
    avg+=(score[i]/clss)
print(avg)


