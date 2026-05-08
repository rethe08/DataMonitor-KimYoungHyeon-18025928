import config
from monitor.data_loader import DataLoader
from monitor.display import Display


def print_menu():
    print()
    print("=" * 40)
    print("   DataMonitor - 반도체 시료 모니터링")
    print("=" * 40)
    print("  [1] 시료 현황 조회")
    print("  [2] 주문 현황 조회")
    print("  [3] 주문 상태별 요약")
    print("  [4] 재고 상태 요약")
    print("  [R] 새로고침")
    print("  [0] 종료")
    print("=" * 40)
    print()


def main():
    loader = DataLoader(config.SAMPLES_FILE, config.ORDERS_FILE)
    display = Display()

    print_menu()

    while True:
        choice = input("선택: ").strip().upper()

        if choice == "1":
            samples = loader.load_samples()
            display.show_samples(samples)

        elif choice == "2":
            orders = loader.load_orders()
            display.show_orders(orders)

        elif choice == "3":
            orders = loader.load_orders()
            display.show_order_status_summary(orders)

        elif choice == "4":
            samples = loader.load_samples()
            orders = loader.load_orders()
            display.show_stock_summary(samples, orders)

        elif choice == "R":
            print_menu()

        elif choice == "0":
            print("종료합니다.")
            break

        else:
            print("잘못된 입력입니다.")

        print_menu()


if __name__ == "__main__":
    main()
