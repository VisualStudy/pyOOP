# pyOOP

# Python `print()` 함수의 `end` 매개변수 이해하기

## 1. `print()` 함수란?

Python에서 `print()` 함수는 화면에 값을 출력할 때 사용하는 함수이다.

```python
print("Hello")
```

실행 결과:

```text
Hello
```

보통 `print()`를 여러 번 사용하면 출력 결과가 줄마다 따로 나타난다.

```python
print("Hello")
print("Python")
print("World")
```

실행 결과:

```text
Hello
Python
World
```

이렇게 되는 이유는 `print()` 함수가 기본적으로 출력 끝에 줄바꿈 문자인 `\n`을 붙이기 때문이다.

---

## 2. `end` 매개변수란?

`end`는 `print()` 함수가 출력한 뒤 마지막에 무엇을 붙일지 정하는 매개변수이다.

기본값은 줄바꿈 문자 `\n`이다.

```python
print("Hello", end="\n")
```

위 코드는 기본 `print("Hello")`와 같은 의미이다.

즉, 다음 두 코드는 같은 결과를 만든다.

```python
print("Hello")
```

```python
print("Hello", end="\n")
```

실행 결과:

```text
Hello
```

화면에는 줄바꿈이 보이지 않지만, 실제로는 `Hello` 뒤에 줄바꿈이 들어간다.

---

## 3. `end`의 핵심 역할

`end`는 현재 `print()`가 출력된 뒤에 붙는 값을 바꾼다.

예를 들어:

```python
print("Hello", end=" ")
print("Python")
```

실행 결과:

```text
Hello Python
```

첫 번째 `print()`에서 `end=" "`를 사용했기 때문에 `"Hello"` 뒤에 줄바꿈이 아니라 공백이 붙는다.

그래서 다음 `print("Python")`의 출력이 같은 줄에 이어서 나타난다.

---

## 4. `end`는 다음 `print()` 결과에 영향을 준다

`end`는 자기 자신이 속한 `print()`의 출력 끝을 바꾸는 기능이다.

하지만 출력 위치가 바뀌기 때문에, 결과적으로 다음 `print()`가 어디에 출력되는지에 영향을 준다.

```python
print("A", end="")
print("B")
```

실행 결과:

```text
AB
```

첫 번째 `print()`는 `"A"`를 출력한 뒤 줄바꿈을 하지 않는다.

따라서 다음 `print("B")`는 같은 줄에서 이어서 출력된다.

즉, 첫 번째 `print()`의 `end` 설정이 다음 `print()`의 출력 위치에 영향을 준 것이다.

---

## 5. `end=""`의 의미

`end=""`는 출력 뒤에 아무것도 붙이지 않겠다는 뜻이다.

```python
print("A", end="")
print("B", end="")
print("C")
```

실행 결과:

```text
ABC
```

각 출력 뒤에 줄바꿈이 없으므로 모두 같은 줄에 붙어서 출력된다.

---

## 6. `end=" "`의 의미

`end=" "`는 출력 뒤에 공백 한 칸을 붙이겠다는 뜻이다.

```python
print("A", end=" ")
print("B", end=" ")
print("C")
```

실행 결과:

```text
A B C
```

각 출력 뒤에 공백이 들어가기 때문에 한 줄에 띄어쓰기되어 출력된다.

---

## 7. `end="-"`의 의미

`end`에는 줄바꿈이나 공백뿐 아니라 원하는 문자열을 넣을 수 있다.

```python
print("2026", end="-")
print("05", end="-")
print("23")
```

실행 결과:

```text
2026-05-23
```

첫 번째 `print()` 뒤에는 `-`가 붙고, 두 번째 `print()` 뒤에도 `-`가 붙는다.

따라서 날짜 형식처럼 출력할 수 있다.

---

## 8. 기본 `print()`와 `end` 지정 비교

### 기본 출력

```python
print("A")
print("B")
print("C")
```

실행 결과:

```text
A
B
C
```

각 `print()` 뒤에 자동으로 줄바꿈이 들어간다.

---

### `end=""` 사용

```python
print("A", end="")
print("B", end="")
print("C")
```

실행 결과:

```text
ABC
```

줄바꿈이 없어져서 모두 붙어 출력된다.

---

### `end=" "` 사용

```python
print("A", end=" ")
print("B", end=" ")
print("C")
```

실행 결과:

```text
A B C
```

줄바꿈 대신 공백이 들어가서 한 줄에 출력된다.

---

## 9. `end`는 영구 설정이 아니다

중요한 점은 `end`가 영구적으로 바뀌는 것은 아니라는 것이다.

`end`는 해당 `print()` 함수에만 적용된다.

```python
print("A", end="")
print("B")
print("C")
```

실행 결과:

```text
AB
C
```

첫 번째 `print("A", end="")`는 줄바꿈을 하지 않는다.

그래서 두 번째 `print("B")`는 같은 줄에 이어서 출력된다.

하지만 두 번째 `print("B")`는 `end`를 따로 지정하지 않았으므로 기본값인 `\n`이 적용된다.  
따라서 `"B"` 출력 후에는 줄바꿈이 일어나고, `"C"`는 다음 줄에 출력된다.

즉:

```text
print("A", end="") → A 출력 후 줄바꿈 없음
print("B")         → B 출력 후 줄바꿈 있음
print("C")         → 다음 줄에 C 출력
```

---

## 10. “다음 print문에 무조건 영향을 미친다”의 정확한 의미

`end`는 다음 `print()`의 설정을 바꾸는 것은 아니다.

하지만 현재 출력 뒤에 줄바꿈을 할지 말지를 결정하기 때문에, 다음 `print()`가 출력될 위치에는 영향을 준다.

예를 들어:

```python
print("A", end="")
print("B")
```

실행 결과:

```text
AB
```

이 코드에서 `end=""`는 두 번째 `print("B")`의 옵션을 바꾼 것이 아니다.

두 번째 `print()`는 여전히 기본값 `end="\n"`을 가진다.

하지만 첫 번째 `print()`가 줄바꿈을 하지 않았기 때문에, 두 번째 출력이 같은 줄에 이어서 나온다.

따라서 다음처럼 이해하면 된다.

```text
end는 다음 print문의 기능을 바꾸는 것은 아니다.
하지만 다음 print문이 출력될 위치에는 영향을 준다.
```

---

## 11. 예제로 이해하기

### 예제 1

```python
print("안녕", end="")
print("하세요")
```

실행 결과:

```text
안녕하세요
```

첫 번째 출력 뒤에 아무것도 붙지 않으므로 두 번째 출력이 바로 이어진다.

---

### 예제 2

```python
print("안녕", end=" ")
print("하세요")
```

실행 결과:

```text
안녕 하세요
```

첫 번째 출력 뒤에 공백이 붙기 때문에 두 번째 출력이 한 칸 띄어져 이어진다.

---

### 예제 3

```python
print("안녕", end="\n")
print("하세요")
```

실행 결과:

```text
안녕
하세요
```

`end="\n"`은 기본값과 같으므로 줄바꿈이 일어난다.

---

### 예제 4

```python
print("A", end="")
print("B", end="")
print("C", end="")
print("D")
```

실행 결과:

```text
ABCD
```

앞의 세 `print()`가 모두 줄바꿈을 하지 않기 때문에 마지막까지 한 줄에 출력된다.

---

## 12. 반복문에서 `end` 사용하기

`end`는 반복문에서 한 줄 출력할 때 자주 사용된다.

```python
for i in range(1, 6):
    print(i, end=" ")
```

실행 결과:

```text
1 2 3 4 5 
```

기본 `print()`는 매번 줄바꿈을 하므로 다음처럼 출력된다.

```python
for i in range(1, 6):
    print(i)
```

실행 결과:

```text
1
2
3
4
5
```

하지만 `end=" "`를 사용하면 줄바꿈 대신 공백을 붙이므로 한 줄에 출력된다.

---

## 13. `end`와 줄바꿈 문자 `\n`

기본적으로 `print()`의 `end` 값은 `"\n"`이다.

```python
print("A")
```

는 사실상 다음과 같다.

```python
print("A", end="\n")
```

`\n`은 줄바꿈 문자이다.

따라서 다음 코드는:

```python
print("A", end="\n")
print("B")
```

다음과 같이 출력된다.

```text
A
B
```

반대로 `end=""`를 사용하면 줄바꿈 문자가 사라진다.

```python
print("A", end="")
print("B")
```

실행 결과:

```text
AB
```

---

## 14. 한눈에 정리

| 코드 | 의미 | 다음 출력 위치 |
|---|---|---|
| `print("A")` | 기본 출력, 끝에 줄바꿈 | 다음 줄 |
| `print("A", end="\n")` | 기본값과 같음 | 다음 줄 |
| `print("A", end="")` | 출력 뒤에 아무것도 붙이지 않음 | 같은 줄 바로 뒤 |
| `print("A", end=" ")` | 출력 뒤에 공백 추가 | 같은 줄 한 칸 뒤 |
| `print("A", end="-")` | 출력 뒤에 `-` 추가 | 같은 줄 `-` 뒤 |

---

## 15. 핵심 정리

`print()`의 `end` 매개변수는 출력이 끝난 뒤에 무엇을 붙일지 정한다.

기본값은 줄바꿈 문자 `\n`이다.

```python
print("A")
```

는 다음과 같다.

```python
print("A", end="\n")
```

`end`를 바꾸면 다음 `print()`가 출력될 위치가 달라진다.

```python
print("A", end="")
print("B")
```

실행 결과:

```text
AB
```

즉, `end=""`를 사용하면 줄바꿈을 하지 않기 때문에 다음 `print()`가 같은 줄에 이어서 출력된다.

하지만 `end`가 다음 `print()`의 옵션 자체를 바꾸는 것은 아니다.  
다음 `print()`는 여전히 자기 자신의 `end` 값을 가진다.

정리하면 다음과 같다.

```text
end는 현재 print문의 출력 끝을 바꾼다.
그 결과 다음 print문이 출력될 위치에 영향을 준다.
end는 다음 print문의 설정을 직접 바꾸는 것은 아니다.
```

# Python 조건문: `if`만 여러 번 사용하는 경우와 `if`-`elif`를 사용하는 경우의 차이

## 1. 개요

Python에서 조건문을 만들 때는 `if`, `elif`, `else`를 사용한다.

그런데 조건을 여러 개 검사할 때 다음 두 방식은 결과가 달라질 수 있다.

```python
if 조건1:
    실행문1

if 조건2:
    실행문2

if 조건3:
    실행문3
```

```python
if 조건1:
    실행문1
elif 조건2:
    실행문2
elif 조건3:
    실행문3
```

겉보기에는 비슷해 보이지만, 두 방식은 중요한 차이가 있다.

---

## 2. 핵심 차이

가장 중요한 차이는 다음과 같다.

```text
if만 여러 번 사용
→ 각각의 조건을 모두 따로 검사한다.

if-elif 사용
→ 위에서부터 조건을 검사하다가 하나라도 참이면, 나머지는 검사하지 않는다.
```

즉, `if` 여러 개는 **독립적인 조건문**이고, `if-elif`는 **하나의 연결된 조건문**이다.

---

## 3. `if`만 여러 번 사용하는 경우

