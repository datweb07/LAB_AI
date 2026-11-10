from constraint import Problem, AllDifferentConstraint

problem = Problem()

letters = ['T', 'W', 'O', 'F', 'U', 'R']
problem.addVariables(letters, range(10))

# Các chữ số đôi một khác nhau
problem.addConstraint(AllDifferentConstraint())

# Chữ số đứng đầu không được bằng 0
problem.addConstraint(lambda t: t != 0, ['T'])
problem.addConstraint(lambda f: f != 0, ['F'])

# Ràng buộc phép cộng TWO + TWO = FOUR
def sum_constraint(t, w, o, f, u, r):
    two = 100 * t + 10 * w + o
    four = 1000 * f + 100 * o + 10 * u + r
    return two + two == four

problem.addConstraint(sum_constraint, ['T', 'W', 'O', 'F', 'U', 'R'])

solutions = problem.getSolutions()
print(f"\n--- Cryptarithmetic TWO+TWO=FOUR (Slide 10): Tìm thấy {len(solutions)} nghiệm ---")
for sol in solutions:
    t, w, o = sol['T'], sol['W'], sol['O']
    f, u, r = sol['F'], sol['U'], sol['R']
    print(f"T={t}, W={w}, O={o}, F={f}, U={u}, R={r} -> {t}{w}{o} + {t}{w}{o} = {f}{o}{u}{r}")