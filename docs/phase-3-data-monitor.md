# phase-3-data-monitor.md - 데이터 모니터링 Tool (개요)

## 개요
- 목적: 저장된 JSON 데이터 상태를 콘솔에서 실시간 조회하는 독립 관리자 도구
- 폴더: `3_DataMonitor-yhyeon08.kim-18025928/`
- 역할: Read 전용 (데이터 변경 없음)
- JSON 포맷: Phase 2 (DataPersistence)와 동일한 형식 사용

---

## Sub-Phase 목록

| Sub-Phase | 이름 | 세부 문서 | 상태 |
|-----------|------|-----------|------|
| 3-1 | 프로젝트 초기 구조 설정 | phase-3-1-project-setup.md | 완료 |
| 3-2 | DataLoader 구현 | phase-3-2-data-loader.md | 완료 |
| 3-3 | Display 구현 | phase-3-3-display.md | 완료 |
| 3-4 | main.py 통합 | phase-3-4-main.md | 완료 |

---

## 최종 디렉토리 구조 (전체 완성 시)

```
3_DataMonitor-yhyeon08.kim-18025928/
├── monitor/
│   ├── __init__.py
│   ├── data_loader.py      # JSON 파일 읽기
│   └── display.py          # 콘솔 출력 포맷
├── data/                   # 모니터링 대상 JSON 파일 위치 (설정 가능)
│   ├── samples.json
│   └── orders.json
├── config.py               # 데이터 경로 등 설정값
├── main.py                 # 진입점
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   └── test_display.py
├── docs/
│   ├── phase-3-data-monitor.md   (본 파일)
│   ├── phase-3-1-project-setup.md
│   ├── phase-3-2-data-loader.md
│   ├── phase-3-3-display.md
│   └── phase-3-4-main.md
├── requirements.txt
└── .gitignore
```

---

## 구현 항목

### `config.py`
- `DATA_DIR`: JSON 파일이 위치한 디렉토리 경로 (기본값: `./data`)
- `SAMPLES_FILE`: samples.json 경로
- `ORDERS_FILE`: orders.json 경로

### `monitor/data_loader.py`
- `DataLoader` 클래스
  - `load_samples()` → samples.json 읽어 dict 반환 (파일 없으면 빈 dict)
  - `load_orders()` → orders.json 읽어 dict 반환

### `monitor/display.py`
- `Display` 클래스
  - `show_samples(samples)` → 시료 목록 테이블 출력
    - 컬럼: ID / 이름 / 평균생산시간 / 수율 / 재고
  - `show_orders(orders)` → 주문 목록 테이블 출력
    - 컬럼: 주문번호 / 시료ID / 고객명 / 수량 / 상태
  - `show_order_status_summary(orders)` → 상태별 주문 건수 요약
    - RESERVED / PRODUCING / CONFIRMED / RELEASE 각 건수
  - `show_stock_summary(samples, orders)` → 시료별 재고 상태 요약
    - 상태 표기: 여유 / 부족 / 고갈

### `main.py`
- DataLoader, Display 인스턴스 생성
- 모니터링 메뉴 루프
  - [1] 시료 현황 조회
  - [2] 주문 현황 조회
  - [3] 주문 상태별 요약
  - [4] 재고 상태 요약
  - [R] 새로고침 (데이터 재로딩)
  - [0] 종료

---

## 재고 상태 판단 기준

| 상태 | 조건 |
|------|------|
| 고갈 | stock == 0 |
| 부족 | 0 < stock < RESERVED 상태 주문의 총 수량 합 |
| 여유 | stock >= RESERVED 상태 주문의 총 수량 합 |

---

## 단위 테스트 항목

### `tests/test_data_loader.py` (5개)
- `test_load_samples_file_exists`: 정상 파일 로드
- `test_load_samples_file_missing`: 파일 없을 때 빈 dict 반환
- `test_load_orders_file_exists`: 정상 파일 로드
- `test_load_orders_file_missing`: 파일 없을 때 빈 dict 반환
- `test_reload_reflects_changes`: 파일 변경 후 재로드 시 최신 데이터 반영

### `tests/test_display.py` (7개)
- `test_show_samples_empty`: 빈 dict → "등록된 시료가 없습니다." 출력
- `test_show_samples_with_data`: 시료 데이터 → ID·이름·재고 출력 확인
- `test_show_orders_empty`: 빈 dict → "등록된 주문이 없습니다." 출력
- `test_show_order_status_summary`: 상태별 건수 정확 출력
- `test_show_stock_summary_excess`: 재고 ≥ RESERVED 총량 → "여유" 출력
- `test_show_stock_summary_shortage`: 0 < 재고 < RESERVED 총량 → "부족" 출력
- `test_show_stock_summary_depleted`: 재고 == 0 → "고갈" 출력

**총 단위 테스트: 12개 (5 + 7)**

---

## 체크리스트

- [x] config.py 경로 설정 구현 (3-2에서 생성)
- [x] monitor/data_loader.py 구현
- [x] monitor/display.py 4가지 출력 메서드 구현
- [x] main.py 모니터링 메뉴 루프 구현 (새로고침 포함)
- [x] 단위 테스트 12개 작성 및 전체 통과 (test_data_loader 5개 + test_display 7개)
- [x] Phase 2와 동일한 JSON 포맷 호환 확인
