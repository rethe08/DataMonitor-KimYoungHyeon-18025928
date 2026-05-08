# phase-3-2-data-loader.md - DataLoader 구현

## 목표
`config.py`와 `DataLoader` 클래스를 구현하고 단위 테스트로 검증한다.
DataLoader는 JSON 파일을 읽어 dict로 반환하는 역할만 담당한다.

---

## 구현 항목

### `config.py`

```python
# 데이터 파일 경로 설정
# DATA_DIR     : JSON 파일이 위치한 디렉토리 경로 (기본값: ./data)
# SAMPLES_FILE : samples.json 절대/상대 경로
# ORDERS_FILE  : orders.json 절대/상대 경로
```

### `monitor/data_loader.py`

```python
# DataLoader 클래스
# 역할: JSON 파일을 읽어 dict로 반환 (Read 전용, 데이터 변경 없음)
#
# 생성자:
#   __init__(samples_path, orders_path)
#     - samples_path: samples.json 파일 경로 (str 또는 Path)
#     - orders_path : orders.json 파일 경로 (str 또는 Path)
#
# 메서드:
#   load_samples() -> dict
#     - samples_path 의 JSON을 읽어 dict 반환
#     - 파일이 없으면 빈 dict 반환 (예외 발생 금지)
#
#   load_orders() -> dict
#     - orders_path 의 JSON을 읽어 dict 반환
#     - 파일이 없으면 빈 dict 반환 (예외 발생 금지)
```

### `main.py`에서의 생성 방식 (참고)
```python
import config
loader = DataLoader(config.SAMPLES_FILE, config.ORDERS_FILE)
```

---

## 의존 관계
- `config.py`의 경로 상수 참조 (main.py 에서 주입)
- 표준 라이브러리 `json`, `pathlib` 만 사용 (외부 패키지 금지)
- Display / main.py import 금지

---

## JSON 호환 포맷 (Phase 2와 동일)

### samples.json
```json
{
  "S-001": {
    "id": "S-001",
    "name": "실리콘 웨이퍼-8인치",
    "avg_production_time": 1.5,
    "yield_rate": 0.9,
    "stock": 100
  }
}
```

### orders.json
```json
{
  "ORD-20260508-0001": {
    "order_id": "ORD-20260508-0001",
    "sample_id": "S-001",
    "customer_name": "삼성전자 파운드리",
    "quantity": 50,
    "status": "RESERVED"
  }
}
```

---

## 단위 테스트 (`tests/test_data_loader.py`)

| 테스트명 | 검증 내용 |
|---------|----------|
| `test_load_samples_file_exists` | 정상 JSON 파일 로드 → 데이터 dict 정확히 반환 |
| `test_load_samples_file_missing` | 파일 없을 때 빈 dict 반환, 예외 미발생 |
| `test_load_orders_file_exists` | 정상 JSON 파일 로드 → 데이터 dict 정확히 반환 |
| `test_load_orders_file_missing` | 파일 없을 때 빈 dict 반환, 예외 미발생 |
| `test_reload_reflects_changes` | 파일 내용 변경 후 재호출 시 최신 데이터 반영 |

> 모든 테스트는 `tmp_path` 픽스처를 사용하여 실제 `data/` 폴더에 의존하지 않는다.

---

## 체크리스트

- [x] `config.py` 경로 상수 3종 구현 (`DATA_DIR`, `SAMPLES_FILE`, `ORDERS_FILE`)
- [x] `monitor/data_loader.py` DataLoader 클래스 구현
- [x] `load_samples()` 구현 (파일 미존재 시 빈 dict 반환)
- [x] `load_orders()` 구현 (파일 미존재 시 빈 dict 반환)
- [x] `tests/test_data_loader.py` 단위 테스트 5개 작성
- [x] `pytest` 실행 시 5개 전체 PASS
- [x] DataLoader 내부에서 Display import 없음 확인
