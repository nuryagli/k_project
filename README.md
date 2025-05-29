# Smart Shopping Route Optimiser

> **Find the cheapest shopping route across local markets using the Artificial Bee Colony (ABC) algorithm.**

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Key Features

| Capability | Description |
|------------|-------------|
| 📶 Dynamic Data Load | Reads market names (`market_names.txt`), distance matrix (`uzaklik.xlsx`) and product prices (`marketler...xlsx`) at runtime. |
| 🐝 ABC Optimisation | Uses Artificial Bee Colony meta-heuristic to minimise **total price + distance**. |
| ⚙️ Modular Code | `data_loader`, `abc_optimizer`, `utils` — each with a single responsibility. |
| 🖥️ Interactive CLI | Prompt-driven: choose start location, enter products, get optimal route. |
| 🧹 Clean Code | Type hints, docstrings, error handling, fits PEP 8 & Clean Code principles. |

---

## 📂 Project Structure

```
kubra_python/
├── main.py              # CLI orchestrator
├── abc_optimizer.py     # ABC algorithm class
├── data_loader.py       # Data ingestion helpers
├── utils.py             # Shared utilities
├── requirements.txt     # Dependencies
├── market_names.txt     # Market list (one per line)
├── uzaklik.xlsx         # NxN distance matrix
└── marketler*.xlsx      # Product prices per market
```

---

## 🚀 Quick Start

```bash
# 1  Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2  Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3  Run the optimiser
python main.py
```

### Example Session

```
Başlangıç konumunuzu seçin:
1 - Sakarya Üniversitesi
2 - Serdivan AVM
3 - Ada AVM
Seçiminiz (1-3): 1
Almak istediğiniz ürünleri virgülle ayırarak girin: şampuan, yumurta, süt

Başlangıç: Sakarya Üniversitesi
şampuan → Market A  | Fiyat: 50.00 TL | Mesafe: 120 m
yumurta  → Market B  | Fiyat: 60.00 TL | Mesafe:  90 m
süt      → Market B  | Fiyat: 35.00 TL | Mesafe:   0 m

Toplam Fiyat : 145.00 TL
Toplam Mesafe: 210 m
Fitness      : 2.0384
```

---

## 📊 Data Requirements

| File | Purpose |
|------|---------|
| **`market_names.txt`** | One market name per line. The first three markets are *start-only* locations and do **not** sell products. |
| **`uzaklik.xlsx`** | Square distance matrix (rows = cols = markets). Distances in **metres**. |
| **`marketler ... .xlsx`** | First column = market name, each other column = product price. Column names become product names. |

If duplicate market rows exist in the price file, they are automatically averaged and a warning is displayed.

---

## ⚙️ Algorithm Details (ABC)

The Artificial Bee Colony algorithm mimics the foraging behaviour of honey bees:

1. **Employed Bees** explore neighbouring solutions.
2. **Onlooker Bees** probabilistically choose good solutions to refine.
3. **Scout Bees** abandon poor solutions after a limit.

Fitness = *(normalised price + normalised distance)⁻¹*  with a small penalty per visited market to discourage excessive hops.

Parameter defaults live in `abc_optimizer.py` and can be tuned easily:

```python
NUM_EMPLOYED_BEES = 5
NUM_ONLOOKER_BEES = 5
MAX_CYCLES       = 100
SCOUT_LIMIT      = 20
```

---

## 🛠️ Development Guide

* **Formatting** – Run `black .` and `isort .`.
* **Linting** – Optionally enable `ruff` or `flake8`.
* **Typing** – Pass `mypy --strict`.
* **Tests** – Add `pytest` tests under `tests/` for loaders and optimiser.

---

## 📄 License

This project is licensed under the MIT License – see [LICENSE](LICENSE) for details.
