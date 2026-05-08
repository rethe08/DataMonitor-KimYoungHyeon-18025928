import json
from pathlib import Path


class DataLoader:
    """JSON 파일을 읽어 dict로 반환하는 Read 전용 클래스."""

    def __init__(self, samples_path, orders_path):
        """
        Args:
            samples_path: samples.json 파일 경로 (str 또는 Path)
            orders_path:  orders.json 파일 경로 (str 또는 Path)
        """
        self._samples_path = Path(samples_path)
        self._orders_path = Path(orders_path)

    def load_samples(self) -> dict:
        """samples.json을 읽어 dict 반환.

        파일이 없으면 빈 dict를 반환하며 예외를 발생시키지 않는다.
        """
        return self._load_json(self._samples_path)

    def load_orders(self) -> dict:
        """orders.json을 읽어 dict 반환.

        파일이 없으면 빈 dict를 반환하며 예외를 발생시키지 않는다.
        """
        return self._load_json(self._orders_path)

    def _load_json(self, path: Path) -> dict:
        """주어진 경로의 JSON 파일을 읽어 dict로 반환한다.

        파일이 없거나 읽을 수 없는 경우 빈 dict를 반환한다.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except (json.JSONDecodeError, OSError):
            return {}
