class Display:
    """모니터링 데이터를 콘솔에 출력하는 Read 전용 클래스."""

    # 주문 상태 집계 대상 (REJECTED 제외 - PRD §5.4.1)
    _MONITORED_STATUSES = ("RESERVED", "PRODUCING", "CONFIRMED", "RELEASE")

    def show_samples(self, samples: dict) -> None:
        """시료 목록을 테이블 형태로 출력한다.

        Args:
            samples: {sample_id: {id, name, avg_production_time, yield_rate, stock}, ...}
        """
        if not samples:
            print("등록된 시료가 없습니다.")
            return

        header = f"{'ID':<12} {'이름':<20} {'평균생산시간(min/ea)':>20} {'수율':>6} {'재고':>6}"
        separator = "-" * len(header)
        print(separator)
        print(header)
        print(separator)
        for sample in samples.values():
            sid = sample.get("id", "")
            name = sample.get("name", "")
            avg_time = sample.get("avg_production_time", 0)
            yield_rate = sample.get("yield_rate", 0)
            stock = sample.get("stock", 0)
            print(f"{sid:<12} {name:<20} {avg_time:>20} {yield_rate:>6} {stock:>6}")
        print(separator)

    def show_orders(self, orders: dict) -> None:
        """주문 목록을 테이블 형태로 출력한다.

        Args:
            orders: {order_id: {order_id, sample_id, customer_name, quantity, status}, ...}
        """
        if not orders:
            print("등록된 주문이 없습니다.")
            return

        header = f"{'주문번호':<22} {'시료ID':<12} {'고객명':<20} {'수량':>6} {'상태':<12}"
        separator = "-" * len(header)
        print(separator)
        print(header)
        print(separator)
        for order in orders.values():
            order_id = order.get("order_id", "")
            sample_id = order.get("sample_id", "")
            customer = order.get("customer_name", "")
            quantity = order.get("quantity", 0)
            status = order.get("status", "")
            print(f"{order_id:<22} {sample_id:<12} {customer:<20} {quantity:>6} {status:<12}")
        print(separator)

    def show_order_status_summary(self, orders: dict) -> None:
        """상태별 주문 건수 요약을 출력한다.

        집계 대상: RESERVED / PRODUCING / CONFIRMED / RELEASE
        REJECTED는 PRD §5.4.1에 따라 제외한다.

        Args:
            orders: {order_id: {order_id, sample_id, customer_name, quantity, status}, ...}
        """
        counts = {status: 0 for status in self._MONITORED_STATUSES}

        for order in orders.values():
            status = order.get("status", "")
            if status in counts:
                counts[status] += 1

        print("=== 주문 상태별 요약 ===")
        for status in self._MONITORED_STATUSES:
            print(f"  {status:<12}: {counts[status]}건")

    def show_stock_summary(self, samples: dict, orders: dict) -> None:
        """시료별 재고 상태 요약을 출력한다.

        재고 상태 판단 기준 (phase-3-3-display.md):
          - 고갈: stock == 0
          - 부족: 0 < stock < RESERVED 주문의 총 수량 합
          - 여유: stock >= RESERVED 주문의 총 수량 합
                 (RESERVED 주문이 없으면: stock > 0 → 여유, stock == 0 → 고갈)

        Args:
            samples: {sample_id: {id, name, ..., stock}, ...}
            orders:  {order_id: {sample_id, quantity, status, ...}, ...}
        """
        # 시료별 RESERVED 총 수량 집계
        reserved_totals: dict[str, int] = {}
        for order in orders.values():
            if order.get("status") == "RESERVED":
                sid = order.get("sample_id", "")
                reserved_totals[sid] = reserved_totals.get(sid, 0) + order.get("quantity", 0)

        print("=== 재고 상태 요약 ===")
        if not samples:
            print("  등록된 시료가 없습니다.")
            return

        header = f"{'ID':<12} {'이름':<20} {'재고':>6} {'RESERVED':>10} {'상태':<6}"
        separator = "-" * len(header)
        print(separator)
        print(header)
        print(separator)

        for sample in samples.values():
            sid = sample.get("id", "")
            name = sample.get("name", "")
            stock = sample.get("stock", 0)
            reserved_qty = reserved_totals.get(sid, 0)

            if stock == 0:
                status_label = "고갈"
            elif reserved_qty == 0:
                # RESERVED 주문이 없고 재고 > 0 → 여유
                status_label = "여유"
            elif stock >= reserved_qty:
                status_label = "여유"
            else:
                status_label = "부족"

            print(f"{sid:<12} {name:<20} {stock:>6} {reserved_qty:>10} {status_label:<6}")

        print(separator)
