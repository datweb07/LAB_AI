"""GA tự cài đặt và chuyển CSP N hậu sang SearchProblem của SimpleAI."""

from dataclasses import dataclass
from functools import lru_cache
import random

from simpleai.search import SearchProblem, genetic

from csp_models import make_queens_csp, satisfies


class QueensSearchProblem(SearchProblem):
    """Trạng thái đầy đủ (r1,...,rn), ri là hàng của hậu ở cột i."""

    def __init__(self, n=5, seed=42):
        self.csp = make_queens_csp(n)
        self.n = n
        self.rng = random.Random(seed)
        self.max_pairs = n * (n - 1) // 2
        self.best_state = None
        self.best_score = -1
        self.calls = {"initialize": 0, "crossover": 0, "mutate": 0}
        super().__init__(initial_state=tuple(1 for _ in range(n)))

    def assignment(self, state):
        return dict(zip(self.csp.variables, state))

    @lru_cache(maxsize=32768)
    def conflicts(self, state):
        assignment = self.assignment(state)
        return sum(not check(vs, tuple(assignment[v] for v in vs))
                   for vs, check in self.csp.constraints)

    def value(self, state):
        # +1 giữ mọi trọng số roulette của SimpleAI dương, kể cả n=1.
        score = 1 + self.max_pairs - self.conflicts(state)
        if score > self.best_score:
            self.best_state, self.best_score = tuple(state), score
        return score

    def is_goal(self, state):
        return len(state) == self.n and satisfies(self.csp, self.assignment(state))

    def actions(self, state):
        return [(c, r) for c in range(self.n) for r in range(1, self.n + 1)
                if r != state[c]]

    def result(self, state, action):
        col, row = action
        child = list(state)
        child[col] = row
        return tuple(child)

    def generate_random_state(self):
        self.calls["initialize"] += 1
        return tuple(self.rng.choice(self.csp.domains[c]) for c in self.csp.variables)

    def crossover(self, state1, state2):
        self.calls["crossover"] += 1
        if self.n == 1:
            return tuple(state1)
        cut = self.rng.randrange(1, self.n)
        return state1[:cut] + state2[cut:]

    def mutate(self, state):
        self.calls["mutate"] += 1
        if self.n == 1:
            return tuple(state)
        col = self.rng.randrange(self.n)
        row = self.rng.choice([r for r in range(1, self.n + 1) if r != state[col]])
        return self.result(state, (col, row))


@dataclass
class GAResult:
    state: tuple
    solved: bool
    generations: int
    history: list
    calls: dict


def validate_settings(population_size, mutation_chance, generations):
    if population_size < 2:
        raise ValueError("Quần thể cần ít nhất 2 cá thể")
    if not 0 <= mutation_chance <= 1:
        raise ValueError("Xác suất đột biến phải thuộc [0,1]")
    if generations < 1:
        raise ValueError("Số thế hệ phải >= 1")


def custom_genetic(n=8, seed=42, population_size=120,
                   mutation_chance=0.25, generations=2000):
    """Tournament, lai một điểm, đột biến, elite và 10% cá thể nhập cư."""
    validate_settings(population_size, mutation_chance, generations)
    problem = QueensSearchProblem(n, seed)
    population = [problem.generate_random_state() for _ in range(population_size)]
    history = []
    stagnant = 0
    for generation in range(generations + 1):
        population.sort(key=problem.value, reverse=True)
        best = population[0]
        history.append(problem.conflicts(best))
        stagnant = stagnant + 1 if len(history) > 1 and history[-1] == history[-2] else 0
        if problem.is_goal(best) or generation == generations:
            return GAResult(best, problem.is_goal(best), generation, history, problem.calls.copy())

        def select_parent():
            candidates = problem.rng.sample(population, min(3, population_size))
            return max(candidates, key=problem.value)

        next_population = [best]  # Elitism: nghiệm tốt nhất không bị mất.
        if stagnant >= 50:
            # Giữ elite nhưng tái khởi tạo phần còn lại sau 50 thế hệ không tiến bộ.
            population = next_population + [problem.generate_random_state()
                                            for _ in range(population_size - 1)]
            stagnant = 0
            continue
        # Bổ sung gene mới để giảm hội tụ sớm ở cấu hình gần nghiệm.
        immigrant_count = min(population_size - 2, max(1, population_size // 10))
        next_population.extend(problem.generate_random_state() for _ in range(immigrant_count))
        while len(next_population) < population_size:
            child = problem.crossover(select_parent(), select_parent())
            if problem.rng.random() < mutation_chance:
                child = problem.mutate(child)
            next_population.append(child)
        population = next_population


def simpleai_genetic(n=5, seed=42, population_size=120,
                     mutation_chance=0.25, generations=200):
    validate_settings(population_size, mutation_chance, generations)
    problem = QueensSearchProblem(n, seed)
    # SimpleAI chọn cha mẹ và quyết định đột biến bằng random toàn cục.
    # Lưu/khôi phục để lần chạy có seed mà không làm đổi RNG của chương trình gọi.
    previous_random = random.getstate()
    random.seed(seed)
    try:
        final_node = genetic(problem, population_size=population_size,
                             mutation_chance=mutation_chance,
                             iterations_limit=generations)
    finally:
        random.setstate(previous_random)
    # SimpleAI 0.8.3 chỉ trả cá thể tốt nhất ở thế hệ CUỐI, không có elitism.
    # value() lưu cá thể tốt nhất đã đánh giá, gồm cả quần thể ban đầu.
    best = problem.best_state
    return (GAResult(best, problem.is_goal(best), generations, [], problem.calls.copy()),
            final_node.state)
