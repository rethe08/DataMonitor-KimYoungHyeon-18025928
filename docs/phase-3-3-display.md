# phase-3-3-display.md - Display 구현

## 목표
`Display` 클래스를 구현하고 단위 테스트로 검증한다.
Display는 콘솔 출력만 담당하며, 재고 상태 판단 로직을 포함한다.

---

## 구현 항목

### `monitor/display.py`

```python
# Display 클래스
# 역할: 모니터링 데이터를 콘솔에 출력 (Read 전용)
#
# 메서드:
#   show_samples(samples: dict) -> None
#     - 시료 목록 테이블 출력
#     - 컬럼: ID | 이름 | 평균생산시간(min/ea) | 수율 | 재고
#     - samples가 비어있으면 "등록된 시료가 없습니다." 출력
#
#   show_orders(orders: dict) -> None
#     - 주문 목록 테이블 출력
#     - 컬럼: 주문번호 | 시료ID | 고객명 | 수량 | 상태
#     - orders가 비어있으면 "등록된 주문이 없습니다." 출력
#
#   show_order_status_summary(orders: dict) -> None
#     - 상태별 주문 건수 요약 출력
#     - 집계 대상 상태: RESERVED / PRODUCING / CONFIRMED / RELEASE
#     - REJECTED 제외 (PRD §5.4.1)
#
#   show_stock_summary(samples: dict, orders: dict) -> None
#     - 시료별 재고 상태 요약 출력
#     - 상태 판단: 아래 기준표 참고
```

---

## 의존 관계
- 표준 라이브러리만 사용
- DataLoader / main.py import 금지

---

## 재고 상태 판단 기준 (`show_stock_summary` 내부 로직)

| 상태 | 조건 |
|------|------|
| 고갈 | `stock == 0` |
| 부족 | `0 < stock < RESERVED 상태 주문의 총 수량 합` |
| 여유 | `stock >= RESERVED 상태 주문의 총 수량 합` (같은 경우 포함) |

**비교 기준을 RESERVED로 한정하는 근거**
- `PRODUCING` 주문: 생산 라인이 이미 부족분을 생산 중 → 재고 부족 여부 재판단 불필요
- `CONFIRMED` 주문: 재고가 이미 확보(또는 생산 완료) → 현재 재고와의 비교 대상이 아님
- `RESERVED` 주문: 아직 승인 전이므로 현재 재고로 충족 가능한지 판단이 필요한 유일한 상태
- 따라서 PRD §5.4.2의 "주문 대비"는 **RESERVED 주문의 총 수량 합**으로 해석한다.

> RESERVED 주문이 없는 시료: stock > 0 이면 "여유", stock == 0 이면 "고갈"

---

## 단위 테스트 (`tests/test_display.py`)

| 테스트명 | 검증 내용 |
|---------|----------|
| `test_show_samples_empty` | 빈 dict → "등록된 시료가 없습니다." 포함 출력 |
| `test_show_samples_with_data` | 시료 dict → ID·이름·재고 값 출력 포함 확인 |
| `test_show_orders_empty` | 빈 dict → "등록된 주문이 없습니다." 포함 출력 |
| `test_show_order_status_summary` | 상태별 건수 정확 출력 (RESERVED 2건, CONFIRMED 1건 등) |
| `test_show_stock_summary_excess` | 재고 ≥ RESERVED 총량 → "여유" 출력 |
| `test_show_stock_summary_shortage` | 0 < 재고 < RESERVED 총량 → "부족" 출력 |
| `test_show_stock_summary_depleted` | 재고 == 0 → "고갈" 출력 |

> 출력 검증은 pytest의 `capsys.readouterr()` 픽스처를 사용한다.

---

## 체크리스트

- [x] `monitor/display.py` Display 클래스 구현
- [x] `show_samples()` 구현 (빈 목록 처리 포함)
- [x] `show_orders()` 구현 (빈 목록 처리 포함)
- [x] `show_order_status_summary()` 구현 (REJECTED 제외)
- [x] `show_stock_summary()` 구현 (고갈/부족/여유 판단 포함)
- [x] `tests/test_display.py` 단위 테스트 7개 작성
- [x] `pytest` 실행 시 7개 전체 PASS
- [x] Display 내부에서 DataLoader import 없음 확인
