# phase-3-4-main.md - main.py 통합

## 목표
DataLoader와 Display를 연결하는 `main.py`를 구현하여
모니터링 콘솔 앱의 전체 흐름을 완성한다.

---

## 구현 항목

### `main.py`

```python
# 진입점 및 모니터링 메뉴 루프
#
# 흐름:
#   1. config를 참조하여 DataLoader, Display 인스턴스 생성
#   2. 메뉴 루프 시작
#      - 메뉴 항목 출력
#      - 입력 수신
#      - 선택에 따라 loader.load_*() → display.show_*() 호출
#      - "0" 입력 시 루프 종료
#
# 메뉴 동작:
#   [1] 시료 현황 조회
#       - loader.load_samples() → display.show_samples()
#   [2] 주문 현황 조회
#       - loader.load_orders() → display.show_orders()
#   [3] 주문 상태별 요약
#       - loader.load_orders() → display.show_order_status_summary()
#   [4] 재고 상태 요약
#       - loader.load_samples(), loader.load_orders()
#         → display.show_stock_summary()
#   [R] 새로고침
#       - 메뉴 화면을 재출력한다.
#       - DataLoader는 load_samples()/load_orders() 호출 시마다 파일을 새로 읽으므로,
#         [R] 자체에 별도 파일 로딩 로직은 없다.
#         (다음 메뉴 선택 시 자동으로 최신 데이터를 읽어온다)
#   [0] 종료
#       - "종료합니다." 출력 후 루프 탈출
#   그 외
#       - "잘못된 입력입니다." 출력 후 메뉴 재출력
```

---

## 레이어 분리 최종 확인

| 레이어 | 허용 | 금지 |
|--------|------|------|
| DataLoader | JSON 파일 I/O, config 경로 참조 | Display import |
| Display | 콘솔 출력, 재고 상태 계산 | DataLoader import |
| main.py | DataLoader·Display 연결, config 참조 | 비즈니스 로직 직접 구현 |

---

## 통합 확인 시나리오 (수동 실행 체크리스트)
> main.py는 표준입력을 사용하므로 자동화 테스트 대상이 아님.
> 수동 검증 완료 후 아래 항목을 [x] 로 표시한다.

1. 앱 실행 → 메뉴 출력 확인
2. `[1]` 선택 → data/samples.json 데이터 테이블 출력 확인
3. `[2]` 선택 → data/orders.json 데이터 테이블 출력 확인
4. `[3]` 선택 → 상태별 주문 건수(RESERVED/PRODUCING/CONFIRMED/RELEASE) 출력 확인
5. `[4]` 선택 → 시료별 재고 상태(여유/부족/고갈) 출력 확인
6. `[R]` 선택 → 메뉴 재출력 확인
7. `[0]` 선택 → "종료합니다." 출력 후 종료 확인
8. 잘못된 입력 → "잘못된 입력입니다." 출력 후 메뉴 재출력 확인

---

## 체크리스트

- [x] `main.py` 구현 (메뉴 루프 + DataLoader·Display 연결)
- [x] 메뉴 [1] 시료 현황 조회 동작 확인
- [x] 메뉴 [2] 주문 현황 조회 동작 확인
- [x] 메뉴 [3] 주문 상태별 요약 동작 확인
- [x] 메뉴 [4] 재고 상태 요약 동작 확인
- [x] 메뉴 [R] 새로고침 동작 확인
- [x] 메뉴 [0] 종료 동작 확인
- [x] 잘못된 입력 처리 확인
- [x] 전체 단위 테스트 (5 + 7 = 12개) PASS 확인
- [x] 레이어 분리 원칙 최종 확인 (DataLoader ↔ Display 상호 import 없음)
