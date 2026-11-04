"""Kiểm tra nghiệm với oracle độc lập, không chỉ kiểm tra chương trình chạy."""

import itertools
import random
import unittest

from simpleai.search import CspProblem, SearchProblem, backtrack

from csp_models import (compare_backtracking, make_equations_csp,
                        make_queens_csp, satisfies, solve_equations)
from genetic_queens import QueensSearchProblem, custom_genetic, simpleai_genetic


def independent_queens_check(rows):
    n = len(rows)
    return (all(1 <= r <= n for r in rows)
            and len(set(rows)) == n
            and len({r + c for c, r in enumerate(rows)}) == n
            and len({r - c for c, r in enumerate(rows)}) == n)


class AssignmentTests(unittest.TestCase):
    def test_csp_matches_all_3125_assignments_and_has_10_solutions(self):
        problem = make_queens_csp(5)
        self.assertIsInstance(problem, CspProblem)
        solutions = 0
        for rows in itertools.product(range(1, 6), repeat=5):
            valid = satisfies(problem, dict(zip(range(1, 6), rows)))
            self.assertEqual(valid, independent_queens_check(rows))
            solutions += valid
        self.assertEqual(solutions, 10)
        self.assertFalse(satisfies(problem, {1: 1}))

    def test_all_14_backtrack_configurations(self):
        records = compare_backtracking(5)
        self.assertEqual(len(records), 14)
        for label, inference, solution, checks in records:
            with self.subTest(label=label, inference=inference):
                self.assertTrue(independent_queens_check(tuple(solution[c] for c in range(1, 6))))
                self.assertGreater(checks, 0)

    def test_equations_unique_integer_solution(self):
        expected = [{"x": x, "y": y} for x in range(-10, 11) for y in range(-10, 11)
                    if 3*x + 2*y == 25 and 2*x - y == 5]
        self.assertEqual(expected, [{"x": 5, "y": 5}])
        self.assertEqual(len(make_equations_csp().constraints), 2)
        for inference in (False, True):
            self.assertEqual(solve_equations(inference), expected[0])

    def test_unsatisfiable_sizes(self):
        for n in (2, 3):
            self.assertIsNone(backtrack(make_queens_csp(n)))
            result = custom_genetic(n, population_size=12, generations=5)
            self.assertFalse(result.solved)
            self.assertEqual(result.generations, 5)

    def test_custom_ga_8_queens_and_seed(self):
        result = custom_genetic()
        repeat = custom_genetic()
        self.assertTrue(result.solved)
        self.assertTrue(independent_queens_check(result.state))
        self.assertEqual(result, repeat)
        self.assertEqual(result.history, sorted(result.history, reverse=True))
        self.assertGreater(result.calls["crossover"], 0)
        self.assertGreater(result.calls["mutate"], 0)

    def test_simpleai_ga_5_queens_and_global_rng(self):
        random_state = random.getstate()
        result, final = simpleai_genetic(population_size=40, generations=40)
        self.assertEqual(random.getstate(), random_state)
        self.assertTrue(result.solved)
        self.assertTrue(independent_queens_check(result.state))
        self.assertGreater(result.calls["crossover"], 0)
        self.assertGreater(result.calls["mutate"], 0)
        self.assertEqual(len(final), 5)

    def test_search_conversion_and_genetic_operators(self):
        problem = QueensSearchProblem(5)
        self.assertIsInstance(problem, SearchProblem)
        start = (1, 1, 1, 1, 1)
        self.assertEqual(len(problem.actions(start)), 20)
        for action in problem.actions(start):
            child = problem.result(start, action)
            self.assertEqual(sum(a != b for a, b in zip(start, child)), 1)
        for _ in range(20):
            a, b = problem.generate_random_state(), problem.generate_random_state()
            child = problem.crossover(a, b)
            self.assertTrue(any(child == a[:cut] + b[cut:] for cut in range(1, 5)))
            mutant = problem.mutate(child)
            self.assertEqual(sum(x != y for x, y in zip(child, mutant)), 1)
            self.assertTrue(all(1 <= row <= 5 for row in mutant))
        for rows in itertools.product(range(1, 6), repeat=5):
            expected = independent_queens_check(rows)
            self.assertEqual(problem.is_goal(rows), expected)
            self.assertEqual(problem.value(rows) == 11, expected)

    def test_single_queen_and_invalid_settings(self):
        self.assertTrue(custom_genetic(1).solved)
        self.assertTrue(simpleai_genetic(1, population_size=2, generations=1)[0].solved)
        for kwargs in ({"n": 0}, {"population_size": 1},
                       {"mutation_chance": 1.5}, {"generations": 0}):
            with self.assertRaises(ValueError):
                custom_genetic(**kwargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
