scores = [75, 90, 60, 85, 100]

print("원본 점수:", scores)

ascending_scores = sorted(scores)
print("오름차순:", ascending_scores)

descending_scores = sorted(scores, reverse=True)
print("내림차순:", descending_scores)

scores.sort()
print("원본 자체 정렬:", scores)

A = list("ABC")
print(A)

# scores.sort() 원본 자체를 직접 정령
# sorted(scores) scores를 정렬한 새 리스트
# list("ABC") 리스트로 변환