다음과 같이 `if`를 여러 번 쓰면 각각의 조건문은 서로 독립적으로 실행된다.

```python
score = 85

if score >= 60:
    print("합격")

if score >= 80:
    print("우수")

if score >= 90:
    print("최우수")
```

실행 결과:

```text
합격
우수
```

`score`가 85이므로 첫 번째 조건과 두 번째 조건이 모두 참이다.

따라서 두 문장이 모두 출력된다.

```text
score >= 60 → 참
score >= 80 → 참
score >= 90 → 거짓
```

즉, `if`를 여러 번 사용하면 참인 조건은 모두 실행된다.

---

## 4. `if`와 `elif`를 사용하는 경우

이번에는 `if`와 `elif`를 사용해 보자.

```python
score = 85

if score >= 60:
    print("합격")
elif score >= 80:
    print("우수")
elif score >= 90:
    print("최우수")
```

실행 결과:

```text
합격
```

이 경우 `score >= 60`이 참이므로 `"합격"`만 출력된다.

그 아래의 `elif` 조건들은 검사하지 않는다.

```text
score >= 60 → 참
score >= 80 → 검사하지 않음
score >= 90 → 검사하지 않음
```

따라서 `if-elif` 구조에서는 가장 먼저 참이 된 조건 하나만 실행된다.

---

## 5. `if-elif`에서 조건 순서가 중요한 이유

위 예제에서는 사실 의도한 결과가 이상할 수 있다.

점수가 85점이면 `"우수"`가 나와야 할 것 같은데, 실제로는 `"합격"`만 출력된다.

그 이유는 조건 순서 때문이다.

```python
score = 85

if score >= 60:
    print("합격")
elif score >= 80:
    print("우수")
elif score >= 90:
    print("최우수")
```

`85`는 이미 `60` 이상이므로 첫 번째 조건에서 걸려 버린다.

따라서 더 구체적인 조건인 `score >= 80`까지 가지 않는다.

이럴 때는 큰 조건부터 검사해야 한다.

```python
score = 85

if score >= 90:
    print("최우수")
elif score >= 80:
    print("우수")
elif score >= 60:
    print("합격")
else:
    print("불합격")
```

실행 결과:

```text
우수
```

조건을 위에서부터 검사하므로, 범위가 겹치는 조건에서는 더 구체적이거나 더 높은 기준을 먼저 써야 한다.

---

## 6. `if` 여러 개와 `if-elif`의 비교

## 6.1 예제 1: 여러 조건이 동시에 참일 수 있는 경우

```python
temperature = 32

if temperature >= 30:
    print("덥다")

if temperature >= 20:
    print("따뜻하다")

if temperature >= 10:
    print("선선하다")
```

실행 결과:

```text
덥다
따뜻하다
선선하다
```

세 조건이 모두 참이므로 모두 실행된다.

반면 `elif`를 사용하면 다음과 같다.

```python
temperature = 32

if temperature >= 30:
    print("덥다")
elif temperature >= 20:
    print("따뜻하다")
elif temperature >= 10:
    print("선선하다")
```

실행 결과:

```text
덥다
```

첫 번째 조건이 참이므로 나머지 조건은 검사하지 않는다.

---

## 6.2 예제 2: 하나의 결과만 골라야 하는 경우

성적 등급처럼 하나의 결과만 나와야 하는 경우에는 `if-elif-else`가 적절하다.

```python
score = 92

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(grade)
```

실행 결과:

```text
A
```

성적 등급은 동시에 A이면서 B일 수 없다.  
따라서 이런 경우에는 `if-elif-else`를 사용하는 것이 좋다.

---

## 6.3 예제 3: 여러 조건을 모두 확인해야 하는 경우

반대로 여러 조건을 각각 확인해야 하는 경우에는 `if`를 여러 번 쓰는 것이 적절하다.

```python
user = "admin"
is_logged_in = True
has_permission = True

if is_logged_in:
    print("로그인 상태입니다.")

if user == "admin":
    print("관리자 계정입니다.")

if has_permission:
    print("권한이 있습니다.")
```

실행 결과:

```text
로그인 상태입니다.
관리자 계정입니다.
권한이 있습니다.
```

이 경우 세 조건은 서로 배타적인 관계가 아니다.  
즉, 동시에 여러 조건이 참일 수 있다.

따라서 `if`를 각각 따로 쓰는 것이 자연스럽다.

---

## 7. `else`와 함께 사용할 때의 차이

`else`는 바로 위의 `if` 또는 `if-elif` 묶음과 연결된다.

다음 코드를 보자.

```python
x = 10

if x > 0:
    print("양수")

if x % 2 == 0:
    print("짝수")
else:
    print("홀수")
```

실행 결과:

```text
양수
짝수
```

여기서 `else`는 첫 번째 `if x > 0`과 연결된 것이 아니라, 바로 위의 `if x % 2 == 0`과 연결되어 있다.

즉, 구조는 다음과 같다.

```text
if x > 0:
    print("양수")

if x % 2 == 0:
    print("짝수")
else:
    print("홀수")
```

첫 번째 `if`와 두 번째 `if-else`는 서로 다른 조건문이다.

---

## 8. 잘못 사용하기 쉬운 예

다음 코드는 초보자가 자주 헷갈리는 예이다.

```python
score = 95

if score >= 90:
    print("A")

if score >= 80:
    print("B")

if score >= 70:
    print("C")
```

실행 결과:

```text
A
B
C
```

95점은 90 이상이면서 80 이상이고, 70 이상이기도 하다.  
그래서 세 조건이 모두 참이 되어 모두 출력된다.

하지만 성적 등급은 하나만 나와야 하므로 이 경우에는 `elif`를 사용해야 한다.

```python
score = 95

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
```

실행 결과:

```text
A
```

---

## 9. 언제 `if`를 여러 번 써야 할까?

다음과 같은 경우에는 `if`를 여러 번 사용하는 것이 좋다.

```text
여러 조건이 동시에 참일 수 있을 때
각 조건마다 독립적으로 실행해야 할 때
여러 상태를 동시에 검사해야 할 때
```

예시:

```python
password = "abc12345"

if len(password) >= 8:
    print("길이 조건 통과")

if any(ch.isdigit() for ch in password):
    print("숫자 포함")

if any(ch.isalpha() for ch in password):
    print("문자 포함")
```

실행 결과:

```text
길이 조건 통과
숫자 포함
문자 포함
```

비밀번호 검사는 여러 조건을 동시에 만족할 수 있다.  
따라서 각각의 조건을 따로 검사하는 것이 자연스럽다.

---

## 10. 언제 `if-elif-else`를 써야 할까?

다음과 같은 경우에는 `if-elif-else`를 사용하는 것이 좋다.

```text
여러 조건 중 하나만 선택해야 할 때
결과가 서로 배타적일 때
위에서부터 조건을 검사하다가 하나만 실행해야 할 때
```

예시:

```python
age = 17

if age >= 20:
    print("성인")
elif age >= 14:
    print("청소년")
elif age >= 8:
    print("어린이")
else:
    print("유아")
```

실행 결과:

```text
청소년
```

나이는 동시에 성인이면서 청소년일 수 없다.  
따라서 이런 경우에는 `if-elif-else` 구조가 적절하다.

---

## 11. 한눈에 비교하기

| 구분 | `if` 여러 번 | `if-elif` |
|---|---|---|
| 조건 관계 | 서로 독립적 | 하나의 조건 묶음 |
| 조건 검사 방식 | 모든 `if`를 각각 검사 | 참인 조건을 만나면 아래는 검사하지 않음 |
| 실행 개수 | 여러 개 실행될 수 있음 | 하나만 실행됨 |
| 사용 상황 | 여러 조건을 모두 확인해야 할 때 | 여러 조건 중 하나만 선택해야 할 때 |
| 예시 | 권한 검사, 비밀번호 조건 검사 | 성적 등급, 나이 구분, 메뉴 선택 |

---

## 12. 핵심 정리

`if`만 여러 번 쓰면 각 조건이 독립적으로 검사된다.

```python
if 조건1:
    실행문1

if 조건2:
    실행문2

if 조건3:
    실행문3
```

이 경우 조건1, 조건2, 조건3이 모두 참이면 실행문도 모두 실행된다.

반면 `if-elif`는 하나의 조건 묶음이다.

```python
if 조건1:
    실행문1
elif 조건2:
    실행문2
elif 조건3:
    실행문3
```

이 경우 위에서부터 검사하다가 참인 조건을 하나 만나면 그 부분만 실행하고 나머지는 건너뛴다.

따라서 다음처럼 기억하면 된다.

```text
if 여러 개
→ 참인 조건을 모두 실행한다.

if-elif
→ 참인 조건 중 가장 먼저 만난 하나만 실행한다.
```

즉, 여러 조건을 모두 확인해야 하면 `if`를 여러 번 쓰고, 여러 경우 중 하나만 골라야 하면 `if-elif-else`를 사용한다.

# Python `for i in range()`에서 `range()` 함수의 매개변수 정리

## 1. `range()` 함수란?

Python에서 `range()` 함수는 일정한 규칙을 가진 숫자들을 만들어 주는 함수이다.

주로 `for` 반복문과 함께 사용한다.

```python
for i in range(5):
    print(i)
```

실행 결과:

```text
0
1
2
3
4
```

여기서 `range(5)`는 `0`부터 `4`까지의 숫자를 만든다.

주의할 점은 `5`까지 포함하는 것이 아니라, `5` 바로 전까지만 포함한다는 것이다.

---

## 2. `range()`의 기본 형태

`range()`는 매개변수를 1개, 2개, 3개까지 받을 수 있다.

```python
range(stop)
range(start, stop)
range(start, stop, step)
```

| 형태 | 의미 |
|---|---|
| `range(stop)` | `0`부터 `stop - 1`까지 |
| `range(start, stop)` | `start`부터 `stop - 1`까지 |
| `range(start, stop, step)` | `start`부터 `stop` 직전까지 `step`만큼 증가 또는 감소 |

---

## 3. `range(stop)`

매개변수가 1개일 때는 그 값이 `stop`이 된다.

```python
range(5)
```

의미:

```text
0부터 5 전까지
```

즉, 실제로 만들어지는 숫자는 다음과 같다.

```text
0, 1, 2, 3, 4
```

예제:

```python
for i in range(5):
    print(i)
```

실행 결과:

```text
0
1
2
3
4
```

핵심은 다음과 같다.

```text
range(5)는 1부터 5까지가 아니라 0부터 4까지이다.
```

---

## 4. 왜 `range(5)`는 5를 포함하지 않을까?

Python의 `range()`는 끝값을 포함하지 않는다.

```python
range(5)
```

은 다음과 같다.

```text
0 이상 5 미만
```

수학적으로 표현하면 다음과 같다.

```text
0 <= i < 5
```

그래서 `5`는 포함되지 않는다.

이 방식은 반복 횟수를 세기 편하다.

```python
for i in range(5):
    print("Hello")
```

실행 결과:

```text
Hello
Hello
Hello
Hello
Hello
```

`0, 1, 2, 3, 4` 총 5개의 숫자가 만들어지므로 반복도 정확히 5번 실행된다.

---

## 5. `range(start, stop)`

매개변수가 2개일 때는 첫 번째 값이 `start`, 두 번째 값이 `stop`이다.

