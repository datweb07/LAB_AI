"""Mô hình CSP: N hậu và hệ phương trình, sử dụng SimpleAI."""

from itertools import combinations

from simpleai.search import CspProblem, backtrack
from simpleai.search.csp import (
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
    MOST_CONSTRAINED_VARIABLE,
)


def queens_constraint(variables, values):
    """Biến là cột (1..n); giá trị là hàng (1..n)."""
    col1, col2 = variables
    row1, row2 = values
    return row1 != row2 and abs(row1 - row2) != abs(col1 - col2)


def make_queens_csp(n=5, descending=False, counter=None):
    if n < 1:
        raise ValueError("Kích thước bàn cờ phải >= 1")
    variables = tuple(range(1, n + 1))
    rows = list(range(n, 0, -1) if descending else range(1, n + 1))
    domains = {col: rows[:] for col in variables}

    def constraint(variables, values):
        if counter is not None:
            counter["checks"] += 1
        return queens_constraint(variables, values)

    constraints = [(pair, constraint) for pair in combinations(variables, 2)]
    return CspProblem(variables, domains, constraints)


def satisfies(problem, assignment):
    """Kiểm tra đủ biến, đúng miền và đúng TẤT CẢ ràng buộc."""
    if assignment is None or set(assignment) != set(problem.variables):
        return False
    if any(assignment[v] not in problem.domains[v] for v in problem.variables):
        return False
    return all(check(vs, tuple(assignment[v] for v in vs))
               for vs, check in problem.constraints)


STRATEGIES = (
    ("Thứ tự biến; hàng tăng", "", "", False),
    ("MRV; hàng tăng", MOST_CONSTRAINED_VARIABLE, "", False),
    ("Degree; hàng tăng", HIGHEST_DEGREE_VARIABLE, "", False),
    ("Thứ tự biến; LCV SimpleAI", "", LEAST_CONSTRAINING_VALUE, False),
    ("MRV + LCV SimpleAI", MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, False),
    ("Degree + LCV SimpleAI", HIGHEST_DEGREE_VARIABLE, LEAST_CONSTRAINING_VALUE, False),
    ("Thứ tự biến; hàng giảm", "", "", True),
)


def compare_backtracking(n=5):
    """Đếm cả kiểm tra heuristic và AC-3; không gọi đó là số nút."""
    records = []
    for inference in (False, True):
        for label, variable_h, value_h, descending in STRATEGIES:
            counter = {"checks": 0}
            problem = make_queens_csp(n, descending, counter)
            solution = backtrack(problem, variable_heuristic=variable_h,
                                 value_heuristic=value_h, inference=inference)
            checks = counter["checks"]
            if solution is not None and not satisfies(make_queens_csp(n), solution):
                raise AssertionError("Backtrack trả về nghiệm không hợp lệ")
            records.append((label, inference, solution, checks))
    return records


def equation_one(variables, values):
    x, y = values
    return 3 * x + 2 * y == 25


def equation_two(variables, values):
    x, y = values
    return 2 * x - y == 5


def make_equations_csp():
    variables = ("x", "y")
    domains = {v: list(range(-10, 11)) for v in variables}
    # Hai phương trình là HAI ràng buộc độc lập, cùng phạm vi (x, y).
    constraints = [(variables, equation_one), (variables, equation_two)]
    return CspProblem(variables, domains, constraints)


def solve_equations(inference=False):
    # Mặc định tắt suy diễn để thể hiện backtracking thuần túy.
    return backtrack(make_equations_csp(), inference=inference)


def board_text(state):
    n = len(state)
    return "\n".join(" ".join("Q" if state[c] == r else "."
                               for c in range(n)) for r in range(1, n + 1))
