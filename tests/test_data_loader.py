import json
import pytest
from monitor.data_loader import DataLoader


class TestLoadSamples:
    def test_load_samples_file_exists(self, tmp_path):
        """정상 JSON 파일 로드 시 데이터 dict를 정확히 반환한다."""
        samples_data = {
            "S-001": {
                "id": "S-001",
                "name": "실리콘 웨이퍼-8인치",
                "avg_production_time": 1.5,
                "yield_rate": 0.9,
                "stock": 100,
            }
        }
        samples_file = tmp_path / "samples.json"
        samples_file.write_text(json.dumps(samples_data, ensure_ascii=False), encoding="utf-8")

        orders_file = tmp_path / "orders.json"
        orders_file.write_text("{}", encoding="utf-8")

        loader = DataLoader(samples_file, orders_file)
        result = loader.load_samples()

        assert result == samples_data
        assert result["S-001"]["name"] == "실리콘 웨이퍼-8인치"
        assert result["S-001"]["stock"] == 100

    def test_load_samples_file_missing(self, tmp_path):
        """samples.json이 없을 때 빈 dict를 반환하고 예외를 발생시키지 않는다."""
        missing_samples = tmp_path / "nonexistent_samples.json"
        orders_file = tmp_path / "orders.json"
        orders_file.write_text("{}", encoding="utf-8")

        loader = DataLoader(missing_samples, orders_file)
        result = loader.load_samples()

        assert result == {}


class TestLoadOrders:
    def test_load_orders_file_exists(self, tmp_path):
        """정상 JSON 파일 로드 시 데이터 dict를 정확히 반환한다."""
        orders_data = {
            "ORD-20260508-0001": {
                "order_id": "ORD-20260508-0001",
                "sample_id": "S-001",
                "customer_name": "삼성전자 파운드리",
                "quantity": 50,
                "status": "RESERVED",
            }
        }
        samples_file = tmp_path / "samples.json"
        samples_file.write_text("{}", encoding="utf-8")

        orders_file = tmp_path / "orders.json"
        orders_file.write_text(json.dumps(orders_data, ensure_ascii=False), encoding="utf-8")

        loader = DataLoader(samples_file, orders_file)
        result = loader.load_orders()

        assert result == orders_data
        assert result["ORD-20260508-0001"]["customer_name"] == "삼성전자 파운드리"
        assert result["ORD-20260508-0001"]["status"] == "RESERVED"

    def test_load_orders_file_missing(self, tmp_path):
        """orders.json이 없을 때 빈 dict를 반환하고 예외를 발생시키지 않는다."""
        samples_file = tmp_path / "samples.json"
        samples_file.write_text("{}", encoding="utf-8")

        missing_orders = tmp_path / "nonexistent_orders.json"

        loader = DataLoader(samples_file, missing_orders)
        result = loader.load_orders()

        assert result == {}


class TestReload:
    def test_reload_reflects_changes(self, tmp_path):
        """파일 내용 변경 후 재호출 시 최신 데이터가 반영된다."""
        samples_file = tmp_path / "samples.json"
        orders_file = tmp_path / "orders.json"

        initial_data = {"S-001": {"id": "S-001", "name": "초기 시료", "stock": 10}}
        samples_file.write_text(json.dumps(initial_data, ensure_ascii=False), encoding="utf-8")
        orders_file.write_text("{}", encoding="utf-8")

        loader = DataLoader(samples_file, orders_file)

        # 첫 번째 로드 - 초기 데이터 확인
        first_result = loader.load_samples()
        assert first_result["S-001"]["stock"] == 10

        # 파일 내용 변경
        updated_data = {
            "S-001": {"id": "S-001", "name": "초기 시료", "stock": 10},
            "S-002": {"id": "S-002", "name": "신규 시료", "stock": 50},
        }
        samples_file.write_text(json.dumps(updated_data, ensure_ascii=False), encoding="utf-8")

        # 두 번째 로드 - 최신 데이터 반영 확인
        second_result = loader.load_samples()
        assert "S-002" in second_result
        assert second_result["S-002"]["stock"] == 50