```python
range(2, 6)
```

의미:

```text
2부터 6 전까지
```

즉, 실제로 만들어지는 숫자는 다음과 같다.

```text
2, 3, 4, 5
```

예제:

```python
for i in range(2, 6):
    print(i)
```

실행 결과:

```text
2
3
4
5
```

정리하면:

```text
range(2, 6) → 2, 3, 4, 5
```

끝값 `6`은 포함되지 않는다.

---

## 6. `range(start, stop, step)`

매개변수가 3개일 때는 다음과 같다.

```python
range(start, stop, step)
```

각 매개변수의 의미는 다음과 같다.

| 매개변수 | 의미 |
|---|---|
| `start` | 시작값 |
| `stop` | 끝값 직전 |
| `step` | 증가 또는 감소 간격 |

예제:

```python
for i in range(1, 10, 2):
    print(i)
```

실행 결과:

```text
1
3
5
7
9
```

이 코드는 다음 뜻이다.

```text
1부터 시작
10 전까지 반복
2씩 증가
```

즉:

```text
1, 3, 5, 7, 9
```

가 만들어진다.

---

## 7. `step`의 역할

`step`은 숫자가 얼마나씩 변할지를 정한다.

```python
range(0, 10, 2)
```

의미:

```text
0부터 10 전까지 2씩 증가
```

결과:

```text
0, 2, 4, 6, 8
```

예제:

```python
for i in range(0, 10, 2):
    print(i)
```

실행 결과:

```text
0
2
4
6
8
```

---

## 8. `step`을 생략하면 기본값은 1이다

다음 두 코드는 같은 의미이다.

```python
range(1, 5)
```

```python
range(1, 5, 1)
```

둘 다 결과는 다음과 같다.

```text
1, 2, 3, 4
```

즉, `step`을 생략하면 자동으로 1씩 증가한다.

---

## 9. 감소하는 `range()`

`step`에 음수를 넣으면 숫자가 감소한다.

```python
for i in range(5, 0, -1):
    print(i)
```

실행 결과:

```text
5
4
3
2
1
```

의미:

```text
5부터 시작
0 전까지
1씩 감소
```

여기서도 `stop` 값인 `0`은 포함되지 않는다.

따라서 결과는 `5, 4, 3, 2, 1`이다.

---

## 10. 감소할 때도 끝값은 포함되지 않는다

예를 들어:

```python
range(10, 5, -1)
```

은 다음과 같다.

```text
10, 9, 8, 7, 6
```

`5`는 포함되지 않는다.

```python
for i in range(10, 5, -1):
    print(i)
```

실행 결과:

```text
10
9
8
7
6
```

즉, 감소하는 경우에도 원리는 같다.

```text
start부터 시작해서 stop에 도달하기 전까지만 반복한다.
```

---

## 11. `step`이 0이면 안 된다

`step`은 0이 될 수 없다.

```python
range(1, 10, 0)
```

이 코드는 오류가 난다.

```text
ValueError: range() arg 3 must not be zero
```

왜냐하면 0씩 증가하면 숫자가 변하지 않기 때문이다.

```text
1, 1, 1, 1, ...
```

이렇게 되면 반복이 끝날 수 없다.

그래서 Python은 `step = 0`을 허용하지 않는다.

---

## 12. `range()` 결과를 직접 보고 싶을 때

`range()` 자체를 출력하면 숫자 목록이 바로 보이지 않는다.

```python
print(range(5))
```

실행 결과:

```text
range(0, 5)
```

숫자 목록처럼 보고 싶다면 `list()`로 감싸면 된다.

```python
print(list(range(5)))
```

실행 결과:

```python
[0, 1, 2, 3, 4]
```

예시:

```python
print(list(range(2, 6)))
print(list(range(1, 10, 2)))
print(list(range(5, 0, -1)))
```

실행 결과:

```python
[2, 3, 4, 5]
[1, 3, 5, 7, 9]
[5, 4, 3, 2, 1]
```

---

## 13. 자주 헷갈리는 예제

## 13.1 `range(1, 5)`

```python
for i in range(1, 5):
    print(i)
```

실행 결과:

```text
1
2
3
4
```

`5`는 포함되지 않는다.

---

## 13.2 `range(1, 6)`

```python
for i in range(1, 6):
    print(i)
```

실행 결과:

```text
1
2
3
4
5
```

1부터 5까지 출력하고 싶다면 `stop`에 6을 넣어야 한다.

---

## 13.3 `range(0, 10, 3)`

```python
for i in range(0, 10, 3):
    print(i)
```

실행 결과:

```text
0
3
6
9
```

10은 포함되지 않는다.

---

## 13.4 `range(10, 0, -2)`

```python
for i in range(10, 0, -2):
    print(i)
```

실행 결과:

```text
10
8
6
4
2
```

0은 포함되지 않는다.

---

## 14. 반복 횟수와 `range()`

`range(n)`은 반복을 `n`번 하고 싶을 때 자주 사용한다.

```python
for i in range(3):
    print("안녕")
```

실행 결과:

```text
안녕
안녕
안녕
```

`range(3)`은 다음 숫자를 만든다.

```text
0, 1, 2
```

숫자는 0부터 시작하지만, 개수는 총 3개이다.

따라서 반복은 3번 실행된다.

---

## 15. 인덱스와 함께 사용하기

리스트의 인덱스를 사용할 때도 `range()`가 자주 쓰인다.

```python
fruits = ["사과", "바나나", "포도"]

for i in range(len(fruits)):
    print(i, fruits[i])
```

실행 결과:

```text
0 사과
1 바나나
2 포도
```

여기서 `len(fruits)`는 3이다.

따라서:

```python
range(len(fruits))
```

는 다음과 같다.

```python
range(3)
```

결과적으로 인덱스 `0, 1, 2`가 만들어진다.

---

## 16. 한눈에 정리

| 코드 | 만들어지는 숫자 |
|---|---|
| `range(5)` | `0, 1, 2, 3, 4` |
| `range(1, 5)` | `1, 2, 3, 4` |
| `range(1, 6)` | `1, 2, 3, 4, 5` |
| `range(0, 10, 2)` | `0, 2, 4, 6, 8` |
| `range(1, 10, 2)` | `1, 3, 5, 7, 9` |
| `range(5, 0, -1)` | `5, 4, 3, 2, 1` |
| `range(10, 0, -2)` | `10, 8, 6, 4, 2` |

---

## 17. 핵심 정리

`range()` 함수는 반복문에서 사용할 숫자 범위를 만들어 준다.

형태는 세 가지가 있다.

```python
range(stop)
range(start, stop)
range(start, stop, step)
```

각 매개변수의 의미는 다음과 같다.

```text
start → 시작값
stop  → 끝값 직전
step  → 증가 또는 감소 간격
```

가장 중요한 규칙은 다음과 같다.

```text
stop 값은 포함되지 않는다.
```

예를 들어:

```python
range(1, 5)
```

는 1부터 5까지가 아니라 다음 숫자를 만든다.

```text
1, 2, 3, 4
```

1부터 5까지 출력하고 싶다면 다음처럼 써야 한다.

```python
range(1, 6)
```

즉, `range()`는 다음처럼 기억하면 된다.

```text
range(시작, 끝 직전, 간격)
```

# Python `input()` 함수와 형 변환 정리

## 1. `input()` 함수란?

Python에서 `input()` 함수는 사용자가 키보드로 입력한 값을 받아오는 함수이다.

```python
name = input("이름을 입력하세요: ")
```

위 코드를 실행하면 사용자가 입력한 값이 `name` 변수에 저장된다.

예를 들어 사용자가 다음과 같이 입력했다면:

```text
홍길동
```

`name`에는 `"홍길동"`이라는 값이 저장된다.

---

## 2. `input()`으로 입력받은 값은 기본적으로 문자열이다

`input()` 함수로 입력받은 값은 항상 문자열, 즉 `str` 자료형이다.

예를 들어 사용자가 숫자처럼 보이는 값을 입력해도 Python은 그것을 문자열로 저장한다.

```python
age = input("나이를 입력하세요: ")

print(age)
print(type(age))
```

사용자가 다음과 같이 입력했다고 하자.

```text
20
```

실행 결과는 다음과 같다.

```python
20
<class 'str'>
```

겉으로 보기에는 숫자 `20`처럼 보이지만, 실제 자료형은 문자열이다.

즉, `input()`으로 입력된 `"20"`은 숫자 `20`이 아니라 문자 `"20"`이다.

---

## 3. 문자열 숫자와 실제 숫자의 차이

문자열 `"20"`과 정수 `20`은 다르다.

```python
a = "20"
b = 20

print(type(a))
print(type(b))
```

실행 결과:

```python
<class 'str'>
<class 'int'>
```

`"20"`은 문자열이고, `20`은 정수이다.

따라서 다음 코드는 오류가 난다.

```python
age = input("나이를 입력하세요: ")

next_age = age + 1
print(next_age)
```

사용자가 `20`을 입력하면 `age`에는 `"20"`이라는 문자열이 저장된다.

문자열과 정수는 바로 더할 수 없기 때문에 오류가 발생한다.

```text
TypeError: can only concatenate str (not "int") to str
```

---

## 4. `int()`를 이용한 정수 변환

입력받은 값을 정수로 사용하고 싶다면 `int()`를 사용해야 한다.

```python
age = input("나이를 입력하세요: ")
age = int(age)

print(age + 1)
```

사용자가 다음과 같이 입력하면:

```text
20
```

실행 결과는 다음과 같다.

```python
21
```

이 과정을 한 줄로 쓸 수도 있다.

```python
age = int(input("나이를 입력하세요: "))
```

이 코드는 다음 과정을 한 번에 처리한다.

```text
1. input()으로 값을 입력받는다.
2. 입력받은 문자열을 int()로 정수로 바꾼다.
3. 변환된 정수를 age에 저장한다.
```

---

## 5. `float()`를 이용한 실수 변환

소수점이 있는 숫자를 입력받고 싶다면 `float()`를 사용한다.

```python
height = float(input("키를 입력하세요: "))

print(height)
print(type(height))
```

사용자가 다음과 같이 입력하면:

```text
170.5
```

실행 결과는 다음과 같다.

```python
170.5
<class 'float'>
```

즉, `"170.5"`라는 문자열이 `170.5`라는 실수로 변환된다.

---

## 6. `int()`와 `float()`의 차이

`int()`는 정수로 변환할 때 사용하고, `float()`는 실수로 변환할 때 사용한다.

| 함수 | 변환 결과 | 예시 |
|---|---|---|
| `int()` | 정수 | `10`, `-3`, `0` |
| `float()` | 실수 | `3.14`, `170.5`, `-2.5` |

예시:

```python
a = int("10")
b = float("10")
c = float("3.14")

print(a)
print(b)
print(c)
```

실행 결과:

```python
10
10.0
3.14
```

---

## 7. 숫자 형태의 문자열만 변환할 수 있다

`int()`나 `float()`는 아무 문자열이나 숫자로 바꿀 수 있는 것이 아니다.

숫자 형태로 적힌 문자열만 변환할 수 있다.

가능한 예:

```python
int("10")       # 10
int("-5")       # -5
float("3.14")   # 3.14
float("10")     # 10.0
```

불가능한 예:

