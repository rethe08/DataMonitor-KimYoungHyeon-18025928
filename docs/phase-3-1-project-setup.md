# phase-3-1-project-setup.md - 프로젝트 초기 구조 설정

## 목표
DataMonitor Tool의 패키지 폴더 구조와 프로젝트 기반 파일을 생성한다.
코드 구현은 하지 않으며, 구조와 설정 파일만 완성한다.

> **범위 명시**: `config.py`는 Phase 3-2(DataLoader 구현)에서 생성한다.
> 3-1은 순수 구조(폴더·패키지·설정 파일)만 담당하며, Python 비즈니스 코드는 포함하지 않는다.

---

## 구현 항목

### 생성할 파일 및 폴더

```
3_DataMonitor-yhyeon08.kim-18025928/
├── monitor/
│   └── __init__.py          # 빈 파일
├── tests/
│   └── __init__.py          # 빈 파일
├── data/                    # 모니터링 대상 JSON 파일 위치
│   ├── samples.json         # 초기값: {}
│   └── orders.json          # 초기값: {}
├── requirements.txt
└── .gitignore
```

### `requirements.txt`
```
pytest==8.3.5
```

### `.gitignore`
```
__pycache__/
*.pyc
*.pyo
.pytest_cache/
*.egg-info/
dist/
build/
.venv/
venv/
```

---

## 체크리스트

- [x] monitor/ 폴더 및 `__init__.py` 생성
- [x] tests/ 폴더 및 `__init__.py` 생성
- [x] data/ 폴더 생성 및 빈 JSON 파일 초기화 (`{}`)
- [x] `requirements.txt` 작성
- [x] `.gitignore` 작성
- [x] `pytest` 설치 및 실행 확인 (테스트 없음 상태에서 오류 없이 종료)
