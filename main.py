from abc_optimizer import ABCOptimizer
from data_loader import load_all
from typing import List

SELL_START_INDEX = 3

# --------------------------------------------------
# Ana fonksiyon
# --------------------------------------------------

def main() -> None:
    markets, distances, products = load_all()
    optimizer = ABCOptimizer(markets, distances, products)

    start_idx = _get_start_location(markets)
    selected_products: List[str] = _get_user_products(products)
    if not selected_products:
        print("Seçilen geçerli ürün yok. Çıkılıyor.")
        return

    solution, fitness = optimizer.solve(selected_products, start_idx)
    _display_results(markets, distances, products, selected_products, solution, start_idx, fitness)


# --------------------------------------------------
# CLI helpers (kept private)
# --------------------------------------------------

def _get_start_location(markets: List[str]) -> int:
    print("Başlangıç konumunuzu seçin:")
    for idx in range(SELL_START_INDEX):
        print(f"{idx + 1} - {markets[idx]}")
    while True:
        try:
            choice = int(input(f"Seçiminiz (1-{SELL_START_INDEX}): ").strip()) - 1
            if 0 <= choice < SELL_START_INDEX:
                return choice
        except ValueError:
            pass
        print("Geçersiz seçim, tekrar deneyin.")


def _get_user_products(products: dict) -> List[str]:
    raw = input("Almak istediğiniz ürünleri virgülle ayırarak girin: ")
    wanted = [p.strip().lower() for p in raw.split(",") if p.strip()]
    valid: List[str] = []
    for p in wanted:
        if p in products:
            valid.append(p)
        else:
            print(f"[Uyarı] '{p}' bulunamadı.")
    return valid


def _display_results(
    markets: List[str],
    distances: List[List[float]],
    products: dict,
    selected_products: List[str],
    solution: dict,
    start_idx: int,
    fitness: float,
) -> None:
    print("\nBaşlangıç:", markets[start_idx])
    total_price, total_dist = 0.0, 0.0
    last = start_idx
    for mkt_idx, prod_idxs in solution.items():
        if not prod_idxs:
            continue
        dist = distances[last][mkt_idx]
        total_dist += dist
        mkt_name = markets[mkt_idx]
        for p_idx in prod_idxs:
            p_name = selected_products[p_idx]
            price = products[p_name][mkt_idx]
            total_price += price
            print(f"{p_name} → {mkt_name} | Fiyat: {price:.2f} TL | Mesafe: {dist:.0f} m")
        last = mkt_idx
    print(f"\nToplam Fiyat : {total_price:.2f} TL")
    print(f"Toplam Mesafe: {total_dist:.0f} m")
    print(f"Fitness      : {fitness:.4f}")


if __name__ == "__main__":
    main()