```python
int("ten")      # 오류
int("3.14")     # 오류
float("hello")  # 오류
```

`"ten"`은 사람이 보기에는 10을 뜻하는 영어 단어지만, Python은 그 의미를 해석하지 않는다.

따라서 다음 코드는 오류가 난다.

```python
number = int("ten")
```

실행 결과:

```text
ValueError: invalid literal for int() with base 10: 'ten'
```

---

## 8. `"3.14"`는 `int()`로 바로 변환할 수 없다

다음 코드는 오류가 난다.

```python
number = int("3.14")
```

`"3.14"`는 실수 형태의 문자열이지, 정수 형태의 문자열이 아니기 때문이다.

실행 결과:

```text
ValueError: invalid literal for int() with base 10: '3.14'
```

이 경우에는 먼저 `float()`로 바꾼 뒤 `int()`를 사용할 수 있다.

```python
number = int(float("3.14"))

print(number)
```

실행 결과:

```python
3
```

단, 이 경우 반올림이 아니라 소수점 아래가 버려진다.

---

## 9. 실수 값을 `int()`로 바꾸면 소수점 아래가 버려진다

실제 실수 값을 `int()`에 넣으면 정수로 변환된다.

```python
print(int(3.8))
print(int(3.1))
print(int(3.99))
```

실행 결과:

```python
3
3
3
```

`int()`는 반올림하지 않고 소수점 아래를 버린다.

음수도 0에 가까운 방향으로 잘린다.

```python
print(int(-3.8))
```

실행 결과:

```python
-3
```

반올림을 하고 싶다면 `round()`를 사용해야 한다.

```python
print(round(3.8))
```

실행 결과:

```python
4
```

---

## 10. 입력값을 계산에 사용하려면 형 변환이 필요하다

사용자에게 두 숫자를 입력받아 더하는 코드를 생각해 보자.

먼저 형 변환을 하지 않은 경우이다.

```python
a = input("첫 번째 숫자: ")
b = input("두 번째 숫자: ")

print(a + b)
```

사용자가 다음과 같이 입력하면:

```text
첫 번째 숫자: 10
두 번째 숫자: 20
```

실행 결과는 다음과 같다.

```python
1020
```

왜냐하면 `a`와 `b`는 숫자가 아니라 문자열이기 때문이다.

문자열끼리 `+`를 사용하면 덧셈이 아니라 문자열 연결이 된다.

```python
"10" + "20"
```

결과:

```python
"1020"
```

숫자 덧셈을 하려면 `int()`로 변환해야 한다.

```python
a = int(input("첫 번째 숫자: "))
b = int(input("두 번째 숫자: "))

print(a + b)
```

사용자가 다음과 같이 입력하면:

```text
첫 번째 숫자: 10
두 번째 숫자: 20
```

실행 결과는 다음과 같다.

```python
30
```

---

## 11. 정수 입력 예제

```python
age = int(input("나이를 입력하세요: "))

print("내년 나이:", age + 1)
```

입력:

```text
20
```

출력:

```text
내년 나이: 21
```

이 코드에서 `input()`은 `"20"`이라는 문자열을 입력받고, `int()`가 그것을 정수 `20`으로 변환한다.

---

## 12. 실수 입력 예제

```python
height = float(input("키를 입력하세요: "))
weight = float(input("몸무게를 입력하세요: "))

bmi = weight / ((height / 100) ** 2)

print("BMI:", bmi)
```

입력:

```text
키를 입력하세요: 170.5
몸무게를 입력하세요: 60.2
```

이 경우 `height`와 `weight`는 실수로 저장된다.

```python
height = 170.5
weight = 60.2
```

따라서 소수점 계산이 가능하다.

---

## 13. 자주 발생하는 오류

## 13.1 숫자가 아닌 값을 입력한 경우

```python
age = int(input("나이를 입력하세요: "))
```

여기서 사용자가 다음처럼 입력하면 오류가 난다.

```text
스무살
```

실행 결과:

```text
ValueError: invalid literal for int() with base 10
```

`int()`는 `"스무살"`이라는 문자열을 정수로 바꿀 수 없기 때문이다.

---

## 13.2 실수를 정수로 바로 입력한 경우

```python
number = int(input("정수를 입력하세요: "))
```

여기서 사용자가 다음처럼 입력하면 오류가 난다.

```text
3.8
```

왜냐하면 `input()`은 `"3.8"`이라는 문자열을 받고, `int("3.8")`은 불가능하기 때문이다.

이 경우 실수를 허용하려면 `float()`을 사용해야 한다.

```python
number = float(input("숫자를 입력하세요: "))
```

---

## 14. 입력값 변환 흐름 정리

정수 입력:

```python
age = int(input("나이를 입력하세요: "))
```

흐름:

```text
사용자 입력: 20
input() 결과: "20"
int("20") 결과: 20
age에 저장: 20
```

실수 입력:

```python
height = float(input("키를 입력하세요: "))
```

흐름:

```text
사용자 입력: 170.5
input() 결과: "170.5"
float("170.5") 결과: 170.5
height에 저장: 170.5
```

---

## 15. 한눈에 정리

| 코드 | 입력값 | 결과 | 설명 |
|---|---|---|---|
| `input()` | `10` | `"10"` | 문자열로 저장 |
| `int(input())` | `10` | `10` | 정수로 변환 |
| `float(input())` | `10` | `10.0` | 실수로 변환 |
| `float(input())` | `3.14` | `3.14` | 실수로 변환 |
| `int(input())` | `3.14` | 오류 | `"3.14"`는 정수 문자열이 아님 |
| `int(float(input()))` | `3.14` | `3` | 실수로 바꾼 뒤 정수로 변환 |
| `int(input())` | `ten` | 오류 | 숫자 형태가 아닌 문자열 |

---

## 16. 핵심 정리

Python에서 `input()`으로 입력받은 값은 기본적으로 문자열이다.

```python
value = input("값 입력: ")
print(type(value))
```

사용자가 숫자를 입력해도 결과는 문자열이다.

```text
입력: 10
자료형: str
```

따라서 입력받은 값을 숫자로 계산하려면 형 변환이 필요하다.

```python
age = int(input("나이 입력: "))
height = float(input("키 입력: "))
```

정리하면 다음과 같다.

```text
input()              → 문자열로 입력받음
int(input())         → 정수로 변환
float(input())       → 실수로 변환
int(float(input()))  → 실수 형태 문자열을 정수로 변환
```

가장 중요한 점은 다음과 같다.

```text
input()으로 입력된 값은 항상 문자열이다.
숫자로 계산하려면 int()나 float()로 변환해야 한다.
```

# Python `int()` 형 변환 정리

## 1. `int()`란?

Python의 `int()`는 값을 정수형으로 바꾸는 함수이다.

```python
int(값)
```

예를 들어 숫자 형태의 문자열이나 실수를 정수로 바꿀 수 있다.

---

## 2. 숫자 형태의 문자열은 정수로 바꿀 수 있다

문자열이 숫자처럼 생겼다면 `int()`로 정수 변환이 가능하다.

```python
int("10")
```

결과:

```python
10
```

다음과 같은 문자열도 변환할 수 있다.

```python
int("003")   # 3
int("-5")    # -5
int("+7")    # 7
int(" 42 ")  # 42
```

즉, `int()`는 숫자 형태로 적힌 문자열을 정수로 바꿀 수 있다.

---

## 3. 영어 단어는 정수로 바꿀 수 없다

사람이 보기에는 `"ten"`이 숫자 10을 뜻하지만, Python의 `int()`는 영어 단어의 의미를 해석하지 않는다.

```python
int("ten")
```

결과:

```text
ValueError: invalid literal for int() with base 10: 'ten'
```

즉, `"ten"`은 숫자 의미를 가진 단어일 뿐, 숫자 형태의 문자열은 아니다.

따라서 `int()`로 바로 변환할 수 없다.

```python
int("ten")  # 오류
int("one")  # 오류
```

---

## 4. 실수 형태의 문자열은 `int()`로 바로 바꿀 수 없다

`"3.8"`은 문자열이지만, 정수 형태가 아니라 실수 형태이다.

```python
int("3.8")
```

결과:

```text
ValueError: invalid literal for int() with base 10: '3.8'
```

즉, `"3.8"`은 숫자처럼 보이지만 정수 문자열이 아니기 때문에 `int()`로 바로 변환할 수 없다.

가능한 문자열:

```python
int("3")   # 3
int("10")  # 10
```

불가능한 문자열:

```python
int("3.8")  # 오류
int("10개") # 오류
int("ten")  # 오류
```

---

## 5. `"3.8"`을 정수로 바꾸고 싶다면

실수 형태의 문자열 `"3.8"`을 정수로 바꾸고 싶다면 먼저 `float()`으로 실수로 변환한 뒤, 다시 `int()`를 사용해야 한다.

```python
int(float("3.8"))
```

결과:

```python
3
```

과정은 다음과 같다.

```text
"3.8" → float("3.8") → 3.8 → int(3.8) → 3
```

---

## 6. 실수 `3.8`은 `int()`로 변환할 수 있다

문자열 `"3.8"`은 오류가 나지만, 실수 `3.8`은 `int()`로 변환할 수 있다.

```python
int(3.8)
```

결과:

```python
3
```

여기서 중요한 점은 `int()`가 반올림을 하지 않는다는 것이다.

---

## 7. `int()`는 소수점 아래를 버린다

실수에 `int()`를 사용하면 소수점 아래를 버린다.

```python
int(3.1)   # 3
int(3.8)   # 3
int(3.99)  # 3
```

즉, `int(3.8)`은 4가 아니라 3이다.

`int()`는 반올림 함수가 아니라 정수 부분만 남기는 함수이다.

---

## 8. 음수 실수의 경우

음수 실수도 `int()`를 사용하면 소수점 아래를 버린다.

```python
int(-3.8)
```

결과:

```python
-3
```

주의할 점은 더 작은 정수인 `-4`가 되는 것이 아니라, 0에 가까운 방향으로 잘린다는 것이다.

```python
int(-3.1)   # -3
int(-3.8)   # -3
int(-3.99)  # -3
```

---

## 9. 반올림하고 싶다면 `round()`를 사용한다

`int()`는 반올림하지 않는다.

반올림을 원한다면 `round()`를 사용해야 한다.

```python
round(3.8)
```

결과:

```python
4
```

비교하면 다음과 같다.

```python
int(3.8)    # 3
round(3.8)  # 4
```

---

## 10. 정리

Python의 `int()`는 값을 정수로 바꾸는 함수이다.

하지만 모든 문자열을 숫자로 바꿀 수 있는 것은 아니다.

| 입력값 | 결과 | 설명 |
|---|---:|---|
| `int("10")` | `10` | 숫자 형태의 문자열이라 가능 |
| `int("003")` | `3` | 앞의 0은 제거됨 |
| `int("ten")` | 오류 | 영어 단어는 해석하지 않음 |
| `int("3.8")` | 오류 | 실수 형태의 문자열은 바로 변환 불가 |
| `int(float("3.8"))` | `3` | 문자열 → 실수 → 정수 순서로 변환 |
| `int(3.8)` | `3` | 실수는 정수로 변환 가능 |
| `round(3.8)` | `4` | 반올림 |

핵심은 다음과 같다.

