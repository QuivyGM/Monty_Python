N = int(input())
coordinates = []

for _ in range(N):
    xi, yi = map(int, input().split())
    # maps으로 입력을 int으로 변환 한다음에 xi, yi으로 split 이력
    coordinates.append((xi, yi))
    # coordinates에 묶어서 좌표 append

coordinates = sorted(coordinates)
# coordinates을 정렬 (sorted는 자동 정렬 함수)

for xi, yi in coordinates:
    print(xi, yi)
#출력