Aden's Needle Trial v5 - Original Audio Edition
===============================================

이번 버전의 핵심 변경점
----------------------
1. 사망/R 리셋 오류 수정
   - AttributeError: 'Level' object has no attribute 'reset_dynamic_objects' 문제를 방어적으로 수정했습니다.
   - 사망하거나 R 키로 체크포인트 재시작 시 레벨의 동적 오브젝트를 안전하게 다시 생성합니다.
   - 무너지는 발판, 튀어나오는 가시, 레이저, 적, 보스, 탄환이 모두 다시 초기화됩니다.
   - 체크포인트 스폰 위치는 유지됩니다.

2. 완전 자체 제작 오디오 적용
   - 업로드된 외부 MP3 음악 파일은 포함하지 않았습니다.
   - Python으로 직접 생성한 오리지널 WAV 배경음악과 효과음만 포함했습니다.
   - 저작권 걱정 없이 사용할 수 있는 자체 제작 오디오입니다.

3. 자체 제작 BGM 구성
   - 1~20단계: original_stage_early.wav
   - 21단계 중간 보스: original_mid_boss.wav
   - 22~30단계: original_stage_late.wav
   - 31단계 최종 보스: original_final_boss.wav
   - 엔딩: original_ending.wav

4. 자체 제작 효과음 구성
   - jump.wav
   - dash.wav
   - shoot.wav
   - hit.wav
   - death.wav
   - checkpoint.wav
   - portal.wav
   - boss_hit.wav
   - laser.wav
   - clear.wav

실행 방법
---------
1. Python 설치
2. pygame 설치
   python -m pip install pygame
3. 실행
   python main.py

조작법
------
- 이동: ← / → 또는 A / D
- 점프: Z / Space / W / ↑
- 대시: Shift 또는 C
- 원거리 공격: X 또는 J
- 체크포인트 재시작: R
- 종료: ESC

맵 문자 규칙
------------
. = 빈 공간
# = 일반 발판
B = 무너지는 발판
^ = 고정 가시
! = 가까이 가면 갑자기 튀어나오는 가시
L = 갑자기 켜지는 수직 레이저
P = 플레이어 시작 위치
C = 체크포인트
O = 다음 단계 포탈
E = 워커형 적
S = 슈터형 적
K = 기존 보스
M = 21단계 보스 Needle Warden
Z = 최종 보스 Void Heart

중요
----
기존 aden_precision_game_v4 폴더에서 실행하지 말고,
이 zip을 새 폴더에 압축 해제한 뒤 그 안의 main.py를 실행하세요.