```text
int("3")    → 가능
int("3.8")  → 오류
int(3.8)    → 3
int("ten")  → 오류
```

즉, `int()`는 숫자 형태의 문자열이나 실제 숫자 값을 정수로 바꿀 수 있지만, `"ten"` 같은 영어 단어나 `"3.8"` 같은 실수형 문자열은 바로 정수로 바꿀 수 없다.

# 매개변수, 파라미터, 인수, 인자 용어 정리

## 1. 개요

프로그래밍에서 함수를 공부하다 보면 다음 용어들이 자주 나온다.

```text
매개변수
파라미터
인수
인자
argument
parameter
```

처음에는 전부 비슷해 보여서 헷갈리기 쉽다.  
하지만 핵심만 잡으면 어렵지 않다.

가장 간단히 정리하면 다음과 같다.

```text
매개변수(parameter)
→ 함수를 정의할 때 괄호 안에 적는 변수

인수(argument)
→ 함수를 호출할 때 실제로 넣어 주는 값
```

---

## 2. 기본 예제

```python
def greet(name):
    print("안녕하세요,", name)

greet("철수")
```

이 코드에서:

```python
def greet(name):
```

의 `name`은 **매개변수**이다.

```python
greet("철수")
```

의 `"철수"`는 **인수**이다.

정리하면:

| 구분 | 코드 | 의미 |
|---|---|---|
| 매개변수 | `name` | 함수가 값을 받을 자리 |
| 인수 | `"철수"` | 함수에 실제로 전달한 값 |

---

## 3. 매개변수란?

매개변수는 함수를 정의할 때 사용하는 변수이다.

```python
def add(a, b):
    return a + b
```

여기서 `a`와 `b`가 매개변수이다.

```text
a, b
→ 함수가 값을 받을 자리
```

즉, 매개변수는 아직 실제 값이 아니라, 나중에 함수가 호출될 때 값을 받기 위한 이름이다.

---

## 4. 인수란?

인수는 함수를 호출할 때 실제로 전달하는 값이다.

```python
add(3, 5)
```

여기서 `3`과 `5`가 인수이다.

```text
3, 5
→ 함수에 실제로 넣은 값
```

함수를 호출하면 인수가 매개변수에 전달된다.

```python
def add(a, b):
    return a + b

add(3, 5)
```

이때 내부적으로는 다음처럼 연결된다.

```text
a ← 3
b ← 5
```

즉, 인수 `3`은 매개변수 `a`에 들어가고, 인수 `5`는 매개변수 `b`에 들어간다.

---

## 5. 파라미터와 매개변수

`파라미터`는 영어 `parameter`를 그대로 읽은 말이다.

한국어로는 보통 **매개변수**라고 한다.

```text
parameter = 파라미터 = 매개변수
```

예시:

```python
def introduce(name, age):
    print(name, age)
```

여기서 `name`, `age`는 매개변수이자 파라미터이다.

---

## 6. 아규먼트와 인수/인자

`argument`는 함수를 호출할 때 전달하는 실제 값이다.

한국어로는 **인수** 또는 **인자**라고 부른다.

```text
argument = 아규먼트 = 인수 = 인자
```

예시:

```python
introduce("영희", 20)
```

여기서 `"영희"`, `20`은 인수 또는 인자이다.

---

## 7. 용어 대응표

| 영어 | 한국어 | 의미 |
|---|---|---|
| parameter | 매개변수, 파라미터 | 함수를 정의할 때 값을 받을 변수 |
| argument | 인수, 인자 | 함수를 호출할 때 실제로 넣는 값 |

---

## 8. 한눈에 보는 차이

```python
def say(message):
    print(message)

say("Hello")
```

이 코드에서:

```python
def say(message):
```

`message`는 매개변수이다.

```python
say("Hello")
```

`"Hello"`는 인수이다.

정리하면:

```text
매개변수
→ 함수 정의할 때 사용
→ 값을 받을 이름

인수
→ 함수 호출할 때 사용
→ 실제 전달하는 값
```

---

## 9. 비유로 이해하기

함수를 자판기에 비유하면 다음과 같다.

```python
def vending_machine(money):
    print("받은 돈:", money)
```

여기서 `money`는 매개변수이다.

```text
money
→ 돈을 받을 자리
```

이제 함수를 호출한다.

```python
vending_machine(1000)
```

여기서 `1000`은 인수이다.

```text
1000
→ 실제로 넣은 돈
```

즉:

```text
매개변수 = 받을 자리
인수 = 실제로 넣은 값
```

---

## 10. 여러 개의 매개변수와 인수

```python
def add(a, b):
    print(a + b)

add(10, 20)
```

여기서:

| 구분 | 값 |
|---|---|
| 매개변수 | `a`, `b` |
| 인수 | `10`, `20` |

함수가 호출되면 다음처럼 값이 전달된다.

```text
a ← 10
b ← 20
```

그래서 함수 내부에서는:

```python
print(a + b)
```

가 다음처럼 실행된다.

```python
print(10 + 20)
```

결과:

```text
30
```

---

## 11. 위치 인수

함수를 호출할 때 순서대로 전달하는 값을 위치 인수라고 한다.

```python
def introduce(name, age):
    print("이름:", name)
    print("나이:", age)

introduce("철수", 17)
```

이때 전달은 순서대로 이루어진다.

```text
name ← "철수"
age ← 17
```

따라서 결과는 다음과 같다.

```text
이름: 철수
나이: 17
```

순서가 바뀌면 결과도 바뀐다.

```python
introduce(17, "철수")
```

이 경우:

```text
name ← 17
age ← "철수"
```

가 되어 의미가 이상해진다.

---

## 12. 키워드 인수

인수를 전달할 때 매개변수 이름을 직접 지정할 수도 있다.

```python
def introduce(name, age):
    print("이름:", name)
    print("나이:", age)

introduce(name="철수", age=17)
```

여기서 `name="철수"`, `age=17`은 키워드 인수이다.

키워드 인수를 사용하면 순서를 바꿔도 된다.

```python
introduce(age=17, name="철수")
```

이 경우도 다음처럼 전달된다.

```text
name ← "철수"
age ← 17
```

---

## 13. 기본값 매개변수

매개변수에는 기본값을 줄 수도 있다.

```python
def greet(name="손님"):
    print("안녕하세요,", name)

greet()
greet("철수")
```

실행 결과:

```text
안녕하세요, 손님
안녕하세요, 철수
```

여기서 `name="손님"`은 기본값 매개변수이다.

함수를 호출할 때 인수를 넣지 않으면 기본값 `"손님"`이 사용된다.

```python
greet()
```

내부적으로는 다음처럼 동작한다.

```text
name ← "손님"
```

인수를 넣으면 넣은 값이 사용된다.

```python
greet("철수")
```

내부적으로는 다음처럼 동작한다.

```text
name ← "철수"
```

---

## 14. 자주 헷갈리는 말 정리

### 14.1 매개변수와 파라미터

둘은 같은 말이다.

```text
매개변수 = 파라미터 = parameter
```

예시:

```python
def f(x):
    pass
```

여기서 `x`는 매개변수이자 파라미터이다.

---

### 14.2 인수와 인자

둘도 거의 같은 말로 사용된다.

```text
인수 = 인자 = argument
```

예시:

```python
f(10)
```

여기서 `10`은 인수 또는 인자이다.

---

### 14.3 매개변수와 인수의 차이

```python
def f(x):
    print(x)

f(10)
```

여기서:

```text
x  → 매개변수
10 → 인수
```

매개변수는 함수를 만들 때 적는 이름이고, 인수는 함수를 사용할 때 넣는 실제 값이다.

---

## 15. 실전 예제

```python
def calculate_price(price, count):
    total = price * count
    print("총 가격:", total)

calculate_price(1000, 3)
```

이 코드에서:

| 구분 | 내용 |
|---|---|
| 함수 이름 | `calculate_price` |
| 매개변수 | `price`, `count` |
| 인수 | `1000`, `3` |

값 전달 과정은 다음과 같다.

```text
price ← 1000
count ← 3
```

그래서 함수 내부에서는:

```python
total = price * count
```

가 다음처럼 계산된다.

```python
total = 1000 * 3
```

결과:

```text
총 가격: 3000
```

---

## 16. `range()` 예제로 이해하기

```python
for i in range(1, 6):
    print(i)
```

여기서 `range()` 함수에 전달된 `1`, `6`은 인수이다.

```python
range(1, 6)
```

`range` 함수의 입장에서 보면:

```text
1 → start에 전달되는 인수
6 → stop에 전달되는 인수
```

즉, 함수에 실제로 넣은 값은 인수이다.

만약 `range()`의 정의를 설명한다면 다음처럼 말할 수 있다.

```text
range(start, stop, step)
```

여기서 `start`, `stop`, `step`은 매개변수이다.

---

## 17. `print()` 예제로 이해하기

```python
print("Hello", end="")
```

여기서 `"Hello"`와 `end=""`는 인수이다.

```text
"Hello" → 출력할 값으로 전달한 인수
end=""  → end 매개변수에 전달한 키워드 인수
```

`print()` 함수에는 여러 매개변수가 있다.

예를 들면:

```text
print(*objects, sep=' ', end='\n', file=None, flush=False)
```

여기서 `sep`, `end`, `file`, `flush` 등은 매개변수이다.

사용자가 `end=""`처럼 값을 넣으면, 그것은 `end` 매개변수에 값을 전달하는 인수이다.

---

## 18. 핵심 비교

| 상황 | 용어 | 예시 |
|---|---|---|
| 함수를 정의할 때 | 매개변수, 파라미터 | `def add(a, b):`의 `a`, `b` |
| 함수를 호출할 때 | 인수, 인자 | `add(3, 5)`의 `3`, `5` |

---

## 19. 가장 쉬운 암기법

다음처럼 외우면 쉽다.

```text
매개변수는 받는 이름
인수는 넣는 값
```

또는:

```text
함수 만들 때 괄호 안 → 매개변수
함수 부를 때 괄호 안 → 인수
```

예시:

```python
def hello(name):   # name은 매개변수
    print(name)

hello("철수")      # "철수"는 인수
```

---

## 20. 요약

매개변수와 파라미터는 같은 말이다.

```text
매개변수 = 파라미터 = parameter
```

인수와 인자도 거의 같은 말이다.

```text
인수 = 인자 = argument
```

가장 중요한 차이는 다음과 같다.

```text
매개변수
→ 함수를 정의할 때 값을 받을 변수

인수
→ 함수를 호출할 때 실제로 전달하는 값
```

예를 들어:

```python
def add(a, b):
    return a + b

add(3, 5)
```

여기서:

```text
a, b → 매개변수
3, 5 → 인수
```

즉, 함수는 매개변수라는 자리를 만들어 두고, 호출할 때 인수라는 실제 값을 넣어 실행된다.

# Python 함수 호출과 `print(함수())` 출력 결과 정리

## 1. 예제 함수

다음과 같은 함수가 있다고 하자.

```python
def message_print():
    print("--------------------")
    print("|                  |")
    print("|  You can do it!  |")
    print("|                  |")
    print("++++++++++++++++++++")
```

이 함수는 문자열을 반환하는 함수가 아니라, 함수 내부에서 직접 출력하는 함수이다.

