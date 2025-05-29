"""Artificial Bee Colony optimisation for shopping route planning."""
from __future__ import annotations

import random
from typing import Dict, List, Tuple

from utils import normalize

NUM_EMPLOYED_BEES = 5
NUM_ONLOOKER_BEES = 5
MAX_CYCLES = 100
SCOUT_LIMIT = 20
SELL_START_INDEX = 3


class ABCOptimizer:
    """Artificial Bee Colony optimiser wrapper."""

    def __init__(self, markets: List[str], distances: List[List[float]], products: Dict[str, List[float]]):
        self.markets = markets
        self.distances = distances
        self.products = products
        self.normalized_distances = [normalize(row) for row in distances]
        self.normalized_products = {k: normalize(v) for k, v in products.items()}

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def solve(self, requested_products: List[str], start_index: int) -> Tuple[Dict[int, List[int]], float]:
        population = [
            self._initial_solution(requested_products, start_index) for _ in range(NUM_EMPLOYED_BEES)
        ]
        scout_counters = [0] * NUM_EMPLOYED_BEES
        best_solution, best_fitness = None, 0.0

        for _ in range(MAX_CYCLES):
            # Employed bees
            for i in range(NUM_EMPLOYED_BEES):
                candidate = self._produce_new(population[i], len(requested_products))
                candidate = self._greedy_select(population[i], candidate, requested_products, start_index)
                if candidate != population[i]:
                    population[i] = candidate
                    scout_counters[i] = 0
                else:
                    scout_counters[i] += 1

            # Onlooker bees
            fitnesses = [self._fitness(sol, requested_products, start_index) for sol in population]
            probs = [f / sum(fitnesses) for f in fitnesses]
            for _ in range(NUM_ONLOOKER_BEES):
                chosen = random.choices(population, probs)[0]
                candidate = self._produce_new(chosen, len(requested_products))
                self._greedy_select(chosen, candidate, requested_products, start_index)

            # Scout bees
            for i in range(NUM_EMPLOYED_BEES):
                if scout_counters[i] >= SCOUT_LIMIT:
                    population[i] = self._initial_solution(requested_products, start_index)
                    scout_counters[i] = 0

            # Track best
            for sol in population:
                fit = self._fitness(sol, requested_products, start_index)
                if fit > best_fitness:
                    best_solution, best_fitness = sol, fit

        return best_solution or population[0], best_fitness

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------

    def _fitness(self, solution: Dict[int, List[int]], products_sel: List[str], start: int) -> float:
        total_cost, last_idx = 0.0, start
        visited: set[int] = set()

        for market_idx, prod_idx_list in solution.items():
            if not prod_idx_list:
                continue
            if market_idx not in visited:
                total_cost += self.normalized_distances[last_idx][market_idx]
                visited.add(market_idx)
                last_idx = market_idx
            for p_idx in prod_idx_list:
                product_name = products_sel[p_idx]
                total_cost += self.normalized_products[product_name][market_idx]
        penalty = len(visited) * 0.05
        return 1.0 / (total_cost + penalty + 1e-6)

    def _initial_solution(self, products_sel: List[str], start: int) -> Dict[int, List[int]]:
        sol: Dict[int, List[int]] = {i: [] for i in range(SELL_START_INDEX, len(self.markets))}
        for idx, product in enumerate(products_sel):
            prices = self.products[product]
            min_price = min(prices[SELL_START_INDEX:])
            best_mkt, best_score = None, float("inf")
            for mkt in range(SELL_START_INDEX, len(self.markets)):
                price = prices[mkt]
                np = self.normalized_products[product][mkt]
                nd = self.normalized_distances[start][mkt]
                score = 0.5 * np + 0.5 * nd
                if abs(price - min_price) < 0.01:
                    if best_mkt is None or self.distances[start][mkt] < self.distances[start][best_mkt]:
                        best_mkt, best_score = mkt, score
                elif score < best_score:
                    best_mkt, best_score = mkt, score
            assert best_mkt is not None
            sol[best_mkt].append(idx)
        return sol

    @staticmethod
    def _produce_new(solution: Dict[int, List[int]], num_products: int) -> Dict[int, List[int]]:
        new_sol = {k: v[:] for k, v in solution.items()}
        prod_idx = random.randint(0, num_products - 1)
        target_mkt = random.choice(list(new_sol.keys()))
        for mk in new_sol:
            if prod_idx in new_sol[mk]:
                new_sol[mk].remove(prod_idx)
        new_sol[target_mkt].append(prod_idx)
        return new_sol

    def _greedy_select(
        self,
        current: Dict[int, List[int]],
        candidate: Dict[int, List[int]],
        products_sel: List[str],
        start: int,
    ) -> Dict[int, List[int]]:
        return candidate if self._fitness(candidate, products_sel, start) > self._fitness(current, products_sel, start) else current
