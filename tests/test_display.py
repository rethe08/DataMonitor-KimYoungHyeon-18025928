import pytest
from monitor.display import Display


@pytest.fixture
def display():
    return Display()


@pytest.fixture
def sample_data():
    return {
        "S-001": {
            "id": "S-001",
            "name": "실리콘 웨이퍼-8인치",
            "avg_production_time": 1.5,
            "yield_rate": 0.9,
            "stock": 100,
        },
        "S-002": {
            "id": "S-002",
            "name": "GaN 기판",
            "avg_production_time": 2.0,
            "yield_rate": 0.85,
            "stock": 30,
        },
    }


@pytest.fixture
def order_data():
    return {
        "ORD-20260508-0001": {
            "order_id": "ORD-20260508-0001",
            "sample_id": "S-001",
            "customer_name": "삼성전자 파운드리",
            "quantity": 50,
            "status": "RESERVED",
        },
        "ORD-20260508-0002": {
            "order_id": "ORD-20260508-0002",
            "sample_id": "S-001",
            "customer_name": "SK하이닉스",
            "quantity": 20,
            "status": "RESERVED",
        },
        "ORD-20260508-0003": {
            "order_id": "ORD-20260508-0003",
            "sample_id": "S-002",
            "customer_name": "LG전자",
            "quantity": 10,
            "status": "CONFIRMED",
        },
        "ORD-20260508-0004": {
            "order_id": "ORD-20260508-0004",
            "sample_id": "S-002",
            "customer_name": "퀄컴 코리아",
            "quantity": 5,
            "status": "PRODUCING",
        },
        "ORD-20260508-0005": {
            "order_id": "ORD-20260508-0005",
            "sample_id": "S-001",
            "customer_name": "인텔 코리아",
            "quantity": 15,
            "status": "REJECTED",
        },
    }


class TestShowSamples:
    def test_show_samples_empty(self, display, capsys):
        """빈 dict 입력 시 '등록된 시료가 없습니다.'를 출력한다."""
        display.show_samples({})
        captured = capsys.readouterr()
        assert "등록된 시료가 없습니다." in captured.out

    def test_show_samples_with_data(self, display, capsys, sample_data):
        """시료 데이터 입력 시 ID, 이름, 재고 값이 출력에 포함된다."""
        display.show_samples(sample_data)
        captured = capsys.readouterr()

        assert "S-001" in captured.out
        assert "실리콘 웨이퍼-8인치" in captured.out
        assert "100" in captured.out
        assert "S-002" in captured.out
        assert "GaN 기판" in captured.out
        assert "30" in captured.out


class TestShowOrders:
    def test_show_orders_empty(self, display, capsys):
        """빈 dict 입력 시 '등록된 주문이 없습니다.'를 출력한다."""
        display.show_orders({})
        captured = capsys.readouterr()
        assert "등록된 주문이 없습니다." in captured.out


class TestShowOrderStatusSummary:
    def test_show_order_status_summary(self, display, capsys, order_data):
        """상태별 건수가 정확하게 출력된다.

        order_data 구성:
          RESERVED  2건 (ORD-0001, ORD-0002)
          CONFIRMED 1건 (ORD-0003)
          PRODUCING 1건 (ORD-0004)
          RELEASE   0건
          REJECTED  1건 (ORD-0005, 집계 제외)
        """
        display.show_order_status_summary(order_data)
        captured = capsys.readouterr()

        assert "RESERVED" in captured.out
        assert "PRODUCING" in captured.out
        assert "CONFIRMED" in captured.out
        assert "RELEASE" in captured.out

        # REJECTED는 출력에 포함되지 않아야 한다
        assert "REJECTED" not in captured.out

        # 건수 확인: RESERVED 2건
        lines = captured.out.splitlines()
        reserved_line = next(l for l in lines if "RESERVED" in l)
        assert "2" in reserved_line

        # CONFIRMED 1건
        confirmed_line = next(l for l in lines if "CONFIRMED" in l)
        assert "1" in confirmed_line


class TestShowStockSummary:
    def test_show_stock_summary_excess(self, display, capsys):
        """재고 >= RESERVED 총량인 경우 '여유'가 출력된다."""
        # S-001: stock=100, RESERVED 총량=50+20=70 → 여유
        samples = {
            "S-001": {
                "id": "S-001",
                "name": "실리콘 웨이퍼-8인치",
                "avg_production_time": 1.5,
                "yield_rate": 0.9,
                "stock": 100,
            }
        }
        orders = {
            "ORD-0001": {
                "order_id": "ORD-0001",
                "sample_id": "S-001",
                "customer_name": "고객A",
                "quantity": 50,
                "status": "RESERVED",
            },
            "ORD-0002": {
                "order_id": "ORD-0002",
                "sample_id": "S-001",
                "customer_name": "고객B",
                "quantity": 20,
                "status": "RESERVED",
            },
        }
        display.show_stock_summary(samples, orders)
        captured = capsys.readouterr()

        assert "여유" in captured.out

    def test_show_stock_summary_shortage(self, display, capsys):
        """0 < 재고 < RESERVED 총량인 경우 '부족'이 출력된다."""
        # S-001: stock=30, RESERVED 총량=50+20=70 → 부족
        samples = {
            "S-001": {
                "id": "S-001",
                "name": "실리콘 웨이퍼-8인치",
                "avg_production_time": 1.5,
                "yield_rate": 0.9,
                "stock": 30,
            }
        }
        orders = {
            "ORD-0001": {
                "order_id": "ORD-0001",
                "sample_id": "S-001",
                "customer_name": "고객A",
                "quantity": 50,
                "status": "RESERVED",
            },
            "ORD-0002": {
                "order_id": "ORD-0002",
                "sample_id": "S-001",
                "customer_name": "고객B",
                "quantity": 20,
                "status": "RESERVED",
            },
        }
        display.show_stock_summary(samples, orders)
        captured = capsys.readouterr()

        assert "부족" in captured.out

    def test_show_stock_summary_depleted(self, display, capsys):
        """재고 == 0인 경우 '고갈'이 출력된다."""
        samples = {
            "S-001": {
                "id": "S-001",
                "name": "실리콘 웨이퍼-8인치",
                "avg_production_time": 1.5,
                "yield_rate": 0.9,
                "stock": 0,
            }
        }
        orders = {
            "ORD-0001": {
                "order_id": "ORD-0001",
                "sample_id": "S-001",
                "customer_name": "고객A",
                "quantity": 50,
                "status": "RESERVED",
            }
        }
        display.show_stock_summary(samples, orders)
        captured = capsys.readouterr()

        assert "고갈" in captured.out