즉, 함수 안에 이미 여러 개의 `print()`가 들어 있다.

---

## 2. 그냥 함수만 호출하는 경우

```python
message_print()
```

실행 결과:

```text
--------------------
|                  |
|  You can do it!  |
|                  |
++++++++++++++++++++
```

이 경우 함수 안에 있는 `print()`들이 실행되어 메시지 박스가 출력된다.

이 함수의 정상적인 사용 방식은 보통 다음과 같다.

```python
message_print()
```

---

## 3. `print(message_print())`로 출력하는 경우

이번에는 함수를 다시 `print()` 안에 넣어 보자.

```python
print(message_print())
```

실행 결과:

```text
--------------------
|                  |
|  You can do it!  |
|                  |
++++++++++++++++++++
None
```

마지막에 `None`이 출력된다.

---

## 4. 왜 `None`이 출력될까?

`print(message_print())`의 실행 순서는 다음과 같다.

```text
1. 먼저 message_print() 함수가 실행된다.
2. 함수 안의 print()들이 실행되어 메시지 박스가 출력된다.
3. message_print() 함수가 끝난다.
4. 그런데 message_print()에는 return 값이 없다.
5. Python에서 return 값이 없는 함수는 자동으로 None을 반환한다.
6. 바깥쪽 print()가 그 None을 출력한다.
```

즉, `message_print()`는 실제로 다음과 비슷하게 동작한다.

```python
def message_print():
    print("--------------------")
    print("|                  |")
    print("|  You can do it!  |")
    print("|                  |")
    print("++++++++++++++++++++")
    return None
```

`return None`을 직접 쓰지 않아도, Python은 반환값이 없는 함수에 대해 자동으로 `None`을 반환한다.

---

## 5. 함수 내부의 `print()`와 함수의 반환값은 다르다

다음 두 개념은 다르다.

```text
출력
→ 화면에 보여 주는 것

반환
→ 함수가 호출된 자리로 값을 돌려주는 것
```

예를 들어:

```python
def message_print():
    print("Hello")
```

이 함수는 `"Hello"`를 화면에 출력하지만, 값을 반환하지는 않는다.

따라서:

```python
result = message_print()
print(result)
```

실행 결과:

```text
Hello
None
```

`message_print()`가 `"Hello"`를 출력한 뒤, 반환값이 없기 때문에 `result`에는 `None`이 들어간다.

---

## 6. `print(message_print())`가 이상하게 보이는 이유

다음 코드를 보자.

```python
print(message_print())
```

이 코드는 겉으로는 `message_print()`의 출력 결과를 다시 출력하는 것처럼 보인다.

하지만 실제 의미는 다르다.

```text
message_print()를 실행한 뒤,
그 함수의 반환값을 print()로 출력한다.
```

그런데 `message_print()`는 반환값이 없으므로 반환값은 `None`이다.

그래서 마지막에 `None`이 출력된다.

---

## 7. 괄호가 있는 경우와 없는 경우

함수를 사용할 때 괄호 `()`가 있느냐 없느냐도 중요하다.

---

## 7.1 `message_print()`

```python
message_print()
```

의미:

```text
message_print 함수를 실행한다.
```

출력:

```text
--------------------
|                  |
|  You can do it!  |
|                  |
++++++++++++++++++++
```

---

## 7.2 `print(message_print())`

```python
print(message_print())
```

의미:

```text
message_print 함수를 실행한 뒤,
그 함수의 반환값을 출력한다.
```

출력:

```text
--------------------
|                  |
|  You can do it!  |
|                  |
++++++++++++++++++++
None
```

---

## 7.3 `print(message_print)`

```python
print(message_print)
```

의미:

```text
함수를 실행하지 않고, 함수 객체 자체를 출력한다.
```

출력 예시:

```text
<function message_print at 0x000001A2B3C4D5E0>
```

이 결과는 함수가 메모리 어딘가에 존재한다는 정보를 보여 주는 것이다.

함수 안의 내용은 실행되지 않는다.

---

## 8. 세 가지 코드 비교

| 코드 | 의미 | 결과 |
|---|---|---|
| `message_print()` | 함수 실행 | 메시지 박스 출력 |
| `print(message_print())` | 함수 실행 후 반환값 출력 | 메시지 박스 출력 후 `None` 출력 |
| `print(message_print)` | 함수 자체 출력 | 함수 객체 정보 출력 |

---

## 9. 반환값이 있는 함수와 비교

이번에는 `print()`가 아니라 `return`을 사용하는 함수를 보자.

```python
def message_return():
    return "You can do it!"
```

이 함수는 화면에 직접 출력하지 않고 문자열을 반환한다.

```python
print(message_return())
```

실행 결과:

```text
You can do it!
```

이 경우에는 `message_return()`이 `"You can do it!"`이라는 값을 반환하므로, 바깥쪽 `print()`가 그 값을 출력한다.

---

## 10. 출력용 함수와 반환용 함수의 차이

### 출력용 함수

```python
def message_print():
    print("You can do it!")
```

사용:

```python
message_print()
```

결과:

```text
You can do it!
```

이 함수는 이미 내부에서 출력하므로 `print(message_print())`로 감쌀 필요가 없다.

---

### 반환용 함수

```python
def message_return():
    return "You can do it!"
```

사용:

```python
print(message_return())
```

결과:

```text
You can do it!
```

이 함수는 값을 반환만 하므로, 화면에 보이게 하려면 `print()`로 출력해야 한다.

---

## 11. 예제 함수는 어떻게 사용하는 것이 맞을까?

처음 예제 함수는 내부에서 이미 `print()`를 사용하고 있다.

```python
def message_print():
    print("--------------------")
    print("|                  |")
    print("|  You can do it!  |")
    print("|                  |")
    print("++++++++++++++++++++")
```

따라서 올바른 사용은 다음과 같다.

```python
message_print()
```

굳이 이렇게 쓰지 않는다.

```python
print(message_print())
```

왜냐하면 이 경우 마지막에 `None`이 추가로 출력되기 때문이다.

---

## 12. 핵심 정리

함수 안에 이미 `print()`가 들어 있다면, 그 함수는 보통 그냥 호출하면 된다.

```python
message_print()
```

만약 다음처럼 쓰면:

```python
print(message_print())
```

함수 내부의 출력이 먼저 실행되고, 함수의 반환값이 다시 출력된다.

그런데 반환값이 없는 함수는 자동으로 `None`을 반환한다.

그래서 결과는 다음과 같이 된다.

```text
--------------------
|                  |
|  You can do it!  |
|                  |
++++++++++++++++++++
None
```

정리하면 다음과 같다.

```text
message_print()
→ 함수 실행, 내부 print() 출력

print(message_print())
→ 함수 실행, 내부 print() 출력
→ 함수 반환값 None을 다시 출력

print(message_print)
→ 함수 실행 X
→ 함수 객체 정보 출력
```

가장 중요한 결론은 다음과 같다.

```text
함수 안에 print()가 이미 있다면 print(함수())로 감싸지 말고 그냥 함수()로 호출한다.
```

# 파이썬 인터프리터
---
# Python 인터프리터와 함수 정의, 전역 변수 접근 원리

## 1. 의문점

Python은 보통 인터프리터 언어라고 배운다.

그래서 다음과 같은 의문이 생길 수 있다.

```python
def print_message():
    print(message)

message = "Hello"

print_message()
```

위 코드에서 함수 `print_message()`는 코드의 맨 위에 정의되어 있다.  
그런데 함수 안에서는 아래쪽에 있는 전역 변수 `message`를 사용한다.

그렇다면 이런 의문이 생긴다.

```text
Python은 인터프리터라면서?
위에서 아래로 한 줄씩 실행한다면서?
그런데 함수는 어떻게 아래에 있는 전역 변수 message에 접근할 수 있는 걸까?
Python은 파싱도 안 하는 걸까?
```

결론부터 말하면, Python도 파싱을 한다.  
다만 함수 안의 코드는 함수가 정의될 때 바로 실행되지 않고, 함수가 호출될 때 실행된다.

---

## 2. Python도 파싱을 한다

Python이 인터프리터 언어라는 말은 코드를 전혀 분석하지 않는다는 뜻이 아니다.

Python은 코드를 실행하기 전에 먼저 다음 과정을 거친다.

```text
소스 코드
→ 파싱
→ 바이트코드로 컴파일
→ Python 인터프리터가 바이트코드 실행
```

즉, Python도 실행 전에 문법 구조를 분석한다.

다만 C나 C++처럼 실행 파일을 미리 만들어 두고 실행하는 방식이 아니라, Python 인터프리터가 바이트코드를 실행하는 방식이다.

---

## 3. `def`를 만나면 함수 본문은 바로 실행되지 않는다

다음 코드를 보자.

```python
def print_message():
    print(message)

message = "Hello"

print_message()
```

Python이 위 코드를 실행할 때 `def print_message():`를 만나면 함수 안의 코드를 바로 실행하지 않는다.

즉, 이 부분은 즉시 실행되지 않는다.

```python
print(message)
```

대신 Python은 다음 작업을 한다.

```text
1. print_message라는 함수 객체를 만든다.
2. 그 함수 객체를 print_message라는 이름에 저장한다.
3. 함수 본문은 나중에 함수가 호출될 때 실행하기 위해 보관한다.
```

따라서 `def`는 함수를 “실행”하는 것이 아니라, 함수를 “정의”하는 코드이다.

---

## 4. 실행 순서로 이해하기

다음 코드를 다시 보자.

```python
def print_message():
    print(message)

message = "Hello"

print_message()
```

실행 순서는 다음과 같다.

```text
1. def print_message(): 를 만난다.
2. print_message 함수가 정의된다.
3. 함수 안의 print(message)는 아직 실행되지 않는다.
4. message = "Hello"가 실행된다.
5. 전역 변수 message가 만들어진다.
6. print_message()가 호출된다.
7. 그제야 함수 안의 print(message)가 실행된다.
8. 이 시점에는 message가 이미 존재하므로 "Hello"가 출력된다.
```

실행 결과:

```text
Hello
```

핵심은 다음과 같다.

```text
함수 안의 변수 이름은 함수 정의 시점이 아니라 함수 호출 시점에 찾는다.
```

---

## 5. 전역 변수는 호출 시점에 존재하면 사용할 수 있다

함수 안에서 전역 변수를 사용할 때 중요한 것은 함수가 어디에 정의되었는지가 아니다.

중요한 것은 함수가 호출되는 시점에 그 전역 변수가 존재하는지이다.

다음 코드는 정상 작동한다.

```python
def print_message():
    print(message)

message = "Hello"

print_message()
```

이유는 `print_message()`가 호출될 때 이미 `message`가 만들어져 있기 때문이다.

```text
message = "Hello" 실행 완료
→ print_message() 호출
→ 함수 안에서 message 찾기
→ 전역 변수 message 존재
→ 정상 출력
```

---

## 6. 호출 전에 전역 변수가 없으면 오류가 난다

반대로 다음 코드는 오류가 난다.

```python
def print_message():
    print(message)

print_message()

message = "Hello"
```

이 코드는 함수 정의 자체는 가능하다.

하지만 문제는 `print_message()`를 너무 일찍 호출했다는 점이다.

실행 순서는 다음과 같다.

```text
1. print_message 함수가 정의된다.
2. print_message()가 호출된다.
3. 함수 안에서 message를 찾는다.
4. 아직 message = "Hello"가 실행되지 않았다.
5. 따라서 message라는 이름이 존재하지 않는다.
6. NameError가 발생한다.
```

오류 예시:

```text
NameError: name 'message' is not defined
```

즉, 아래쪽에 전역 변수가 있더라도 함수 호출 전에 만들어지지 않았다면 사용할 수 없다.

---

## 7. 함수 정의 위치와 변수 접근의 관계

다음 두 코드를 비교해 보자.

### 정상 작동하는 코드

```python
def print_message():
    print(message)

message = "Hello"

print_message()
```

실행 결과:

```text
Hello
```

이 코드는 함수 호출 전에 `message`가 만들어져 있으므로 정상 작동한다.

---

### 오류가 나는 코드

```python
def print_message():
    print(message)

print_message()

message = "Hello"
```

실행 결과:

```text
NameError: name 'message' is not defined
```

이 코드는 함수 호출 시점에 `message`가 아직 없으므로 오류가 난다.

---

## 8. 함수 안의 코드는 “예약”되어 있다가 나중에 실행된다

`def` 안에 있는 코드는 함수가 정의될 때 실행되는 것이 아니라, 함수가 호출될 때 실행된다.

```python
def test():
    print("함수 실행됨")

print("함수 호출 전")
test()
print("함수 호출 후")
```

실행 결과:

```text
함수 호출 전
함수 실행됨
함수 호출 후
```

`def test():`를 만났을 때 `"함수 실행됨"`이 출력되지 않는다.  
`test()`를 호출해야 비로소 함수 안의 코드가 실행된다.

---

## 9. Python이 인터프리터 언어라는 말의 정확한 의미

Python이 인터프리터 언어라는 말은 보통 다음 의미로 사용된다.

```text
컴파일된 실행 파일을 미리 만들어 실행하는 방식이 아니라,
Python 인터프리터가 코드를 해석하고 실행한다.
```

하지만 이것이 다음 뜻은 아니다.

```text
Python은 파싱을 전혀 하지 않는다.
Python은 아래쪽 코드를 전혀 모른다.
Python은 함수 본문을 정의 시점에 바로 실행한다.
```

Python은 실행 전에 소스 코드를 분석하고, 바이트코드로 컴파일한 뒤 실행한다.

즉, Python도 내부적으로는 다음 과정을 거친다.

```text
작성한 .py 코드
→ 문법 분석
→ 바이트코드 생성
→ 인터프리터 실행
```

그래서 Python은 인터프리터 언어이면서도 파싱과 컴파일 과정을 가진다.

---

## 10. 변수 이름은 언제 찾을까?

함수 안에서 전역 변수 이름을 찾는 시점은 함수 정의 시점이 아니라 함수 실행 시점이다.

예를 들어:

```python
def show():
    print(x)

x = 10
show()
```

실행 결과:

```text
10
```

이 코드에서 `x`는 함수보다 아래에 있지만, `show()`가 호출될 때는 이미 `x = 10`이 실행된 상태이다.

따라서 함수 안에서 `x`를 찾을 수 있다.

---

## 11. 함수 정의 시점에는 이름 존재 여부를 엄격히 검사하지 않는다

다음 코드는 함수 정의 자체는 가능하다.

```python
def show():
    print(x)
```

이 시점에 `x`가 없어도 함수 정의는 된다.

하지만 함수를 호출하면 문제가 될 수 있다.

```python
show()
```

만약 호출 시점에도 `x`가 없으면 오류가 난다.

```text
NameError: name 'x' is not defined
```

즉, Python은 함수 안의 전역 변수 이름을 함수 정의 순간에 바로 값으로 확정하지 않는다.  
대부분의 이름 조회는 실행 시점에 이루어진다.

---

## 12. 정리 예제

```python
def print_message():
    print(message)

message = "Hello"

print_message()
```

이 코드는 다음과 같이 이해하면 된다.

```text
def print_message():
→ print_message라는 함수를 등록한다.
→ 함수 안의 print(message)는 아직 실행하지 않는다.

message = "Hello"
→ 전역 변수 message를 만든다.

print_message()
→ 함수를 실행한다.
→ 함수 안에서 message를 찾는다.
→ 전역 변수 message가 있으므로 "Hello" 출력
```

---

## 13. 잘못 이해하기 쉬운 부분

### 오해 1. Python은 인터프리터라서 파싱을 안 한다

틀린 이해이다.

Python도 코드를 실행하기 전에 문법을 분석한다.

```text
Python도 파싱한다.
Python도 바이트코드로 컴파일한다.
그 바이트코드를 인터프리터가 실행한다.
```

---

### 오해 2. 함수는 정의될 때 내부 코드가 바로 실행된다

틀린 이해이다.

```python
def hello():
    print("Hello")
```

위 코드만으로는 `"Hello"`가 출력되지 않는다.

다음처럼 호출해야 실행된다.

```python
hello()
```

---

### 오해 3. 함수보다 아래에 있는 전역 변수는 절대 사용할 수 없다

틀린 이해이다.

함수보다 아래에 전역 변수가 있더라도, 함수 호출 전에 그 변수가 만들어졌다면 사용할 수 있다.

```python
def show():
    print(x)

x = 10
show()
```

실행 결과:

```text
10
```

---

## 14. 핵심 정리

Python은 인터프리터 언어이지만, 코드를 전혀 분석하지 않는 것은 아니다.  
Python도 실행 전에 코드를 파싱하고 바이트코드로 컴파일한다.

`def`를 만나면 함수 객체가 만들어지고, 함수 이름에 저장된다.  
하지만 함수 본문은 그 자리에서 바로 실행되지 않는다.

함수 안의 코드는 함수가 호출될 때 실행된다.

따라서 다음 코드는 정상 작동한다.

```python
def print_message():
    print(message)

message = "Hello"

print_message()
```

이유는 다음과 같다.

```text
함수 정의 시점에는 print(message)가 실행되지 않는다.
message = "Hello"가 먼저 실행된다.
그 후 print_message()가 호출된다.
호출 시점에는 message가 이미 존재한다.
따라서 함수 안에서 전역 변수 message에 접근할 수 있다.
```

반대로 다음 코드는 오류가 난다.

```python
def print_message():
    print(message)

print_message()

message = "Hello"
```

이유는 함수 호출 시점에 `message`가 아직 만들어지지 않았기 때문이다.

가장 중요한 결론은 다음과 같다.

```text
Python은 인터프리터 언어이지만 파싱을 한다.
def는 함수를 등록할 뿐, 함수 본문을 바로 실행하지 않는다.
전역 변수는 함수 호출 시점에 존재하면 접근할 수 있다.
```

# OOP(Object Oriented Programming)

## 3. 클래스와 객체

OOP에서 가장 중요한 개념은 **클래스(Class)**와 **객체(Object)**입니다.

### 3-1. 클래스란?

**클래스**는 객체를 만들기 위한 설계도입니다.

예를 들어 자동차를 만들기 전에 설계도가 필요하듯이, 객체를 만들기 위해서는 클래스가 필요합니다.

```python
class Car:
    pass
```

위 코드는 `Car`라는 클래스를 정의한 것입니다.

아직 구체적인 기능은 없지만, 자동차 객체를 만들 수 있는 기본 틀입니다.

---

### 3-2. 객체란?

**객체**는 클래스를 바탕으로 실제로 만들어진 대상입니다.

```python
class Car:
    pass


car1 = Car()
car2 = Car()
```

여기서 `Car`는 클래스이고, `car1`, `car2`는 객체입니다.

즉, 하나의 클래스로 여러 개의 객체를 만들 수 있습니다.

| 클래스 | 객체 |
|---|---|
| 설계도 | 실제 만들어진 것 |
| 자동차 설계도 | 실제 자동차 |
| 붕어빵 틀 | 붕어빵 |
| 회원 설계도 | 실제 회원 데이터 |

---

## 4. 속성(Attribute)

**속성**은 객체가 가지고 있는 데이터입니다.

예를 들어 자동차 객체는 다음과 같은 속성을 가질 수 있습니다.

- 색상
- 브랜드
- 속도

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color


car1 = Car("Hyundai", "Black")
car2 = Car("Kia", "White")

print(car1.brand)
print(car2.color)
```

실행 결과:

```text
Hyundai
White
```

여기서 `brand`, `color`가 객체의 속성입니다.

---

## 5. 메서드(Method)

**메서드**는 클래스 안에 정의된 함수입니다.

객체가 수행할 수 있는 동작을 표현합니다.

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color
        self.speed = 0

    def drive(self):
        print(f"{self.brand} 자동차가 달립니다.")

    def stop(self):
        print(f"{self.brand} 자동차가 멈춥니다.")


car = Car("Hyundai", "Black")

car.drive()
car.stop()
```

실행 결과:

```text
Hyundai 자동차가 달립니다.
Hyundai 자동차가 멈춥니다.
```

여기서 `drive()`와 `stop()`은 메서드입니다.

---

## 6. 생성자 `__init__`

`__init__`은 객체가 생성될 때 자동으로 실행되는 특별한 메서드입니다.

주로 객체의 초기값을 설정할 때 사용합니다.

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade


student1 = Student("민수", 3)

print(student1.name)
print(student1.grade)
```

실행 결과:

```text
민수
3
```

`Student("민수", 3)`으로 객체를 만들면 `__init__`이 자동으로 호출됩니다.

---

## 7. `self`란?

`self`는 객체 자기 자신을 의미합니다.

클래스 안에서 객체의 속성이나 메서드에 접근할 때 사용합니다.

```python
class Person:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(f"안녕하세요. 저는 {self.name}입니다.")


person = Person("지은")
person.introduce()
```

실행 결과:

```text
안녕하세요. 저는 지은입니다.
```

여기서 `self.name`은 현재 객체가 가진 `name` 값을 의미합니다.

---

## 8. OOP의 4대 특징

객체 지향 프로그래밍에는 대표적인 4가지 특징이 있습니다.

1. 캡슐화
2. 상속
3. 다형성
4. 추상화

---

### 8-1. 캡슐화 Encapsulation

**캡슐화**는 데이터와 기능을 하나의 클래스 안에 묶는 것을 말합니다.

또한 외부에서 객체 내부의 데이터를 함부로 변경하지 못하도록 보호하는 의미도 있습니다.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance

    def deposit(self, money):
        self.__balance += money

    def withdraw(self, money):
        if self.__balance >= money:
            self.__balance -= money
        else:
            print("잔액이 부족합니다.")

    def get_balance(self):
        return self.__balance


account = BankAccount("민수", 10000)

account.deposit(5000)
account.withdraw(3000)

print(account.get_balance())
```

실행 결과:

```text
12000
```

여기서 `__balance`는 외부에서 직접 접근하기 어렵게 만든 속성입니다.

즉, 잔액은 `deposit()`, `withdraw()`, `get_balance()` 같은 정해진 메서드를 통해서만 다루도록 만든 것입니다.

이처럼 중요한 데이터를 보호하고, 정해진 방식으로만 사용하게 하는 것이 캡슐화입니다.

---

### 8-2. 상속 Inheritance

**상속**은 기존 클래스의 속성과 기능을 새로운 클래스가 물려받는 것입니다.

기존 클래스를 **부모 클래스**, 상속받는 클래스를 **자식 클래스**라고 합니다.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name}가 먹이를 먹습니다.")


class Dog(Animal):
    def bark(self):
        print(f"{self.name}가 멍멍 짖습니다.")


dog = Dog("초코")

dog.eat()
dog.bark()
```

실행 결과:

```text
초코가 먹이를 먹습니다.
초코가 멍멍 짖습니다.
```

`Dog` 클래스에는 `eat()` 메서드가 직접 정의되어 있지 않습니다.

하지만 `Animal` 클래스를 상속받았기 때문에 `eat()`을 사용할 수 있습니다.

상속을 사용하면 중복 코드를 줄이고, 기존 코드를 재사용할 수 있습니다.

---

### 8-3. 오버라이딩 Overriding

상속받은 메서드를 자식 클래스에서 다시 정의하는 것을 **오버라이딩**이라고 합니다.

```python
class Animal:
    def speak(self):
        print("동물이 소리를 냅니다.")


class Dog(Animal):
    def speak(self):
        print("강아지가 멍멍 짖습니다.")


class Cat(Animal):
    def speak(self):
        print("고양이가 야옹 웁니다.")


dog = Dog()
cat = Cat()

dog.speak()
cat.speak()
```

실행 결과:

```text
강아지가 멍멍 짖습니다.
고양이가 야옹 웁니다.
```

부모 클래스의 `speak()` 메서드를 자식 클래스에서 각각 다르게 다시 정의했습니다.

---

### 8-4. 다형성 Polymorphism

**다형성**은 같은 이름의 메서드가 객체에 따라 다르게 동작하는 것을 말합니다.

```python
class Dog:
    def speak(self):
        print("멍멍")


class Cat:
    def speak(self):
        print("야옹")


class Duck:
    def speak(self):
        print("꽥꽥")


animals = [Dog(), Cat(), Duck()]

for animal in animals:
    animal.speak()
```

실행 결과:

```text
멍멍
야옹
꽥꽥
```

모두 `speak()`라는 같은 메서드를 호출했지만, 객체의 종류에 따라 다른 결과가 나왔습니다.

이것이 다형성입니다.

---

### 8-5. 추상화 Abstraction

**추상화**는 복잡한 내부 구현은 숨기고, 필요한 기능만 외부에 보여주는 것입니다.

예를 들어 자동차를 운전할 때 운전자는 엔진이 내부적으로 어떻게 동작하는지 몰라도 됩니다.

운전자는 다음 기능만 알면 됩니다.

- 시동 걸기
- 가속하기
- 브레이크 밟기
- 핸들 돌리기

프로그래밍에서도 마찬가지입니다.

사용자는 내부 코드가 어떻게 구현되어 있는지 몰라도, 정해진 메서드를 사용하면 됩니다.

```python
class RemoteControl:
    def turn_on(self):
        print("TV를 켭니다.")

    def turn_off(self):
        print("TV를 끕니다.")

    def change_channel(self, channel):
        print(f"{channel}번 채널로 변경합니다.")


remote = RemoteControl()

remote.turn_on()
remote.change_channel(7)
remote.turn_off()
```

실행 결과:

```text
TV를 켭니다.
7번 채널로 변경합니다.
TV를 끕니다.
```

사용자는 리모컨 내부 회로가 어떻게 동작하는지 알 필요 없이 메서드만 사용하면 됩니다.

이것이 추상화의 핵심입니다.

---

## 9. OOP 예제: 학생 관리 프로그램

아래는 OOP를 활용한 간단한 학생 관리 예제입니다.

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def show_info(self):
        print(f"이름: {self.name}, 점수: {self.score}")

    def is_passed(self):
        return self.score >= 60


student1 = Student("민수", 85)
student2 = Student("지은", 45)

student1.show_info()
student2.show_info()

print(student1.is_passed())
print(student2.is_passed())
```

실행 결과:

```text
이름: 민수, 점수: 85
이름: 지은, 점수: 45
True
False
```

이 예제에서 `Student` 클래스는 학생이라는 객체를 표현합니다.

| 구성 요소 | 설명 |
|---|---|
| `name` | 학생 이름 |
| `score` | 학생 점수 |
| `show_info()` | 학생 정보 출력 |
| `is_passed()` | 합격 여부 확인 |

---

## 10. OOP 예제: 상속을 활용한 회원 시스템

```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def login(self):
        print(f"{self.username}님이 로그인했습니다.")

    def show_info(self):
        print(f"아이디: {self.username}")
        print(f"이메일: {self.email}")


class AdminUser(User):
    def delete_user(self, target_username):
        print(f"{target_username} 사용자를 삭제했습니다.")


class CustomerUser(User):
    def buy_product(self, product_name):
        print(f"{self.username}님이 {product_name} 상품을 구매했습니다.")


admin = AdminUser("admin", "admin@example.com")
customer = CustomerUser("user01", "user01@example.com")

admin.login()
admin.show_info()
admin.delete_user("bad_user")

customer.login()
customer.show_info()
customer.buy_product("노트북")
```

실행 결과:

```text
admin님이 로그인했습니다.
아이디: admin
이메일: admin@example.com
bad_user 사용자를 삭제했습니다.
user01님이 로그인했습니다.
아이디: user01
이메일: user01@example.com
user01님이 노트북 상품을 구매했습니다.
```

이 예제에서 `AdminUser`와 `CustomerUser`는 공통적으로 `User` 클래스를 상속받습니다.

따라서 로그인 기능과 정보 출력 기능을 중복해서 작성하지 않아도 됩니다.

---

## 11. OOP를 사용하는 이유

OOP를 사용하는 이유는 다음과 같습니다.

### 11-1. 코드 재사용성이 높아진다

상속을 사용하면 이미 만들어진 클래스를 다시 활용할 수 있습니다.

```python
class Animal:
    def eat(self):
        print("먹이를 먹습니다.")


class Dog(Animal):
    pass


dog = Dog()
dog.eat()
```

`Dog` 클래스에 `eat()`을 다시 작성하지 않아도 사용할 수 있습니다.

---

### 11-2. 유지보수가 쉬워진다

관련 데이터와 기능이 클래스 안에 함께 들어 있기 때문에 코드를 관리하기 쉽습니다.

예를 들어 회원 관련 기능은 `User` 클래스에, 상품 관련 기능은 `Product` 클래스에 모아둘 수 있습니다.

---

### 11-3. 코드 구조가 현실 세계와 비슷해진다

현실 세계의 개념을 객체로 표현하기 때문에 프로그램 구조를 이해하기 쉬워집니다.

예를 들어 쇼핑몰 프로그램은 다음과 같은 객체들로 구성할 수 있습니다.

- User
- Product
- Order
- Payment
- Cart

---

### 11-4. 확장성이 좋아진다

기존 코드를 크게 수정하지 않고 새로운 기능을 추가하기 좋습니다.

예를 들어 `User` 클래스를 기반으로 다음과 같이 여러 종류의 사용자를 만들 수 있습니다.

- AdminUser
- CustomerUser
- SellerUser

---

## 12. 절차 지향 프로그래밍과 객체 지향 프로그래밍 비교

### 12-1. 절차 지향 프로그래밍

절차 지향 프로그래밍은 프로그램을 순서대로 실행되는 절차 중심으로 작성합니다.

```python
name = "민수"
score = 85

print(f"이름: {name}")
print(f"점수: {score}")

if score >= 60:
    print("합격")
else:
    print("불합격")
```

간단한 프로그램에서는 이해하기 쉽지만, 코드가 커지면 데이터와 기능이 흩어져 관리가 어려워질 수 있습니다.

---

### 12-2. 객체 지향 프로그래밍

객체 지향 프로그래밍은 데이터와 기능을 객체 안에 묶어서 관리합니다.

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def show_result(self):
        print(f"이름: {self.name}")
        print(f"점수: {self.score}")

        if self.score >= 60:
            print("합격")
        else:
            print("불합격")


student = Student("민수", 85)
student.show_result()
```

객체 지향 방식은 코드가 길어 보일 수 있지만, 프로그램이 커질수록 구조적으로 관리하기 쉽습니다.

---

## 13. OOP 핵심 용어 정리

| 용어 | 의미 |
|---|---|
| 클래스 | 객체를 만들기 위한 설계도 |
| 객체 | 클래스로부터 만들어진 실제 대상 |
| 인스턴스 | 객체와 거의 같은 의미로 사용됨 |
| 속성 | 객체가 가진 데이터 |
| 메서드 | 객체가 수행하는 기능 |
| 생성자 | 객체 생성 시 자동 실행되는 메서드 |
| 캡슐화 | 데이터와 기능을 하나로 묶고 보호하는 것 |
| 상속 | 부모 클래스의 기능을 자식 클래스가 물려받는 것 |
| 오버라이딩 | 부모의 메서드를 자식 클래스에서 다시 정의하는 것 |
| 다형성 | 같은 메서드가 객체에 따라 다르게 동작하는 것 |
| 추상화 | 복잡한 내부 구현은 숨기고 필요한 기능만 보여주는 것 |

---

## 14. OOP 전체 흐름 예제

아래 예제는 클래스, 객체, 상속, 오버라이딩, 다형성을 한 번에 보여줍니다.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("동물이 소리를 냅니다.")


class Dog(Animal):
    def speak(self):
        print(f"{self.name}가 멍멍 짖습니다.")


class Cat(Animal):
    def speak(self):
        print(f"{self.name}가 야옹 웁니다.")


class Cow(Animal):
    def speak(self):
        print(f"{self.name}가 음메 웁니다.")


animals = [
    Dog("초코"),
    Cat("나비"),
    Cow("얼룩이")
]

for animal in animals:
    animal.speak()
```

실행 결과:

```text
초코가 멍멍 짖습니다.
나비가 야옹 웁니다.
얼룩이가 음메 웁니다.
```

이 예제에서 확인할 수 있는 OOP 개념은 다음과 같습니다.

| 개념 | 코드에서의 예 |
|---|---|
| 클래스 | `Animal`, `Dog`, `Cat`, `Cow` |
| 객체 | `Dog("초코")`, `Cat("나비")`, `Cow("얼룩이")` |
| 상속 | `class Dog(Animal)` |
| 오버라이딩 | 각 클래스의 `speak()` |
| 다형성 | `animal.speak()` 호출 시 객체마다 다른 동작 |

---

## 15. 정리

OOP는 프로그램을 객체 중심으로 설계하는 방식입니다.

객체는 속성과 기능을 함께 가지고 있으며, 클래스는 객체를 만들기 위한 설계도입니다.

OOP의 핵심 특징은 다음 네 가지입니다.

1. **캡슐화**: 데이터와 기능을 하나로 묶고 보호한다.
2. **상속**: 기존 클래스의 기능을 새로운 클래스가 물려받는다.
3. **다형성**: 같은 메서드가 객체에 따라 다르게 동작한다.
4. **추상화**: 복잡한 내부 구현은 숨기고 필요한 기능만 보여준다.

객체 지향 프로그래밍은 처음에는 조금 어렵게 느껴질 수 있지만, 프로그램이 커질수록 코드를 체계적으로 관리하고 확장하기 쉽게 만들어 줍니다.
